from django.http.response import JsonResponse
from quality.view.API.model import Modeldata
from quality.view.API.model import Modelversion
from quality.view.API_version.API_model import Testapi
from quality.view.API_version.API_model import Executinglog
from quality.view.API_version.API_model import Testvariable, Testcookies,Dingmessage

from django.core import serializers
from quality.common.logger import Log
from quality.common.msg import msgMessage, msglogger
from quality.common.msg import loginRequired
import copy, re

log = Log()

import json, re, requests, ast, datetime
from quality.common.commonbase import commonList
from quality.view.API.APIClass import APITest
from quality.common.functionlist import FunctionList
from quality.view.API_version.API_function import requestObject,createDataFinally
from quality.view.API_version.API_dataList import DataList
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler

#添加定时任务
scheduler = BackgroundScheduler()

def selectSigleVersionBugData(request):
    '''bug条件查询'''
    requestData = json.loads(request.body)
    title = requestData['title']
    version_report = requestData['version_report']
    reporter = requestData['reporter']
    severity = requestData['severity']
    status_alias = requestData['status']
    priority = requestData['priority']
    created = requestData['createdTime']

    sql = 'SELECT * FROM quality_bugAnalysis WHERE '
    conditions = []

    if len(version_report) > 0:
        version_conditions = ["version_report = '{}'".format(v) for v in version_report]
        conditions.append("(" + " OR ".join(version_conditions) + ")")

    if len(reporter) > 0:
        reporter_conditions = ["reporter = '{}'".format(r) for r in reporter]
        conditions.append("(" + " OR ".join(reporter_conditions) + ")")

    if len(severity) > 0:
        severity_conditions = ["severity = '{}'".format(s) for s in severity]
        conditions.append("(" + " OR ".join(severity_conditions) + ")")

    if len(status_alias) > 0:
        status_conditions = ["status_alias = '{}'".format(s) for s in status_alias]
        conditions.append("(" + " OR ".join(status_conditions) + ")")

    if len(priority) > 0:
        priority_conditions = ["priority = '{}'".format(p) for p in priority]
        conditions.append("(" + " OR ".join(priority_conditions) + ")")

    if len(created) == 2:
        start_time, end_time = created
        start_time = datetime.datetime.fromisoformat(start_time)
        end_time = datetime.datetime.fromisoformat(end_time)


        # Format timestamps as "年-月-日 时-分-秒"
        start_time_formatted = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time_formatted = end_time.strftime("%Y-%m-%d %H:%M:%S")

        conditions.append("created BETWEEN '{}' AND '{}'".format(start_time_formatted, end_time_formatted))

    if len(title) > 0:
        conditions.append("title = '{}'".format(title))

    if conditions:
        sql += " AND ".join(conditions)

    if len(version_report)==0 and len(reporter)==0 and len(severity)==0 and len(status_alias)==0 and len(priority)==0 and len(created)==0:
        sql='SELECT * FROM quality_bugAnalysis'

    print('=======sql========', sql)
    data = commonList().getModelData(sql)

    # 获取版本信息
    reportSql = 'SELECT DISTINCT version_report  FROM quality_buganalysis where version_report IS NOT NULL ORDER BY version_report  desc'
    reportListData = commonList().getModelData(reportSql)
    reportList = []
    for report in reportListData:
        reportdict = {}
        reportdict['label'] = report['version_report']
        reportdict['value'] = report['version_report']
        reportList.append(reportdict)

    # 获取处理人信息
    current_ownersql = 'SELECT DISTINCT current_owner FROM quality_buganalysis;'
    current_ownerListData = commonList().getModelData(current_ownersql)
    current_ownerList = []
    for current_owner in current_ownerListData:
        current_ownerdict = {}
        current_ownerdict['label'] = current_owner['current_owner']
        current_ownerdict['value'] = current_owner['current_owner']
        current_ownerList.append(current_ownerdict)

    data = {
        "code": 200,
        "data": data,
        "reportList": reportList,
        "current_ownerList": current_ownerList
    }

    return JsonResponse(data, safe=False)












def selectBugDataList(request):
    '''查询BUG数据'''
    sql='select *  from quality_buganalysis ORDER BY created DESC '
    bugList=commonList().getModelData(sql)
    # 获取版本信息
    reportSql = 'SELECT DISTINCT version_report  FROM quality_buganalysis where version_report IS NOT NULL ORDER BY version_report  desc'
    reportListData = commonList().getModelData(reportSql)
    reportList=[]
    for report in reportListData:
        reportdict={}
        reportdict['label']=report['version_report']
        reportdict['value']=report['version_report']
        reportList.append(reportdict)


    # 获取处理人信息
    current_ownersql = 'SELECT DISTINCT current_owner FROM quality_buganalysis;'
    current_ownerListData = commonList().getModelData(current_ownersql)
    current_ownerList=[]
    for current_owner in current_ownerListData:
        current_ownerdict={}
        current_ownerdict['label']=current_owner['current_owner']
        current_ownerdict['value'] = current_owner['current_owner']
        current_ownerList.append(current_ownerdict)

    # 获取未解决BUG
    unsolvesql='select count(*) as number from quality_buganalysis where status_alias=\'新\''
    unsolveData = commonList().getModelData(unsolvesql)

    # 每日新增BUG

    todayBug='select  count(*) as number from quality_buganalysis where Date(created)=CURRENT_DATE'
    todayBugData=commonList().getModelData(todayBug)




    # 获取每日新增BUG


    data = {
        "code": 200,
        "data": bugList,
        "reportList":reportList,
        "current_ownerList":current_ownerList,
        "unSolveBug":unsolveData,
        "todyBugNumber":todayBugData
    }

    return JsonResponse(data, safe=False)

# 设置任务的定时调度
def BUGAnalysis():
    page_number = 1
    page_size = 100
    # 连接到MySQL数据库
    import mysql.connector
    conn = mysql.connector.connect(
        host='rm-2zea97l06569u3s1zyo.mysql.rds.aliyuncs.com',
        user='tk_db_test',
        password='UUueBYYs9U4uptj',
        database='store'
    )
    # 创建游标对象
    cursor = conn.cursor()
    def fetch_data(page_number, page_size):
        url = "https://www.tapd.cn/api/aggregation/bug_aggregation/get_bug_fields_userview_and_list"

        payload = json.dumps({
            "workspace_id": "68121122",
            "conf_id": "1168121122001005815",
            "sort_name": "",
            "confIdType": "URL",
            "order": "desc",
            "perpage": page_size,
            "page": page_number,
            "selected_workspace_ids": "",
            "query_token": "",
            "location": "/bugtrace/bugreports/my_view",
            "target": "68121122/bug/normal",
            "entity_types": [
                "bug"
            ],
            "use_scene": "bug_list",
            "return_url": "https://www.tapd.cn/tapd_fe/68121122/bug/list?confId=1168121122001005815",
            "identifier": "app_for_list_tools,app_for_list_batch",
            "dsc_token": "jaQrBTAvIVofikGw"
        })
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://www.tapd.cn',
            'Connection': 'keep-alive',
            'Referer': 'https://www.tapd.cn/tapd_fe/68121122/bug/list?confId=1168121122001005815',
            'Cookie': '__root_domain_v=.tapd.cn; _qddaz=QD.478904511760278; 68121122bug_create_template=1168121122001000091; tapdsession=17082210181d058c6fd693c418b004e2d46456a6511a0a6e1b0c996a0672e60003b01af2f0; t_u=8c891cbd2c2c530303dcd54cd89ea6eef97d0187946c0125fee119dd27cd9bb270d145c29720a11e32c136ea3f75f7fc21d0c65579af7613b954aa2a70b7918e206fc702bbcd176f%7C1; _t_crop=34798485; tapd_div=101_369; _t_uid=446671291; cloud_current_workspaceId=68121122; dsc-token=jaQrBTAvIVofikGw; locale=zh_CN; iteration_view_type_cookie=card_view; iteration_card__446671291_68121122=1; iteration_card_current_iteration_68121122=1168121122001000208; _wt=eyJ1aWQiOiI0NDY2NzEyOTEiLCJjb21wYW55X2lkIjoiMzQ3OTg0ODUiLCJleHAiOjE3MDgzMTEzMzN9.a4a99403b0a47b8cc100dafed9d18da79eced8cb3d34c70eb409d9279207b0f0; tapdsession=17082210181d058c6fd693c418b004e2d46456a6511a0a6e1b0c996a0672e60003b01af2f0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
        else:
            print('Error:', response.status_code)
            data=None
        return data


    while True:
        data=fetch_data(page_number,page_size)
        print("===正在获取第{}页数据====".format(page_number))
        bugs_list = data['data']['bugs_list_ret']['data']['bugs_list']
        if not bugs_list:
            break
        # 处理当前页的数据
        for item in bugs_list:
            from .sqlData import selectSqlData
            selectSqlData().insert_or_update_data(cursor,conn,item['Bug'])
        conn.commit()
        print("===第{}页数据更新完成====".format(page_number))
        page_number += 1

        if page_number >=2:
            break



    print("=====所有bug数据更新完成========")
    # 关闭数据库连接
    cursor.close()
    conn.close()
    data={
        "code":200,
        "data":"所有bug数据更新完成"
    }

    return JsonResponse(data)
scheduler.add_job(BUGAnalysis, 'interval', minutes=10)

# 启动调度器
scheduler.start()





