# -*- coding: utf-8 -*-
from quality.common.commonbase import commonList
from quality.view.API_version.API_function import requestObject,createDataFinally
from quality.view.API_version.API_dataList import DataList
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.http.response import JsonResponse,FileResponse
from quality.view.documentMan.doc_model import documentMan
import  json,os,datetime
from quality.common.msg import msgMessage
from quality.common.logger import Log
import pandas as pd
from datetime import datetime
from django.db import transaction
from quality.view.testCasesMan.cases_model import testcasemanager
from pathlib import Path
log=Log()
def casesfilesupload(request):
    data=[]
    req = request.FILES.get('file')
    content = {}

    #测试
    path="/Users/hll/Desktop/git/platform/media/cases"

    #线上
    # path="/root/platform/media/cases"
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



        import_excel_to_database(file_path,versionName,username)
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
                print('=====row======',row)
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
                    creater=username,
                    createrTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    versionName=versionName
                )
                instance.save()


def selectCasesData(request):
    '''查找用例信息'''
    requestData = json.loads(request.body)
    tableName=requestData['tableName']

    sql="select * from quality_testcasemanager where versionName='{}'".format(tableName)
    responseData=commonList().getModelData(sql)


    data = {
        "code": 200,
        "data":responseData
    }
    return JsonResponse(data, safe=False)














