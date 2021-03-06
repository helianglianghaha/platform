from django.http.response import JsonResponse
# from quality.models import Version
# from quality.view.API.model import Api
# from quality.view.API.model import Testcase
# from quality.view.API.model import Webtestcase
# from quality.view.API.model import Script
from quality.view.API.model import Modeldata
from quality.view.API.model import Modelversion
from quality.view.API.model import  Scriptproject
from django.core import serializers
from quality.common.logger import Log
import  os,shutil
log=Log()

import json,re
from quality.common.commonbase import commonList
from quality.view.API.APIClass import APITest
from quality.common.functionlist import FunctionList
#上传文件

# def sortProjectData(request):
#     '''查找'''

def upload(request):
    data=[]
    print('上传文件',request.POST)
    req = request.FILES.get('file')
    print(req)
    # 将上传的文件逐行读取保存到list中
    file_info = {'date': '', 'name': '', 'uuid': '', 'path': ''}
    content = {}
    # for line in req.read().splitlines():
    #     content.append(line)

    #测试
    #path="D:\\testPlatForm\\TestPlat\\platForm\\media"

    #线上
    path="/data/wwwroot/platform/media"
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
def deleteApiScript(request):
    '''删除脚本'''
    fileName=request.POST.get('fileName')
    urlName=request.POST.get('urlName')
    projectName = request.POST.get('projectName')
    versionName = request.POST.get('versionName')

    path='/mnt/install/jmeter/apache-jmeter-5.4.1/demo/'
    #获取项目名称
    projectSql = 'select modelData from quality_modeldata where modeldata_id= ' + projectName
    projectName = (commonList().getModelData(projectSql))

    #获取版本名称
    versionSql = 'select modelData from quality_modeldata where modeldata_id= ' + versionName
    versionName = (commonList().getModelData(versionSql))

    totalPathName=path+projectName[0]["modelData"]+"/"+versionName[0]["modelData"]+"/"+fileName
    if os.path.exists(totalPathName):
        os.remove(totalPathName)

    if os.path.exists(urlName):
        os.remove(urlName)
        data = {
            "code": 200,
            "msg": "执行成功"
        }
    else:
        data = {
            "code": 300,
            "msg": "文件不存在"
        }
    return JsonResponse(data, safe=False)

#保存脚本地址
def saveScriptFile(request):
    '''保存脚本文件地址'''
    print(request.POST)
    dataList=request.POST
    for i in  dataList.keys():
        dataDictList=json.loads(i)

        sceiptProject_id = dataDictList['sceiptProject_id']
        projectName = dataDictList['projectName']
        versionName = dataDictList['versionName']
        buildAddress = dataDictList['buildAddress']
        reportAddress = dataDictList['reportAddress']
        scriptName = dataDictList['urlList']
        executeType = dataDictList['executeType']
        performanceData = dataDictList['performanceData']
        performanceReport = dataDictList['performanceReport']
        _scriptProject=Scriptproject()


        if sceiptProject_id:
            _scriptProject.sceiptProject_id=sceiptProject_id
            _scriptProject.projectName = projectName
            _scriptProject.versionName = versionName
            _scriptProject.buildAddress = buildAddress
            _scriptProject.reportAddress = reportAddress
            _scriptProject.scriptName = scriptName
            _scriptProject.executeType = executeType
            _scriptProject.performanceData = performanceData
            _scriptProject.performanceReport = performanceReport
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
            _scriptProject.scriptName = scriptName
            _scriptProject.executeType = executeType
            _scriptProject.performanceData = performanceData
            _scriptProject.performanceReport = performanceReport
            _scriptProject.save()
            data = {
                "code": 200,
                "msg": "接口脚本保存成功"
            }
            return JsonResponse(data, safe=False)
#删除脚本信息
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
    '''查询脚本信息'''
    sql="select * from quality_scriptproject a,quality_modeldata b where a.versionName=b.modeldata_id"
    data = commonList().getModelData(sql)
    return JsonResponse(data, safe=False)
# 执行脚本
def executeScript(request):
    '''执行脚本'''
    # try:
        # print('执行脚本',request.POST)
    executeType=request.POST.get("executeType")
    buildAddress=request.POST.get("buildAddress")
    performanceData=request.POST.get("performanceData")
    scriptName=eval(request.POST.get("scriptName"))

    #获取项目地址
    projectName_id=request.POST.get('projectName')
    sql='select modelData from quality_modeldata where modeldata_id= '+projectName_id
    projectName=(commonList().getModelData(sql))

    #获取版本地址
    modelData=request.POST.get('modelData')
    # print("modelData",modelData)

    #创建build文件目录
    ant_build="/mnt/install/ant/apache-ant-1.9.16/build/"
    if not os.path.exists(ant_build+projectName[0]["modelData"]+"/"+modelData):
        os.makedirs(ant_build+projectName[0]["modelData"]+"/"+modelData)

    #创建测试报告文件夹
    testReportAddress='/data/wwwroot/platform/static/'
    if not  os.path.exists(testReportAddress+projectName[0]["modelData"]+"/"+modelData):
        os.makedirs(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/ApiReport/")
        os.makedirs(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/")

    #创建日志文件
    log_path="/data/wwwroot/platform/logs/"
    if not os.path.exists(log_path+projectName[0]["modelData"]+"/"+modelData):
        os.makedirs(log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/")
        os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/")
        os.mknod(log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text")
        os.mknod(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/" + "log.text")

    #创建脚本目录
    apiScriptFilePath = '/mnt/install/jmeter/apache-jmeter-5.4.1/demo/'
    performanceScriptFilePath = '/mnt/install/jmeter/apache-jmeter-5.4.1/Pro_jmx/'
    if not os.path.exists(apiScriptFilePath+projectName[0]["modelData"] + "/" + modelData):
        os.makedirs(apiScriptFilePath+projectName[0]["modelData"] + "/" + modelData)
    if not os.path.exists(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData):
        os.makedirs(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData)

    #复制脚本到对应的文件夹
    print('scriptName',(scriptName))
    fileUrlList=[i["url"] for i in scriptName]
    print("================================fileUrlList===============",fileUrlList)
    if executeType == '0' or executeType == False:#接口
        for fileUrl in fileUrlList:
            fileName = os.path.split(fileUrl)[1]  # 读取文件名
            fullFilePath = apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData + "/" + fileName
            if os.path.exists(fullFilePath):
                pass
            else:
                print("=========================复制接口脚本=======================")
                sourceFilePath='/data/wwwroot/platform/media/'+fileName
                shutil.copyfile(sourceFilePath,fullFilePath)
    else:#性能
        for fileUrl in fileUrlList:
            fileName = os.path.split(fileUrl)[1]  # 读取文件名
            fullFilePath = performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData + "/" + fileName
            if os.path.exists(fullFilePath):
                pass
            else:
                print("========================复制性能脚本=================")
                sourceFilePath = '/data/wwwroot/platform/media/' + fileName
                shutil.copyfile(sourceFilePath, fullFilePath)

    # 执行脚本前清除数据
    performanceReportPath = '/data/wwwroot/platform/static/' + projectName[0]["modelData"] + '/' + modelData + '/PerformanceReport/*'
    apiReportPatb = '/data/wwwroot/platform/static/' + projectName[0]["modelData"] + '/' + modelData + '/ApiReport/*'



    #测试环境日志文件
    # logPath="D:\\testPlatForm\\TestPlat\\platForm\\logs\\webtestcase.txt"

    #生成环境日志文件
    logPath='/mnt/install/ant/apache-ant-1.9.16/logs/log.text'

    if executeType=='0' or executeType==False :
        os.system("rm -rf " + apiReportPatb)
        shellData='ant -file '+buildAddress+" run  >>"+log_path+projectName[0]["modelData"]+"/"+modelData+"/ApiLog/"+"log.text"
        print('shellData',shellData)
    if executeType=='1' or executeType==True:
        os.system("rm -rf " + performanceReportPath)
        shellData=performanceData+" >> "+log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text"
        print('shellData', shellData)
    os.system(shellData)
    data = {
        "code": 200,
        "msg": "脚本开始执行，请查看日志及测试报告"
        }

    return JsonResponse(data, safe=False)
# def viewTestHtml(request):
#     '''查看测试报告'''
def readHtmlReport(request):
    '''读取html报告'''
    try:
        reportAddress=request.POST.get("reportAddress")
        print("reportAddress",reportAddress)
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
def readScriptLog(request):
    '''读取ant执行日志'''

    # 获取项目地址
    projectName_id = request.POST.get('projectName')
    executeType=request.POST.get("executeType")
    sql = 'select modelData from quality_modeldata where modeldata_id= ' + projectName_id
    projectName = commonList().getModelData(sql)

    # 获取版本地址
    modelData = request.POST.get('modelData')

    #创建目录
    log_path="/data/wwwroot/platform/logs"
    if not os.path.exists(log_path+projectName[0]["modelData"]+"/"+modelData):
        os.makedirs(log_path+projectName[0]["modelData"]+"/"+modelData)
        os.makedirs(log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/")
        os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/")

    # #测试环境
    # path="D:\\testPlatForm\\TestPlat\\platForm\\logs\\webtestcase.txt"

    #线上环境
    print("executeType",executeType)
    print("Type",type(executeType))
    if executeType=='0' or executeType==False :
        path = "/data/wwwroot/platform/logs/" + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/" + "log.text"
        print("API",path)
    if executeType=='1' or executeType==True :
        path = "/data/wwwroot/platform/logs/" + projectName[0]["modelData"] + "/" + modelData + "/PerformanceLog/" + "log.text"
        print("性能",path)
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
        logger=open("/data/wwwroot/platform/logs","r",encoding='UTF-8',errors='ignore')
        loglist=logger.readlines()
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
def addModelVersion(request):
    print('version',request.POST)
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
def selectModelVersion(request):
    sql='select modeldata_id as value,modelData as label from quality_modeldata where subModelData!=0'
    data=commonList().getModelData(sql)
    return JsonResponse(data,safe=False)
#查询模块信息
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
def deleteModelDataList(request):
    print("删除modelData",request.POST)
    modeldata_id=request.POST.get('modeldata_id')
    Modeldatalist=Modeldata.objects.get(modeldata_id=modeldata_id)
    Modeldatalist.delete()
    data={
        "code":200,
        "msg":"删除成功"
    }
    return JsonResponse(data,safe=False)



#查询所有的模块信息
def selectAllModel(request):
    sql="SELECT b.modelData,b.modeldata_id,b.subModelData,b.modelData_proenvironment,b.modelData_testenvironment,b.modelData_pripeople,a.modelData AS"+"\'"+'name'+"\'"+"FROM quality_modeldata b LEFT JOIN quality_modeldata a on a.modeldata_id=b.subModelData order by modeldata_id  desc"
    data = commonList().getModelData(sql)   
    return JsonResponse(data,safe=False)
#查询模块信息
def selectModelList(request):
    sql="select modeldata_id 'value' , modelData 'label' from quality_modeldata where subModelData=0"
    data = commonList().getModelData(sql)
    return JsonResponse(data,safe=False)

#保存模块信息
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
            if projectId is '':
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
    print(request.POST)
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

    print((script_timeout))
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



