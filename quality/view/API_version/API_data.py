# -*- coding:utf-8 -*-
# Author:heliangliang
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
from quality.view.API_version.API_function import requestObject


@loginRequired
@msgMessage
def selectCookiesSelection(request):
    '''查询cookies'''
    sql = 'select cookie_name as label,cookie_name as value from quality_testcookies'
    data = commonList().getModelData(sql)
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def delCookies(request):
    '''删除cookies'''
    cookie_id = request.POST.get('cookie_id')
    _delCookie = Testcookies.objects.get(cookie_id=cookie_id)
    _delCookie.delete()
    data = {
        "code": 200,
        "msg": '删除用例成功'
    }
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def selectCookies(request):
    '''查找cookies'''
    sql = 'select * from quality_testcookies'
    data = commonList().getModelData(sql)
    log.info('cookies:%s' % data)
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def saveCookies(request):
    '''保存cookies'''
    cookie_id = request.POST.get("cookie_id")
    cookie_name = request.POST.get("cookie_name")
    cookie_value = request.POST.get("cookie_value")
    cookie_domain = request.POST.get("cookie_domain")
    cookie_path = request.POST.get("cookie_path")
    _cookies = Testcookies()
    if cookie_id:
        _cookies.cookie_id = cookie_id
        _cookies.cookie_name = cookie_name
        _cookies.cookie_value = cookie_value
        _cookies.cookie_domain = cookie_domain
        _cookies.cookie_path = cookie_path
        _cookies.save()
        data = {
            "code": 200,
            "msg": '用例编辑成功'
        }
    else:
        _cookies.cookie_name = cookie_name
        _cookies.cookie_value = cookie_value
        _cookies.cookie_domain = cookie_domain
        _cookies.cookie_path = cookie_path
        _cookies.save()
        data = {
            "code": 200,
            "msg": '用例保存成功'
        }
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def saveTestSort(request):
    '''保存用例排序'''
    print("用例排序", request.POST)
    for i in request.POST:
        idList = json.loads(i)
        print('idList length', idList['resetList'])

        for i in range(0, len(idList['resetList'])):
            print('i', i)
            if len(idList['resetList']) != 0:
                if idList['resetList'][i] != idList['testCaseID'][i]:
                    print('i', i)
                    print('resetList', idList['resetList'][i])
                    print('testCaseID', idList['testCaseID'][i])

                    _testCaseList = Testapi.objects.get(testapi_id=idList['resetList'][i])
                    _testResetCaseList = Testapi.objects.get(testapi_id=idList['testCaseID'][i])
                    idList['resetList'].remove(idList['resetList'][i])
                    print(idList['resetList'])
                    idList['resetList'].remove(idList['testCaseID'][i])
                    print(idList['resetList'])

                    _copytestCaseList = copy.deepcopy(_testCaseList)
                    _copytestResetCaseList = copy.deepcopy(_testResetCaseList)

                    _copytestCaseList.testmodelData = _testResetCaseList.testmodelData
                    _copytestCaseList.Modelversion_id_id = _testResetCaseList.Modelversion_id_id
                    _copytestCaseList.testapiHost = _testResetCaseList.testapiHost
                    _copytestCaseList.testapiname = _testResetCaseList.testapiname
                    _copytestCaseList.testapiMethod = _testResetCaseList.testapiMethod
                    _copytestCaseList.testapiUrl = _testResetCaseList.testapiUrl
                    _copytestCaseList.testapiBody = _testResetCaseList.testapiBody
                    _copytestCaseList.testapiExtractName = _testResetCaseList.testapiExtractName
                    _copytestCaseList.testapiExtractExpression = _testResetCaseList.testapiExtractExpression
                    _copytestCaseList.testapiExtractResponse = _testResetCaseList.testapiExtractResponse

                    _copytestCaseList.testapiAssert = _testResetCaseList.testapiAssert
                    _copytestCaseList.testapiResponse = _testResetCaseList.testapiResponse
                    _copytestCaseList.testcookiesValue = _testResetCaseList.testcookiesValue
                    _copytestCaseList.testresult = _testResetCaseList.testresult
                    _copytestCaseList.teststatuscode = _testResetCaseList.teststatuscode
                    _copytestCaseList.testencoding = _testResetCaseList.testencoding
                    _copytestCaseList.testheader = _testResetCaseList.testheader
                    _copytestCaseList.testurl = _testResetCaseList.testurl
                    _copytestCaseList.testaddPassWordFree = _testResetCaseList.testaddPassWordFree
                    _copytestCaseList.testpassWordFree = _testResetCaseList.testpassWordFree
                    _copytestCaseList.testapiRequest = _testResetCaseList.testapiRequest

                    _copytestResetCaseList.testmodelData = _testCaseList.testmodelData
                    _copytestResetCaseList.Modelversion_id_id = _testCaseList.Modelversion_id_id
                    _copytestResetCaseList.testapiHost = _testCaseList.testapiHost
                    _copytestResetCaseList.testapiname = _testCaseList.testapiname
                    _copytestResetCaseList.testapiMethod = _testCaseList.testapiMethod
                    _copytestResetCaseList.testapiUrl = _testCaseList.testapiUrl
                    _copytestResetCaseList.testapiBody = _testCaseList.testapiBody
                    _copytestResetCaseList.testapiExtractName = _testCaseList.testapiExtractName
                    _copytestResetCaseList.testapiExtractExpression = _testCaseList.testapiExtractExpression
                    _copytestResetCaseList.testapiExtractResponse = _testCaseList.testapiExtractResponse

                    _copytestResetCaseList.testapiAssert = _testCaseList.testapiAssert
                    _copytestResetCaseList.testapiResponse = _testCaseList.testapiResponse
                    _copytestResetCaseList.testcookiesValue = _testCaseList.testcookiesValue
                    _copytestResetCaseList.testresult = _testCaseList.testresult
                    _copytestResetCaseList.teststatuscode = _testCaseList.teststatuscode
                    _copytestResetCaseList.testencoding = _testCaseList.testencoding
                    _copytestResetCaseList.testheader = _testCaseList.testheader
                    _copytestResetCaseList.testurl = _testCaseList.testurl
                    _copytestResetCaseList.testaddPassWordFree = _testCaseList.testaddPassWordFree
                    _copytestResetCaseList.testpassWordFree = _testCaseList.testpassWordFree
                    _copytestResetCaseList.testapiRequest = _testCaseList.testapiRequest

                    _copytestCaseList.save()
                    _copytestResetCaseList.save()
                    break
                else:
                    pass
            else:
                pass
    data = {
        "code": 200,
        "msg": '用例调整成功'
    }
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def delVariable(request):
    '''删除全局变量'''
    variable_id = request.POST.get("variable_id")
    _vari = Testvariable.objects.get(variable_id=variable_id)
    _vari.delete()
    data = {
        "code": 200,
        "msg": '删除变量成功'
    }
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def selectGlobalVariable(request):
    '''查找全局变量'''
    sql = 'select * from quality_testvariable'
    variableList = commonList().getModelData(sql)
    log.info('response:%s' % variableList)
    data = {
        "code": 200,
        "msg": variableList
    }
    return JsonResponse(data, safe=False)


# 保存全局变量
@loginRequired
@msgMessage
def saveGlobalVari(request):
    '''保存全局变量'''
    variable_id = request.POST.get("varId")
    variableKey = request.POST.get("variKey")
    variableValue = request.POST.get("variValue")

    _variable = Testvariable()
    if variable_id:
        _variable.variable_id = variable_id
        _variable.variableKey = variableKey
        _variable.variableValue = variableValue
        _variable.save()
        data = {
            "code": 200,
            "msg": '全局变量编辑成功'
        }
    else:
        _variable.variableKey = variableKey
        _variable.variableValue = variableValue
        _variable.save()
        data = {
            "code": 200,
            "msg": "全局变量保存成功"
        }
    log.info('response:%s' % data)
    return JsonResponse(data, safe=False)


# 查询关键字和用例信息
@loginRequired
@msgMessage
def selectTestKey(request):
    '''查询关键字和用例信息'''
    sql_keyWord = 'select key_name as value,key_name as label from quality_keyword'
    sql_testCase = 'select testcase_id as value,testcase_caseName as label from quality_testcase'
    keyWord_data = commonList().getModelData(sql_keyWord)
    testCase_data = commonList().getModelData(sql_testCase)
    data = {
        "code": 200,
        "msg": "获取关键字和用例信息成功",
        "keyWord_data": keyWord_data,
        "testCase_data": testCase_data
    }
    return JsonResponse(data, safe=False)


# 查询报告
@loginRequired
@msgMessage
def selectReportList(request):
    '''查看报告'''
    # print('查看报告',request.POST)
    executing_testmd = request.POST.get("executing_name")
    sql = "select * from quality_executinglog a,quality_testapi b where a.executing_testmd=" + "\'" + executing_testmd + "\'" + "and a.executing_testapi_id=b.testapi_id"
    # print('sql',sql)
    TestcaseList = commonList().getModelData(sql)

    # 获取执行人姓名
    username = request.session.get('username', False)

    # 获取执行脚本项目
    Modelversion_id_id = TestcaseList[0]['Modelversion_id_id']
    selectVersion = 'select modeldata_name from quality_modelversion where Modelversion_id=' + str(Modelversion_id_id)
    versionNameList = commonList().getModelData(selectVersion)
    versionName = versionNameList[0]["modeldata_name"]

    sql_num = "SELECT SUM(CASE WHEN a.testresult = 1 THEN 1 ELSE 0 END) count_success,SUM(CASE WHEN a.testresult = 2 THEN 1 ELSE 0 END) count_fail,SUM(CASE WHEN a.testresult is  null THEN 1 ELSE 0 END) count_null,count(*) total from quality_testapi a," \
              + "quality_executinglog b WHERE a.testapi_id=b.executing_testapi_id AND b.executing_testmd=" + "\'" + executing_testmd + "\'"
    print('sql_num', sql_num)
    testResult=[]
    for testCase in range (len(TestcaseList)):
        print('testCase',TestcaseList[testCase])
        testapiBody=(TestcaseList[testCase]['testapiBody']).replace("null","\'\'")
        TestcaseList[testCase]['testheader']=eval((TestcaseList[testCase]['testheader']))
        TestcaseList[testCase]['testapiBody'] =eval(testapiBody)
    TestcaseNum = commonList().getModelData(sql_num)
    data = {
        "code": 200,
        "msg": "获取报告成功",
        "testCaseList": TestcaseList,
        "testCaseNums": TestcaseNum,
        "testResult":testResult,
        "username":username,
        "version":versionName
    }
    return JsonResponse(data, safe=False)


# 删除单个版本
@loginRequired
@msgMessage
def deletaSingleVersion(request):
    '''删除单个版本'''
    Modelversion_id = request.POST.get('Modelversion_id')
    testModelVersion = Modelversion.objects.get(Modelversion_id=Modelversion_id)
    testModelVersion.delete()
    data = {
        "code": 0,
        "msg": "删除成功"
    }
    return JsonResponse(data, safe=False)


# 搜索单个版本
@loginRequired
@msgMessage
def selectSingleVersion(request):
    '''查询单个版本'''
    modelVersion = request.POST.get("modelVersion")
    sql = "select * from quality_modelversion where modeldata_name=" + "\'" + modelVersion + "\'"
    data = commonList().getModelData(sql)
    return JsonResponse(data, safe=False)


# 复制接口测试用例
@loginRequired
@msgMessage
def copyApiTestCases(request):
    '''复制接口测试用例'''
    requestData = json.loads(request.body)
    
    # cookiesValue = requestData("testaddCookiesValue")
    addPassWordFree = requestData["testaddPassWordFree"]
    passWordFree = requestData["testpassWordFree"]
    modelData = requestData["testmodelData"]
    print('modelData',modelData)
    versionData = (requestData["Modelversion_id_id"])
    apiRequest = requestData['testapiRequest']
    apiName = requestData["testapiname"]
    testaddCookiesValue = requestData['testaddCookiesValue']
    apiHost = requestData["testapiHost"]
    apiExtractName = requestData['testapiExtract']

    apiMethod = requestData["testapiMethod"]
    apiUrl = requestData["testapiUrl"]
    apiBody = requestData["testapiBody"]
    apiExtract=requestData["testapiExtract"]
    apiHeader = requestData["testapiHeader"]
    apiAssert = requestData["testapiAssert"]
    # apiResponse = request.POST.get["apiResponse"]

    _testapi = Testapi()
    _testapi.testmodelData = (modelData)
    _testapi.Modelversion_id_id = versionData
    _testapi.testapiHost = apiHost
    _testapi.testapiname = apiName
    _testapi.testapiMethod = apiMethod
    _testapi.testapiRequest = apiRequest
    _testapi.testapiUrl = apiUrl
    _testapi.testapiBody = apiBody
    _testapi.testapiExtract=apiExtract
    _testapi.testapiHeader = apiHeader
    _testapi.testaddCookiesValue = testaddCookiesValue
    _testapi.testapiExtractName = apiExtractName


    _testapi.testapiAssert = apiAssert
    # _testapi.testapiResponse = apiResponse
    # _testapi.testcookiesValue = cookiesValue
    _testapi.testaddPassWordFree = addPassWordFree
    _testapi.testpassWordFree = passWordFree
    _testapi.save()
    data = {
        "code": 0,
        "msg": "复制测试用例成功"
    }

    return JsonResponse(data, safe=False)


# 删除接口用例
@loginRequired
@msgMessage
def deleteApiTestCases(request):
    '''删除接口用例'''
    print("获取要删除的用例ID", request.POST)
    testapi_id = request.POST.get("testapi_id")
    testCase = Testapi.objects.get(testapi_id=testapi_id)
    testCase.delete()
    data = {
        "code": 0,
        "msg": "删除成功"
    }
    return JsonResponse(data, safe=False)


# 编辑接口用例
# 查询接口用例
@loginRequired
@msgMessage
def selectApiCases(request):
    '''查询接口用例'''
    import ast
    modeldata_name = request.POST.get("tableData")
    sql = "select testapi_id,testmodelData,Modelversion_id_id,testapiHost,testapiname,testapiMethod,testapiUrl,testapiBody,testapiAssert,testcookiesValue,testaddPassWordFree,testpassWordFree,testapiRequest,testapiExtract,testaddCookiesValue,testapiHeader from quality_testapi where Modelversion_id_id=(select Modelversion_id from quality_modelversion where modeldata_name=" + "\'" + modeldata_name + "\'" + ")"
    data = commonList().getModelData(sql)
    for case in range(len(data)):
        print(data[case])
        if data[case]["testapiAssert"]:
            data[case]["testapiAssert"] = (eval(data[case]["testapiAssert"]))
        if data[case]["testapiHeader"]:
            data[case]["testapiHeader"] = (eval(data[case]["testapiHeader"]))
        if data[case]["testapiExtract"]:
            data[case]["testapiExtract"] = (eval(data[case]["testapiExtract"]))
    return JsonResponse(data, safe=False)


# 保存接口用例
@loginRequired
@msgMessage
def saveApiTestCase(request):
    '''保存接口用例'''
    print(json.loads(request.body))
    requestData = json.loads(request.body)
    
    pId = requestData["pId"]
    cookiesValue = requestData["cookiesValue"]
    addPassWordFree = requestData["addPassWordFree"]
    passWordFree = requestData["passWordFree"]
    modelData = int(requestData["modelData"])
    versionData = int(requestData["versionData"])
    apiRequest = requestData['apiRequest']
    apiName = requestData["apiName"]
    testaddCookiesValue = requestData['addCookiesValue']
    apiHost = requestData["apiHost"]
    apiExtract = requestData['apiExtract']

    apiMethod = requestData["apiMethod"]
    apiHeader = requestData['apiHeader']
    apiUrl = requestData["apiUrl"]
    apiBody = requestData["apiBody"]
    # apiExtract=requestData["apiExtract"]
    apiAssert = requestData["apiAssert"]
    # apiResponse=requestData["apiResponse"]

    if pId:
        _testapi = Testapi()
        _testapi.testapi_id = int(pId)
        _testapi.testmodelData = int(modelData)
        _testapi.Modelversion_id_id = versionData
        _testapi.testapiHost = apiHost
        _testapi.testapiname = apiName
        _testapi.testapiMethod = apiMethod
        _testapi.testapiRequest = apiRequest
        _testapi.testaddCookiesValue = testaddCookiesValue
        _testapi.testapiHeader = apiHeader
        _testapi.testapiUrl = apiUrl
        _testapi.testapiBody = apiBody
        # _testapi.testapiExtract=apiExtract

        _testapi.testapiExtract= apiExtract


        _testapi.testapiAssert = apiAssert
        # _testapi.testapiResponse=apiResponse
        _testapi.testcookiesValue = cookiesValue
        _testapi.testaddPassWordFree = addPassWordFree
        _testapi.testpassWordFree = passWordFree
        _testapi.save()
        data = {
            "code": 0,
            "msg": "编辑测试用例成功"
        }
    else:
        _testapi = Testapi()
        _testapi.testmodelData = int(modelData)
        _testapi.Modelversion_id_id = versionData
        _testapi.testapiHost = apiHost
        _testapi.testapiname = apiName
        _testapi.testapiMethod = apiMethod
        _testapi.testapiRequest = apiRequest
        _testapi.testapiUrl = apiUrl
        _testapi.testapiBody = apiBody
        _testapi.testapiHeader = apiHeader
        # _testapi.testapiExtract=apiExtract
        _testapi.testaddCookiesValue = testaddCookiesValue
        _testapi.testapiExtract= apiExtract


        _testapi.testapiAssert = apiAssert
        # _testapi.testapiResponse=apiResponse
        _testapi.testcookiesValue = cookiesValue
        _testapi.testaddPassWordFree = addPassWordFree
        _testapi.testpassWordFree = passWordFree
        _testapi.save()
        data = {
            "code": 0,
            "msg": "保存测试用例成功"
        }
    return JsonResponse(data, safe=False)


# 批量执行接口用例
@loginRequired
@msgMessage
def todoBatchExection(request):
    '''批量执行接口用例'''
    # try:
    dataList = request.POST.items()
    print("dataList", dataList)

    for test_list in dataList:
        print(test_list)
        caseList = json.loads(test_list[0])

        # 判断列表是否为空
        if len(list(caseList)) == 0:
            data = {
                "code": 10002,
                "msg": "接口用例为空,请选择接口用例",
            }
            return JsonResponse(data, safe=False)
        # 获取执行人姓名
        username = request.session.get('username', False)




        # 判断是否是单个项目

        # 判断是否是多个项目

        # 判断列表是否为一个元素
        if len(list(caseList)) == 1:
            caseList = str(caseList[0])
            sql = 'select * from quality_testapi where testapi_id = ' + caseList
        else:
            caseList = str(tuple(caseList))
            sql = 'select * from quality_testapi where testapi_id in ' + caseList
        print("sql", sql)
        caseList = commonList().getModelData(sql)
        print(caseList)

        # 获取执行脚本项目
        Modelversion_id_id = caseList[0]['Modelversion_id_id']
        selectVersion = 'select modeldata_name,modeldata_id_id from quality_modelversion where Modelversion_id=' + str(Modelversion_id_id)
        versionNameList = commonList().getModelData(selectVersion)
        versionName = versionNameList[0]["modeldata_name"]
        modelDataID=versionNameList[0]["modeldata_id_id"]


        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        executing_testmd = APITest().Hashlib()
        for caseData in caseList:

            # 过滤参数存在变量重新赋值
            from .API_function import responseExecuting
            caseDataSort = responseExecuting().sortVariable(caseData)

            # print('caseData', caseDataSort)
            testapi_id = caseDataSort['testapi_id']
            testmodelData = caseDataSort['testmodelData']
            Modelversion_id_id = caseDataSort['Modelversion_id_id']
            testapiRequest = caseDataSort['testapiRequest']
            testapiHost = caseDataSort['testapiHost']

            testapiHeader=eval(caseDataSort['testapiHeader'])
            testapiAssert=eval(caseDataSort["testapiAssert"])
            # print('testapiHeader',testapiHeader)

            # testapiname=caseData['testapiname']
            testapiMethod = str(caseData['testapiMethod'])
            testapiUrl = caseData['testapiUrl']

            testapiBody = caseData['testapiBody']
            testapiExtract=eval(caseData['testapiExtract'])
            testapiAssert = caseData['testapiAssert']
            url = testapiRequest + "://" + testapiHost + testapiUrl
            # print('testapiExtract', testapiExtract)

            from quality.view.API_version.API_function import responseExecuting
            if caseData['testcookiesValue'] == 'true':

                # 查询登录接口
                sql = "select * from quality_testapi where testapiname='登录' and Modelversion_id_id=" + str(
                    Modelversion_id_id)
                loginData = commonList().getModelData(sql)

                login_url = "https://" + loginData[0]['testapiHost'] + loginData[0]['testapiUrl']
                login_data = loginData[0]['testapiBody']
                response = APITest().updataCookies(login_url, login_data)
                testapiResponse = APITest().apiRequest(url, testapiBody, testapiMethod, response)

                _testCases = Testapi.objects.get(testapi_id=testapi_id)
                _testCases.teststatuscode = testapiResponse.status_code
                _testCases.testencoding = testapiResponse.encoding
                _testCases.testurl = testapiResponse.url
                _testCases.testheader = testapiResponse.headers
                _testCases.testapiResponse = str(bytes.decode(testapiResponse.content))[0:980]

                returnDataList = responseExecuting().assertApiData(testapiResponse, testapiAssert, testapiResponse.status_code)
                _testCases.testapiAssert = returnDataList["assertData"]

                if len(testapiAssert) != 0 and "fail" not in returnDataList["resultList"]:
                    _testCases.testresult = 1
                else:
                    _testCases.testresult = 2
                _testCases.save()

                _executing = Executinglog()
                _executing.executing_name = nowtime
                _executing.executing_testmd = executing_testmd
                _executing.executing_testapi_id = testapi_id
                _executing.executing_starttime = datetime.datetime.now()
                _executing.save()

            else:
                testapiResponse = APITest().requestNoCookie(url, testapiBody, testapiMethod,testapiHeader)
                testapiExtract=responseExecuting().extractApiData(testapiResponse,testapiExtract)
                _testCases = Testapi.objects.get(testapi_id=testapi_id)
                _testCases.testapiResponse = bytes.decode(testapiResponse.content)[0:980]
                _testCases.teststatuscode = testapiResponse.status_code
                _testCases.testencoding = testapiResponse.encoding
                _testCases.testheader = testapiResponse.headers
                _testCases.testurl = testapiResponse.url
                _testCases.testapiExtract=testapiExtract

                returnDataList=responseExecuting().assertApiData(testapiResponse,testapiAssert,testapiResponse.status_code)
                _testCases.testapiAssert=returnDataList["assertData"]

                if len(testapiAssert) != 0 and  "fail" not in returnDataList["resultList"]:
                    _testCases.testresult = 1
                else:
                    _testCases.testresult = 2

                # if len(testapiAssert) != 0 and testapiAssert in str(bytes.decode(testapiResponse.content)):
                #     _testCases.testresult = 1
                # else:
                #     _testCases.testresult = 2
                _testCases.save()

                _executing = Executinglog()
                _executing.executing_name = nowtime
                _executing.executing_testmd = executing_testmd
                _executing.executing_testapi_id = testapi_id
                _executing.executing_starttime = datetime.datetime.now()
                _executing.executing_userName=username
                _executing.executing_versionName=versionName
                _executing.save()
    #查询当前运行版本是否有消息通知
    dingMessageSql='select ding_version version ,ding_address robotAddress,ding_people people from quality_dingmessage  a where a.ding_message=\'True\'and ding_version is not NULL'
    data = commonList().getModelData(dingMessageSql)
    print('data',data)
    if len(data)==0:
        pass
    else:
        from .API_function import createData
        createData().sortDingMessage(data,modelDataID,executing_testmd,versionName,username)

    # for versionList in range(len(data)) :
    #     for version in eval(data[versionList]['version']):
    #         if Modelversion_id_id ==version:
    #             #机器人地址
    #             ding_url=data["ding_address"]
    #             #测试报告地址
    #             testReportAddress='http://127.0.0.1:8080/#/reportManage?label='+executing_testmd
    #             createData().sendDingMessageTotal(ding_url,testReportAddress,executing_testmd,versionName,username)
    #         else:
    #             pass

    #生成报告后URL地址
    data = {
        "code": 200,
        "msg": "接口用例执行成功",
        "label": executing_testmd
    }
    # except Exception as e:
    #     data = {
    #         "code": 10001,
    #         "msg": "接口用例执行出错,出错原因：" + str(e),
    #     }

    return JsonResponse(data, safe=False)
#造数据接口
def createData(request):
    '''造数据接口'''
    requestData = json.loads(request.body)


#冷站智控小工具
def executTools(request):
    '''
    主要测试计算问题
    执行率  已执行数量\已发策略数量
    响应率：（已执行数量+未执行备注数量）/已发策略数量
    核算节能量
    核算节能量
    同比节能率
    同比节能量
    '''
    requestData = json.loads(request.body)
    print('冷站测试小工具', requestData)
    jituan_project_id=requestData['jituan_project_id']#集团ID
    partition_project_id=requestData['partition_project_id']#广场ID
    partition_building_id = requestData['partition_building_id']#建筑ID
    equmentID = requestData['equmentID']#设备ID
    startTime=requestData['startTime']
    endTime=requestData['endTime']

    #获取当前时间段
    nowtime=datetime.datetime.now()
    dateYear=nowtime.year
    dateMonth=nowtime.month
    if len(startTime)==0 or len(endTime)==0:
        if (dateMonth)<10:
            dateMonth='0'+str(dateMonth)
            if int(dateMonth)-1>=0:
                lastYear=dateYear
                lastMont=str(int(dateMonth)-1)
            else:
                lastYear=str(int(dateYear)-1)
                lastMont='12'
        dateDay=nowtime.day
        if (dateDay)<10:
            dateDay='0'+dateDay
        currDate = str(dateYear) + str(dateMonth) + str(dateDay) + "000000"
        lastDate = str(lastYear) + str(lastMont) + str(dateDay) + "000000"
        startMonth=str(lastYear) +"-"+ str(lastMont)+"-"+"01"+" 00:00:00"
        endMonth = str(lastYear) +"-"+ str(lastMont) +"-"+ str(dateDay) + " 23:59:59"
        startMonthLast=str(lastYear-1) +"-"+ str(lastMont)+"-"+"01"+" 00:00:00"
        endMonthLast=str(lastYear-1) +"-"+ str(lastMont) +"-"+ str(dateDay) + " 23:59:59"

        #室内温度满足率 开始时间 结束时间
        startIndoorRateDate=str(dateYear) + str(dateMonth-1) + str(dateDay)
        endIndoorRateDate=str(dateYear) + str(dateMonth) + str(dateDay)
    else:
        currDate=endTime
        lastDate=startTime
        startMonth=startTime[0:4]+"-"+startTime[4:6]+"-"+"01 00:00:00"
        endMonth=startTime[0:4]+"-"+startTime[4:6]+"-"+"31 23:59:59"
        startMonthLast = str(int(startTime[0:4])-1) + "-" + startTime[4:6] + "-" + "01 00:00:00"
        endMonthLast=str(int(startTime[0:4])-1)+"-"+startTime[4:6]+"-"+"31 23:59:59"

        #室内温度满足率
        startIndoorRateDate=startTime[0:8]
        endIndoorRateDate=endTime[0:8]

        #当日室内温度满足率
        currIndoorDate=endTime[0:4]+"-"+endTime[4:6]+"-"+endTime[6:8]+" 00:00:00"


    totallist={}

    #执行率计算 已执行数量\已发策略数量
    sql='SELECT( SUM( CASE WHEN a.is_executed = 1 THEN 1 ELSE 0 END ) ) / (COUNT(*)) executedRate,' \
        '(SUM( CASE WHEN a.is_executed = 1 THEN 1 ELSE 0 END ) + SUM( CASE WHEN a.is_executed = 0 AND a.remarks IS NOT NULL THEN 1 ELSE 0 END ) ) / (COUNT(*)) executedRemarkRate ' \
        'FROM chiller_command a WHERE a.project_id = \''+partition_project_id+'\' AND ( a.create_time BETWEEN \' '+lastDate+'\' AND \''+currDate+'\')'
    print('sql',sql)
    #执行sql
    from .API_function import responseExecuting
    executedRate=responseExecuting().assertSelectSqlData(sql)
    print('executedRate',executedRate)
    if executedRate[0]['executedRate']:
        totallist['executedRate']=round(executedRate[0]['executedRate'],2)
        totallist['executedRemarkRate']=round(executedRate[0]['executedRemarkRate'],2)
    else:
        totallist['executedRate']='数据为空'
        totallist['executedRemarkRate']='数据为空'
    #核算节能量
    saveEnergySql='select c_energy_saving from t_energy_saving   where  c_project_id= \''+partition_project_id+'\''
    energySaveData = responseExecuting().assertSelectSqlData(saveEnergySql)
    if len(energySaveData)>0:
        totallist['energySaving']=energySaveData[0]['c_energy_saving']
    else:
        totallist['energySaving']="节能量数据为空"
        totallist['energySavingRate']="节能量数据为空无法计算"
    #核算节能率 -（核算节能量/今年冷站总能耗）


    #同比节能量-（上年冷站总能耗-今年冷站总能耗）

    sameEnergySavingSql='select sum(energy_value) sameEnergySaving from tb_coldstation_sub_energy_day where project_id=\''\
                        +partition_project_id+'\'and subitem_id=\'EI10102010101001\''+' and date_time >= \''+startMonth+'\' and date_time <= \''+endMonth+'\''
    sameEnergySaving=responseExecuting().assertSelectSqlData(sameEnergySavingSql)

    sameEnergySavingSqlLast='select sum(energy_value) sameEnergySaving from tb_coldstation_sub_energy_day where project_id=\''\
                        +partition_project_id+'\'and subitem_id=\'EI10102010101001\''+' and date_time >= \''+startMonthLast+'\' and date_time <= \''+endMonthLast+'\''
    sameEnergySavingLast = responseExecuting().assertSelectSqlData(sameEnergySavingSqlLast)

    if isinstance(sameEnergySaving[0]["sameEnergySaving"],int):
        totallist['sameEnergySaving']=sameEnergySavingLast[0]['sameEnergySaving']-sameEnergySaving[0]['sameEnergySaving']
        totallist['sameEnergySavingRate']=(sameEnergySavingLast[0]['sameEnergySaving']-sameEnergySaving[0]['sameEnergySaving'])/sameEnergySaving[0]['sameEnergySaving']
    else:
        totallist['sameEnergySaving']="同比节能量数据为空"
        totallist['sameEnergySavingRate']='同比节能率为空'

    #同微气候区核算节能量


    #单日室内温度满足率-单日多系统-rpt_day_project_chiller_v2
    currIndoorRateSql='select sum(tindoor_fill_rate) currindoorRate from rpt_day_project_chiller_v2 WHERE project_id=\''+partition_project_id+'\'and tindoor_fill_rate <> \'-9999\' and (date_time BETWEEN \''+currIndoorDate+'\' and \''+currIndoorDate+'\')'
    currIndoorRate=responseExecuting().assertSelectSqlData(currIndoorRateSql)

    if currIndoorRate[0]['currindoorRate']:
        totallist['currIndoorTate'] = currIndoorRate[0]['currindoorRate']
    else:
        totallist['currIndoorTate']=0
    # 室内温度满足率-rpt_day_space_chiller_v2
    indoorRateSql='select avg(tindoor_fill_rate) indoorRate from rpt_day_space_chiller_v2 WHERE project_id=\''+partition_project_id+'\'and tindoor_fill_rate <> \'-9999\' and (date BETWEEN \''+startIndoorRateDate+'\' and \''+endIndoorRateDate+'\')'
    indoorRate=responseExecuting().assertSelectSqlData(indoorRateSql)
    if indoorRate[0]['indoorRate']:
        totallist['indoorRate']=indoorRate[0]['indoorRate']
    else:
        totallist['indoorRate']=0

    data={
        "code":200,
        "msg":totallist
    }
    return JsonResponse(data, safe=False)
#核算节能量检查接口
def checkEnergySaving(request):
    '''核算节能量检查接口'''
    requestData = json.loads(request.body)
    print('核算节能量',requestData)

    data={
        "code":200,
        "msg":"成功"
    }
    return JsonResponse(data, safe=False)

#保存钉钉消息配置
def saveDingMessage(request):
    '''保存钉钉消息配置'''
    requestData = json.loads(request.body)
    print("钉钉消息配置",requestData)
    openMessage=requestData['openMessage']
    openXunJian=requestData['openXunJian']
    robotAddress = requestData['robotAddress']
    versionList = requestData['versionList']
    dingPeople=requestData['dingPeople']
    dingID=requestData['dingID']

    _dingMessage=Dingmessage()
    if dingID:
        _dingMessage.ding_id=dingID
        _dingMessage.ding_address=robotAddress
        _dingMessage.ding_xunjian=openXunJian
        _dingMessage.ding_message=openMessage
        _dingMessage.ding_version=versionList
        _dingMessage.ding_people = dingPeople
        _dingMessage.save()

        data={
            "code":200,
            "msg":'编辑钉钉消息配置成功'
        }
    else:
        _dingMessage.ding_address = robotAddress
        _dingMessage.ding_xunjian = openXunJian
        _dingMessage.ding_message = openMessage
        _dingMessage.ding_version = versionList
        _dingMessage.ding_people = dingPeople
        _dingMessage.save()
        data = {
            "code": 200,
            "msg": '新增钉钉消息配置成功'
        }
    return JsonResponse(data, safe=False)

#查询钉钉消息
def selectDingMessage(request):
    '''查询钉钉消息配置'''
    sql = 'select *  from quality_dingmessage'
    data = commonList().getModelData(sql)
    return JsonResponse(data, safe=False)
#删除钉钉消息
def delDingMessage(request):
    '''删除钉钉消息配置'''
    requestData = json.loads(request.body)
    dingID = requestData['ding_id']
    _delDing=Dingmessage.objects.get(ding_id=dingID)
    _delDing.delete()
    data={
        'code':200,
        "msg":"删除配置成功"
    }
    return  JsonResponse(data,safe=False)
# 单接口接口请求
@loginRequired
@msgMessage
def apiRequest(request):
    '''单接口调试'''
    requestData = json.loads(request.body)
    print('单接口请求',requestData)
    cookiesValue = requestData["cookiesValue"]
    versionData = requestData["versionData"]
    apiName = requestData["apiName"]
    apiHost = requestData["apiHost"]
    apiMethod = requestData["apiMethod"]
    apiUrl = requestData["apiUrl"]
    apiBody = requestData["apiBody"]
    apiRequest = requestData['apiRequest']
    addPassWordFree = requestData['addPassWordFree']
    if addPassWordFree == "false":
        addPassWordFree = False
    else:
        addPassWordFree = True
    addCookiesValue = requestData['addCookiesValue']
    # if addCookiesValue=="false":
    #     addCookiesValue=False
    # else:
    #     addCookiesValue=True
    apiExtractName = requestData["apiExtract"]
    passWordFree = requestData['passWordFree']
    if passWordFree == 'false':
        passWordFree = False
    else:
        passWordFree = True
    # print('addCookiesValue',addCookiesValue)
    # print('addPassWordFree',addPassWordFree)
    # print('passWordFree',passWordFree)

    url = apiRequest + "://" + apiHost + apiUrl
    method = apiMethod
    data = apiBody
    apiHeader=eval(requestData['apiHeader'])
    if apiHeader:
        header = {
            'Content-Type': 'application/json;charset=UTF-8',
        }
        for headerList in apiHeader:
            if headerList['key']=='':
                pass
            else:
                header[headerList['key']]=headerList["value"]
        print('header',header)
    else:
        header = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Accept': '*/*'
        }
    if addCookiesValue:
        sql = 'select cookie_name,cookie_value from quality_testcookies where cookie_name=' + "\'" + addCookiesValue + "\'"
        cookieList = commonList().getModelData(sql)
        cookie = {}
        # url='http://a.iyunxiao.com/ctboms?go=http://ctb-oms.yunxiao.com'
        # url='http://a.iyunxiao.com/mkp?go=http://mkp.yunxiao.com'
        cookie[cookieList[0]['cookie_name']] = cookieList[0]['cookie_value']
        responseData = requestObject(url, header, data, method, cookies=cookie, apiExtractName=apiExtractName,
                                     passWordFree=passWordFree,
                                     addPassWordFree=addPassWordFree).requestApi()
        log.info('response:%s' % responseData.content)
        data = {
            "code": 200,
            "msg": "接口用例执行成功",
            "data": json.loads(bytes.decode(responseData.content)),
            "apiName": apiName
        }

    else:
        responseData = requestObject(url, header, data, method, cookies='', apiExtractName=apiExtractName,
                                passWordFree=passWordFree,
                                     addPassWordFree=addPassWordFree).requestApi()
        # if apiExtractName or passWordFree or addPassWordFree:
        #     _getToken(apiExtractName,apiExtractExpression,responseData,passWordFree,addPassWordFree)
        # else:
        #     pass
        # print((responseData.url))
        log.info('response:%s' % responseData.content)
        # try:
        data = {
            "code": 200,
            "msg": "接口用例执行成功",
            "data": json.loads(bytes.decode(responseData.content)),
            "apiName": apiName
        }
        # except Exception as e:
        #     data = {
        #         "code": 200,
        #         "msg": "接口用例执行成功",
        #         "data": 'json解析失败，但请求成功了可以查看日志内容',
        #         "apiName": apiName
        #     }
    return JsonResponse(data, safe=False)


# @msglogger
def _getToken(ExtractName, ExtractExpression, responseData, passWordFree, addPassWordFree):
    '''
    addPassWordFree 提取cookies
    passWordFree URL提取
    获取token
    '''
    if addPassWordFree == 'true':
        # print('提取cookies==================================', responseData.cookies)
        cookieslist = responseData.cookies
        cookie = requests.utils.dict_from_cookiejar(cookieslist)  # 将cookies转换成字典
        # print('获取的字典列表是%s' % cookie)
    else:
        if passWordFree == 'true':
            tokenString = responseData.url
            # print('tokenString1111', tokenString)
        else:
            tokenString = (responseData.content).decode('utf-8')
            # print('tokenString', tokenString)
        variable = re.findall(ExtractExpression, tokenString)
        if len(variable) == 0:
            log.info('获取的token为空')
        else:
            log.info('token:%s' % variable)
            exitVaribale = Testvariable.objects.get(variableKey=ExtractName)
            if exitVaribale:
                exitVaribale.variableKey = ExtractName
                exitVaribale.variableValue = variable[0]
                exitVaribale.save()
            else:
                _globalVal = Testvariable()
                _globalVal.variableKey = ExtractName
                _globalVal.variableValue = variable[0]
                _globalVal.save()


@loginRequired
@msgMessage
def selectVersionData(request):
    '''查询版本信息'''
    sql = 'select Modelversion_id as value,modeldata_name as label from quality_modelversion'
    data = commonList().getModelData(sql)
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def selectVersionList(request):
    '''获取到项目信息'''
    modeldata_name = request.POST.get("modelData")
    sql = 'select Modelversion_id as value,modeldata_name as label from quality_modelversion where modeldata_id_id=' + str(
        modeldata_name)
    data = commonList().getModelData(sql)
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def selectExecuting(request):
    '''查询测试报告'''
    testType = request.POST.get('testtype')
    if testType == 'API':
        sql = 'select * from quality_executinglog  where executing_testapi_id is not null group by executing_testmd ORDER BY executing_starttime desc'
    else:
        sql = 'SELECT * FROM quality_executinglog  where executing_testui_id is not null  GROUP BY executing_testmd ORDER BY executing_starttime DESC '
    data = commonList().getModelData(sql)
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def selectCaseTime(request):
    # print("获取到的日志报告", request.POST)
    executing_name = request.POST.get("executing_name")
    sql = 'select * from quality_executinglog where executing_testmd=' + "\'" + executing_name + "\'"
    data = commonList().getModelData(sql)
    return JsonResponse(data, safe=False)


# 删除日志报告
@loginRequired
@msgMessage
def deleteExecutingLog(request):
    '''删除日志报告'''
    executing_testmd = request.POST.get('executing_testmd')
    sql = 'delete from quality_executinglog where executing_testmd=' + "\'" + executing_testmd + "\'"
    datalist = commonList().getModelData(sql)
    data = {
        "code": 200,
        "msg": "删除日志成功",
    }
    return JsonResponse(data, safe=False)
# "__main__"
# # if __name__=="__main__":
# #
# #     print("test")

