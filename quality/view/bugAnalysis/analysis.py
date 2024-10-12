from django.http.response import JsonResponse
from quality.common.logger import Log
log = Log()
import json, re, requests, ast, datetime
from quality.common.commonbase import commonList
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
from quality.view.testCasesMan.cases_model import testresult
from django.core.exceptions import ObjectDoesNotExist
from quality.view.bugAnalysis.Bug_model import versionUpdate

#添加定时任务
scheduler = BackgroundScheduler()
def selectReportBugList(request):
    '''查询测试报告中遗留BUG'''
    requestData = json.loads(request.body)
    versionName = requestData['versionName']

    sql="select * from quality_testresult where versionName=\'{}\'".format(versionName)
    response=commonList().getModelData(sql)
    if len(response)!=0:
        # if isinstance(response[0]['BUGList'],list):
        BUGList=response[0]['BUGList'].replace("None", "''").replace("'", '"')
        BUGList=json.loads(BUGList)
        # else:
        #     BUGList=[]
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
def updateVersion(request):
    '''更新版本信息'''
    requestData = json.loads(request.body)
    print(requestData)
    versionTpye=requestData['versionType']
    result=0

    _versionUpdate=versionUpdate()
    _versionUpdate.versionType=versionTpye
    _versionUpdate.result=result
    from datetime import datetime
    time = datetime.now()
    _versionUpdate.createtime = time.strftime("%Y-%m-%d %H:%M:%S")
    _versionUpdate.save()

    data={
        "code":200,
        "msg":"版本更新成功"
    }
    return JsonResponse(data, safe=False)

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
                tableID,
                COUNT(*) AS bug_count,
                SUM(CASE WHEN `status` = 'active' THEN 1 ELSE 0 END) AS active_bug_count,
                SUM(CASE WHEN `status` = 'resolved' THEN 1 ELSE 0 END) AS resolved_bug_count,
                SUM(CASE WHEN `status` = 'closed' THEN 1 ELSE 0 END) AS closed_bug_count
            FROM (
                SELECT DISTINCT 
                    b.id AS m, 
                    b.title, 
                    b.`status`, 
                    b.closedDate,
                    c.tableID
                FROM zt_bug b
                LEFT JOIN zt_project a ON a.id = b.execution 
                LEFT JOIN quality_versionmanager c ON c.version = a.name 
                WHERE c.version IS NOT NULL
            ) AS zt_bug_subquery
            GROUP BY tableID
            ORDER BY tableID
        '''
    print(sql)
    bugData = commonList().getModelData(sql)

    # 汇总数据
    sqlTotal='''
            SELECT 
            SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) AS close_count,
            SUM(CASE WHEN status = 'closed' THEN 1 ELSE 0 END) AS closed_count,
            count(id is not NULL) AS total_count
            FROM zt_bug
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

    #根据版本内容查询禅道实际版本
    actlSql='''
            SELECT DISTINCT(version) from quality_versionmanager where tableID=\'{}\'
            '''.format(tableID)
    versionList=commonList().getModelData(actlSql)
    singleVersion=versionList[0]['version']


    sql='''
    SELECT DISTINCT b.id AS id, b.title, b.`status`, b.closedDate,b.pri,b.severity,b.closedBy,b.openedBy,b.openedDate,b.assignedTo
        FROM zt_bug b
        where 
        execution =
    ( SELECT a.id FROM zt_project a LEFT JOIN zt_project b ON a.project = b.id WHERE a.project != 0 AND a.team = \'{}\' )
        and 
    '''.format(singleVersion)

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
        SELECT *
        FROM zt_bug b
        where 
        execution =
        ( SELECT a.id FROM zt_project a LEFT JOIN zt_project b ON a.project = b.id WHERE a.project != 0 AND a.team = \'{}\' )
        '''.format(singleVersion)

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


def compare_trees(request):
    '''
        对比接口结果树
    '''
    global oldTree
    requestData = json.loads(request.body)
    newTree=requestData['newTree']
    url=requestData['url']
    domain=requestData['domain']
    path=""

    # 聚好麦测试域名
    if domain in ['api.yifangli.cn','ad.yixikeji.cn','boss.yifang.cn','boss.yixikeji.cn']:
        sql="select * from jhm_api_endpoints where path like '%{}%'".format(url)
        apiData=commonList().getModelData(sql)
        
        if len(apiData)!=0:
            oldTree=json.loads(apiData[0]['responses'])
            
        else:
            data = {
            "code": 2002,
            "data": "测试平台没有找到-jhm接口API记录,请补充API后再执行"
                }
            dingMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2',"测试平台没有找到-jhm接口API记录-{},请补充API后再执行".format(url))
            
            return JsonResponse(data, safe=False)

    # 好又多测试域名
    if domain in ['tboss.hupozhidao.com','tad.hupozhidao.com','ad.hupozhidao.com','boss.hupozhidao.com']:
        sql="select * from hyd_api_endpoints where path like '%{}%'".format(url)
        apiData=commonList().getModelData(sql)
        oldTree=apiData['responses']
        if len(apiData)!=0:
            oldTree=eval(apiData[0]['responses'])
        else:
            data = {
            "code": 2002,
            "data": "测试平台没有找到-hyd接口API记录,请补充API后再执行"
                }
            dingMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2',"测试平台没有找到-hyd接口API记录-{},请补充API后再执行".format(url))
            return JsonResponse(data, safe=False)


    # 量多多测试域名
    if domain in ['tad.ldd888.com','tboss.ldd888.com','ad.ldd888.com','boss.ldd888.com']:
        sql="select * from ldd_api_endpoints where path like '%{}%'".format(url)
        apiData=commonList().getModelData(sql)
        oldTree=apiData['responses']
        if len(apiData)!=0:
            oldTree=apiData[0]['responses']
        else:
            data = {
            "code": 2002,
            "data": "测试平台没有找到-ldd接口API记录,请补充API后再执行"
                }
            dingMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2',"测试平台没有找到-hyd接口API记录-{},请补充API后再执行".format(url))
            return JsonResponse(data, safe=False)


    # else:
    #     data = {
    #     "code": 200,
    #     "data": "域名不匹配，请修改域名后再检查"
    #         }

    #     return JsonResponse(data, safe=False)
    global differences
    differences = []
    def compare_dicts(dict1, dict2, path=""):
        # print("开始执行compare_dicts")
        print("dict1",(dict1))
        print("dict2",(dict2))

        # for key in dict1.keys():
        #     if key not in dict2:
        #         differences.append(f"'{url}'==新接口==字段缺失=='{path}{key}' ")
        #     else:
        #         if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
        #             print("====key===dict===",key)
        #             # 如果值是字典，递归比较
        #             compare_dicts(dict1[key], dict2[key], f"{path}{key}.")
        #         elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
        #             print("===key=list=",key)
        #             # 如果值是列表，递归比较每个元素
        #             compare_lists(dict1[key], dict2[key], f"{path}{key}")
                   
                # 判断key对应的值是否相同
                # elif dict1[key] != dict2[key]:
                #     differences.append(f"Value at '{path}{key}' differs: {dict1[key]} != {dict2[key]}")

        # 对比测试平台和执行接口字段比较

        for key in dict2.keys():
            if key not in dict1:
                differences.append(f"【'{url}'】==<'{path}{key}'>>接口字段缺失<<")
            else:
                if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                    # 如果值是字典，递归比较
                    compare_dicts(dict1[key], dict2[key], f"{path}{key}.")

                elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
                    print("===key=list=",key)
                    # 如果值是列表，递归比较每个元素
                    compare_lists(dict1[key], dict2[key], f"{path}{key}")
                   

                # 判断key对应的值是否相同
                # elif dict1[key] != dict2[key]:
                #     differences.append(f"Value at '{path}{key}' differs: {dict1[key]} != {dict2[key]}")
   
    def compare_lists(list1, list2, path=""):
        if list1 is None or list2 is None:
            if list1 != list2:
                differences.append(f"List at '{path}' differs: {list1} != {list2}")
            return differences

        len1, len2 = len(list1), len(list2)

        if len1 != len2:
            differences.append(f"List at '{path}' has different lengths: {len1} != {len2}")

        for i, (item1, item2) in enumerate(zip(list1, list2)):
            if isinstance(item1, dict) and isinstance(item2, dict):
                compare_dicts(item1, item2, f"{path}[{i}].")
            elif item1 != item2:
                differences.append(f"Value at '{path}[{i}]' differs: {item1} != {item2}")

    compare_dicts(newTree, oldTree)

    if len(differences)>0:
        data = {
            "code": 2001,
            "data": differences
                }
        
        dingMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2',differences)

    else:

        data = {
            "code": 200,
            "data": "接口断言成功"
                }

    return JsonResponse(data, safe=False)

def sortReportApi(request):
    '''
        分析html导入测试平台，区分平台，测试环境，生产环境
    '''
    import os
    import logging
    file_list=[]
    # 聚好麦测试环境
    jhm_test_api_endpoints=[]
    # 聚好麦生产环境
    jhm_api_endpoints=[]

    # 好又多测试环境
    hyd_test_api_endpoints=[]
    # 好又多生产环境
    hyd_api_endpoints=[]

    # 量多多测试环境
    ldd_test_api_endpoints=[]
    # 量多多生产环境
    ldd_api_endpoints=[]
    def find_test_report_files(root_folder):
        # 遍历根目录及其子目录
        for dirpath, dirnames, filenames in os.walk(root_folder):
            for filename in filenames:
                # 检查文件名是否为 TestReport.html
                if filename == 'TestReport.html':
                    # 获取完整路径
                    file_path = os.path.join(dirpath, filename)
                    file_list.append(file_path)


    # root_folder = '/platform/static'
    root_folder = '/Users/hll/Desktop/static'
    # 过滤文件路径
    find_test_report_files(root_folder)


    def extract_data_from_report(html_file):
        '''分析html文件'''
        from bs4 import BeautifulSoup
        with open(html_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 使用 BeautifulSoup 解析 HTML 内容
        soup = BeautifulSoup(content, 'html.parser')

        requests = []
        soup_list=soup.find_all('div', class_='group')

        for i in range(len(soup_list)):
            request_title = soup_list[i].text.strip()
            if 'Request' in request_title:
                method_url = soup_list[i].find_next('pre', class_='data').text.strip()
                url_list = method_url.split()
                if len(url_list)<=1:
                    break
                
                # Find the next response section
                response_section = soup_list[i + 1].find_next('pre', class_='data', id=True).text.strip()
                # print("====response_section===", response_section)

                # if '聚好麦' in html_file and '生产环境' not in html_file:

                #     sql = f'''INSERT INTO jhm_test_api_endpoints(path, responses) VALUES (\'{url_list[1]}\', '{response_section}\')'''
                #     # print('===sql====',sql)
                #     try:
                #         commonList().getModelData(sql)
                #     except:
                #         logging.info('method_url{}接口录入失败，请手动录入'.format(method_url))

                # if '聚好麦' in html_file and '生产环境' in html_file:
                #     sql='''
                #         INSERT INTO  jhm_api_endpoints(path,responses) values ('{}','{}')
                #         '''.format(url_list[1],response_section)
                #     # print('===sql====',sql)
                #     try:
                #         commonList().getModelData(sql)
                #     except:
                #         logging.info('method_url{}接口录入失败，请手动录入'.format(method_url))

                # if '好又多' in html_file and '生产环境' not in html_file:
                #     sql='''
                #         INSERT INTO  hyd_test_api_endpoints(path,responses) values ('{}','{}')
                #         '''.format(url_list[1],response_section)
                #     # print('===sql====',sql)
                #     try:
                #         commonList().getModelData(sql)
                #     except:
                #         logging.info('method_url{}接口录入失败，请手动录入'.format(method_url))
                # if'好又多' in html_file and '生产环境' in html_file:
                #     sql='''
                #         INSERT INTO  hyd_api_endpoints(path,responses) values ('{}','{}')
                #         '''.format(url_list[1],response_section)
                #     # print('===sql====',sql)
                #     try:
                #         commonList().getModelData(sql)
                #     except:
                #         logging.info('method_url{}接口录入失败，请手动录入'.format(method_url))

                if '量多多' in html_file and '生产环境' not in html_file:
                    sql='''
                        INSERT INTO  ldd_test_api_endpoints(path,responses) values ('{}','{}')
                        '''.format(url_list[1],response_section)
                    # print('===sql====',sql)
                    try:
                        commonList().getModelData(sql)
                    except:
                        logging.info('method_url{}接口录入失败，请手动录入'.format(method_url))
                if '量多多' in html_file and '生产环境'  in html_file:
                    sql='''
                        INSERT INTO  ldd_api_endpoints(path,responses) values ('{}','{}')
                        '''.format(url_list[1],response_section)
                    # print('===sql====',sql)
                    try:
                        commonList().getModelData(sql)
                    except:
                        logging.info('method_url{}接口录入失败，请手动录入'.format(method_url))
            print('===不能录入的接口====',requests)

    


        # for request_section in soup.find_all('div', class_='group'):
        #     request_title = request_section.text.strip()
        #     request_dict={}
        #     if 'Request' in request_title:
        #         method_url = request_section.find_next('pre', class_='data').text.strip()
        #         url_list=method_url.split()
        #         request_dict['url']= url_list[1]
            
        #     if 'Response' in request_title:

        #         response_section = request_section.find_next('pre', class_='data',id=True).text.strip()
        #         print("====response_section===",response_section)
        #         request_dict['Response']= response_section
        #     print(request_dict)

            
        
    if len(file_list)>0:
        for response in file_list:
            print('====开始录入接口=====',response)
            extract_data_from_report(response)
            

    data = {
        "code": 200,
        "data": "接口导入完成"
    }

    return JsonResponse(data, safe=False)



    



def dingMessage(url,versionStart):
    '''叮叮消息通知'''
    import requests
    import json

    url = url

    payload = json.dumps({
    "msgtype": "markdown",
    "markdown": {
        "title": "版本信息更新",
        "text": versionStart,
        "at": {
        "isAtAll": False
        }
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

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






