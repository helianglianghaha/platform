from django.http.response import JsonResponse
from quality.common.logger import Log
log = Log()
import json, re, requests, ast, datetime
from quality.common.commonbase import commonList
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
from quality.view.testCasesMan.cases_model import testresult
from django.core.exceptions import ObjectDoesNotExist

#添加定时任务
scheduler = BackgroundScheduler()
def selectReportBugList(request):
    '''查询测试报告中遗留BUG'''
    requestData = json.loads(request.body)
    versionName = requestData['versionName']

    sql="select * from quality_testresult where versionName=\'{}\'".format(versionName)
    response=commonList().getModelData(sql)
    if len(response)!=0:
        if isinstance(response[0]['BUGList'],list):
            BUGList=response[0]['BUGList'].replace("None", "''").replace("'", '"')
            BUGList=json.loads(BUGList)
        else:
            BUGList=[]
        result=response[0]["result"]
    else:
        BUGList=[]
        result=''
    data={
        "code":200,
        "yiliuBugList":BUGList,
        "testResult":result
    }
    return JsonResponse(data,safe=False)
def clearTestBugs(request):
    '''删除版本对应BUG'''
    requestData = json.loads(request.body)
    versionName = requestData['versionName']
    try:
        _testresult = testresult.objects.get(versionName=versionName)
        _testresult.versionName = versionName
        _testresult.BUGList = ''
        _testresult.save()
        data = {
            "code": 200,
            "msg": "清除成功"
        }
        return JsonResponse(data, safe=False)
    except ObjectDoesNotExist:
        data = {
            "code": 200,
            "msg": "没有找到对应记录，不用删除"
        }
        return JsonResponse(data, safe=False)

def saveTestResults(request):
    '''保存测试结论'''
    requestData = json.loads(request.body)
    versionName=requestData['versionName']
    print(requestData)
    if 'BUGidList' in requestData.keys():
        BUGidList = requestData['BUGidList']
        print(BUGidList)
    if 'testResult' in requestData.keys():
        testResult = requestData['testResult']
    type = requestData['type']

    if versionName=='':
        return JsonResponse("版本名称不能为空")
    if type=='addBUG':
        try:
            _testresult = testresult.objects.get(versionName=versionName)
            _testresult.versionName = versionName
            _testresult.BUGList = BUGidList
            _testresult.save()
            data={
                "code":200,
                "msg":"BUG列表编辑成功"
            }
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            _testresult = testresult()
            _testresult.versionName = versionName
            _testresult.BUGList = BUGidList
            _testresult.save()
            data = {
                "code": 200,
                "msg": "BUG列表保存成功"
            }
            return JsonResponse(data, safe=False)
    else:
        try:
            _testresult = testresult.objects.get(versionName=versionName)
            _testresult.versionName = versionName
            _testresult.result = testResult
            _testresult.save()

            data = {
                "code": 200,
                "msg": "测试结论编辑成功"
            }
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            _testresult = testresult()
            _testresult.versionName = versionName
            _testresult.result = testResult
            _testresult.save()
            data = {
                "code": 200,
                "msg": "测试结论保存成功"
            }
            return JsonResponse(data, safe=False)










def selectTopBugData(request):
    '''查询首页数据'''
    sql = '''
            SELECT 
            version_report,
            SUM(CASE WHEN severity = 'suggestion' THEN 1 ELSE 0 END) AS suggestion_count,
            SUM(CASE WHEN severity = 'prompt' THEN 1 ELSE 0 END) AS prompt_count,
            SUM(CASE WHEN severity = 'normal' THEN 1 ELSE 0 END) AS normal_count,
            SUM(CASE WHEN severity = 'serious' THEN 1 ELSE 0 END) AS serious_count,
            SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) AS critical_count,
            SUM(CASE WHEN status_alias = '新' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN status_alias = '已解决' THEN 1 ELSE 0 END) AS close_count,
            SUM(CASE WHEN status_alias = '已关闭' THEN 1 ELSE 0 END) AS closed_count,
            count(version_report is not NULL) AS total_count
            FROM quality_buganalysis
            GROUP BY version_report
            ORDER BY MAX(created) DESC
        '''
    print(sql)
    bugData = commonList().getModelData(sql)

    # 汇总数据
    sqlTotal='''
            SELECT 
            SUM(CASE WHEN status_alias = '新' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN status_alias = '已解决' THEN 1 ELSE 0 END) AS close_count,
            SUM(CASE WHEN status_alias = '已关闭' THEN 1 ELSE 0 END) AS closed_count,
            count(version_report is not NULL) AS total_count
            FROM quality_buganalysis
    '''
    totalBugData=commonList().getModelData(sqlTotal)

    versiondata='''
            SELECT 
            SUM(CASE WHEN status = '开发中' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN status = '已上线' THEN 1 ELSE 0 END) AS ready_count,
            SUM(CASE WHEN status = '规划中' THEN 1 ELSE 0 END) AS guihua_count,
            SUM(CASE WHEN status = '待测试' THEN 1 ELSE 0 END) AS test_count,
            SUM(CASE WHEN status = '暂停' THEN 1 ELSE 0 END) AS stop_count,
            SUM(CASE WHEN status = '已测试待上线' THEN 1 ELSE 0 END) AS already_count,
            SUM(CASE WHEN status = '测试中' THEN 1 ELSE 0 END) AS testing_count,
            SUM(CASE WHEN status = '部分上线' THEN 1 ELSE 0 END) AS bufenReady_count
            FROM quality_versionmanager
    '''
    print(versiondata)
    versionList=commonList().getModelData(versiondata)



    data = {
        "code": 200,
        "data": bugData,
        "version":versionList,
        "total":totalBugData
        }
    return JsonResponse(data, safe=False)

def selectSigleVersionBugData(request):
    '''bug条件查询'''
    requestData = json.loads(request.body)
    title = requestData['title']
    openedBy = requestData['reporter']
    severity = requestData['severity']
    status = requestData['status']
    pri = requestData['priority']
    created = requestData['createdTime']
    tableID=requestData['tableID']

    sql='''
    SELECT DISTINCT b.id AS id, b.title, b.`status`, b.closedDate,c.version,b.pri,b.severity,j.first_name,b.closedBy,b.openedDate,b.assignedTo
        FROM zt_bug b
        LEFT JOIN zt_project a ON a.id = b.execution 
            AND a.project = 2 
            AND a.type = 'stage' 
            AND a.name LIKE '%v%'
        LEFT JOIN quality_versionmanager c ON c.version = a.name 
            AND c.tableID=\'{}\'
            LEFT JOIN auth_user j ON j.username = b.openedBy
            WHERE c.version is not NULL AND j.username IS NOT NULL
        and 
    '''.format(tableID)

    conditions = []

    if len(openedBy) > 0:
        reporter_conditions = ["b.openedBy = '{}'".format(r) for r in openedBy]
        conditions.append("(" + " OR ".join(reporter_conditions) + ")")

    if len(severity) > 0:
        severity_conditions = ["b.severity = '{}'".format(s) for s in severity]
        conditions.append("(" + " OR ".join(severity_conditions) + ")")

    if len(status) > 0 and "all" not in status:
        status_conditions = ["b.status = '{}'".format(s) for s in status]
        conditions.append("(" + " OR ".join(status_conditions) + ")")

    if len(pri) > 0:
        priority_conditions = ["b.pri = '{}'".format(p) for p in pri]
        conditions.append("(" + " OR ".join(priority_conditions) + ")")

    if len(created) == 2:
        start_time, end_time = created
        start_time = datetime.datetime.fromisoformat(start_time)
        end_time = datetime.datetime.fromisoformat(end_time)

        start_time += datetime.timedelta(days=1)
        end_time += datetime.timedelta(days=1)

        start_time_formatted = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time_formatted = end_time.strftime("%Y-%m-%d %H:%M:%S")

        conditions.append("b.openedDate BETWEEN '{}' AND '{}'".format(start_time_formatted, end_time_formatted))

    if len(title) > 0:
        conditions.append("b.title = '{}'".format(title))

    print(conditions)

    if conditions :
        print("conditions执行")
        sql += " AND ".join(conditions)

    if  len(openedBy)==0 and len(severity)==0 and (len(status)==0 or 'all' in status) and len(pri)==0 and len(created)==0 :
        sql='''
        SELECT DISTINCT b.id AS id, b.title, b.`status`, b.closedDate,c.version,b.pri,b.severity,j.first_name,b.closedBy,b.openedDate,b.assignedTo
        FROM zt_bug b
        LEFT JOIN zt_project a ON a.id = b.execution 
            AND a.project = 2 
            AND a.type = 'stage' 
            AND a.name LIKE '%v%'
        LEFT JOIN quality_versionmanager c ON c.version = a.name 
            AND c.tableID=\'{}\'
            LEFT JOIN auth_user j ON j.username = b.openedBy
            WHERE c.version is not NULL AND j.username IS NOT NULL
        '''.format(tableID)

    sql += " ORDER BY  b.openedDate DESC"

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
    sql='select *  from zt_bug ORDER BY openedDate DESC '
    bugList=commonList().getModelData(sql)
    # 获取版本信息
    reportSql = 'select  DISTINCT b.name from zt_bug a,zt_project b WHERE a.execution =b.id'
    reportListData = commonList().getModelData(reportSql)
    reportList=[]
    for report in reportListData:
        reportdict={}
        reportdict['label']=report['name']
        reportdict['value']=report['name']
        reportList.append(reportdict)


    # # 获取处理人信息
    # current_ownersql = 'SELECT DISTINCT current_owner FROM ;'
    # current_ownerListData = commonList().getModelData(current_ownersql)
    # current_ownerList=[]
    # for current_owner in current_ownerListData:
    #     current_ownerdict={}
    #     current_ownerdict['label']=current_owner['current_owner']
    #     current_ownerdict['value'] = current_owner['current_owner']
    #     current_ownerList.append(current_ownerdict)

    # 获取未解决BUG
    unsolvesql='select count(*) as number from zt_bug where status=\'active\''
    unsolveData = commonList().getModelData(unsolvesql)

    # 每日新增BUG
    todayBug='select  count(*) as number from zt_bug where Date(openedDate)=CURRENT_DATE'
    todayBugData=commonList().getModelData(todayBug)

    # 获取每日新增BUG
    data = {
        "code": 200,
        "data": bugList,
        "reportList":reportList,
        # "current_ownerList":current_ownerList,
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
            # print('Error:', response.status_code)
            data=None
        return data


    while True:
        data=fetch_data(page_number,page_size)
        # print("===正在获取第{}页数据====".format(page_number))
        bugs_list = data['data']['bugs_list_ret']['data']['bugs_list']
        if not bugs_list:
            break
        # 处理当前页的数据
        for item in bugs_list:
            from .sqlData import selectSqlData
            selectSqlData().insert_or_update_data(cursor,conn,item['Bug'])
        conn.commit()
        # print("===第{}页数据更新完成====".format(page_number))
        page_number += 1

        if page_number >=3:
            break

    # print("=====所有bug数据更新完成========")
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
# scheduler.start()






