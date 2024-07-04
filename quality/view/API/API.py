# import datetime
from datetime import datetime

from django.http.response import JsonResponse,FileResponse
# from quality.models import Version
# from quality.view.API.model import Api
# from quality.view.API.model import Testcase
# from quality.view.API.model import Webtestcase
# from quality.view.API.model import Script
from quality.view.API.model import Modeldata
from quality.view.API.model import Modelversion
from quality.view.API.model import  Scriptproject
from quality.view.API.model import Versionmanager
from quality.view.API.model import taskmanager
from django.core import serializers
from quality.common.logger import Log
from quality.common.msg import msgMessage, msglogger
from quality.common.msg import loginRequired
from quality.common.logger import Log
from pathlib import Path
from datetime import datetime
import  os,shutil
log=Log()

import json,re,os,zipfile
from quality.common.commonbase import commonList
from quality.view.API.APIClass import APITest
from quality.common.functionlist import FunctionList
def delTaskInfo(request):
    '''删除任务信息'''
    requestData = json.loads(request.body)
    taskInfo=requestData['value']
    print(taskInfo)

    id=taskInfo['id']
    _taskmanager=taskmanager.objects.get(id=id)
    _taskmanager.delete()

    data = {
            "code": 200,
            "data": "删除成功"
            }
    return JsonResponse(data, safe=False)




def selectTaskInfo(request):
    '''查询任务信息'''
    requestData = json.loads(request.body)
    taskInfo=requestData['value']
    # print(type(taskInfo))


    sql = 'SELECT * FROM quality_taskmanager WHERE '
    conditions = []

    if len(taskInfo) > 0:
        owner_conditions = ["owner LIKE '%{}%'".format(v) for v in taskInfo]
        conditions.append("(" + " OR ".join(owner_conditions) + ")")

    if len(taskInfo) == 0:
        sql = "SELECT * FROM quality_taskmanager ORDER BY updateTime desc "

    if conditions:
        sql += " AND ".join(conditions)+"ORDER BY updateTime desc"

    data = commonList().getModelData(sql)
    print(sql)


    def convert_lists(item):
        if item['owner']:
            item['owner'] = eval(item['owner'])
        else:
            item['owner']=[]
        
        return item

    modified_list = [convert_lists(item) for item in data]
    # print(modified_list)

    data = {
                "code": 200,
                "data": modified_list
            }
    return JsonResponse(data, safe=False)

def saveTaskInfo(request):
    '''保存任务信息'''
    requestData = json.loads(request.body)
    print(requestData)
    taskInfo=requestData['value']
    id=taskInfo['id']
    taskType=taskInfo['taskType']
    owner=taskInfo['owner']
    taskName=taskInfo['taskName']
    remark=taskInfo['remark']
    beginTime=taskInfo['beginTime']
    endTime=taskInfo['endTime']
    createTime=taskInfo['createTime']
    from dateutil import parser
    

    def to_datetime(time_str):
    # 解析时间字符串为 datetime 对象
        if not time_str:
            return None
        try:
            time_obj = parser.isoparse(time_str)
        # 如果包含时区信息，将其转换为没有时区信息的本地时间
            if time_obj.tzinfo is not None:
                time_obj = time_obj.astimezone(tz=None).replace(tzinfo=None)
            return time_obj
        except ValueError:
            return None
    if taskInfo['beginTime']:
    
        beginTime_dt = to_datetime(taskInfo['beginTime'])
    else:
        beginTime_dt=None

    if taskInfo['endTime']:
        endTime_dt = to_datetime(taskInfo['endTime'])
    else:
        endTime_dt=None

    if taskInfo['createTime']:
        createTime_dt = to_datetime(taskInfo['createTime'])
    else:
        createTime_dt =datetime.now()

    updateTime=datetime.now()

    username = request.session.get('username', False)
    selectUserNameSql = "select first_name from auth_user where username=\'{}\'".format(username)
    returnUserNamedata = commonList().getModelData(selectUserNameSql)
    if returnUserNamedata:
        username = returnUserNamedata[0]['first_name']
    else:
        username = "万里悲秋常作客更新了任务"

    url='https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2'

    taskStart='> 任务信息更新：'

    _taskmanger=taskmanager()
    if id:
        _taskmanger.id=id
        _taskmanger.status=taskType
        _taskmanger.owner=owner
        _taskmanger.taskName=taskName
        _taskmanger.remark=remark
        _taskmanger.beginTime=beginTime_dt
        _taskmanger.endTime=endTime_dt
        _taskmanger.updateTime=updateTime
        _taskmanger.createTime=createTime_dt
        _taskmanger.save()
        taskDingMessage(url,taskStart,username,taskName,owner,taskType,beginTime_dt,endTime_dt,remark)
    else:
        _taskmanger.status=taskType
        _taskmanger.owner=owner
        _taskmanger.taskName=taskName
        _taskmanger.remark=remark
        _taskmanger.beginTime=beginTime_dt
        _taskmanger.endTime=endTime_dt
        _taskmanger.createTime=createTime_dt

        # taskDingMessage(url,taskStart,username,taskName,owner,taskType,beginTime_dt,endTime_dt,remark)

        _taskmanger.save()

    data = {
                "code": 200,
                "msg": "保存成功",
            }
    return JsonResponse(data, safe=False)

def taskDingMessage(url,taskStart,username,task,owner,status,beginTime,endTime,remark):
    '''叮叮消息通知'''
    import requests
    import json


    taskInfo = '''
                \n\n > 更新人: <font color=#303133>{}</font>  
                \n\n > 任务 : <font color=#303133>{}</font> 
                \n\n > 负责人 : <font color=#303133>{}</font>  
                \n\n > 任务状态 : <font color=#303133>{}</font>  
                \n\n > 开始时间 : <font color=#303133>{}</font>  
                \n\n > 结束时间 ：<font color=#303133>{}</font>  
                \n\n > 备注 ：<font color=#303133>{}</font>  
                '''.format(username,task,owner,status,beginTime,endTime,remark)
    taskStart = taskStart + taskInfo + '\n'

    url = url

    payload = json.dumps({
    "msgtype": "markdown",
    "markdown": {
        "title": "任务信息更新",
        "text": taskStart,
        "at": {
        "isAtAll": True
        }
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)



def selectVersionTotalData(request):
    '''筛选所有版本数据'''
    requestData = json.loads(request.body)
    version=requestData['version']

    # 汇总数据
    sqlTotal = '''
                SELECT 
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active,
                SUM(CASE WHEN status = 'closed' THEN 1 ELSE 0 END) AS closed,
                SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) AS resolved,
                count(id is not NULL) AS totalBugNum
                FROM zt_bug
        '''
    totalBugData = commonList().getModelData(sqlTotal)

    versiondata = '''
                SELECT 
                COALESCE(SUM(CASE WHEN result = '成功' THEN 1 ELSE 0 END), 0) AS success,
                COALESCE(SUM(CASE WHEN result = '失败' THEN 1 ELSE 0 END), 0) AS fail,
                COALESCE(SUM(CASE WHEN result = '未执行' THEN 1 ELSE 0 END), 0) AS unExect,
                COALESCE(SUM(CASE WHEN result = '阻塞' THEN 1 ELSE 0 END), 0) AS undo_count,
                COALESCE(COUNT(CASE WHEN id IS NOT NULL THEN 1 END), 0) AS totalNum
                FROM 
                    quality_xmind_data
                WHERE 
                    version ='{}'
        '''.format(version)
    print(versiondata)
    TestCaseList = commonList().getModelData(versiondata)


    data = {
                "code": 200,
                "totalBugData": totalBugData,
                "TestCaseList":TestCaseList
            }
    return JsonResponse(data, safe=False)

def selectVersionList(request):
    '''筛选版本名称'''

    requestData = json.loads(request.body)
    owner=requestData['select_owner_value']
    development = requestData['select_development_value']
    status=requestData['select_status_value']
    tableID=requestData['tabelID']

    sql = 'SELECT * FROM quality_versionmanager WHERE '
    conditions = []

    if len(owner) > 0:
        owner_conditions = ["owner LIKE '%{}%'".format(v) for v in owner]
        conditions.append("(" + " OR ".join(owner_conditions) + ")")

    if len(development) > 0:
        development_conditions = ["development LIKE '%{}%'".format(r) for r in development]
        conditions.append("(" + " OR ".join(development_conditions) + ")")

    if len(status) > 0 and '全部' not in status:
        status_conditions = ["status LIKE '%{}%'".format(s) for s in status]
        conditions.append("(" + " OR ".join(status_conditions) + ")")

    if conditions:
        sql += " AND ".join(conditions)

    if len(owner) != 0 or len(development) != 0 or len(status) != 0:
        sql += " and tableID='{}'".format(tableID)

    if len(owner) == 0 and len(development) == 0 and (len(status) == 0 or '全部' in status):
        sql = "SELECT * FROM quality_versionmanager where tableID='{}'".format(tableID)


    print('=======sql========', sql)
    data = commonList().getModelData(sql)


    def convert_lists(item):
        if item['owner']:
            item['owner'] = eval(item['owner'])
        else:
            item['owner']=[]
        if item['development']:
            item['development'] = eval(item['development'])
        else:
            item['development']=[]

        if item['product']:
            item['product'] = eval(item['product'])
        else:
            item['product']=[]
        return item

    # Apply the conversion to each dictionary in the list
    modified_list = [convert_lists(item) for item in data]

    data = {
                "code": 200,
                "data": modified_list
            }
    return JsonResponse(data, safe=False)


@msgMessage
def delVersionManger(request):
    '''删除版本名称'''
    requestData = json.loads(request.body)
    tableID = requestData['tableID']
    autoTableID = requestData['autoTableID']
    print(autoTableID)

    sql='select * from  quality_versionmanager where tableID='+'\''+str(tableID)+'\''
    print('sql=======',sql)
    result=commonList().getModelData(sql)
    if len(result)==1:
        data = {
            "code": 200,
            "msg": "不能再删了，就剩一条了"
        }
    else:
        _Versionmanager = Versionmanager.objects.get(autoTableID=autoTableID)
        print('=====111111======',autoTableID)
        _Versionmanager.delete()
        data = {
            "code": 200,
            "msg": "删除成功"
        }
    return JsonResponse(data, safe=False)

@msgMessage
def editTagsManger(request):
    '''修改版本管理名称'''
    requestData = json.loads(request.body)
    tabledata = requestData['tabledata']

def selectTagsManger(request):
    '''页面初始化查询'''
    sqldata='SELECT tableID FROM quality_versionmanager GROUP BY tableID ORDER BY MAX(autoTableID) desc '
    data = commonList().getModelData(sqldata)
    # print("====data====",data)
    # for i in data:
    #     print(i)
    #     data[i]['owner']=json.loads(i['owner'])
    #     data[i]['development']=json.loads(i['development'])
    return JsonResponse(data, safe=False)
@msgMessage
def selectVersionManger(request):
    '''查询版本管理'''
    requestData = json.loads(request.body)
    tableName=requestData['tableName']

    sql='select * from  quality_versionmanager where tableID ='+"\'"+tableName+"\'"
    # print("sql====", sql)
    data=commonList().getModelData(sql)
    # print("data====", data)

    def convert_lists(item):
        if item['owner']:
            item['owner'] = eval(item['owner'])
        else:
            item['owner']=[]
        if item['development']:
            item['development'] = eval(item['development'])
        else:
            item['development']=[]
        if item['product']:
            item['product'] = eval(item['product'])
        else:
            item['product']=[]
        return item

    # Apply the conversion to each dictionary in the list
    modified_list = [convert_lists(item) for item in data]

    return JsonResponse(modified_list, safe=False)

@msgMessage
def saveSingleVersionManger(request):
    '''保存单个版本'''
    requestData = json.loads(request.body)
    autoTableID = requestData['tabledata']['autoTableID']
    tableName = requestData['tabledata']['tableName']
    tableID = requestData['tabledata']['tableID']
    version = requestData['tabledata']['version']
    description = requestData['tabledata']['description']
    priority = requestData['tabledata']['priority']
    owner = requestData['tabledata']['owner']
    development = requestData['tabledata']['development']
    status = requestData['tabledata']['status']
    testCases = requestData['tabledata']['testCases']
    testCaseReview = requestData['tabledata']['testCaseReview']
    firstRoundTest = requestData['tabledata']['firstRoundTest']
    secondRoundTest = requestData['tabledata']['secondRoundTest']
    thirdRoundTest = requestData['tabledata']['thirdRoundTest']
    remarks = requestData['tabledata']['remarks']
    yueLinProgress = requestData['tabledata']['yueLinProgress']
    yueLinRemarks = requestData['tabledata']['yueLinRemarks']
    juHaoMaiProgress = requestData['tabledata']['juHaoMaiProgress']
    juHaoMaiRemarks = requestData['tabledata']['juHaoMaiRemarks']
    editable = requestData['tabledata']['editable']

    _Versionmanager = Versionmanager()
    if autoTableID:
        _Versionmanager.autoTableID = autoTableID
        _Versionmanager.tableID = tableID
        _Versionmanager.tableName = tableName
        _Versionmanager.version = version
        _Versionmanager.description = description
        _Versionmanager.priority = priority
        _Versionmanager.owner = owner
        _Versionmanager.development = development
        _Versionmanager.status = status
        _Versionmanager.testCases = testCases
        _Versionmanager.testCaseReview = testCaseReview
        _Versionmanager.firstRoundTest = firstRoundTest
        _Versionmanager.secondRoundTest = secondRoundTest
        _Versionmanager.thirdRoundTest = thirdRoundTest
        _Versionmanager.remarks = remarks
        _Versionmanager.yueLinProgress = yueLinProgress
        _Versionmanager.yueLinRemarks = yueLinRemarks
        _Versionmanager.juHaoMaiProgress = juHaoMaiProgress
        _Versionmanager.juHaoMaiRemarks = juHaoMaiRemarks
        _Versionmanager.editable = 0
    else:
        _Versionmanager.tableID = tableID
        _Versionmanager.version = version
        _Versionmanager.tableName = tableName
        _Versionmanager.description = description
        _Versionmanager.priority = priority
        _Versionmanager.owner = owner
        _Versionmanager.development = development
        _Versionmanager.status = status
        _Versionmanager.testCases = testCases
        _Versionmanager.testCaseReview = testCaseReview
        _Versionmanager.firstRoundTest = firstRoundTest
        _Versionmanager.secondRoundTest = secondRoundTest
        _Versionmanager.thirdRoundTest = thirdRoundTest
        _Versionmanager.remarks = remarks
        _Versionmanager.yueLinProgress = yueLinProgress
        _Versionmanager.yueLinRemarks = yueLinRemarks
        _Versionmanager.juHaoMaiProgress = juHaoMaiProgress
        _Versionmanager.juHaoMaiRemarks = juHaoMaiRemarks
        _Versionmanager.editable = 0
    _Versionmanager.save()

    data = {
        "code": 200,
        "msg": "Success"
    }
    return JsonResponse(data, safe=False)
def copyVersionManger(request):
    '''复制当前版本管理'''
    requestData = json.loads(request.body)
    for versionManer in requestData:
        tableName = versionManer['tableName']
        tableID = versionManer['tableID']
        version = versionManer['version']
        description = versionManer['description']
        priority = versionManer['priority']
        owner = versionManer['owner']
        development = versionManer['development']
        status = versionManer['status']
        testCases = versionManer['testCases']
        testCaseReview = versionManer['testCaseReview']
        firstRoundTest = versionManer['firstRoundTest']
        secondRoundTest = versionManer['secondRoundTest']
        thirdRoundTest = versionManer['thirdRoundTest']
        remarks = versionManer['remarks']
        testingTime = versionManer['testingTime']
        product = versionManer['product']
        yueLinProgress = versionManer['yueLinProgress']
        yueLinRemarks = versionManer['yueLinRemarks']
        juHaoMaiProgress = versionManer['juHaoMaiProgress']
        juHaoMaiRemarks = versionManer['juHaoMaiRemarks']
        liveTime = versionManer['liveTime']
        _Versionmanager = Versionmanager()

        _Versionmanager.tableID = tableID
        _Versionmanager.version = version
        _Versionmanager.tableName = tableName
        _Versionmanager.description = description
        _Versionmanager.priority = priority
        _Versionmanager.owner = owner
        _Versionmanager.development = development
        _Versionmanager.status = status
        _Versionmanager.testCases = testCases
        _Versionmanager.testCaseReview = testCaseReview
        _Versionmanager.firstRoundTest = firstRoundTest
        _Versionmanager.secondRoundTest = secondRoundTest
        _Versionmanager.thirdRoundTest = thirdRoundTest
        _Versionmanager.remarks = remarks
        _Versionmanager.liveTime = liveTime
        _Versionmanager.testingTime = testingTime
        _Versionmanager.product = product
        _Versionmanager.yueLinProgress = yueLinProgress
        _Versionmanager.yueLinRemarks = yueLinRemarks
        _Versionmanager.juHaoMaiProgress = juHaoMaiProgress
        _Versionmanager.juHaoMaiRemarks = juHaoMaiRemarks
        _Versionmanager.editable = 0
        _Versionmanager.save()

    data = {
        "code": 200,
        "msg": "复制版本管理信息成功"
    }
    return JsonResponse(data, safe=False)
@msgMessage
def saveVersionManger(request):
    '''保存版本管理'''
    requestData = json.loads(request.body)
    print(requestData)
    if len(requestData)>5: #超过5个内容更新不通知企信
        for versionManer in requestData:
            print(versionManer)
            versionStart = '> 版本信息更新：'
            autoTableID=versionManer['autoTableID']
            tableName=versionManer['tableName']
            tableID=versionManer['tableID']
            version = versionManer['version']
            description = versionManer['description']
            priority = versionManer['priority']
            owner = versionManer['owner']
            development = versionManer['development']
            status = versionManer['status']
            testCases = versionManer['testCases']

            testCaseReview = versionManer['testCaseReview']
            firstRoundTest = versionManer['firstRoundTest']
            secondRoundTest = versionManer['secondRoundTest']
            thirdRoundTest = versionManer['thirdRoundTest']

            remarks = versionManer['remarks']
            yueLinProgress = versionManer['yueLinProgress']
            yueLinRemarks = versionManer['yueLinRemarks']
            juHaoMaiProgress = versionManer['juHaoMaiProgress']
            juHaoMaiRemarks = versionManer['juHaoMaiRemarks']
            testingTime = versionManer['testingTime']
            product=versionManer['product']
            liveTime=versionManer['liveTime']
            editable = versionManer['editable']

            username = request.session.get('username', False)
            selectUserNameSql = "select first_name from auth_user where username=\'{}\'".format(username)
            returnUserNamedata = commonList().getModelData(selectUserNameSql)
            if returnUserNamedata:
                username = returnUserNamedata[0]['first_name']
            else:
                username = "猜猜我是谁，一个来自外太空M78星云的陌生人"
            _Versionmanager = Versionmanager()

            if autoTableID:
                _Versionmanager.autoTableID=autoTableID
                _Versionmanager.tableID = tableID
                _Versionmanager.tableName=tableName
                _Versionmanager.version = version
                _Versionmanager.description = description
                _Versionmanager.priority = priority
                _Versionmanager.owner = owner
                _Versionmanager.development = development
                _Versionmanager.status = status
                _Versionmanager.testCases = testCases
                _Versionmanager.testCaseReview = testCaseReview
                _Versionmanager.firstRoundTest = firstRoundTest
                _Versionmanager.secondRoundTest = secondRoundTest
                _Versionmanager.thirdRoundTest = thirdRoundTest
                _Versionmanager.liveTime=liveTime
                _Versionmanager.testingTime = testingTime
                _Versionmanager.product=product
                _Versionmanager.remarks = remarks
                _Versionmanager.yueLinProgress = yueLinProgress
                _Versionmanager.yueLinRemarks = yueLinRemarks
                _Versionmanager.juHaoMaiProgress = juHaoMaiProgress
                _Versionmanager.juHaoMaiRemarks = juHaoMaiRemarks
                _Versionmanager.editable = 0
                _Versionmanager.save()

            else:
                _Versionmanager.tableID = tableID
                _Versionmanager.version = version
                _Versionmanager.tableName = tableName
                _Versionmanager.description = description
                _Versionmanager.priority = priority
                _Versionmanager.owner = owner
                _Versionmanager.development = development
                _Versionmanager.status = status
                _Versionmanager.testCases = testCases
                _Versionmanager.testCaseReview = testCaseReview
                _Versionmanager.firstRoundTest = firstRoundTest
                _Versionmanager.secondRoundTest = secondRoundTest
                _Versionmanager.thirdRoundTest = thirdRoundTest
                _Versionmanager.remarks = remarks
                _Versionmanager.testingTime = testingTime
                _Versionmanager.product = product
                _Versionmanager.liveTime = liveTime
                _Versionmanager.yueLinProgress = yueLinProgress
                _Versionmanager.yueLinRemarks = yueLinRemarks
                _Versionmanager.juHaoMaiProgress = juHaoMaiProgress
                _Versionmanager.juHaoMaiRemarks = juHaoMaiRemarks
                _Versionmanager.editable = 0
                _Versionmanager.save()
        
    else:    
        for versionManer in requestData:
            print(versionManer)
            versionStart = '> 版本信息更新：'
            autoTableID=versionManer['autoTableID']
            tableName=versionManer['tableName']
            tableID=versionManer['tableID']
            version = versionManer['version']
            description = versionManer['description']
            priority = versionManer['priority']
            owner = versionManer['owner']
            development = versionManer['development']
            status = versionManer['status']
            testCases = versionManer['testCases']

            testCaseReview = versionManer['testCaseReview']
            firstRoundTest = versionManer['firstRoundTest']
            secondRoundTest = versionManer['secondRoundTest']
            thirdRoundTest = versionManer['thirdRoundTest']

            remarks = versionManer['remarks']
            yueLinProgress = versionManer['yueLinProgress']
            yueLinRemarks = versionManer['yueLinRemarks']
            juHaoMaiProgress = versionManer['juHaoMaiProgress']
            juHaoMaiRemarks = versionManer['juHaoMaiRemarks']
            testingTime = versionManer['testingTime']
            product=versionManer['product']
            liveTime=versionManer['liveTime']
            editable = versionManer['editable']

            username = request.session.get('username', False)
            selectUserNameSql = "select first_name from auth_user where username=\'{}\'".format(username)
            returnUserNamedata = commonList().getModelData(selectUserNameSql)
            if returnUserNamedata:
                username = returnUserNamedata[0]['first_name']
            else:
                username = "猜猜我是谁，一个来自外太空M78星云的陌生人"
            _Versionmanager = Versionmanager()

            if autoTableID:
                _Versionmanager.autoTableID=autoTableID
                _Versionmanager.tableID = tableID
                _Versionmanager.tableName=tableName
                _Versionmanager.version = version
                _Versionmanager.description = description
                _Versionmanager.priority = priority
                _Versionmanager.owner = owner
                _Versionmanager.development = development
                _Versionmanager.status = status
                _Versionmanager.testCases = testCases
                _Versionmanager.testCaseReview = testCaseReview
                _Versionmanager.firstRoundTest = firstRoundTest
                _Versionmanager.secondRoundTest = secondRoundTest
                _Versionmanager.thirdRoundTest = thirdRoundTest
                _Versionmanager.liveTime=liveTime
                _Versionmanager.testingTime = testingTime
                _Versionmanager.product=product
                _Versionmanager.remarks = remarks
                _Versionmanager.yueLinProgress = yueLinProgress
                _Versionmanager.yueLinRemarks = yueLinRemarks
                _Versionmanager.juHaoMaiProgress = juHaoMaiProgress
                _Versionmanager.juHaoMaiRemarks = juHaoMaiRemarks
                _Versionmanager.editable = 0
                _Versionmanager.save()

                if len(testCases) == 0:
                    testCases = 0
                if len(testCaseReview) == 0:
                    testCaseReview = 0
                if len(firstRoundTest) == 0:
                    firstRoundTest = 0
                if len(secondRoundTest) == 0:
                    secondRoundTest = 0
                if len(thirdRoundTest) == 0:
                    thirdRoundTest = 0

                from datetime import  datetime,timedelta


                if liveTime:
                    liveTime=liveTime[:10]
                    date_obj = datetime.strptime(liveTime, "%Y-%m-%d")
                    next_day = date_obj + timedelta(days=1)
                    liveTime = next_day.strftime("%Y-%m-%d")
                else:
                    liveTime=''

                if testingTime:
                    testingTime=testingTime[:10]
                    testing_date_obj = datetime.strptime(testingTime, "%Y-%m-%d")
                    testing_next_day = testing_date_obj + timedelta(days=1)
                    testingTime = testing_next_day.strftime("%Y-%m-%d")
                else:
                    testingTime=''
        
                dingMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2',versionStart,username,tableID,version,description,owner,development,product, status,
                                                    testingTime, liveTime, testCases, testCaseReview,
                                                    firstRoundTest, secondRoundTest, thirdRoundTest, remarks)

            else:
                _Versionmanager.tableID = tableID
                _Versionmanager.version = version
                _Versionmanager.tableName = tableName
                _Versionmanager.description = description
                _Versionmanager.priority = priority
                _Versionmanager.owner = owner
                _Versionmanager.development = development
                _Versionmanager.status = status
                _Versionmanager.testCases = testCases
                _Versionmanager.testCaseReview = testCaseReview
                _Versionmanager.firstRoundTest = firstRoundTest
                _Versionmanager.secondRoundTest = secondRoundTest
                _Versionmanager.thirdRoundTest = thirdRoundTest
                _Versionmanager.remarks = remarks
                _Versionmanager.testingTime = testingTime
                _Versionmanager.product = product
                _Versionmanager.liveTime = liveTime
                _Versionmanager.yueLinProgress = yueLinProgress
                _Versionmanager.yueLinRemarks = yueLinRemarks
                _Versionmanager.juHaoMaiProgress = juHaoMaiProgress
                _Versionmanager.juHaoMaiRemarks = juHaoMaiRemarks
                _Versionmanager.editable = 0
                _Versionmanager.save()

    data = {
        "code": 200,
        "msg": "保存版本管理信息成功"
    }
    return JsonResponse(data, safe=False)

def dingMessage(url,versionStart,username,tableID,version,description,owner,development,product, status,
                        testingTime, liveTime, testCases, testCaseReview,
                        firstRoundTest, secondRoundTest, thirdRoundTest, remarks):
    '''叮叮消息通知'''
    import requests
    import json

    versionInfo = '''
                \n\n > 更新人: <font color=#303133>{}</font>  
                \n\n > 迭代: <font color=#303133>{}</font> 
                \n\n > 版本 : <font color=#303133>{}</font> 
                \n\n > 需求 : <font color=#303133>{}</font>  
                \n\n > 负责人 : <font color=#303133>{}</font>  
                \n\n > 开发者 : <font color=#303133>{}</font>  
                \n\n > 产品 : <font color=#303133>{}</font>  
                \n\n > 需求状态 ：<font color=#303133>{}</font>  
                \n\n > 提测时间 ：<font color=#303133>{}</font>  
                \n\n > 上线时间 ：<font color=#303133>{}</font>  
                \n\n > 编写测试用例 ：<font color=#303133>{}%</font>  
                \n\n > 测试用例评审 ：<font color=#303133>{}%</font>  
                \n\n > 一轮测试进度 ：<font color=#303133>{}%</font>  
                \n\n > 二轮测试进度 ：<font color=#303133>{}%</font>  
                \n\n > 三轮测试进度 ：<font color=#303133>{}%</font>
                \n\n > 版本备注：<font color=#303133>{}</font>
                '''.format(
                    username,tableID, version, description, owner, development, product, status,
                    testingTime, liveTime, testCases, testCaseReview,
                    firstRoundTest, secondRoundTest, thirdRoundTest, remarks
                )
    versionStart = versionStart + versionInfo + '\n'

    url = url

    payload = json.dumps({
    "msgtype": "markdown",
    "markdown": {
        "title": "版本信息更新",
        "text": versionStart,
        "at": {
        "isAtAll": True
        }
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)



def readLog(request):
    '''读取日志文件'''
    # log_file_path = '/Users/hll/Desktop/git/platform/logs/webtestcase.txt'
    log_file_path = '/root/platform/logs/webtestcase.txt'
    logList=[]
    # 或者按行读取日志文件内容
    with open(log_file_path, 'r', encoding='gbk') as log_file:
        for line in log_file:
            line=line.strip()
            logList.append(line)
    return JsonResponse(logList, safe=False)
@msgMessage
def selectTableList(request):
    '''查询所有表'''
    import mysql.connector
    # 连接到MySQL数据库
    conn = mysql.connector.connect(
        host='rm-2zea97l06569u3s1zyo.mysql.rds.aliyuncs.com',
        user='tk_db_test',
        password='UUueBYYs9U4uptj',
        database='store'
    )
    # 创建游标对象
    cursor = conn.cursor()
    sql = 'show tables'
    cursor.execute(sql)
    response=cursor.fetchall()
    responsedata=[{'value': table[0], 'label': table[0]} for table in response]
    # print(response)
    conn.close()
    cursor.close()
    return  JsonResponse(responsedata, safe=False)

@msgMessage
def selectTableDegion(request):
    '''查询表结构'''
    import mysql.connector
    # 连接到MySQL数据库
    conn = mysql.connector.connect(
        host='rm-2zea97l06569u3s1zyo.mysql.rds.aliyuncs.com',
        user='tk_db_test',
        password='UUueBYYs9U4uptj',
        database='store'
    )

    cursor = conn.cursor()
    requestData = json.loads(request.body)
    tableName=requestData['tableName']
    sql_info = "SELECT COLUMN_NAME,IS_NULLABLE,DATA_TYPE,COLUMN_TYPE,COLUMN_COMMENT FROM INFORMATION_SCHEMA.COLUMNS WHERE  TABLE_NAME = '{}'".format(tableName)
    cursor.execute(sql_info)
    # for column_info in  cursor.fetchall():
    #     print(f"Name: {column_info[0]}, Type: {column_info[1]}, Nullable: {column_info[2]}, Key: {column_info[3]}, Comment: {column_info[4]}{column_info[6]}")

    def dictfetchall(varr):
        "将游标返回的结果保存到一个字典对象中"
        desc = varr.description
        return [dict(zip([col[0] for col in desc], row)) for row in varr.fetchall()]

    formatted_data=dictfetchall(cursor)
    # formatted_data = [
    #     {
    #         "field": row[0],
    #         "type": row[1],
    #         "length": row[2],
    #         "isNullable": row[3] == "YES",
    #         "isPrimary": row[4] == "PRI",
    #         "defaultValue": row[5],
    #         "comments": row[6]
    #     }
    #     for row in response
    # ]

    conn.close()
    cursor.close()

    return JsonResponse(formatted_data, safe=False)
@msgMessage
#sql语句查询
def sqlcat(request):
    """sql查询"""
    try:
        import mysql.connector
        # 连接到MySQL数据库
        conn = mysql.connector.connect(
            host='rm-2zea97l06569u3s1zyo.mysql.rds.aliyuncs.com',
            user='tk_db_test',
            password='UUueBYYs9U4uptj',
            database='store'
        )
        def dictfetchall(varr):
            "将游标返回的结果保存到一个字典对象中"
            desc = varr.description
            return [dict(zip([col[0] for col in desc], row))for row in varr.fetchall()]

        # 创建游标对象
        cursor = conn.cursor()
        requestData = json.loads(request.body)
        sql=requestData['sql']
        if  'select' in sql:
            if "limit" not in sql:
                sql=sql+' limit 100'

            try:
                cursor.execute(sql)
            except Exception as e:
                return JsonResponse(e, safe=False)
            # 获取查询结果的字段名称
            columns = [desc[0] for desc in cursor.description]
            tableData=dictfetchall(cursor)
            response = {
                "sql":sql,
                'columns':columns,
                'tableData':tableData
            }
            cursor.close()

        else:
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            response={
                "status":"success"
            }
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse(e, safe=False)
@msgMessage
#上传文件
def download_files(request):
    file_paths = json.loads(request.body)
    log.info("file_paths==={}".format(file_paths))
    files_exist = all(Path(file_path["url"]).exists() for file_path in file_paths)
    if files_exist:
        zip_file_path = '/root/zip/file.zip'
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for file_path in file_paths:
                zip_file.write(file_path["url"], os.path.basename(file_path["name"]))

        response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_file_path)}"'
        return response
    else:
        return JsonResponse({'error': 'One or more files do not exist.'}, status=400)



@msgMessage
def upload(request):
    data=[]
    # print('上传文件',request.POST)
    req = request.FILES.get('file')
    # print(req)
    # 将上传的文件逐行读取保存到list中
    file_info = {'date': '', 'name': '', 'uuid': '', 'path': ''}
    content = {}
    # for line in req.read().splitlines():
    #     content.append(line)

    #测试
    #path="D:\\testPlatForm\\TestPlat\\platForm\\media"

    #线上
    path="/root/platform/media"
    fileName=os.path.join(path, req.name)
    # 打开特定的文件进行二进制的写操作
    destination = open(fileName, 'wb+')
    for chunk in req.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    content["name"]=req.name
    content["url"]=fileName

    #返回状态信息
    data.append(content)

    return JsonResponse(data, safe=False)

#删除脚本
@msgMessage
def deleteApiScript(request):
    '''删除脚本'''
    urlName=request.POST.get('urlName')
    projectName = request.POST.get('projectName')
    versionName = request.POST.get('versionName')

    #获取项目名称
    projectSql = 'select modelData from quality_modeldata where modeldata_id= ' + projectName
    projectName = (commonList().getModelData(projectSql))

    #获取版本名称
    versionSql = 'select modelData from quality_modeldata where modeldata_id= ' + versionName
    versionName = (commonList().getModelData(versionSql))


    API_path=os.path.join('/root/jmeter/apache-jmeter-5.4.1/script/',projectName[0]["modelData"],versionName[0]["modelData"],urlName)
    Perfer_path=os.path.join('/root/jmeter/apache-jmeter-5.4.1/ProScript/',projectName[0]["modelData"],versionName[0]["modelData"],urlName)
    firstFileName='/root/platform/media/'+urlName


    if os.path.exists(API_path):
        os.remove(API_path)

    if os.path.exists(Perfer_path):
        os.remove(Perfer_path)

    if os.path.exists(firstFileName):
        os.remove(firstFileName)
        data = {
            "code": 200,
            "msg": "执行成功"
        }

    return JsonResponse(data, safe=False)

@msgMessage
def createScriptFile(request):
    '''新建脚本文件'''
    dataList = request.POST
    print()

    for i in dataList.keys():
        dataDictList = json.loads(i)
        # 获取执行人姓名
        username = request.session.get('username', False)

        # 获取项目地址
        projectName_id = dataDictList['projectName']
        sql = 'select modelData from quality_modeldata where modeldata_id= ' + str(projectName_id)
        projectName = (commonList().getModelData(sql))

        # 获取版本地址
        modelDataId = dataDictList['versionName']
        modelDataSql = 'select modelData from quality_modeldata where modeldata_id= ' + str(modelDataId)
        modelDataLIst = (commonList().getModelData(modelDataSql))
        modelData = modelDataLIst[0]["modelData"]

        # 创建build文件目录
        ant_build = "/root/ant/apache-ant-1.9.16/build/"
        if not os.path.exists(ant_build + projectName[0]["modelData"] + "/" + modelData):
            os.makedirs(ant_build + projectName[0]["modelData"] + "/" + modelData)

        # ant build文件地址
        antBuildAddress = ant_build + projectName[0]["modelData"] + "/" + modelData + "/build.xml"

        # 创建测试报告文件夹
        testReportAddress = '/root/platform/static/'

        if not os.path.exists(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/html/"):
            os.makedirs(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/html/")
        if not os.path.exists(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/jtl/"):
            os.makedirs(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/jtl/")

        if not os.path.exists(
                testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/html/"):
            os.makedirs(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/html/")

        folder_path = os.path.join(testReportAddress, projectName[0]["modelData"], modelData, "PerformanceReport",
                                   "jtl")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        performanceJtlAddress = testReportAddress + projectName[0][
            "modelData"] + "/" + modelData + "/PerformanceReport/jtl/"

        # 接口报告文件夹
        apiReportAdd = testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/"

        # 性能测试报告文件夹
        perFormanceReportAdd = testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/"

        # 接口报告
        apiReport = '/static/' + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/" + "html/TestReport.html"

        # 性能测试报告
        perFormanceReport = '/static/' + projectName[0][
            "modelData"] + "/" + modelData + "/PerformanceReport/" + "html/index.html"

        # 创建日志文件
        log_path = "/root/platform/logs/"

        if not os.path.exists(
                os.path.join(log_path + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/")):
            os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/")
        if not os.path.exists(os.path.join(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/")):
            os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/")
        if not os.path.exists(os.path.join(
                log_path + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/" + "log.text")):
            os.mknod(log_path + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/" + "log.text")
        if not os.path.exists(
                os.path.join(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/" + "log.text")):
            os.mknod(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/" + "log.text")

        # 创建脚本目录
        # 接口测试脚本
        apiScriptFilePath = '/root/jmeter/apache-jmeter-5.4.1/script/'

        # 性能测试脚本
        performanceScriptFilePath = '/root/jmeter/apache-jmeter-5.4.1/ProScript/'

        if not os.path.exists(apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData):
            os.makedirs(apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData)

        if not os.path.exists(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData):
            os.makedirs(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData)

        apiScriptfile = apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData
        perFormanceScriptfile = performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData + "/*.jmx"

        performanceData = "jmeter -n -t " + perFormanceScriptfile + " -l " + performanceJtlAddress + " -e -o " + perFormanceReportAdd + "html"

        if "projectstatus" not in dataDictList.keys():
            status = "Flase"
        else:
            status = dataDictList['projectstatus']

        if dataDictList['buildAddress'] == '':
            dataDictList['buildAddress'] = antBuildAddress

        if dataDictList['reportAddress'] == "":
            dataDictList['reportAddress'] = apiReport

        if dataDictList['performanceReport'] == '':
            dataDictList['performanceReport'] = perFormanceReport

        environmentData = dataDictList['environment']
        sceiptProject_id = dataDictList['sceiptProject_id']
        projectName = dataDictList['projectName']
        versionName = dataDictList['versionName']
        buildAddress = dataDictList['buildAddress']
        reportAddress = dataDictList['reportAddress']

        scriptName = dataDictList['urlList']
        executeType = dataDictList['executeType']
        performanceData = performanceData
        performanceReport = dataDictList['performanceReport']
        if dataDictList['creater'] == '':
            creater = username
        else:
            creater = dataDictList['creater']
        _scriptProject = Scriptproject()


        _scriptProject.projectName = projectName
        _scriptProject.versionName = versionName
        _scriptProject.buildAddress = buildAddress
        _scriptProject.reportAddress = reportAddress
        _scriptProject.environment = environmentData
        _scriptProject.scriptName = scriptName
        _scriptProject.executeType = executeType
        _scriptProject.performanceData = performanceData
        _scriptProject.performanceReport = performanceReport
        _scriptProject.creater = creater
        _scriptProject.status = status
        time = datetime.now()
        _scriptProject.createtime = time.strftime("%Y-%m-%d %H:%M:%S")
        _scriptProject.save()
        data = {
            "code": 200,
            "msg": "接口脚本保存成功"
        }
        return JsonResponse(data, safe=False)

#保存脚本地址
@msgMessage
def saveScriptFile(request):
    '''保存脚本文件地址'''
    dataDictList = json.loads(request.body)
    # 获取执行人姓名
    username = request.session.get('username', False)

    # 获取项目地址
    projectName_id =dataDictList['projectName']
    sql = 'select modelData from quality_modeldata where modeldata_id= ' + str(projectName_id)
    projectName = (commonList().getModelData(sql))

    # 获取版本地址
    modelDataId = dataDictList['versionName']
    modelDataSql = 'select modelData from quality_modeldata where modeldata_id= ' + str(modelDataId)
    modelDataLIst=(commonList().getModelData(modelDataSql))
    modelData=modelDataLIst[0]["modelData"]


    # 创建build文件目录
    ant_build = "/root/ant/apache-ant-1.9.16/build/"
    # if not os.path.exists(ant_build + projectName[0]["modelData"] + "/" + modelData):
    #     os.makedirs(ant_build + projectName[0]["modelData"] + "/" + modelData)

    #ant build文件地址
    antBuildAddress=ant_build + projectName[0]["modelData"] + "/" + modelData+"/build.xml"

    # 创建测试报告文件夹
    testReportAddress = '/root/platform/static/'

    # if not os.path.exists(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/html/"):
    #
    #     os.makedirs(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/html/")
    # if not os.path.exists(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/jtl/"):
    #     os.makedirs(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/jtl/")
    #
    # if not os.path.exists(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/html/"):
    #     os.makedirs(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/html/")
    #
    # folder_path = os.path.join(testReportAddress, projectName[0]["modelData"], modelData, "PerformanceReport","jtl")
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)

    performanceJtlAddress=testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/jtl/"

    #接口报告文件夹
    apiReportAdd = testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/"

    #性能测试报告文件夹
    perFormanceReportAdd=testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/"

    testUIReportAddress="/root/platform/playwright/UI_test_framework/testcase/"

    #UI测试报告文件夹
    UIPormanceReportAdd=testReportAddress + projectName[0]["modelData"] + "/" + modelData+"/UIReport"

    #UI脚本执行结果文件夹
    UIreportRestlt=testReportAddress + projectName[0]["modelData"] + "/" + modelData+"/UIReport/results"

    #UI脚本执行生成测试报告文件夹
    UIreportHtml=testReportAddress + projectName[0]["modelData"] + "/" + modelData+"/UIReport/html"

    #UI测试报告
    UIreport="/static/" + projectName[0]["modelData"] + "/" + modelData+"/UIReport/"+"html/index.html"

    #UI测试脚本位置
    UIscriptAddress=testUIReportAddress+projectName[0]["modelData"] + "/" + modelData+"/UIReport/script"



    #判断是否有脚本执行文件，没有会创建
    # if not  os.path.exists(UIscriptAddress):
    #     os.makedirs(UIscriptAddress)

    #UI执行命令
    UIdata="pytest  {}  --alluredir={}".format(UIscriptAddress,UIreportRestlt)

    #UI根据生成的测试数据生成测试报告
    execUIReport="allure generate {} -o {} --clean".format(UIreportRestlt,UIreportHtml)

    #接口报告
    apiReport='/static/'+ projectName[0]["modelData"] + "/" + modelData + "/ApiReport/"+"html/TestReport.html"

    #性能测试报告
    perFormanceReport='/static/'+ projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/"+"html/index.html"

    # 创建日志文件
    log_path = "/root/platform/logs/"


    # if not os.path.exists(os.path.join(log_path + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/")):
    #     os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/")
    # if not os.path.exists(os.path.join(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/")):
    #     os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/")
    # if not os.path.exists(os.path.join(log_path + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/" + "log.text")):
    #     os.mknod(log_path + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/" + "log.text")
    # if not os.path.exists(os.path.join(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/" + "log.text")):
    #     os.mknod(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/" + "log.text")

    #创建脚本目录
    #接口测试脚本
    apiScriptFilePath = '/root/jmeter/apache-jmeter-5.4.1/script/'

    #性能测试脚本
    performanceScriptFilePath = '/root/jmeter/apache-jmeter-5.4.1/ProScript/'

    if not os.path.exists(apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData):
        os.makedirs(apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData)
        log.info("=====接口文件已创建==="+apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData)
    
    if not os.path.exists(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData):
        os.makedirs(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData)
        log.info("======性能脚本文件已创建======"+performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData)

    if not os.path.exists(UIscriptAddress):
        os.makedirs(UIscriptAddress)
        log.info("======UI脚本文件已创建======"+UIscriptAddress)

        

    apiScriptfile=apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData
    perFormanceScriptfile=performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData+"/*.jmx"

    performanceData = "jmeter -n -t "+perFormanceScriptfile+" -l "+performanceJtlAddress+" -e -o "+perFormanceReportAdd+"html"


    if "projectstatus" not in dataDictList.keys():
        status="Flase"
    else:
        status=dataDictList['projectstatus']

    if dataDictList['buildAddress']=='':
        dataDictList['buildAddress']=antBuildAddress

    if dataDictList['reportAddress']=="":
        dataDictList['reportAddress']=apiReport

    if dataDictList['performanceReport']=='':
        dataDictList['performanceReport']=perFormanceReport

    environmentData=dataDictList['environment']
    sceiptProject_id = dataDictList['sceiptProject_id']
    projectName = dataDictList['projectName']
    versionName = dataDictList['versionName']
    buildAddress = dataDictList['buildAddress']
    reportAddress = dataDictList['reportAddress']

    scriptName = dataDictList['urlList']
    executeType = dataDictList['executeType']
    performanceData = performanceData
    performanceReport = dataDictList['performanceReport']
    if dataDictList['creater']=='':
        creater = username
    else:
        creater=dataDictList['creater']
    _scriptProject=Scriptproject()

    if sceiptProject_id:
        _scriptProject.sceiptProject_id=sceiptProject_id
        _scriptProject.projectName = projectName
        _scriptProject.versionName = versionName
        _scriptProject.buildAddress = buildAddress
        _scriptProject.reportAddress = reportAddress
        _scriptProject.environment = environmentData
        _scriptProject.scriptName = scriptName
        _scriptProject.executeType = executeType
        _scriptProject.performanceData = performanceData
        _scriptProject.performanceReport = performanceReport
        _scriptProject.UIdata=UIdata
        _scriptProject.UIExcReport=execUIReport
        _scriptProject.UIReport=UIreport
        _scriptProject.UIScript=UIscriptAddress
        _scriptProject.creater=creater
        time = datetime.now()
        _scriptProject.createtime = time.strftime("%Y-%m-%d %H:%M:%S")
        _scriptProject.status=status
        _scriptProject.save()
        data={
            "code":200,
            "msg":"接口脚本编辑成功"
        }
        return JsonResponse(data,safe=False)
    else:
        _scriptProject.projectName = projectName
        _scriptProject.versionName = versionName
        _scriptProject.buildAddress = buildAddress
        _scriptProject.reportAddress = reportAddress
        _scriptProject.environment = environmentData
        _scriptProject.scriptName = scriptName
        _scriptProject.executeType = executeType
        _scriptProject.UIdata=UIdata
        _scriptProject.UIExcReport=execUIReport
        _scriptProject.UIReport=UIreport
        _scriptProject.UIScript=UIscriptAddress
        _scriptProject.performanceData = performanceData
        _scriptProject.performanceReport = performanceReport
        _scriptProject.creater = creater
        _scriptProject.status = status
        time = datetime.now()
        _scriptProject.createtime = time.strftime("%Y-%m-%d %H:%M:%S")
        _scriptProject.save()
        data = {
            "code": 200,
            "msg": "接口脚本保存成功"
        }
        return JsonResponse(data, safe=False)
#删除脚本信息
@msgMessage
def deleteScriptFile(request):
    '''删除脚本信息'''
    sceiptProject_id = request.POST.get('sceiptProject_id')
    _Scriptproject = Scriptproject.objects.get(sceiptProject_id=sceiptProject_id)
    _Scriptproject.delete()
    data={
        "code":200,
        "msg":"脚本文件删除成功"
    }
    return JsonResponse(data, safe=False)
#查询接口脚本信息
def selectScriptFile(request):
    '''查询测试脚本信息'''
    response = json.loads(request.body)
    versionName=response['versionName']
    import ast
    sql='''SELECT
            a.*, 
            b.*, 
            c.*, 
            d.modeldata
        FROM
            quality_scriptproject a
        JOIN
            quality_modeldata b ON a.versionName = b.modeldata_id
        JOIN
            auth_user c ON a.creater = c.username
        JOIN
            quality_modeldata d ON b.subModelData = d.modeldata_id
        WHERE
            a.environment = '1'
            and d.modelData=\'{}\'
        ORDER BY
            a.createtime DESC'''.format(versionName)
    # print(sql)
    data = commonList().getModelData(sql)
    # print(data)
    for projectData in data:
        # print(projectData["scriptName"])
        projectData["scriptName"]=ast.literal_eval(projectData["scriptName"])
    return JsonResponse(data, safe=False)
@msgMessage
def selectProScriptFile(request):
    '''查询生产脚本信息'''
    import ast
    sql="select * from quality_scriptproject a,quality_modeldata b,auth_user C where a.versionName=b.modeldata_id AND a.creater=c.username and a.environment='2' order by a.createtime DESC "
    data = commonList().getModelData(sql)
    # print(data)
    for projectData in data:
        # print(projectData["scriptName"])
        projectData["scriptName"]=ast.literal_eval(projectData["scriptName"])
    return JsonResponse(data, safe=False)

# 获取测试报告地址是否存在
@msgMessage
def getReportFileData(request):
    '''获取报告状态'''
    requestData = json.loads(request.body)

    reportAddress=requestData['reportAddress']
    performanceReport = requestData['performanceReport']
    UIReport=requestData['UIReport']
    executeType = requestData['executeType']

    if executeType=='0' and os.path.exists('/root/platform'+reportAddress):
        data = {
            "code": 200,
            "msg": "接口测试报告地址存在"
        }
        return  JsonResponse(data, safe=False)

    elif executeType=='1' and os.path.exists('/root/platform'+performanceReport):
        data = {
            "code": 200,
            "msg": "性能测试报告地址存在"
        }
        return JsonResponse(data, safe=False)
    elif executeType=='0'and not os.path.exists('/root/platform'+reportAddress):

        data = {
            "code": 401,
            "msg": "接口测试报告还未生成,请稍等"
        }

        return JsonResponse(data, safe=False)
    elif executeType=='2' and os.path.exists('/root/platform'+UIReport):

        data = {
            "code": 200,
            "msg": "UI测试报告地址存在"
        }

        return JsonResponse(data, safe=False)
    elif executeType=='2' and not os.path.exists('/root/platform'+UIReport):

        data = {
            "code": 402,
            "msg": "UI测试报告还未生成,请稍等"
        }

        return JsonResponse(data, safe=False)
    else:
        data = {
            "code": 403,
            "msg": "测试报告还未生成,请稍等"
        }

        return JsonResponse(data, safe=False)



# 执行脚本
@msgMessage
def executeScript(request):
    '''执行脚本'''
    # try:
    log.info("======自动化开始执行======")
    requestData = json.loads(request.body)
    executeType=requestData["executeType"]
    buildAddress=requestData["buildAddress"]
    performanceData=requestData["performanceData"]
    scriptName=requestData["scriptName"]
    sceiptProject_id=requestData['sceiptProject_id']

    # 获取项目地址
    projectName_id = requestData['projectName']
    sql = 'select modelData from quality_modeldata where modeldata_id= ' + str(projectName_id)
    projectName = (commonList().getModelData(sql))

    # 获取版本地址
    modelDataId = requestData['versionName']
    modelDataSql = 'select modelData from quality_modeldata where modeldata_id= ' + str(modelDataId)
    modelDataLIst = (commonList().getModelData(modelDataSql))
    modelData = modelDataLIst[0]["modelData"]
    log.info("获取到的项目名称{},版本名称{}".format(projectName,modelData))
    UIScriptAddress='/root/platform/playwright/UI_test_framework/testcase/'

    #判断是否有删除文件
    def check_and_delete_files(folder_path, files_to_check):
        log.info("======删除文件开始执行========")
        all_files = os.listdir(folder_path)

        for file_name in all_files:
            # 构建文件的完整路径
            file_path = os.path.join(folder_path, file_name)
            log.info("file_path={}".format(file_path))
            # 检查文件是否存在于文件名列表中
            matching_files = [file for file in files_to_check if file["name"] == file_name and os.path.isfile(file_path)]
            # 如果没有找到匹配的文件，删除文件
            if not matching_files:
                # os.remove(file_path)
                os.system("rm -rf {}".format(file_path))
                log.info("没有匹配上文件,开始删除文件{}".format(file_path))
    substrings_to_check=scriptName
    if executeType == '0' or executeType == False:#接口
        directory_path='/root/jmeter/apache-jmeter-5.4.1/script/'+projectName[0]["modelData"] + "/" + modelData + "/"
    elif executeType == '2':#UI
        directory_path='/root/platform/playwright/UI_test_framework/testcase/'+projectName[0]["modelData"] + "/" + modelData + "/UIReport/script/"
    else:
        directory_path='/root/jmeter/apache-jmeter-5.4.1/ProScript/'+projectName[0]["modelData"] + "/" + modelData + "/"


    #删除已经删除的脚本
    check_and_delete_files(directory_path,substrings_to_check)

    #获取UI
    UIdata=requestData['UIdata']
    UIExcReport=requestData['UIExcReport']
    UIReport=requestData['UIReport']
    UIScript=requestData['UIScript']

    #创建build文件目录
    ant_build="/root/ant/apache-ant-1.9.16/build/"
    log_path="/root/platform/logs/"
    if not os.path.exists(ant_build+projectName[0]["modelData"]+"/"+modelData):
        os.makedirs(ant_build+projectName[0]["modelData"]+"/"+modelData)

    #创建测试报告文件夹
    testReportAddress='/root/platform/static/'
    if not  os.path.exists(testReportAddress+projectName[0]["modelData"]+"/"+modelData):
        os.makedirs(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/ApiReport/")
        os.makedirs(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/")

    #判断UI测试文件夹是否存在
    if not  os.path.exists(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/"):
        os.makedirs(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/results")
        os.makedirs(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/html")
        
    #判断UI测试日志是否存在
    if not  os.path.exists(log_path + projectName[0]["modelData"] + "/" + modelData + "/UILog/"):
        os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/UILog/")
        os.mknod(log_path + projectName[0]["modelData"] + "/" + modelData + "/UILog/" + "log.text")
        log.info("=====UI文件已创建======")
     
    # #创建日志文件
    
    if not os.path.exists(log_path+projectName[0]["modelData"]+"/"+modelData):
        #创建日志文件夹
        os.makedirs(log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/")
        os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/")
       

        #创建日志文件
        os.mknod(log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text")
        os.mknod(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/" + "log.text")
        

    #创建脚本目录
    #接口脚本
    apiScriptFilePath = '/root/jmeter/apache-jmeter-5.4.1/script/'

    #性能接口脚本
    performanceScriptFilePath = '/root/jmeter/apache-jmeter-5.4.1/ProScript/'


    if not os.path.exists(apiScriptFilePath+projectName[0]["modelData"] + "/" + modelData):
        os.makedirs(apiScriptFilePath+projectName[0]["modelData"] + "/" + modelData)
    if not os.path.exists(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData):
        os.makedirs(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData)
    if not os.path.exists(UIScriptAddress + projectName[0]["modelData"] + "/" + modelData+"/UIReport/script/"):
        os.makedirs(UIScriptAddress + projectName[0]["modelData"] + "/" + modelData+"/UIReport/script/") 
        log.info("UI文件不存在开始创建")

    
    #复制脚本到对应的文件夹
    fileUrlList=[i["url"] for i in scriptName]
    if executeType == '0' or executeType == False:#接口
        for fileUrl in fileUrlList:
            fileName = os.path.split(fileUrl)[1]  # 读取文件名
            fullFilePath = apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData + "/" + fileName
            if os.path.exists(fullFilePath):
                pass
            else:
                log.info("=========================复制接口脚本=======================")
                sourceFilePath='/root/platform/media/'+fileName
                shutil.copyfile(sourceFilePath,fullFilePath)
                log.info("复制接口脚本成功{}".format(fullFilePath))
    elif executeType == '2':
        log.info("========开始复制文件=======")
        for fileUrl in fileUrlList:
            fileName = os.path.split(fileUrl)[1]  # 读取文件名
            fullFilePath = UIScriptAddress + projectName[0]["modelData"] + "/" + modelData+"/UIReport/script/"+ fileName
            if os.path.exists(fullFilePath):
                pass
            else:
                log.info("=========================开始复制UI脚本=======================")
                sourceFilePath='/root/platform/media/'+fileName
                shutil.copyfile(sourceFilePath,fullFilePath)
                log.info("=======复制UI脚本成功{}=========".format(fullFilePath))

    else:
        for fileUrl in fileUrlList:
            fileName = os.path.split(fileUrl)[1]  # 读取文件名
            fullFilePath = performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData + "/" + fileName
            if os.path.exists(fullFilePath):
                pass
            else:
                log.info("========================复制性能脚本=================")
                sourceFilePath = '/root/platform/media/' + fileName
                shutil.copyfile(sourceFilePath, fullFilePath)
                log.info("复制接口脚本成功{}".format(fullFilePath))

    testReportAddress = '/root/platform/static/'
    buildSourceFilePath = '/root/ant/apache-ant-1.9.16/build/build.xml'

    # 执行脚本前清除报告数据
    performanceReportPath = testReportAddress + projectName[0]["modelData"] + '/' + modelData + '/PerformanceReport/*'
    apiReportPatb = testReportAddress + projectName[0]["modelData"] + '/' + modelData + '/ApiReport/*'
    UIHtml=testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/html/*"

    #执行脚本前清理日志文件-jmeter执行日志文件-ant执行日志文件
    #Jmeter执行文件地址
    jmeterAPiLogPath=log_path+projectName[0]["modelData"]+"/"+modelData+"/ApiLog/"+"log.text"
    jmeterPerforLogPath=log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text"

    #执行UI脚本前清理日志- results数据-测试报告文件- log日志
    UIResult=testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/results/*"
    UILog=testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/logs/*"
    
    #Ant执行日志文件
    antApiLogPath=log_path+projectName[0]["modelData"]+"/"+modelData+"/ApiLog/"+"log.text"
    antPerForLogPath=log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text"

    if executeType=='0' or executeType==False :
        os.system("rm -rf " + jmeterAPiLogPath)
        os.system("rm -rf " + antApiLogPath)
        log.info("接口测试执行数据清理完成")

    if executeType == '1' or executeType == True:
        os.system("rm -rf " + jmeterPerforLogPath)
        os.system("rm -rf " + antPerForLogPath)
        log.info("性能测试执行数据清理完成")

    if executeType == '2':
        os.system("rm -rf " + UIResult)
        os.system("rm -rf " + UIHtml)
        os.system("rm -rf " + UILog)
        os.system("rm -rf "+log_path+projectName[0]["modelData"]+"/"+modelData+"/UILog/*")
        log.info("UI测试执行数据清理完成")


    os.system("rm -rf " + '/root/ant/apache-ant-1.9.16/build/' +projectName[0]["modelData"] + "/" + modelData+"/build.xml")
    log.info("=====删除日志和报告文件=====")
    # 复制build文件

    destFilePath = '/root/ant/apache-ant-1.9.16/build/' +projectName[0]["modelData"] + "/" + modelData+"/build.xml"
    shutil.copyfile(buildSourceFilePath, destFilePath)
    log.info("=======复制build文件{}======".format(destFilePath))

    # 修改build文件内容
    buildJtlData = "sed -i 's|<property name=\"jmeter.result.jtl.dir\" value=\"/root/ant/report/jtl\" />|<property name=\"jmeter.result.jtl.dir\" value="+"\"" + testReportAddress + \
    projectName[0]["modelData"] + '/' + modelData + "/ApiReport/jtl\" />|' " + destFilePath

    buildHtmlData = "sed -i 's|<property name=\"jmeter.result.html.dir\" value=\"/root/ant/report/html\" />|<property name=\"jmeter.result.html.dir\" value=" + "\"" + testReportAddress + \
                projectName[0]["modelData"] + '/' + modelData + "/ApiReport/html\" />|' " + destFilePath

    buildScriptData = "xmlstarlet ed --inplace -u '//testplans/@dir' -v '/root/jmeter/apache-jmeter-5.4.1/script/"+projectName[0]["modelData"] + '/' + modelData +"' " + destFilePath

    os.system(buildJtlData)
    os.system(buildHtmlData)
    os.system(buildScriptData)

    log.info("=====修改build文件内容=========")

    #执行前更新项目状态
    sql = 'update quality_scriptproject set runstatus=1 where sceiptProject_id='+str(sceiptProject_id)
    commonList().getModelData(sql)

    if executeType=='0' or executeType==False :
        os.system("rm -rf " + apiReportPatb)
        shellData='ant -file '+buildAddress+" run  >>"+log_path+projectName[0]["modelData"]+"/"+modelData+"/ApiLog/"+"log.text"
        log.info('shellData:{}'.format(shellData))
        

    if executeType=='1' or executeType==True:
        os.system("rm -rf " + performanceReportPath)
        shellData=performanceData+" >> "+log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text"
        log.info('shellData:{}'.format(shellData))


    if executeType=='2':
        os.system("rm -rf " + UIHtml)
        shellData=UIdata+" >> "+log_path+projectName[0]["modelData"]+"/"+modelData+"/UILog/"+"log.text"
        log.info('shellData:{}'.format(shellData))
    

    os.system(shellData)
    log.info("脚本已执行完成")

    #判断是否是UI自动化，根据已执行的数据生成测试报告
    if executeType=='2':
        shellData=UIExcReport+" >> "+log_path+projectName[0]["modelData"]+"/"+modelData+"/UILog/"+"log.text"
        log.info('shellData:{}'.format(shellData))
        os.system(shellData)
        log.info("=====UI测试报告已生成==========")

    #获取企信消息通知-开启状态-企信地址
    dingMessageSql = 'select ding_address,ding_version,ding_message,ding_people  from quality_dingmessage'
    dingMessageLIst = (commonList().getModelData(dingMessageSql))
    username = request.session.get('username', False)
    selectUserNameSql="select first_name from auth_user where username=\'{}\'".format(username)
    returnUserNamedata=commonList().getModelData(selectUserNameSql)
    if returnUserNamedata:
        username=returnUserNamedata[0]['first_name']
    else:
        username="猜猜我是谁，一个来自外太空M78星云的陌生人"
    if len(dingMessageLIst)==0:
        log.info("====企信通知地址配置为空======")
    else:
        for dingmessage in dingMessageLIst:
            log.info("dingMessageLIst==={}".format(dingMessageLIst))
            modelDataList=json.loads(dingmessage['ding_version'])
            openDingMessAge=dingmessage["ding_message"]
            dingAddress=dingmessage['ding_address']
            dingPeople=dingmessage['ding_people']
            if len(modelDataList)==0:
                log.info("====版本配置为空=====")
            else:
                if int(modelDataId) in  modelDataList:
                    reportAddress = requestData['reportAddress']
                    performanceReport = requestData['performanceReport']

                    # 根据测试报告是否生成,巡检状态,开启群通知
                    if executeType==0 and os.path.exists('/root/platform'+reportAddress) and openDingMessAge=="True" :
                        testReportAddress = '/root/platform/static/'
                        performanceJtlAddress = testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/jtl/TestReport.jtl"

                        with open(performanceJtlAddress, 'r') as file:
                            content = file.read()
                        # 统计总数
                        total_count = content.count('<failure>true</failure>') + content.count(
                            '<failure>false</failure>')
                        # 统计 <failure>true</failure> 的数量
                        success_cont=content.count(
                            '<failure>false</failure>')
                        true_count = content.count('<failure>true</failure>')

                        if true_count>0:
                            result="构建失败"
                        else:
                            result="构建成功"

                        # 计算占比
                        true_percentage =(success_cont / total_count) * 100 if total_count > 0 else 0
                        true_percentage = round(true_percentage, 2)
                        dingScriptMessage(dingAddress, projectName[0]["modelData"], modelData,username, total_count, true_count, true_percentage, result,reportAddress)

                    elif executeType==1 and os.path.exists('/root/platform'+performanceReport) and bool(openDingMessAge) :
                        curlData = '''curl '{}' \
                        -H 'Content-Type: application/json' \
                        --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "本消息由系统自动发出，无需回复！ \n>各位同事，大家好，以下为【{}】-【{}】项目构建信息\n>执行人: {}\n>构建结果 ：Success \n>查看：[性能测试报告](http://192.168.8.22:8050{})","mentioned_mobile_list":["{}"]}}'
                        --compressed
                        '''.format(dingAddress, projectName[0]["modelData"], modelData, username, performanceReport,
                                    dingPeople)
                        os.system(curlData)

                    elif executeType==2 and os.path.exists('/root/platform'+UIReport) and bool(openDingMessAge):
                        
                        dingUIMessage(dingAddress, projectName[0]["modelData"], modelData,username,UIReport)

                    else:
                        log.info("=====不满足企信推送条件=====")
                else:
                    log.info("=====没有配置该项目企信通知=======")
    data = {
        "code": 200,
        "msg": "脚本开始执行，请查看日志及测试报告"
    }
    # except Exception as e:
    #     curlData = '''curl '{}' \
    #                 -H 'Content-Type: application/json' \
    #                 --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{}","mentioned_mobile_list":[]}}'
    #                 --compressed
    #                 '''.format('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d543363b-8fa5-4e66-9274-8dc0cf99afd6',e)
    #     os.system(curlData)
    #     data = {
    #         "code": 200,
    #         "msg": "脚本执行报错：{}".format(e)
    #     }
    return JsonResponse(data, safe=False)

def countElement(sourceList,targetList):
    '''统计占用比例'''
    number=0
    for source in sourceList:
        if source in targetList:
            number+=1
    precent=round(number/len(targetList)*100,2)
    return precent
def dingUIMessage(dingAddress,projectName,modelData,username,reportAddress):
    '''叮叮消息通知'''
    import requests
    import json

    content='''
            \n\n><font color=#303133>本消息由系统自动发出，无需回复！</font> 
            \n\n>各位同事，大家好，以下为【<font color=#E6A23C>{}</font>】-【<font color=#E6A23C>{}</font>】项目构建信息
            \n\n>执行人 : <font color=#E6A23C>{}</font>
            \n\n>构建结果 : <font color=#E6A23C>执行成功</font>
            \n\n>[查看UI测试报告](http://192.168.8.22:8050{})
            '''.format(projectName,modelData,username,reportAddress)
    url = dingAddress

    payload = json.dumps({
    "msgtype": "markdown",
    "markdown": {
        "title": "接口自动化",
        "text": content,
        "at": {
        "isAtAll": True
        }
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=payload)
def dingScriptMessage(dingAddress,projectName,modelData,username, total_count, true_count, true_percentage, result,reportAddress):
    '''叮叮消息通知'''
    import requests
    import json

    content='''
            \n\n><font color=#303133>本消息由系统自动发出，无需回复！</font> 
            \n\n>各位同事，大家好，以下为【<font color=#E6A23C>{}</font>】-【<font color=#E6A23C>{}</font>】项目构建信息
            \n\n>执行人 : <font color=#E6A23C>{}</font>
            \n\n>执行接口 : <font color=#409EFF>{}</font>个 
            \n\n>失败接口 : <font color=#F56C6C>{}</font>个
            \n\n>执行成功率 : <font color=#67C23A>{}</font>%
            \n\n>构建结果 : <font color=#E6A23C>{}</font>
            \n\n>[查看接口测试报告](http://192.168.8.22:8050{})
            '''.format(projectName,modelData,username, total_count, true_count, true_percentage, result,reportAddress)
    url = dingAddress

    payload = json.dumps({
    "msgtype": "markdown",
    "markdown": {
        "title": "接口自动化",
        "text": content,
        "at": {
        "isAtAll": True
        }
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

def sendQiXinMessgae(dingAddress,projectName,versionName,username,total_count,true_count,true_percentage,result,reportAddress):
    '''执行企信通知'''
    try:
        import requests
        headers={
            'Content-Type: application/json'
        }

        payload=json.dumps({
              "msgtype": "markdown",
              "markdown": {
                "content": "本消息由系统自动发出，无需回复！ \n>各位同事，大家好，以下为【"+projectName+"】-【"+versionName+"】项目构建信息\n>负责人 : "+username+"\n>执行接口 : "+total_count+"个 \n>失败接口 : "+
               true_count+"个\n>执行成功率 : "+true_percentage+"%\n>构建结果 ："+result+" \n>[测试结果=>查看接口测试报告](http://192.168.8.22:8050"+reportAddress+")","mentioned_mobile_list":[]+"\""
              }
            })
        requests.request("POST", dingAddress,headers=headers, data=payload)

        print(response.text)
    except Exception as e:
        log.info("企信通知报错:{}".format(e))


@msgMessage
def readHtmlReport(request):
    '''读取html报告'''
    try:
        reportAddress=request.POST.get("reportAddress")
        # print("reportAddress",reportAddress)
        #测试环境
        path="D:\\Jmeter\\apache-jmeter-5.4.1\\TestReport.html"

        #线上环境
        # path="/mnt/install/ant/apache-ant-1.9.16/logs/log.text"
        logger=open(path,"r",encoding='UTF-8',errors='ignore')
        loglist=logger.readlines()
        logger.close()
        data={
            "code":200,
            "msg":loglist
        }
    except Exception as e:
        log.error("获取html报告出错",e)
        data={
            "code":677,
            "msg":'获取日志出错'
        }
    return JsonResponse(data,safe=False)

@msgMessage
def readScriptLog(request):
    '''读取ant执行日志'''
    requestData = json.loads(request.body)
    # print(requestData)
    # 获取项目地址
    projectName_id = requestData['projectName']
    executeType=requestData["executeType"]
    sql = 'select modelData from quality_modeldata where modeldata_id= ' + str(projectName_id)
    projectName = commonList().getModelData(sql)

    # 获取版本地址
    modelData = requestData['modelData']

    #创建目录
    log_path="/root/platform/logs"
    if not os.path.exists(log_path+projectName[0]["modelData"]+"/"+modelData):
        os.makedirs(log_path+projectName[0]["modelData"]+"/"+modelData)
        os.makedirs(log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/")
        os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/")

    # #测试环境
    # path="D:\\testPlatForm\\TestPlat\\platForm\\logs\\webtestcase.txt"

    #线上环境

    if executeType=='0' or executeType==False :
        path = "/root/platform/logs/" + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/" + "log.text"
        log.info("====apilog====")
    if executeType=='1' or executeType==True :
        path = "/root/platform/logs/" + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/" + "log.text"
        log.info("=====performanceLog====")
    if executeType=='2':
        path = "/root/platform/logs/" + projectName[0]["modelData"] + "/" + modelData + "/UILog/" + "log.text"
        log.info("=====UILog====")
    logger=open(path,"r",encoding='UTF-8',errors='ignore')
    loglist=logger.readlines()
    logger.close()

    data={
        "code":200,
        "msg":loglist
    }

    return JsonResponse(data,safe=False)
#读取日志记录
def readlog(request):
    try:
        logger=open("/root/platform/logs","r",encoding='UTF-8',errors='ignore')
        loglist=logger.readlines()
        loglist = loglist[::-1]
        logger.close()
        data={
            "code":200,
            "msg":loglist
        }
    except Exception as e :
        log.error("获取日志信息出错")
        data={
            "code":677,
            "msg":'获取日志出错'
        }
    return JsonResponse(data,safe=False)

@msgMessage
def addModelVersion(request):
    # print('version',request.POST)
    Modelversion_id=request.POST.get('Modelversion_id')
    modeldata_id_id=request.POST.get("modeldata_id_id")
    modeldata_name=request.POST.get("modeldata_name")

    exitModelversion=Modelversion.objects.filter(modeldata_name=modeldata_name)
    if exitModelversion:
        data = {
            "code": 201,
            "msg": "版本已存在请重新添加"
        }
    else:
        _modelversion=Modelversion()
        if Modelversion_id:
            _modelversion.Modelversion_id=Modelversion_id
            _modelversion.modeldata_name=modeldata_name
            _modelversion.modeldata_id_id=modeldata_id_id
            _modelversion.save()
            data={
                "code":200,
                "msg":"修改版本信息成功"
            }
        else:
            _modelversion.modeldata_name=modeldata_name
            _modelversion.modeldata_id_id=modeldata_id_id
            _modelversion.save()
            data={
                "code":200,
                "msg":"保存版本信息成功"
            }
    return JsonResponse(data,safe=False)


#查询版本信息
@msgMessage
def selectModelVersion(request):

    sql='select modeldata_id as value,modelData as label from quality_modeldata where subModelData!=0'
    data=commonList().getModelData(sql)
    return JsonResponse(data,safe=False)
#查询模块信息
@msgMessage
def selectAllModelTree(request):
    sql='select * from quality_modeldata where subModelData=0'
    data1=commonList().getModelData(sql)
    sql2='select * from quality_modeldata where subModelData!=0'
    data2=commonList().getModelData(sql2)
    sql3='select * from quality_modelversion'
    versionlist=commonList().getModelData(sql3)
    data=[]
    if data1:
        id=0
        for modelList in data1:
            id=id+1
            datalist={"id":0,"label":'',"children":[]}
            datalist["label"]=modelList['modelData']
            datalist["id"]=id
            if data2:
                for childrenlist in data2:
                    id=id+1
                    # print("childrenlist",childrenlist)
                    data3={"id":id,"label":'',"children":[]}
                    if modelList["modeldata_id"]==childrenlist["subModelData"]:
                        data3["label"]=childrenlist['modelData']
                        data3["id"]=id
                        for childrenlist3 in (versionlist):
                            id=id+1
                            tablelist={}
                            if childrenlist3["modeldata_id_id"]==childrenlist["modeldata_id"]:
                                tablelist["label"]=(childrenlist3["modeldata_name"])
                                tablelist["id"]=id
                                data3["children"].append(tablelist)
                            else:
                                pass
                        datalist["children"].append(data3)
                    else:
                        pass
            else:
                print("子模块为空")
            data.append(datalist)
            # print("获取到的tree信息是",data)
    else:
        print("主模块为空")
    return JsonResponse(data,safe=False)


#删除模块信息
@msgMessage
def deleteModelDataList(request):
    # print("删除modelData",request.POST)
    modeldata_id=request.POST.get('modeldata_id')
    Modeldatalist=Modeldata.objects.get(modeldata_id=modeldata_id)
    Modeldatalist.delete()
    data={
        "code":200,
        "msg":"删除成功"
    }
    return JsonResponse(data,safe=False)



#查询所有的模块信息
@msgMessage
def selectAllModel(request):
    sql="SELECT b.modelData,b.modeldata_id,b.subModelData,b.modelData_proenvironment,b.modelData_testenvironment,b.modelData_pripeople,a.modelData AS"+"\'"+'name'+"\'"+"FROM quality_modeldata b LEFT JOIN quality_modeldata a on a.modeldata_id=b.subModelData order by modeldata_id  desc"
    data = commonList().getModelData(sql)   
    return JsonResponse(data,safe=False)
#查询模块信息
@msgMessage
def selectModelList(request):
    sql="select modeldata_id 'value' , modelData 'label' from quality_modeldata where subModelData=0"
    data = commonList().getModelData(sql)
    return JsonResponse(data,safe=False)

#保存模块信息
@msgMessage
def saveModelData(request):
    modeldata_id=request.POST.get('modeldata_id')
    modelData=request.POST.get('modelData')
    subModelData=request.POST.get('subModelData')
    modelData_pripeople=request.POST.get('modelData_pripeople')
    modelData_testenvironment=request.POST.get('modelData_testenvironment')
    modelData_proenvironment=request.POST.get('modelData_proenvironment')
    if modeldata_id:
        _model=Modeldata()
        _model.modeldata_id=modeldata_id
        _model.modelData=modelData
        _model.subModelData=subModelData
        _model.modelData_pripeople=modelData_pripeople
        _model.modelData_testenvironment=modelData_testenvironment
        _model.modelData_proenvironment=modelData_proenvironment
        _model.save()

        data={
            "code":200,
            "msg":"修改模块信息成功"
        }
    else:
        _model=Modeldata()
        _model.modelData=modelData
        _model.subModelData=subModelData
        _model.modelData_pripeople=modelData_pripeople
        _model.modelData_testenvironment=modelData_testenvironment
        _model.modelData_proenvironment=modelData_proenvironment
        _model.save()

        data={
            "code":200,
            "msg":"保存模块信息成功"
        }
    return JsonResponse(data,safe=False)

#web请求
# def webRequest(request):
#     functionList=FunctionList.__dict__
#     requestList = request.POST.items()
#     for i in requestList:
#         data2 = json.loads(i[0])
#         for webtestCase in data2['list']:
#             webtestcase_id=webtestCase['webtestcase_id']
#             sql="select * from quality_script a,quality_webtestcase b where a.webtestcase_id_id=b.webtestcase_id and b.webtestcase_id="+str(webtestcase_id)
#             data = commonList().getModelData(sql)
#             for datalist in data:
#                 # print("获取的datalist为：",datalist)
#                 if datalist['script_data']==None:
#                     data=['']
#                 else:
#                     data=datalist['script_data'].split(',')
#                 if datalist['script_element']==None:
#                     element=['']
#                 else:
#                     element=datalist['script_element'].split(',')
#                 print('data',data)
#                 print('element',element)
#                 if datalist['script_timeout']==None or datalist['script_timeout']=='' :
#                     timeout=0
#                 else:
#                     timeout=int(datalist['script_timeout'])
#                 functiontest=functionList[datalist['script_keyword']]
                
#                 if len(data)>1:
#                     print("第一步")                    
#                     functiontest(data[0],data[1])
#                 elif len(data)==1 and len(data[0])!=0:
#                     print("第二步")
#                     functiontest(element[0],data[0])
#                 elif len(data[0])==0 and len(element[0])==0:
#                     print("第三步")
#                     functiontest()
#                 elif len(data)==1 and len(element)>1:
#                     print("第四步")
#                     functiontest(element[0],element[1])
#                 else:
#                     print("第五步")
#                     functiontest(element[0],timeout)
#                 elementAssert=datalist['script_assert']
#                 print('elementAssert',elementAssert)
#                 if elementAssert!='' and elementAssert!=None:
#                     FunctionList.assertElement(elementAssert)
#                     print(type(FunctionList.assertElement(elementAssert)))
#                     if FunctionList.assertElement(elementAssert):
#                         webtestcase_id=datalist['webtestcase_id']
#                         modeldata_id_id=datalist['modeldata_id_id']
#                         webtestcase_name=datalist['webtestcase_name']
#                         webtestcase_request=datalist['webtestcase_request']
#                         webtestcase_steps=datalist['webtestcase_steps']
#                         webtestcase_exresponse=datalist['webtestcase_exresponse']
#                         webtestcase_acesponse=datalist['webtestcase_acesponse']
#                         webtestcase_assert=datalist['webtestcase_assert']
#                         webtestcase_result=1

#                         _webtestcase=Webtestcase()
#                         _webtestcase.webtestcase_id=webtestcase_id
#                         _webtestcase.modeldata_id_id=Modeldata.objects.get(modeldata_id=modeldata_id_id)
#                         _webtestcase.webtestcase_name=webtestcase_name
#                         _webtestcase.webtestcase_request=webtestcase_request
#                         _webtestcase.webtestcase_steps=webtestcase_steps
#                         _webtestcase.webtestcase_exresponse=webtestcase_exresponse
#                         _webtestcase.webtestcase_acesponse=webtestcase_acesponse
#                         _webtestcase.webtestcase_assert=webtestcase_assert
#                         _webtestcase.webtestcase_result=webtestcase_result
#                         _webtestcase.save()
#                         data={
#                                 "code":200,
#                                 "msg":"用例执行成功"
#                             }
#                     else:
#                         webtestcase_id=datalist['webtestcase_id']
#                         modeldata_id_id=datalist['modeldata_id_id']
#                         webtestcase_name=datalist['webtestcase_name']
#                         webtestcase_request=datalist['webtestcase_request']
#                         webtestcase_steps=datalist['webtestcase_steps']
#                         webtestcase_exresponse=datalist['webtestcase_exresponse']
#                         webtestcase_acesponse=datalist['webtestcase_acesponse']
#                         webtestcase_assert=datalist['webtestcase_assert']
#                         webtestcase_result=2

#                         _webtestcase=Webtestcase()
#                         _webtestcase.webtestcase_id=webtestcase_id
#                         _webtestcase.modeldata_id_id=Modeldata.objects.get(modeldata_id=modeldata_id_id)
#                         _webtestcase.webtestcase_name=webtestcase_name
#                         _webtestcase.webtestcase_request=webtestcase_request
#                         _webtestcase.webtestcase_steps=webtestcase_steps
#                         _webtestcase.webtestcase_exresponse=webtestcase_exresponse
#                         _webtestcase.webtestcase_acesponse=webtestcase_acesponse
#                         _webtestcase.webtestcase_assert=webtestcase_assert
#                         _webtestcase.webtestcase_result=webtestcase_result
#                         _webtestcase.save()
#                         data={
#                                 "code":200,
#                                 "msg":"用例执行失败"
#                             }
#                 else:
#                     data={
#                                 "code":200,
#                                 "msg":"该用例没有设置检查点"
#                             }


# if datalist['script_keyword'] in functionList.keys():
#     print('script_data',datalist['script_data'])
#     functiontest=functionList[datalist['script_keyword']]
#     print(type(functiontest))
#     print('方法中有几个变量',functiontest.__code__.co_varnames)
#     print(type(functiontest.__code__.co_varnames))
    
    return JsonResponse(data,safe=False)
#版本列表查询
def getVersionListNew(request):

    
    data = {
        "versionListAll": [],
        'total': 0,
    }
    version_name=request.POST.get('version_name')
    projectList=projectss.findProjectRedisList('projectRedisList')
    if projectList.count()==0:
        return JsonResponse(data)
    else:
        resList = []
        for i in projectList:
            resList += [{
                'value': i.project_id,
                'label': i.project_name,
            }]
        data['projectList'] = resList
        projectId = request.POST.get('project_id_id')
        project1 = Project.objects.filter(parent_project_id=0).first()
        if project1:
            if projectId == '':
                projectId = project1.project_id
            if projectId is None:
                projectId = project1.project_id
        if projectId:
            data['project_id'] = projectId          
            page = request.POST.get('pageNo')
            pageSize = int(request.POST.get('pageSize'))
            #查询项目ID
            sqlProjectId="select project_id from quality_project where parent_project_id=0"
            sqlProjectId1=commonList().getModelData(sqlProjectId)
            sqlProjectIdList=commonList().selectList(sqlProjectId1)
            #查询版本ID
            sqlVersionId="select project_id from quality_project where parent_project_id="+str(projectId)
            sqlVersionId1=commonList().getModelData(sqlVersionId)
            sqlVersionIdList=commonList().selectList(sqlVersionId1)

            #查询版本ID
            if int(projectId) in sqlProjectIdList and version_name=='':
                if sqlVersionIdList=="()":
                    list1=[]
                else:
                    sqlversion1="SELECT * FROM (quality_version a LEFT JOIN quality_project b on a.project_id_id=b.project_id ) LEFT JOIN quality_version_time c on a.version_id=c.version_id_id WHERE a.version_archived!= 'True' and b.project_id in"+str(sqlVersionIdList)+" "+"ORDER BY c.release_time DESC"
                    sqlversion2="SELECT * FROM quality_version a,quality_project b WHERE a.project_id_id=b.project_id AND version_archived='True' and b.project_id in"+str(sqlVersionIdList)
                    data1=commonList().getModelData(sqlversion1)
                    data2=commonList().getModelData(sqlversion2)
                    data2[0:0]=data1
                    list1=data2
            elif int(projectId) in sqlProjectIdList and version_name!='':
                sqlversion="select * from quality_version a,quality_project b where a.project_id_id=b.project_id and b.project_id in"+str(sqlVersionIdList)+"and a.version_name like"+"\'"+str(version_name)+"\'"
                list1=commonList().getModelData(sqlversion)
            elif int(projectId) not in sqlProjectIdList and version_name!='':
                sqlversion="SELECT * FROM quality_version a,quality_project b WHERE a.project_id_id=b.project_id AND b.project_id="+str(projectId)+" "+"and a.version_name like "+"\'"+str(version_name)+"\'"
                list1=commonList().getModelData(sqlversion)
            else:
                sqlversion1="SELECT * FROM (quality_version a LEFT JOIN quality_project b on a.project_id_id=b.project_id ) LEFT JOIN quality_version_time c on a.version_id=c.version_id_id WHERE a.version_archived!= 'True' and b.project_id ="+str(projectId)+" "+"ORDER BY c.release_time DESC"
                sqlversion2="SELECT * FROM quality_version a,quality_project b WHERE a.project_id_id=b.project_id AND version_archived='True' and b.project_id ="+str(projectId)
                data1=commonList().getModelData(sqlversion1)
                data2=commonList().getModelData(sqlversion2)
                data2[0:0]=data1
                list1=data2
            versionList=list1
            if versionList:
                paginator = Paginator(versionList, pageSize)
                data['total'] = paginator.count
                try:
                    versions = paginator.page(page)
                except PageNotAnInteger:
                    versions = paginator.page(1)
                except EmptyPage:
                    versions = paginator.page(paginator.num_pages)
                list3=[]
                for version in versions:
                    list3.append(version)
                data["versionListAll"]=list3
                return JsonResponse(data)
            else:
                return JsonResponse(data)
#接口请求
def apiTest(request):
    global response
    aa=request.POST.items()
    for i in aa:
        data2=json.loads(i[0])
        num=0
        for list_analysis in data2["list"]:
            test_id=list_analysis['test_id']
            if num==0:
                url="http://"+str(list_analysis['api_host'])+str(list_analysis['test_url'])
                data=(list_analysis['test_request'])
                host=list_analysis['test_host']
                method=list_analysis['test_method']
                assertData=list_analysis['test_assert']
                response=APITest().login(url,data,host)
                _test=Testcase.objects.get(test_id=test_id)
                _test.test_acesponse=response.get_dict()
                if response:
                    _test.test_results=1
                else:
                    _test.test_results=2
                _test.save()
            else:
                url="http://"+str(list_analysis['api_host'])+str(list_analysis['test_url'])
                data=list_analysis['test_request']
                host=list_analysis['test_host']
                method=list_analysis['test_method']
                assertData=list_analysis['test_assert']
                responseData=APITest().apiRequest(url,data,host,method,response)
                # _test=Testcase.objects.get(test_id=test_id)
                # if re.search(assertData,str(responseData)):
                #     _test.test_results=1
                # else:
                #     _test.test_results=2
                # _test.test_acesponse=responseData
                # _test.save()
            num=num+1
        data={
            "code":200,
            "msg":"接口用例执行成功"
        }
        return JsonResponse(data,safe=False)

#查询用例信息
def selectTestCase(request):
    sql="select  * from quality_api a,quality_testcase b where a.api_id=b.api_id_id"
    data=commonList().getModelData(sql)
    return JsonResponse(data,safe=False)


#删除用例信息
def deleteTestData(request):
    test_id=request.POST.get("test_id")
    TestData=Testcase.objects.get(test_id=test_id)
    TestData.delete()
    data={
        "code":200,
        "msg":"删除接口用例成功"
    }
    return JsonResponse(data)
#删除脚本
def deleteScript(request):
    # print(request.POST)
    script_id=request.POST.get("script_id")
    print('script_id',script_id)
    scriptData=Script.objects.get(script_id=script_id)
    scriptData.delete()
    data={
        "code":200,
        "msg":"删除脚本成功"
    }
    return JsonResponse(data,safe=False)
#保存脚本
def saveScriptData(request):
    script_id=request.POST.get("script_id")
    webtestcase_id=request.POST.get("webtestcase_id")
    script_name=request.POST.get("script_name")
    script_method=request.POST.get("script_method")
    script_element=request.POST.get("script_element")
    script_action=request.POST.get("script_action")
    script_data=request.POST.get("script_data")
    script_timeout=request.POST.get("script_timeout")

    # print((script_timeout))
    script_assert=request.POST.get("script_assert")
    script_keyword=request.POST.get("script_keyword")

    if script_id:
        _script=Script()
        _script.script_id=script_id
        _script.webtestcase_id=Webtestcase.objects.get(webtestcase_id=webtestcase_id)
        _script.script_name=script_name
        _script.script_method=script_method
        _script.script_element=script_element
        _script.script_timeout=script_timeout
        _script.script_action=script_action
        _script.script_data=script_data
        _script.script_assert=script_assert
        _script.script_keyword=script_keyword
        _script.save()
        data={
            "code":200,
            "msg":"Script修改成功"
        }
    else:
        _script=Script()
        _script.webtestcase_id=Webtestcase.objects.get(webtestcase_id=webtestcase_id)
        _script.script_name=script_name
        _script.script_method=script_method
        _script.script_element=script_element
        _script.script_timeout=script_timeout
        _script.script_action=script_action
        _script.script_data=script_data
        _script.script_assert=script_assert
        _script.script_keyword=script_keyword
        _script.save()
        data={
            "code":200,
            "msg":"Script保存成功"
        }
    return JsonResponse(data,safe=False)
#删除web用例信息
def deleteWebTestData(request):
    webtestcase_id=request.POST.get("webtestcase_id")
    WebtestcaseData=Webtestcase.objects.get(webtestcase_id=webtestcase_id)
    WebtestcaseData.delete()
    data={
        "code":200,
        "msg":"删除web用例信息成功"
    }
    return JsonResponse(data)

#保存web用例信息
# def saveWebTestCase(request):
#     webtestcase_id=request.POST.get('webtestcase_id')
#     modeldata_id_id=request.POST.get('modeldata_id_id')
#     webtestcase_name=request.POST.get('webtestcase_name')
#     webtestcase_request=request.POST.get('webtestcase_request')
#     webtestcase_steps=request.POST.get('webtestcase_steps')
#     webtestcase_exresponse=request.POST.get('webtestcase_exresponse')
#     webtestcase_acesponse=request.POST.get('webtestcase_acesponse')
#     webtestcase_assert=request.POST.get('webtestcase_assert')
#     webtestcase_result=request.POST.get('webtestcase_result')

#     if webtestcase_id:
#         _webtestcase=Webtestcase()
#         _webtestcase.webtestcase_id=webtestcase_id
#         _webtestcase.modeldata_id_id=Modeldata.objects.get(modeldata_id=modeldata_id_id)
#         _webtestcase.webtestcase_name=webtestcase_name
#         _webtestcase.webtestcase_request=webtestcase_request
#         _webtestcase.webtestcase_steps=webtestcase_steps
#         _webtestcase.webtestcase_exresponse=webtestcase_exresponse
#         _webtestcase.webtestcase_acesponse=webtestcase_acesponse
#         _webtestcase.webtestcase_assert=webtestcase_assert
#         _webtestcase.webtestcase_result=webtestcase_result
#         _webtestcase.save()
#         data={
#             "code":200,
#             "msg":'测试用例修改成功'
#         }

#     else:
#         _webtestcase=Webtestcase()
#         _webtestcase.modeldata_id=Modeldata.objects.get(modeldata_id=modeldata_id_id)
#         _webtestcase.webtestcase_name=webtestcase_name
#         _webtestcase.webtestcase_request=webtestcase_request
#         _webtestcase.webtestcase_steps=webtestcase_steps
#         _webtestcase.webtestcase_exresponse=webtestcase_exresponse
#         _webtestcase.webtestcase_acesponse=webtestcase_acesponse
#         _webtestcase.webtestcase_assert=webtestcase_assert
#         _webtestcase.webtestcase_result=webtestcase_result
#         _webtestcase.save()
#         data={
#             "code":200,
#             "msg":'测试用例保存成功'
#         }
#     return JsonResponse(data)


#保存用例信息
def saveTestCase(request):
    test_id=request.POST.get('test_id')
    test_host=request.POST.get('test_host')
    test_name=request.POST.get('test_name')
    test_method=request.POST.get('test_method')
    test_url=request.POST.get('test_url')
    test_request=request.POST.get('test_request')
    test_exresponse=request.POST.get('test_exresponse')
    test_acesponse=request.POST.get('test_acesponse')
    test_assert=request.POST.get('test_assert')
    test_results=request.POST.get('test_results')

    if test_id:
        _test=Testcase()
        _test.test_id=test_id
        _test.test_host=test_host
        _test.test_name=test_name
        _test.api_id=Api.objects.get(api_id=test_name)
        _test.test_method=test_method
        _test.test_assert=test_assert
        _test.test_url=test_url
        _test.test_request=test_request
        _test.test_exresponse=test_exresponse
        _test.test_acesponse=test_acesponse
        _test.test_results=test_results
        _test.save()
        data={
            "code":200,
            "msg":'测试用例修改成功'
        }
    else:
        _test=Testcase()
        # _test.test_id=test_id
        _test.test_host=test_host
        _test.test_name=test_name
        _test.api_id=Api.objects.get(api_id=test_name)
        _test.test_method=test_method
        _test.test_url=test_url
        _test.test_assert=test_assert
        _test.test_request=test_request
        _test.test_exresponse=test_exresponse
        _test.test_acesponse=test_acesponse
        _test.test_results=test_results
        _test.save()
        data={
            "code":200,
            "msg":'接口测试用例保存成功'
        }
    return JsonResponse(data)
#查询版本信息
def selectVersionData(request):
    sql="select modeldata_id 'id',modelData 'label' from quality_modeldata where subModelData!=0"
    data=commonList().getModelData(sql)
    return JsonResponse(data,safe=False)
#删除接口管理信息
def deleteApiData(request):
    api_id=request.POST.get("api_id")
    if api_id:
        ApiData=Api.objects.get(api_id=api_id)
        ApiData.delete()
        data={
            "code":200,
            "msg":"删除接口成功"
        }
    else:
        data={
            "code":1314,
            "msg":"没保存还想删除"
        }
    return JsonResponse(data)

#查询接口管理信息
def selectAPIdata(request):
    id=request.POST.get('id')
    if id:
        sql="select api_id 'id',api_name 'value' from quality_api"
        data=commonList().getModelData(sql)
        for i in data:
            i["id"]=str(i['id'])
    else:
        sql="select * from quality_api a,quality_version b where a.version_id_id=b.version_id"
        data=commonList().getModelData(sql)
    
    return JsonResponse(data,safe=False)
#保存接口管理信息
def saveAPIdata(request):
    api_id=request.POST.get("api_id")
    version_id_id=request.POST.get("version_id_id")
    api_name=request.POST.get("api_name")
    api_host=request.POST.get("api_host")
    api_method=request.POST.get("api_method")
    api_url=request.POST.get("api_url")
    api_request=request.POST.get("api_request")
    api_response=request.POST.get("api_response")
    if api_id:
        _Api=Api()
        _Api.version_id=Version.objects.get(version_id=version_id_id)
        _Api.api_id=api_id
        _Api.api_name=api_name
        _Api.api_host=api_host
        _Api.api_method=api_method
        _Api.api_url=api_url
        _Api.api_request=api_request
        _Api.api_response=api_response
        _Api.save()
        data={
            "code":200,
            "msg":"接口管理信息修改成功"
        }
    else:
        _Api=Api()
        _Api.version_id=Version.objects.get(version_id=version_id_id)
        _Api.api_name=api_name
        _Api.api_host=api_host
        _Api.api_method=api_method
        _Api.api_url=api_url
        _Api.api_request=api_request
        _Api.api_response=api_response
        _Api.save()
        data={
            "code":200,
            "msg":"接口管理信息保存成功"
        }
    return JsonResponse(data)



