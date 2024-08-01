# -*- coding: utf-8 -*-
from quality.common.commonbase import commonList
from quality.view.API_version.API_function import requestObject,createDataFinally
from quality.view.API_version.API_dataList import DataList
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.http.response import JsonResponse,FileResponse
from quality.view.documentMan.doc_model import documentMan
import  json,os,os,zipfile,ast,xmindparser
from quality.common.msg import msgMessage
from quality.common.logger import Log
import pandas as pd
from datetime import datetime
from django.db import transaction
from quality.view.testCasesMan.cases_model import testcasemanager
from quality.view.testCasesMan.cases_model import xmind_data
from pathlib import Path
log=Log()


def downloadTemFiles(request):
    '''下载模版文件'''
    zip_file_path = '/root/zip/file.zip'

    # zip_file_path = '/Users/hll/Desktop/git/platform/media/file.zip'

    # 测试环境
    # url = '/root/platform/media/template/测试用例模板.xlsx'

    # url='/Users/hll/Desktop/git/platform/media/template/测试用例模版.xlsx'
    directory = "/root/platform/media/template/"
    # zip_file_path = "/path/to/your/zipfile.zip"  # 修改为你想要保存zip文件的路径

    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, arcname='测试用例模板.xlsx')

    response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_file_path)}"'
    return response
def delXmindCase(request):
    '''删除测试点'''
    returnData = json.loads(request.body)
    print(returnData)
    requestData = returnData['value']
    id = requestData['id']
    _xmind_data = xmind_data()
    _xmind_data = xmind_data.objects.get(id=id)
    _xmind_data.delete()

    data = {
        "code": 200,
        "data": "删除成功"
    }

    return JsonResponse(data, safe=False)

def detTestCase(request):
    '''删除用例'''
    returnData = json.loads(request.body)
    print(returnData)
    requestData = returnData['value']
    case_id = requestData['case_id']
    _testcasemanager = testcasemanager()
    _testcasemanager = testcasemanager.objects.get(case_id=case_id)
    _testcasemanager.delete()

    data = {
        "code": 200,
        "data": "删除成功"
    }

    return JsonResponse(data, safe=False)
def copyTestCase(request):
    '''复制单条用例'''
    returnData = json.loads(request.body)
    print(returnData)
    requestData = returnData['value']
    caseName = requestData['caseName']
    caseType = requestData['caseType']
    case_id = requestData['case_id']
    condition = requestData['condition']
    creater = requestData['creater']

    createrTime = requestData['createrTime']
    exceptResult = requestData['exceptResult']
    firstModel = requestData['firstModel']
    prdName = requestData['prdName']
    secondModel = requestData['secondModel']
    actualResult = requestData['actualResult']
    steps = requestData['steps']
    thirdModel = requestData['thirdModel']
    versionName = requestData['versionName']

    name = request.session.get('username', False)
    sql = "select first_name from auth_user where username='{}'".format(name)
    nameList = commonList().getModelData(sql)
    print(nameList)
    username = nameList[0]['first_name']
    if len(creater) == 0:
        creater = username
    if len(createrTime) == 0:
        createrTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _testcasemanager = testcasemanager()
    _testcasemanager.caseName = caseName
    _testcasemanager.caseType = caseType
    _testcasemanager.condition = condition
    _testcasemanager.creater = creater
    _testcasemanager.actualResult = actualResult
    _testcasemanager.createrTime = createrTime
    _testcasemanager.exceptResult = exceptResult
    _testcasemanager.firstModel = firstModel
    _testcasemanager.prdName = prdName
    _testcasemanager.executor = ''
    _testcasemanager.secondModel = secondModel
    _testcasemanager.steps = steps
    _testcasemanager.thirdModel = thirdModel
    _testcasemanager.versionName = versionName
    _testcasemanager.save()

    data = {
        "code": 200,
        "data": "复制用例成功"
    }

    return JsonResponse(data, safe=False)
def saveXmindCase(request):
    '''保存单条测试点'''
    returnData = json.loads(request.body)
    print(returnData)
    id=returnData['data']['id']
    topic=returnData['data']['topic']
    case=returnData['data']['case']
    result = returnData['data']['result']
    creater=returnData['data']['creater']
    caseType=returnData['data']['caseType']
    remark=returnData['data']['remark']
    version=returnData['data']['version']
    owner=returnData['data']['owner']
    # prdModel=returnData['data']['prdModel']

    name = request.session.get('username', False)
    sql = "select first_name from auth_user where username='{}'".format(name)
    nameList = commonList().getModelData(sql)
    print(nameList)
    xmindStart = '> 测试点执行失败通知：'
    if len(nameList)==0:
        username='去吧，皮卡丘'
    else:
        username = nameList[0]['first_name']
    if not creater:
        creater=username

    _xmind_data=xmind_data()
    if id:
        _xmind_data = xmind_data.objects.get(id=id)
        _xmind_data.topic=topic
        _xmind_data.case = case
        _xmind_data.result = result
        _xmind_data.updater = username
        _xmind_data.caseType=caseType
        _xmind_data.owner=owner
        # _xmind_data.prdModel=prdModel
        _xmind_data.updateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _xmind_data.remark=remark
        _xmind_data.save()
        data = {
            "code": 200,
            "data": "编辑测试点成功"
        }
    else:
        _xmind_data.topic=topic
        _xmind_data.case = case
        _xmind_data.result = result
        _xmind_data.creater = creater
        _xmind_data.caseType=caseType
        _xmind_data.remark=remark
        _xmind_data.owner=owner
        # _xmind_data.prdModel=prdModel
        _xmind_data.updateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _xmind_data.save()
    
        data = {
            "code": 200,
            "data": "新增测试点成功"
        }
    if result in ['失败','阻塞']:#执行失败发送企信通知
        url='https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2'
        dingXmindMessage(url,xmindStart,username,version, topic, case, caseType, result,remark)
        
    return JsonResponse(data, safe=False)

def selectPrd(request):
    '''查询版本'''
    returnData = json.loads(request.body)
    tableID=returnData['value']
    sql='''
        select version,description from quality_versionmanager where tableID=\'{}\'
    '''.format(tableID)
    print("========sql=====",sql)
    response=commonList().getModelData(sql)
    versionList=[]
    for version in response:
        if version['version']!="需求文档地址" and version['version']:
            singeleVersion={}
            singeleVersion['value']=version['version']+"-"+version['description']
            singeleVersion['label']=version['version']+"-"+version['description']
            versionList.append(singeleVersion)
    data={
        "code":200,
        "data":versionList
    }

    return JsonResponse(data, safe=False)

def delXmindDataList(request):
    '''批量删除测试点'''
    returnData = json.loads(request.body)
    print(returnData)
    xindIdList=returnData['value']
    if len(xindIdList)==0:
        data = {
            "code": 200,
            "data": "请选择测试点"
        }
        return  JsonResponse(data, safe=False)
    for xindID  in xindIdList:
        _testcasemanager = xmind_data()
        _testcasemanager = xmind_data.objects.get(id=xindID)
        _testcasemanager.delete()

    data = {
            "code": 200,
            "data": "删除测试点成功"
        }
    
    return JsonResponse(data, safe=False)

    



# 发送企信通知
def dingXmindMessage(url,versionStart,username,version, topic, case, caseType, result,remark):
    '''叮叮消息通知'''
    import requests
    import json

    versionInfo = '''
                \n\n > 更新人: <font color=#409EFF>{}</font>
                \n\n > 版本: <font color=#E6A23C>{}</font>
                \n\n > 执行路径 : <font color=#409EFF>{}</font> 
                \n\n > 测试点 : <font color=#409EFF>{}</font>  
                \n\n > 类型 : <font color=#303133>{}</font>  
                \n\n > 执行结果 : <font color=#E6A23C>{}</font>  
                \n\n > 备注 : <font color=#303133>{}</font>
                '''.format(
                    username, version, topic, case, caseType,result, remark)
    versionStart = versionStart + versionInfo + '\n'

    url = url

    payload = json.dumps({
    "msgtype": "markdown",
    "markdown": {
        "title": "执行失败测试点通知",
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

    

def saveTestCase(request):
    '''保存单条用例'''
    returnData = json.loads(request.body)
    print(returnData)
    requestData=returnData['value']
    caseName=requestData['caseName']
    caseType = requestData['caseType']
    case_id = requestData['case_id']
    condition = requestData['condition']
    creater = requestData['creater']

    createrTime = requestData['createrTime']
    exceptResult = requestData['exceptResult']
    firstModel = requestData['firstModel']
    prdName = requestData['prdName']
    secondModel = requestData['secondModel']
    actualResult=requestData['actualResult']
    steps = requestData['steps']
    thirdModel = requestData['thirdModel']
    versionName = requestData['versionName']
    remark=requestData['remark']

    name = request.session.get('username', False)
    sql = "select first_name from auth_user where username='{}'".format(name)
    nameList = commonList().getModelData(sql)
    print(nameList)
    username = nameList[0]['first_name']
    if len(creater)==0:
        creater=username
    if len(createrTime)==0:
        createrTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    _testcasemanager=testcasemanager()
    if case_id:
        _testcasemanager = testcasemanager.objects.get(case_id=case_id)
        _testcasemanager.caseName=caseName
        _testcasemanager.caseType = caseType
        _testcasemanager.condition = condition
        _testcasemanager.creater = creater
        _testcasemanager.createrTime = createrTime
        _testcasemanager.actualResult=actualResult
        _testcasemanager.exceptResult = exceptResult
        _testcasemanager.firstModel = firstModel
        _testcasemanager.prdName = prdName
        _testcasemanager.secondModel = secondModel
        _testcasemanager.executor = username
        _testcasemanager.steps = steps
        _testcasemanager.thirdModel = thirdModel
        _testcasemanager.versionName = versionName
        _testcasemanager.remark = remark
    else:
        _testcasemanager.caseName = caseName
        _testcasemanager.caseType = caseType
        _testcasemanager.condition = condition
        _testcasemanager.creater = creater
        _testcasemanager.actualResult = actualResult
        _testcasemanager.createrTime = createrTime
        _testcasemanager.exceptResult = exceptResult
        _testcasemanager.firstModel = firstModel
        _testcasemanager.prdName = prdName
        _testcasemanager.executor = username
        _testcasemanager.secondModel = secondModel
        _testcasemanager.steps = steps
        _testcasemanager.thirdModel = thirdModel
        _testcasemanager.versionName = versionName
        _testcasemanager.remark = remark
    _testcasemanager.save()
    data = {
        "code": 200,
        "data": "更新用例成功"
    }

    return JsonResponse(data, safe=False)

def selectTotalXmindCases(request):
    '''查询所有测试点'''
    requestData = json.loads(request.body)
    versionName=requestData['versionName']
    sql="select * from quality_xmind_data where version='{}' order by id desc".format(versionName)
    responseData=commonList().getModelData(sql)

    data = {
        "code": 200,
        "data": responseData
    }

    return JsonResponse(data, safe=False)


def selectTotalCases(request):
    '''查询所有用例'''
    requestData = json.loads(request.body)
    versionName=requestData['versionName']
    sql="select * from quality_testcasemanager where versionName='{}' order by case_id desc".format(versionName)
    responseData=commonList().getModelData(sql)

    data = {
        "code": 200,
        "data": responseData
    }

    return JsonResponse(data, safe=False)
def selectXminData(request):
    '''测试点查询'''
    requestData = json.loads(request.body)
    print(requestData)
    pageSize=requestData['pageSize']
    currentPage=requestData['currentPage']
    owner=requestData['owner']
    result=requestData['result']
    caseType=requestData['caseType']
    case=requestData['caseName']
    version=requestData['versionName']
    prdModel=requestData['prdModel']

    print(pageSize)
    print(currentPage)



    sql = 'SELECT * FROM quality_xmind_data WHERE '
    conditions = []

    if len(owner) > 0:
        owner_conditions = ["owner LIKE '%{}%'".format(s) for s in owner]
        conditions.append("(" + " OR ".join(owner_conditions) + ")")

    if len(case) > 0:
        case = " `case` LIKE '%" + case + "%'"
        case_conditions = [case]
        conditions.append("(" + " OR ".join(case_conditions) + ")")

    if len(prdModel) > 0:
        print("111111111")
        prdModel_conditions = " OR ".join("prdModel LIKE '%{}%'".format(model) for model in prdModel)
        conditions.append(f"({prdModel_conditions})")


    if len(result) > 0 and '全部' not in result:
        development_conditions = ["result LIKE '%{}%'".format(r) for r in result]
        conditions.append("(" + " OR ".join(development_conditions) + ")")

    if len(caseType) > 0:
        status_conditions = ["caseType LIKE '%{}%'".format(s) for s in caseType]
        conditions.append("(" + " OR ".join(status_conditions) + ")")

    if conditions:
        sql += " AND ".join(conditions)

    if len(owner) != 0 or len(result) != 0 or len(caseType) != 0 or len(case) !=0 or len(prdModel)!=0:
        sql += " and version='{}'".format(version)

    if len(owner) == 0 and (len(result) == 0 or '全部' in result) and len(caseType) == 0 and len(case)==0 and len(prdModel)==0:
        sql = "SELECT * FROM quality_xmind_data where version='{}' ".format(version)


    offset = (currentPage - 1) * pageSize
    sql += " LIMIT {} OFFSET {}".format(pageSize, offset)

    print('=======sql========', sql)
    data = commonList().getModelData(sql)


    # 获取用例个数
     # 汇总数据
    sqlTotal='''
                SELECT 
                SUM(CASE WHEN result = '成功' THEN 1 ELSE 0 END) AS successNum,
                SUM(CASE WHEN result = '失败' THEN 1 ELSE 0 END) AS FailNum,
                SUM(CASE WHEN result = '未执行' THEN 1 ELSE 0 END) AS undoNum,
                SUM(CASE WHEN result = '阻塞' THEN 1 ELSE 0 END) AS zusheNum,
                SUM(CASE WHEN result = '废弃' THEN 1 ELSE 0 END) AS unNum,
                SUM(CASE WHEN result = '需求变更' THEN 1 ELSE 0 END) AS changeNum,
                COUNT(id) AS totalNum,
                ROUND(
                    ((SUM(CASE WHEN result = '成功' THEN 1 ELSE 0 END) + 
                    SUM(CASE WHEN result = '失败' THEN 1 ELSE 0 END) + 
                    SUM(CASE WHEN result = '阻塞' THEN 1 ELSE 0 END) + 
                    SUM(CASE WHEN result = '需求变更' THEN 1 ELSE 0 END)) / 
                    COUNT(id)) * 100, 1
                ) AS executPre
                FROM quality_xmind_data
                where version=\'{}\' 
        '''.format(version)
    if conditions:
        sqlTotal= sqlTotal+" and"+" AND ".join(conditions)

    print("=====汇总统计sql=={}".format(sqlTotal))
    
    totalBugData=commonList().getModelData(sqlTotal)


    import ast
    for i in data:
        if i.get('prdModel'):
            i['prdModel']=ast.literal_eval(i['prdModel'])


    data = {
            "code": 200,
            "data": data,
            "totalNum":totalBugData
        }
    return JsonResponse(data, safe=False)
def configCaseOwner(request):
    '''订单配置负责人'''
    requestData = json.loads(request.body)
    print(requestData)
    cases=requestData["cases"]
    owner=requestData["owner"]
    caseType=requestData["xmindType"]
    
    for case in cases:
        id=case['id']
        _xmind=xmind_data.objects.get(id=id)
        _xmind.owner=owner
        _xmind.caseType=caseType
        _xmind.save()

    data = {
            "code": 200,
            "data": "批量设置成功"
        }
    return JsonResponse(data, safe=False)

    




def selectSingleXmindCase(request):
    '''测试点查询'''
    requestData = json.loads(request.body)
    owner=requestData['owner']
    result=requestData['result']
    caseType=requestData['caseType']
    versionName = requestData['versionName']
    caseName=requestData['caseName']
    sql = 'SELECT * FROM quality_xind_data WHERE '
    conditions = []

    if len(owner) > 0:
        owner_conditions = ["creater LIKE '%{}%'".format(s) for s in owner]
        conditions.append("(" + " OR ".join(owner_conditions) + ")")

    if len(caseName) > 0:
        case = "caseName LIKE '%" + caseName + "%'"
        case_conditions = [case]
        conditions.append("(" + " OR ".join(case_conditions) + ")")

    if len(result) > 0 and '全部' not in result:
        development_conditions = ["actualResult LIKE '%{}%'".format(r) for r in result]
        conditions.append("(" + " OR ".join(development_conditions) + ")")

    if len(caseType) > 0:
        status_conditions = ["caseType LIKE '%{}%'".format(s) for s in caseType]
        conditions.append("(" + " OR ".join(status_conditions) + ")")

    if conditions:
        sql += " AND ".join(conditions)

    if len(owner) != 0 or len(result) != 0 or len(caseType) != 0 or len(caseName) !=0:
        sql += " and versionName='{}'".format(versionName)

    if len(owner) == 0 and (len(result) == 0 or '全部' in result) and len(caseType) == 0 and len(caseName)==0:
        sql = "SELECT * FROM quality_testcasemanager where versionName='{}' order by case_id desc".format(versionName)

    print('=======sql========', sql)
    data = commonList().getModelData(sql)

    data = {
            "code": 200,
            "data": data
        }
    return JsonResponse(data, safe=False)



def selectSingleTest(request):
    '''用例查询'''
    requestData = json.loads(request.body)
    owner=requestData['owner']
    result=requestData['result']
    caseType=requestData['caseType']
    versionName = requestData['versionName']
    caseName=requestData['caseName']


    sql = 'SELECT * FROM quality_testcasemanager WHERE '
    conditions = []

    if len(owner) > 0:
        owner_conditions = ["creater LIKE '%{}%'".format(s) for s in owner]
        conditions.append("(" + " OR ".join(owner_conditions) + ")")

    if len(caseName) > 0:
        case = "caseName LIKE '%" + caseName + "%'"
        case_conditions = [case]
        conditions.append("(" + " OR ".join(case_conditions) + ")")

    if len(result) > 0 and '全部' not in result:
        development_conditions = ["actualResult LIKE '%{}%'".format(r) for r in result]
        conditions.append("(" + " OR ".join(development_conditions) + ")")

    if len(caseType) > 0:
        status_conditions = ["caseType LIKE '%{}%'".format(s) for s in caseType]
        conditions.append("(" + " OR ".join(status_conditions) + ")")

    if conditions:
        sql += " AND ".join(conditions)

    if len(owner) != 0 or len(result) != 0 or len(caseType) != 0 or len(caseName) !=0:
        sql += " and versionName='{}'".format(versionName)

    if len(owner) == 0 and (len(result) == 0 or '全部' in result) and len(caseType) == 0 and len(caseName)==0:
        sql = "SELECT * FROM quality_testcasemanager where versionName='{}' order by case_id desc".format(versionName)

    print('=======sql========', sql)
    data = commonList().getModelData(sql)

    data = {
            "code": 200,
            "data": data
        }
    return JsonResponse(data, safe=False)

def ximdfilesupload(request):
    '''xmind文件上传'''
    data=[]
    req = request.FILES.get('file')
    content = {}

    #测试
    # path="/Users/hll/Desktop/git/platform/media/xmind"

    #线上
    path="/root/platform/media/xmind"
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

def casesfilesupload(request):
    data=[]
    req = request.FILES.get('file')
    content = {}

    #测试
    # path="/Users/hll/Desktop/git/platform/media/cases"

    #线上
    path="/root/platform/media/cases"
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
def parse_xmind(file_path):
    data = xmindparser.xmind_to_dict(file_path)
    print(data)

    def extract_table_data(xmind_data):
        table_data = []

        def traverse(node, parent_titles=[]):
            if node.get('topics'):
                for child in node['topics']:
                    traverse(child, parent_titles + [node['title']])
            else:
                # Determine the second-to-last title in the parent_titles list, if it exists
                parent_case = parent_titles[-1] if len(parent_titles) >= 1 else ''
                node_data = {
                    'title': node.get('title', ''),
                    'parent_titles': ' > '.join(parent_titles),
                    'parent_cases': parent_case,
                    'result': '未执行',
                    'caseType': '功能测试',
                    'remark': ''
                }
                table_data.append(node_data)

        for sheet in xmind_data:
            traverse(sheet['topic'])

        return table_data
        
    data=extract_table_data(data)
        
    return data
def testXmindCasesUpload(request):
    '''上传xmind文件'''
    # try:
    requestData = json.loads(request.body)
    print(requestData)

    file_paths = requestData.get('fileName', [])
    if not file_paths:
        data = {
            "code": 200,
            "msg": "上传的文件为空"
        }
        return JsonResponse(data, safe=False)

    file_path = file_paths[0] if isinstance(file_paths, list) and file_paths else None
    if not file_path:
        data = {
            "code": 400,
            "msg": "无效的文件路径"
        }
        return JsonResponse(data, safe=False)

    print(file_path)
    versionName = requestData['versionName']
    if not versionName:
        data = {
            "code": 400,
            "msg": "版本不能为空"
        }
        return JsonResponse(data, safe=False)
    username = request.session.get('username', None)
    
    if not username:
        data = {
            "code": 401,
            "msg": "用户未登录"
        }
        return JsonResponse(data, safe=False)

    sql="select first_name from auth_user where username='{}'".format(username)
    nameList=commonList().getModelData(sql)
    
    
    if not nameList:
        data = {
            "code": 404,
            "msg": "用户未找到"
        }
        return JsonResponse(data, safe=False)
    name=nameList[0]['first_name']


    content = parse_xmind(file_path)
    prdModel=requestData["prdModel"]
    log.info("获取当前用户{}".format(name))
    

    for xmindData in content:
        _xmind=xmind_data()
        _xmind.case=xmindData['title']
        _xmind.topic=xmindData['parent_titles']
        _xmind.result=xmindData['result']
        _xmind.version=versionName
        _xmind.caseType=xmindData['caseType']
        _xmind.owner=name
        _xmind.creater=name
        _xmind.prdModel=prdModel
        _xmind.parentCase=xmindData['parent_cases']
        _xmind.save()

    data = {
        "code": 200,
        "msg": "文件上传成功"
    }
    return JsonResponse(data, safe=False)

    # except Exception as e:
    #     data = {
    #         "code": 500,
    #         "msg": str(e)
    #     }
    #     return JsonResponse(data, safe=False)


def testCasesUpload(request):
    '''上传用例'''
    # try:
    requestData = json.loads(request.body)
    file_path = requestData['fileName']
    versionName=requestData['versionName']
    username = request.session.get('username', False)
    sql="select first_name from auth_user where username='{}'".format(username)
    nameList=commonList().getModelData(sql)
    name=nameList[0]['first_name']


    import_excel_to_database(file_path,versionName,name)
    for file in file_path:
        os.remove(file)
    data = {
        "code": 200,
        "msg": "上传用例成功"
    }
    return JsonResponse(data, safe=False)
    # except Exception as e :
    data = {
        "code": 500,
        "msg": "上传用例失败，出错原因如下\n{}".format(e)
    }
    return JsonResponse(data, safe=False)

@transaction.atomic
def import_excel_to_database(file_paths,versionName,username):

    for file_path in file_paths:
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            df.fillna('', inplace=True)
            for index, row in df.iterrows():
                print(row)
                if len(row['用例类型'])==0:
                    case_type='功能测试'
                else:
                    case_type = row['用例类型']
                if len(row['实际结果'])==0:
                    result='未执行'
                else:
                    result=row['实际结果']
                if len(row['编写人'])==0:
                    user=username
                else:
                    user=row['编写人']
                instance = testcasemanager(
                    prdName=row.get('需求名称', None),
                    firstModel=row.get('一级模块', None),
                    secondModel=row.get('二级模块', None),
                    thirdModel=row.get('三级模块', None),
                    caseName=row.get('用例标题', None),
                    condition=row.get('前置条件', None),
                    steps=row.get('操作步骤', None),
                    exceptResult=row.get('预期结果', None),
                    actualResult=result,
                    caseType=case_type,
                    creater=user,
                    createrTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    versionName=versionName
                )
                instance.save()
def selectSortXmind(request):
    '''查询分段xmin数据'''
    requestData = json.loads(request.body)
    versionName=requestData['versionName']
    startNum=requestData['startNum']
    endNum=requestData['endNum']
    prdModel=requestData['prdModel']
    # 将 prdModel 转换为字符串格式，并用单引号包围每个元素
    prdModel_String=','.join((model) for model in prdModel)

    sql = "select * from quality_xmind_data where version='{}' and prdModel LIKE '%{}%'".format(versionName, prdModel_String)
    print(sql)

    responseData=commonList().getModelData(sql)
    for i in responseData:
        if i.get('prdModel'):
            i['prdModel'] = ast.literal_eval(i['prdModel'])
    if startNum < 0 or endNum < 0:
            data = {
                "code": 1003,
                "data": "起始和结束用例数必须为非负整数"
            }
    elif startNum == 0 and endNum == 0:
        data = {
            "code": 200,
            "data": responseData
        }
    elif startNum == 0 and endNum <= len(responseData):
        data = {
            "code": 200,
            "data": responseData[startNum:endNum]
        }
    elif startNum == 0 and endNum > len(responseData):
        data = {
            "code": 1001,
            "data": "筛选的用例数大于该版本的所有用例数，请重新输入"
        }
    elif startNum != 0 and endNum == 0:
        data = {
            "code": 1001,
            "data": "筛选的结束用例数不为0"
        }
    elif startNum >= len(responseData):
        data = {
            "code": 1003,
            "data": "起始用例数超出范围，请重新输入"
        }
    elif endNum <= startNum:
        data = {
            "code": 1002,
            "data": "筛选的结束用例数必须大于起始用例数"
        }
    else:
        data = {
            "code": 200,
            "data": responseData[startNum:endNum]
        }

    return JsonResponse(data, safe=False)

def selectXmindData(request):
    '''查询所有xmind数据'''
    import ast
    requestData = json.loads(request.body)
    versionName=requestData['versionName']
    sql="select * from quality_xmind_data where version='{}' ".format(versionName)
    responseData=commonList().getModelData(sql)

    for i in responseData:
        if i.get('prdModel'):
            i['prdModel'] = ast.literal_eval(i['prdModel'])

     # 汇总数据
    sqlTotal='''
            SELECT 
            SUM(CASE WHEN result = '成功' THEN 1 ELSE 0 END) AS successNum,
            SUM(CASE WHEN result = '失败' THEN 1 ELSE 0 END) AS FailNum,
            SUM(CASE WHEN result = '未执行' THEN 1 ELSE 0 END) AS undoNum,
            SUM(CASE WHEN result = '阻塞' THEN 1 ELSE 0 END) AS zusheNum,
            SUM(CASE WHEN result = '废弃' THEN 1 ELSE 0 END) AS unNum,
            SUM(CASE WHEN result = '需求变更' THEN 1 ELSE 0 END) AS changeNum,
            COUNT(id) AS totalNum,
            ROUND(
                ((SUM(CASE WHEN result = '成功' THEN 1 ELSE 0 END) + 
                SUM(CASE WHEN result = '失败' THEN 1 ELSE 0 END) + 
                SUM(CASE WHEN result = '阻塞' THEN 1 ELSE 0 END) + 
                SUM(CASE WHEN result = '需求变更' THEN 1 ELSE 0 END)) / 
                COUNT(id)) * 100, 1
            ) AS executPre
            FROM quality_xmind_data
            where version=\'{}\'

    '''.format(versionName)

    totalBugData=commonList().getModelData(sqlTotal)
    
    data = {
        "code": 200,
        "data": responseData,
        "totalNum":totalBugData
    }

    return JsonResponse(data, safe=False)

def selectCasesData(request):
    '''查找用例信息'''
    requestData = json.loads(request.body)
    tableName=requestData['tableName']

    sql="select * from quality_testcasemanager where versionName='{}' order by  case_id desc ".format(tableName)
    responseData=commonList().getModelData(sql)

    tree_sql="select * from quality_xmind_data where version='{}' ".format(tableName)
    responseTreeData=commonList().getModelData(tree_sql)

    for i in responseTreeData:
        if i.get('prdModel'):
            i['prdModel'] = ast.literal_eval(i['prdModel'])


        
    data = {
        "code": 200,
        "data":responseData,
        "treeData":responseTreeData
    }
    return JsonResponse(data, safe=False)














