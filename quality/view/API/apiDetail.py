# -*- coding: utf-8 -*-
import datetime

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
from django.core import serializers
from quality.common.logger import Log
from quality.common.msg import msgMessage, msglogger
from quality.common.msg import loginRequired
from quality.common.logger import Log
from pathlib import Path
import  os,shutil
log=Log()

import json,re,os,zipfile
from quality.common.commonbase import commonList
from quality.view.API.APIClass import APITest
from quality.common.functionlist import FunctionList

def uploadApi(request):
    '''导入Json文件'''
    import mysql.connector
    import json
    requestData = json.loads(request.body)
    filePaths=requestData['fileName']
    firstFile=requestData['firstFile']
    secondFile=requestData['secondFile']
    thirdFile=requestData['thirdFile']
    project=requestData['project']

    db_connection = mysql.connector.connect(
        host="192.168.8.28",
        user="root",
        password="mysql_ciFtek",
        database="testplatfrom"
    )



    for filePath in filePaths:
        with open(filePath,'r') as f:
            openapi_spec = json.load(f)


        db_cursor = db_connection.cursor()
        for path, methods in openapi_spec['paths'].items():
            for method, details in methods.items():
                summary = details.get('summary', '')
                deprecated = details.get('deprecated', False)
                description = details.get('description', '')
                tagsdata=details.get('tags', [])
                tags=json.dumps(details.get('tags', []))
                parameters = json.dumps(details.get('parameters', []))
                responses = json.dumps(details.get('responses', {}))
                security = json.dumps(details.get('security', []))
                print(tags)
                if len(tagsdata)!=0:
                    tags_list = tagsdata[0].split('/')
                    print(tags_list)
                    if len(tags_list)==1:
                        firstFile=tags_list[0]
                    elif len(tags_list) == 2:
                        firstFile = tags_list[0]
                        secondFile = tags_list[1]
                    elif len(tags_list)>2:
                        firstFile = tags_list[0]
                        secondFile=tags_list[1]
                        thirdFile=tags_list[2]
                    else:
                        firstFile = ''
                        secondFile = ''
                        thirdFile = ''
                else:
                    firstFile = project
                    secondFile = ''
                    thirdFile = ''

                query = "INSERT INTO api_endpoints (path, method, summary,tags, deprecated, description, parameters, responses, security,firstFile,secondFile,thirdFile,project) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s,%s)"
                values = (path, method, summary,tags, deprecated, description, parameters, responses, security,firstFile,secondFile,thirdFile,project)
                db_cursor.execute(query, values)
        db_connection.commit()
        db_connection.close()

    for file in filePaths:
        os.remove(file)

    data = {
        "code": 200,
        "msg": '文件导入成功'
    }

    return JsonResponse(data, safe=False)


def jsonfilesupload(request):
    data=[]
    req = request.FILES.get('file')
    content = {}

    #测试
    # path="/Users/hll/Desktop/git/platform/media/json"

    #线上
    path="/root/platform/media/json"
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


def selectAllApiData(request):
    '''查询所有接口'''
    requestData = json.loads(request.body)
    path=requestData['select_path']
    project = requestData['select_project']
    description=requestData['select_apiName']
    environment=requestData['select_environment']
    pageSize=requestData['pageSize']
    currentPage=requestData['currentPage']

    sql = 'SELECT * FROM api_endpoints WHERE '
    count_query = 'SELECT COUNT(*) as total FROM api_endpoints WHERE '
    conditions = []

    if len(path) > 0:
        path_conditions = ["path LIKE '%{}%'".format(path)]
        conditions.append("(" + " OR ".join(path_conditions) + ")")

    if len(project) > 0:
        project_conditions = ["project LIKE '%{}%'".format(r) for r in project]
        conditions.append("(" + " OR ".join(project_conditions) + ")")

    if len(description) > 0:
        description_conditions = ["description LIKE '%{}%'".format(r) for r in description]
        conditions.append("(" + " OR ".join(description_conditions) + ")")

    if len(environment) > 0:
        environment_conditions = ["environment LIKE '%{}%'".format(r) for r in environment]
        conditions.append("(" + " OR ".join(environment_conditions) + ")")


    if conditions:
        sql += " AND ".join(conditions)
        count_query += " AND ".join(conditions)
    else:
        sql = 'SELECT * FROM api_endpoints'
        count_query = 'SELECT COUNT(*) as total FROM api_endpoints'


    offset = (currentPage - 1) * pageSize
    sql += "  LIMIT {} OFFSET {}".format(pageSize, offset)
    # base_query += "  LIMIT {} OFFSET {}".format(pageSize, offset)
    print(sql)
    print(count_query)

    totalNum=commonList().getModelData(count_query)
    responseData=commonList().getModelData(sql)
    data = {
        "code": 200,
        "data": responseData,
        "totalNum":totalNum
    }

    return JsonResponse(data, safe=False)




