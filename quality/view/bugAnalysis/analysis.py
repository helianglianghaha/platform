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
def selectBugDataList(request):
    '''查询BUG数据'''
    sql='select *  from quality_buganalysis ORDER BY created DESC '
    bugList=commonList().getModelData(sql)
    data = {
        "code": 200,
        "data": bugList
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






