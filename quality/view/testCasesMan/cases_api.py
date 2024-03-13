# -*- coding: utf-8 -*-
from quality.common.commonbase import commonList
from quality.view.API_version.API_function import requestObject,createDataFinally
from quality.view.API_version.API_dataList import DataList
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.http.response import JsonResponse,FileResponse
from quality.view.documentMan.doc_model import documentMan
import  json,os,os,zipfile,ast
from quality.common.msg import msgMessage
from quality.common.logger import Log
import pandas as pd
from datetime import datetime
from django.db import transaction
from quality.view.testCasesMan.cases_model import testcasemanager
from pathlib import Path
log=Log()

def downloadTemFiles(request):
    '''下载模版文件'''

    zip_file_path = '/root/zip/file.zip'

    # zip_file_path = '/Users/hll/Desktop/git/platform/media/file.zip'

    # 测试环境
    url = '/root/platform/media/template/测试用例模板.xlsx'

    # url='/Users/hll/Desktop/git/platform/media/template/测试用例模版.xlsx'

    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        zip_file.write(url, '测试用例模板.xlsx')

    response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_file_path)}"'
    return response

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
    _testcasemanager.save()
    data = {
        "code": 200,
        "data": "更新用例成功"
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


def selectSingleTest(request):
    '''用例查询'''
    requestData = json.loads(request.body)
    owner=requestData['owner']
    result=requestData['result']
    caseType=requestData['caseType']
    versionName = requestData['versionName']


    sql = 'SELECT * FROM quality_testcasemanager WHERE '
    conditions = []

    if len(owner) > 0:
        owner_conditions = ["creater LIKE '%{}%'".format(v) for v in owner]
        conditions.append("(" + " OR ".join(owner_conditions) + ")")

    if len(result) > 0:
        development_conditions = ["actualResult LIKE '%{}%'".format(r) for r in result]
        conditions.append("(" + " OR ".join(development_conditions) + ")")

    if len(caseType) > 0:
        status_conditions = ["caseType LIKE '%{}%'".format(s) for s in caseType]
        conditions.append("(" + " OR ".join(status_conditions) + ")")

    if conditions:
        sql += " AND ".join(conditions)

    if len(owner) != 0 or len(result) != 0 or len(caseType) != 0:
        sql += " and versionName='{}'".format(versionName)

    if len(owner) == 0 and len(result) == 0 and len(caseType) == 0:
        sql = "SELECT * FROM quality_testcasemanager where versionName='{}' order by case_id desc".format(versionName)

    print('=======sql========', sql)
    data = commonList().getModelData(sql)

    data = {
            "code": 200,
            "data": data
        }
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

def testCasesUpload(request):
    '''上传用例'''
    try:
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
    except Exception as e :
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


def selectCasesData(request):
    '''查找用例信息'''
    requestData = json.loads(request.body)
    tableName=requestData['tableName']

    sql="select * from quality_testcasemanager where versionName='{}' order by  case_id desc ".format(tableName)
    responseData=commonList().getModelData(sql)


    data = {
        "code": 200,
        "data":responseData
    }
    return JsonResponse(data, safe=False)














