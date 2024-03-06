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
from pathlib import Path
log=Log()


def downFiles(request):
    '''下载文件'''
    responseData = json.loads(request.body)
    file_paths = responseData['fileList']
    url_name_set = [item.get('response') for item in file_paths]

    if url_name_set:
        zip_file_path = '/root/zip/file.zip'
        # 测试环境
        # zip_file_path = '/Users/hll/Desktop/git/platform/media/file.zip'
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for file_info in url_name_set:
                for file_data in file_info:
                    zip_file.write(file_data["url"], os.path.basename(file_data["name"]))

        response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_file_path)}"'
        return response
    else:
        return JsonResponse({'error': 'One or more files do not exist.'}, status=400)

def delFilsList(request):
    requestData = json.loads(request.body)
    print(requestData)
    delfileName = requestData['delfileName']
    saveFile = requestData['saveFile']
    versionName=requestData['versionName']
    print(delfileName)

    import os
    # 指定目录路径-测试环境
    directory = "/Users/hll/Desktop/git/platform/media"

    # 指定目录路径-生产环境
    # directory = "/root/platform/media"

    file_path = os.path.join(directory, delfileName)

    if os.path.exists(file_path):
        os.remove(file_path)

    try:
        _document = documentMan.objects.get(name=versionName)
        _document.children = saveFile
        _document.save()
    except documentMan.DoesNotExist:
        _document = documentMan()
        _document.children = saveFile
        _document.save()

    data = {
        "code": 200,
        "msg": "删除成功"
    }
    return JsonResponse(data, safe=False)

def selectFileLists(request):
    '''查询文件列表'''
    requestData = json.loads(request.body)
    versionName = requestData['versionName']

    sql='select * from quality_documentman where name='+'\''+versionName+'\''
    responseData=commonList().getModelData(sql)
    children=ast.literal_eval(responseData[0]["children"])
    data = {
        "code": 200,
        "data": children
    }
    return JsonResponse(data, safe=False)

def saveFilsList(request):
    '''保存文件'''
    requestData = json.loads(request.body)
    versionName = requestData['versionName']
    filesList=requestData['names']
    print(filesList)
    import os
    import shutil

    # 生产环境
    source_dir = "/root/platform/media"
    destination_dir = "/root/platform/static"

    # 测试环境
    # source_dir = "/Users/hll/Desktop/git/platform/media"
    # destination_dir = "/Users/hll/Desktop/git/platform/static"
    # 获取源目录中的所有文件
    files = os.listdir(source_dir)
    try:
        _document = documentMan.objects.get(name=versionName)
        _document.children = filesList
        _document.save()
    except documentMan.DoesNotExist:
        _document = documentMan()
        _document.children = filesList
        _document.save()

    # fieleList=[]
    # for file_name in filesList:
    #     source_file = os.path.join(source_dir, file_name)
    #     destination_file = os.path.join(destination_dir, file_name)
    #     destination_file=destination_file
    #     fieleList.append(destination_file)
    #     # 如果目标文件不存在，则复制文件
    #     if not os.path.exists(destination_file):
    #         shutil.copy(source_file, destination_dir)
    #         print(f"复制 {file_name} 到 {destination_dir}")
    #     else:
    #         print(f"{file_name} 已存在于 {destination_dir}")


    data = {
        "code": 200,
        "msg": "文件上传成功"
    }
    return JsonResponse(data, safe=False)

@msgMessage
def filesupload(request):
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
    # path="/Users/hll/Desktop/git/platform/media"

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



def selectFiles(request):
    '''查询文件'''
    sql = 'select * from quality_documentman'
    responseData = commonList().getModelData(sql)
    print(responseData)
    responseTotalData = build_tree(responseData, '默认分组')

    data = {
        "code": 200,
        "data": responseTotalData
    }
    return JsonResponse(data, safe=False)

def build_tree(data, parent_name):
    tree = []
    for item in data:
        if item['parentName'] == parent_name:
            children = build_tree(data, item['name'])
            node = {
                'id': item['id'],
                'label': item['name'],
                'children': children
            }
            tree.append(node)
    return tree

def editFiles(request):
    '''编辑目录'''
    requestData = json.loads(request.body)
    oldData = requestData['oldData']
    newData=requestData['newData']

    _document = documentMan.objects.get(name=oldData)
    _document.name=newData
    _document.save()

    data = {
        "code": 200,
        "msg": "编辑分组成功"
    }
    return JsonResponse(data, safe=False)


def delFileName(request):
    '''删除文件目录'''
    requestData = json.loads(request.body)
    docData = requestData['label']
    _document=documentMan.objects.get(name=docData)
    _document.delete()
    data = {
        "code": 200,
        "msg": "删除分组成功"
    }
    return JsonResponse(data, safe=False)


def savefileData(request):
    '''保存文件目录'''
    requestData = json.loads(request.body)
    docData = requestData['docData']
    print(docData)
    id=docData['id']
    name=docData['label']
    children=docData['children']
    parentName=docData['parentName']
    try:
        documentMan.objects.get(name=name)
        data = {
            "code": 50000,
            "msg": "分组名称重复"
        }
    except documentMan.DoesNotExist :
        _docData=documentMan()
        _docData.id=id
        _docData.name=name
        _docData.children=children
        _docData.parentName=parentName
        _docData.save()

        data = {
            "code": 200,
            "msg": "新增分组成功"
        }
    return JsonResponse(data, safe=False)



