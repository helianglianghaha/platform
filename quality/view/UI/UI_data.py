# -*- coding:utf-8 -*-
# Author:heliangliang
from django.http.response import JsonResponse
# from quality.view.API.model import Api
# from quality.view.API.model import Webtestcase
# from quality.view.API.model import Script
from quality.view.API.model import Modeldata
from quality.view.API.model import Modelversion
from quality.view.API_version.API_model import Testcase
from quality.view.API_version.API_model import Testapi
from quality.view.API_version.API_model import Executinglog
from quality.view.API_version.API_model import Keyword
from quality.view.API_version.API_model import Testscript
from quality.view.API_version.API_model import Testemail
# from quality.view.API_version.API_model import Testpicture,Testscript
from quality.view.API.model import Proaddress
from quality.test.seleniumData.prams import connectionList
# from quality.view.project.login import loginRequired

from quality.pageObject.comPage.page import Page
from django.core import serializers
from quality.common.logger import Log
from quality.common.msg import msgMessage
from quality.common.msg import loginRequired

from django.contrib import  auth
from django.contrib.auth.models import  User
from rest_framework.authtoken.models import Token

import json, re, requests, ast, datetime, copy, time
from quality.common.commonbase import commonList
from quality.view.API.APIClass import APITest
from quality.common.functionlist import FunctionList

from quality.view.UI.UIFunction import UiFunction, executSingleCase


#根据版本查找测试用例
def selectTestCaseList(request):
    '''查找测试用例'''
    print(request.POST)
    versionID=request.POST.get("val")
    sql = 'select a.testcase_id value,a.testcase_caseName label from quality_testcase a where a.testcase_caseVersion='+str(versionID)
    dataList=commonList().getModelData(sql)
    data={
        "code":0,
        "dataList":dataList
    }
    return JsonResponse(data, safe=False)
#用户注册
def userRegister(request):
    '''用户注册'''
    username=request.POST.get("username")
    password=request.POST.get("password")
    if len(username)==0:
        data = {
            "code": 101,
            "msg": "用户名不能为空"
        }
        return JsonResponse(data, safe=False)
    if len(password)==0:
        data = {
            "code": 102,
            "msg": "密码不能为空"
        }
        return JsonResponse(data, safe=False)
    if len(password)==0 or len(username)==0:
        data = {
            "code": 103,
            "msg": "用户名或密码不能为空"
        }
        return JsonResponse(data, safe=False)
    print(request.POST)
    # 通过auth模块，进行新用户注册，使用User表创建新用户(create_use普通用户，create_superuser超级用户)
    if not User.objects.filter(username=username).exists():
        try:
            add_user=User.objects.create_user(username=username, password=password)
            add_user.save()
            data={
                "code":0,
                "msg":"注册成功"
            }
            return JsonResponse(data, safe=False)
        except :
            data = {
                "code": 0,
                "msg": "注册成功,请重新登录"
            }
            return JsonResponse(data, safe=False)
    else:
        data={
            "code": 104,
            "msg": "用户名已存在"
        }
        return JsonResponse(data, safe=False)


# 删除代理地址
def deleteProAddress(request):
    '''删除代理地址'''
    proxyid = request.POST.get("proxyid")
    address = Proaddress.objects.get(proxyid=proxyid)
    address.delete()

    # script_id = request.POST.get('script_id')
    # _script = Testscript.objects.get(script_id=script_id)
    # _script.delete()

    data = {
        "code": 200,
        "msg": "删除成功"
    }
    return JsonResponse(data, safe=False)


# 查找代理地址
def selectProAddress(request):
    '''查找代理地址'''
    sql = 'SELECT * from quality_proaddress a,quality_modelversion b WHERE a.Modelversion_id_id=b.Modelversion_id'
    addressList = commonList().getModelData(sql)
    data = {
        'code': 200,
        'msg': addressList
    }
    return JsonResponse(data, safe=False)


# 保存代理地址
def saveProAddress(request):
    '''保存代理地址'''
    # print('代理地址',request.POST)
    proxyid = request.POST.get("proxyid")
    Modelversion_id = request.POST.get("Modelversion_id")
    pro_address = request.POST.get("pro_address")
    pro_openXunjian = request.POST.get("openXunjian")
    pro_qixin = request.POST.get("pro_qixin")
    pro_openQiXin = request.POST.get("openQiXin")
    _Proaddress = Proaddress()
    if proxyid:
        _Proaddress.proxyid = proxyid
        _Proaddress.Modelversion_id_id = Modelversion_id
        _Proaddress.pro_address = pro_address
        _Proaddress.pro_openXunjian = pro_openXunjian
        _Proaddress.pro_qixin=pro_qixin
        _Proaddress.pro_openQiXin=pro_openQiXin
        _Proaddress.save()
        data = {
            "code": 200,
            "msg": "编辑成功"
        }
        return JsonResponse(data, safe=False)
    else:
        _Proaddress.Modelversion_id_id = Modelversion_id
        _Proaddress.pro_address = pro_address
        _Proaddress.pro_openXunjian = pro_openXunjian
        _Proaddress.pro_qixin = pro_qixin
        _Proaddress.pro_openQiXin = pro_openQiXin
        _Proaddress.save()
        data = {
            "code": 200,
            "msg": "保存成功"
        }
        return JsonResponse(data, safe=False)


# 读取日志文件
def readLog(request):
    # path='C:\TestPlat\platForm\logs\webtestcase.txt'
    path = 'D:\\testPlatForm\\TestPlat\\platForm\\logs\\webtestcase.txt'
    with open(path, 'r', encoding='gbk') as f:
        result = []
        seq = re.compile("\s-")
        for line in f:
            lst = seq.split(line.strip())
            item = {
                "time": lst[0],
                "task": lst[2:]
            }
            result.append(item)
        logList = list(reversed(result[-200:]))
    f.close()
    return JsonResponse(logList, safe=False)


# 注销登录
def LogOut(request):
    '''注销登录'''
    request.session.flush()
    # 删除服务端的session，删除当前的会话数据并删除会话的Cookie。
    # request.session.clear_expired()# 将所有Session失效日期小于当前日期的数据删除，将过期的删除
    # del request.session['k1']#django-session表里面同步删除
    # request.session.delete()# 删除当前会话的所有Session数据
    data = {
        "code": 200,
        "msg": '注销成功'
    }
    return JsonResponse(data, safe=False)


# 保存文件
import os


def saveUpLoad(request):
    '''
    保存文件
    :param request:
    :return:
    '''
    file = request.FILES.get('file')
    file_path = '.\\' + 'media' + '\\' + file.name
    with open(file_path, 'wb+') as f:
        f.write(file.read())
        f.close()
    data = {
        'code': 200,
        'msg': '文件保存成功'
    }
    return JsonResponse(data)


# 查询用户名
@loginRequired
@msgMessage
def selectUserInfo(request):
    '''查询用户名'''
    username = request.session.get('username', False)
    return JsonResponse(username, safe=False)


# 批量执行用例
# @loginRequired
@msgMessage
def batchExecutingCases(request):
    '''批量执行用例'''
    testcaseList = request.POST
    for i in testcaseList:
        caseNameList = json.loads(i)
        testcase_id_list = []
        for j in caseNameList:
            testcase_id_list.append(j['testcase_id'])
        testcase_id_listSort = sorted(testcase_id_list)
        # 循环获取每个用例对应的脚本步骤
        sortListBefore = []
        for testScriptID in testcase_id_listSort:
            sql = 'select * from quality_testscript where script_TestDataCase =' + str(testScriptID)
            CaseList = commonList().getModelData(sql)

            #分类全局变量后脚本列表
            sortGlobalCaseList=sortGlobalVar(CaseList)

            #合并赋值后的用例
            sortListBefore.extend((sortGlobalCaseList))

        # print('sortListBefore',sortListBefore)
    if sortListBefore:
        version = sortListBefore[0]['script_testDataVersion']
    sortList = UiFunction().sortList(sortListBefore)
    mdStringValue = executSingleCase().Hashlib()

    #获取执行人姓名
    username = request.session.get('username', False)

    #获取执行脚本项目
    versionID=sortList[0]['script_testDataVersion']
    selectVersion='select modeldata_name from quality_modelversion where Modelversion_id='+versionID
    versionNameList=commonList().getModelData(selectVersion)
    versionName=versionNameList[0]["modeldata_name"]


    # 检查是否有节点，没有节点不运行给出对应提示
    proAddID=sortList[0]['script_testDataVersion']
    proAddID_Sql='select * from quality_proaddress  where Modelversion_id_id='+proAddID
    proAddress=commonList().getModelData(proAddID_Sql)
    if len(proAddress)==0:
        data = {
            "code": 200,
            "msg": "代理节点为空"
        }
    else:
        print("======================================用例开始执行了==================================")
        executeCase(sortList, mdStringValue,username,versionName)
        print("======================================用例执行结束==================================")
    # if version:#执行完用例后清除driver信息
    #     initPrams(version)

        data = {
            "code": 200,
            "msg": "用例执行完成，详情请查看测试报告"
        }
    return JsonResponse(data, safe=False)

def sortGlobalVar(CaseList):
    '''全局变量赋值'''
    sqlGlobal='select variableKey,variableValue from quality_testvariable'

    #查找所有全局变量
    varableList=commonList().getModelData(sqlGlobal)

    for caseScript in CaseList:
        for varable in varableList:
            if caseScript['script_testDataParameter']==varable["variableKey"]:
                caseScript['script_testDataParameter']=copy.deepcopy(varable["variableValue"])
    return  CaseList

def initPrams(version):
    '''初始化项目driver'''
    # print('connectionList',connectionList)
    del connectionList[version]
    # print('connectionList', connectionList)


def executeCase(val, hashlib,userName,versionName):
    # print("executeCase***********val", val)
    for case in val:
        print('executeCase======case', case)
        executSingleCase()._xunHuanExecutSingle(case, 0, hashlib,userName,versionName)


# 查看图片
# def selectPicture(request):
#
#     return
# 查询测试报告内容
def selectTestReportDetail(request):
    executing_testmdValue = request.POST.get("executing_testmd")
    print("executing_testmdValue", executing_testmdValue)
    sql = 'SELECT * FROM ' \
          '(SELECT * FROM ' \
          'quality_executinglog a,' \
          'quality_testcase b,' \
          'quality_testscript f,' \
          'quality_modelversion d' \
          ' WHERE  f.script_testDataVersion = d.Modelversion_id ' \
          'AND a.executing_testscript_id = f.script_id ' \
          'AND f.script_TestDataCase = b.testcase_id ' \
          'AND a.executing_testmd = ' + '\'' + executing_testmdValue + '\'' \
                                                                       ' ) temp ' \
                                                                       'LEFT JOIN (SELECT * FROM(SELECT * FROM quality_testpicture h ORDER BY h.picture_id DESC ) w GROUP BY w.picture_scriptId) ' \
                                                                       'e ON temp.script_id =e.picture_scriptId'
    # GROUP BY f.script_testDataName
    # print('sql',sql)
    reportValue = commonList().getModelData(sql)
    # print('data',reportValue)

    # 冒泡排序,降序排序
    num = len(reportValue)
    for i in range(num):
        for j in range(0, num - i - 1):
            if reportValue[j]['script_id'] > reportValue[j + 1]['script_id']:
                reportValue[j], reportValue[j + 1] = reportValue[j + 1], reportValue[j]

    result = {
        'testCase_list': [],  # 用例名称列表
        'testScrpit_list': [],  # 脚本列表
        'reportDate': '',  # 报告时间
        'modelVersion': '',  # 项目名称
        'testResult': '',  # 测试结果
        'totalTime': '',  # 总时间
        'scriptRate': {
            'successRate': '',  # 成功率
            'fialRate': '',  # 失败率
        },
        'summary': {
            'total': '',  # 总计
            'success': '',
            'fail': '',
            'successRate': '',  # 成功率
            'failRate': '',  # 失败率
            # 'averageTime':'',#平均响应时间
            # 'minTime':'',#最小执行时间
            # 'maxTime':''#最大执行时间
        },
    }

    testcase_result = []  # 测试用例名称
    testcase_result_dict = {
        "caseName": '',
        'result': []
    }
    time_list = []  # 时间列表
    success = 0
    fail = 0
    testCaseListResult = {}
    for testScript in reportValue:
        # 添加执行失败的用例
        if testScript['testcase_caseName'] not in testcase_result and testScript['script_testResult'] in ['失败'] and len(
                testScript['script_testResult']) > 0:
            testcase_result.append(testScript['testcase_caseName'])
            testcase_result_dict['caseName'] = testScript['testcase_caseName']
            testcase_result_dict['result'].append(testScript['script_testResult'])
            result['testCase_list'].append(copy.deepcopy(testcase_result_dict))

        # 添加执行成功的用例
        if testScript['testcase_caseName'] not in testcase_result and testScript['script_testResult'] in ['成功'] and len(
                testScript['script_testResult']) > 0:
            testcase_result.append(testScript['testcase_caseName'])
            testcase_result_dict['caseName'] = testScript['testcase_caseName']
            testcase_result_dict['result'].append(testScript['script_testResult'])
            result['testCase_list'].append(copy.deepcopy(testcase_result_dict))

        # 已经存在且成功的用例为跳过
        if testScript['testcase_caseName'] in testcase_result and testScript['script_testResult'] in ['成功'] and len(
                testScript['script_testResult']) > 0:
            pass

        # 已经存在但是结果为失败的用例，重新赋值
        if testScript['testcase_caseName'] in testcase_result and testScript['script_testResult'] in ['失败'] and len(
                testScript['script_testResult']) > 0:
            for script in result['testCase_list']:
                if script['caseName'] == testScript['testcase_caseName']:
                    script['result'] = testScript['script_testResult']
        time_list.append(testScript['executing_starttime'])

    for testCase in result['testCase_list']:
        if '成功' in testCase['result']:
            success += 1
        else:
            fail += 1

    result['testScrpit_list'] = reportValue
    print('caseLIst===', result['testCase_list'])
    result['modelVersion'] = reportValue[0]['modeldata_name']
    if success + fail == 0:
        result['testResult'] = "未添加断言"
    else:
        if (success / (success + fail)) != 1:
            result['testResult'] = "失败"
        else:
            result['testResult'] = "成功"
        result['totalTime'] = round(((((max(time_list) - min(time_list))).seconds) / 60), 2)
        result['scriptRate']['successRate'] = round((success / (success + fail)), 2)
        result['scriptRate']['failRate'] = round((fail / (success + fail)), 2)
        result['summary']['total'] = success + fail
        result['summary']['success'] = success
        result['summary']['fail'] = fail
        result['summary']['successRate'] = ("%.2f%%" % ((success / (success + fail)) * 100))
        result['summary']['failRate'] = ("%.2f%%" % ((fail / (success + fail)) * 100))
        result['reportDate'] = reportValue[-1]['executing_endtime']
    # result['summary']=list(result['summary'])

    data = {
        'code': 200,
        'msg': result
    }
    return JsonResponse(data, safe=False)


# 删除Script用例
@loginRequired
@msgMessage
def delScriptCase(request):
    '''删除Script用例'''
    script_id = request.POST.get('script_id')
    _script = Testscript.objects.get(script_id=script_id)
    _script.delete()
    data = {
        "code": 200,
        "msg": "Script删除成功"
    }
    return JsonResponse(data, safe=False)


# 复制测试用例
def copyTestUITestCase(request):
    '''
    保存测试用例
    :param request:
    :return:
    '''
    caseName = request.POST.get("testcase_caseName")
    casePrecondition = request.POST.get("testcase_casePrecondition")
    caseSteps = request.POST.get("testcase_caseSteps")
    caseExpected = request.POST.get("testcase_caseExpected")
    caseType = request.POST.get("testcase_caseType")
    caseLeve = request.POST.get("testcase_caseLeve")
    caseVersion = request.POST.get("testcase_caseVersion")
    # casePositioning = request.POST.get("testcase_caseVersion")

    _testcase = Testcase()
    _testcase.testcase_caseName = caseName
    _testcase.testcase_casePrecondition = casePrecondition
    _testcase.testcase_caseSteps = caseSteps
    _testcase.testcase_caseVersion = caseVersion
    _testcase.testcase_caseExpected = caseExpected
    _testcase.testcase_caseType = caseType
    _testcase.testcase_caseLeve = caseLeve
    _testcase.save()

    data = {
        "code": 200,
        "msg": "复制用例成功"
    }
    return JsonResponse(data)


# 批量复制脚本到用例下
def batchCopyScript(request):
    '''
    将脚本批量复制到用例下
    :param request:
    :return:
    '''
    script_testDataName = request.POST.get('script_testDataName')
    script_testDataPositioning = request.POST.get('testDataPositioning')
    script_testDataKeyWord = request.POST.get('script_testDataKeyWord')
    script_testDataPremise = request.POST.get('script_testDataPremise')
    script_testDataElement = request.POST.get('script_testDataElement')
    script_testDataParameter = request.POST.get('script_testDataParameter')
    script_testDataAssert = request.POST.get('script_testDataAssert')
    script_testDataProject = request.POST.get('script_testDataProject')
    script_testDataVersion = request.POST.get('script_testDataVersion')
    script_TestDataCase = request.POST.get('script_TestDataCase')
    caseIDList = request.POST.get('caseIDList')
    print('caseIDList', caseIDList)
    data = {
        'code': 200,
        'msg': '保存脚本成功'
    }
    return JsonResponse(data)

def addScript(request):
    '''新增空白Script'''
    script_testDataVersion=request.POST.get("testcase_caseVersion")
    script_TestDataCase=request.POST.get("testcase_id")
    _script = Testscript()
    _script.script_testDataVersion = script_testDataVersion
    _script.script_TestDataCase = script_TestDataCase
    _script.save()
    data = {
        "code": 200,
        "msg": "新增脚本成功"
    }
    return JsonResponse(data)
# 复制用例脚本
def copyTestUiScript(request):
    print(request)
    script_testDataName = request.POST.get('script_testDataName')
    script_testDataPositioning = request.POST.get('script_testDataPositioning')
    script_testDataKeyWord = request.POST.get('script_testDataKeyWord')
    script_testDataPremise = request.POST.get('script_testDataPremise')
    script_testDataElement = request.POST.get('script_testDataElement')
    script_testDataParameter = request.POST.get('script_testDataParameter')
    script_testDataAssert = request.POST.get('script_testDataAssert')
    script_testDataProject = request.POST.get('script_testDataProject')
    script_testDataVersion = request.POST.get('script_testDataVersion')
    script_TestDataCase = request.POST.get('script_TestDataCase')
    # script_testResult = request.POST.get('script_testResult')

    _script = Testscript()
    _script.script_testDataName = script_testDataName
    _script.script_testDataPositioning = script_testDataPositioning
    _script.script_testDataKeyWord = script_testDataKeyWord
    _script.script_testDataPremise = script_testDataPremise
    _script.script_testDataElement = script_testDataElement
    _script.script_testDataParameter = script_testDataParameter
    _script.script_testDataAssert = script_testDataAssert
    _script.script_testDataProject = script_testDataProject
    _script.script_testDataVersion = script_testDataVersion
    _script.script_TestDataCase = script_TestDataCase
    _script.save()
    data = {
        "code": 200,
        "msg": "复制脚本成功"
    }
    return JsonResponse(data)


# 删除测试用例
@loginRequired
@msgMessage
def delUITestCase(request):
    '''删除UI用例'''
    testcase_id = request.POST.get('testcase_id')
    _testcase = Testcase.objects.get(testcase_id=testcase_id)
    _testcase.delete()
    data = {
        "code": 200,
        "msg": "用例删除成功"
    }
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def saveTestScript(request):
    '''保存脚本'''
    # print('获取到的脚本是',request.POST)
    script_id = request.POST.get('testDataId')
    print('获取的是testDataid', script_id)
    script_testDataName = request.POST.get('testDataName')
    assertList = ['assertElement', 'assertValueElement', 'assertElementIsDisplay', 'assertElementIsSelect']
    script_testDataPositioning = request.POST.get('testDataPositioning')
    script_testDataKeyWord = request.POST.get('testDataKeyWord')
    script_testDataPremise = request.POST.get('testDataPremise')
    script_testDataElement = request.POST.get('testDataElement')
    script_testDataParameter = request.POST.get('testDataParameter')
    script_testDataAssert = request.POST.get('testDataAssert')
    script_testDataProject = request.POST.get('testDataProject')
    script_testDataVersion = request.POST.get('testDataVersion')
    script_TestDataCase = request.POST.get('TestDataCase')
    script_testResult = request.POST.get('testResult')
    _script = Testscript()
    if script_id:
        if script_testDataKeyWord not in assertList:
            _script.script_id = script_id
            _script.script_testDataName = script_testDataName
            _script.script_testDataPositioning = script_testDataPositioning
            _script.script_testDataKeyWord = script_testDataKeyWord
            _script.script_testDataPremise = script_testDataPremise
            _script.script_testDataElement = script_testDataElement
            _script.script_testDataParameter = script_testDataParameter
            _script.script_testDataAssert = script_testDataAssert
            _script.script_testDataProject = script_testDataProject
            _script.script_testDataVersion = script_testDataVersion
            _script.script_TestDataCase = script_TestDataCase
            _script.script_testResult = ''
            _script.save()
            data = {
                "code": 200,
                "msg": "脚本用例编辑成功"
            }
        else:
            _script.script_id = script_id
            _script.script_testDataName = script_testDataName
            _script.script_testDataPositioning = script_testDataPositioning
            _script.script_testDataKeyWord = script_testDataKeyWord
            _script.script_testDataPremise = script_testDataPremise
            _script.script_testDataElement = script_testDataElement
            _script.script_testDataParameter = script_testDataParameter
            _script.script_testDataAssert = script_testDataAssert
            _script.script_testDataProject = script_testDataProject
            _script.script_testDataVersion = script_testDataVersion
            _script.script_TestDataCase = script_TestDataCase
            _script.script_testResult = script_testResult
            _script.save()
            data = {
                "code": 200,
                "msg": "脚本用例编辑成功"
            }
    else:
        _script.script_testDataName = script_testDataName
        _script.script_testDataPositioning = script_testDataPositioning
        _script.script_testDataKeyWord = script_testDataKeyWord
        _script.script_testDataPremise = script_testDataPremise
        _script.script_testDataElement = script_testDataElement
        _script.script_testDataParameter = script_testDataParameter
        _script.script_testDataAssert = script_testDataAssert
        _script.script_testDataProject = script_testDataProject
        _script.script_testDataVersion = script_testDataVersion
        _script.script_TestDataCase = script_TestDataCase
        _script.save()
        data = {
            "code": 200,
            "msg": "脚本用例保存成功"
        }
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def saveKeyWord(request):
    '''保存关键字'''
    print('查询的关键字', request.POST)
    key_id = request.POST.get('key_id')
    key_name = request.POST.get('keyData')
    _key = Keyword()
    if key_id:
        _key.key_id = key_id
        _key.key_name = key_name
        _key.save()
        data = {
            "code": 200,
            "msg": "关键字编辑成功"
        }
    else:
        _key.key_name = key_name
        _key.save()
        data = {
            "code": 200,
            "msg": "关键字保存成功"
        }
    return JsonResponse(data, safe=False)


@loginRequired
@msgMessage
def selectUiTestCase(request):
    '''查询测试用例'''
    # print('查询的测试用例',request.POST)
    modelData = request.POST.get("modelData")
    sql = 'select * from quality_testcase a,quality_modelversion b where a.testcase_caseVersion=b.Modelversion_id and b.modeldata_name=' + "\'" + modelData + "\'"
    sqlTestCase = 'select * from quality_testscript'
    data = commonList().getModelData(sql)
    data2 = commonList().getModelData(sqlTestCase)
    dataList = []
    for i in data:
        i["testcaseList"] = []
        for j in data2:
            if str(i["testcase_id"]) == j["script_TestDataCase"]:
                i["testcaseList"].append(j)
            else:
                pass
        dataList.append(i)
    # print("获取用例",dataList)
    return JsonResponse(dataList, safe=False)


@loginRequired
@msgMessage
def saveTestCase(request):
    '''保存测试用例'''
    # print('保存的测试用例',request.POST)
    testId = request.POST.get("id")
    caseName = request.POST.get("caseName")
    casePrecondition = request.POST.get("casePrecondition")
    caseSteps = request.POST.get("caseSteps")
    caseExpected = request.POST.get("caseExpected")
    caseType = request.POST.get("caseType")
    caseLeve = request.POST.get("caseLeve")
    caseVersion = request.POST.get("caseVersion")
    print('caseLeve', caseLeve)
    if testId:
        _testcase = Testcase()
        _testcase.testcase_id = testId
        _testcase.testcase_caseName = caseName
        _testcase.testcase_casePrecondition = casePrecondition
        _testcase.testcase_caseSteps = caseSteps
        _testcase.testcase_caseVersion = caseVersion
        _testcase.testcase_caseExpected = caseExpected
        _testcase.testcase_caseType = caseType
        _testcase.testcase_caseLeve = caseLeve
        _testcase.save()
        data = {
            "code": 200,
            "msg": "保存编辑成功"
        }
    else:
        _testcase = Testcase()
        _testcase.testcase_caseName = caseName
        _testcase.testcase_casePrecondition = casePrecondition
        _testcase.testcase_caseSteps = caseSteps
        _testcase.testcase_caseVersion = caseVersion
        _testcase.testcase_caseExpected = caseExpected
        _testcase.testcase_caseType = caseType
        _testcase.testcase_caseLeve = caseLeve
        _testcase.save()
        data = {
            "code": 200,
            "msg": "保存用例成功"
        }
    return JsonResponse(data, safe=False)


# 查询邮件配置
@loginRequired
@msgMessage
def selectEmailConfig(request):
    sql = 'select * from quality_testemail a,quality_modelversion b WHERE a.email_emailTeam=b.Modelversion_id'
    data = commonList().getModelData(sql)
    return JsonResponse(data, safe=False)


# 保存邮件配置
@loginRequired
@msgMessage
def saveEmailConfig(request):
    '''邮件配置'''
    print(request.POST)
    email_id = request.POST.get("emailId")
    emailTeam = request.POST.get("emailTeam")
    serverAddress = request.POST.get("serverAddress")
    account = request.POST.get("account")
    password = request.POST.get("password")
    fromAddr = request.POST.get("fromAddr")
    toAddr = request.POST.get("toAddr")
    emailAction = request.POST.get('action')

    if emailAction == 'add':
        _testEmail = Testemail()
        _testEmail.email_emailTeam = emailTeam
        _testEmail.email_serverAddress = serverAddress
        _testEmail.email_account = account
        _testEmail.email_password = password
        _testEmail.email_fromAddr = fromAddr
        _testEmail.email_toAddr = toAddr
        _testEmail.save()
        data = {
            'code': 0,
            "msg": "邮件配置新增成功"
        }
    elif emailAction == 'edit':
        _testEmail = Testemail()
        _testEmail.email_id = email_id
        _testEmail.email_emailTeam = emailTeam
        _testEmail.email_serverAddress = serverAddress
        _testEmail.email_account = account
        _testEmail.email_password = password
        _testEmail.email_fromAddr = fromAddr
        _testEmail.email_toAddr = toAddr
        _testEmail.save()
        data = {
            "code": 0,
            "msg": "邮件配置修改成功"
        }
    else:
        delete_email_id = request.POST.get("emailId")
        print('delete_email_id', delete_email_id)
        _testEmail = Testemail.objects.get(email_id=delete_email_id)
        _testEmail.delete()
        data = {
            "code": 0,
            "msg": "邮件配置删除成功"
        }
    return JsonResponse(data, safe=False)


#
# 保存用例排序
def saveTestCaseSort(request):
    print("保存用例排序", (request.POST))
    newIndex=request.POST.get('newIndex')
    oldIndex=request.POST.get('oldIndex')
    modalData=request.POST.get('modelData')

    # 查找用例ID列表
    testCaseIDList=[]
    ID_Sql='select a.testcase_id from quality_testcase a,quality_modelversion b where a.testcase_caseVersion=b.Modelversion_id and b.modeldata_name=' + "\'" + modalData + "\'"
    sql = 'select * from quality_testcase a,quality_modelversion b where a.testcase_caseVersion=b.Modelversion_id and b.modeldata_name=' + "\'" + modalData + "\'"
    sqlTestCase = 'select * from quality_testscript'

    # 获取用例列表ID
    data_ID=commonList().getModelData(ID_Sql)
    data_ID_List=[ i['testcase_id'] for i in data_ID]
    print('data_ID_List',data_ID_List)
    print('data_ID',data_ID)
    # newIndex,获取开始用例ID
    new_Index=data_ID_List.index(int(newIndex))

    # oldIndex,获取结束用例ID
    old_Index=data_ID_List.index(int(oldIndex))

    data = commonList().getModelData(sql)
    data2 = commonList().getModelData(sqlTestCase)
    dataList = []

    # 获取用例和脚本列表
    for i in data:
        i["testcaseList"] = []
        for j in data2:
            if str(i["testcase_id"]) == j["script_TestDataCase"]:
                i["testcaseList"].append(j)
            else:
                pass
        dataList.append(i)
    old_Index_Pop=dataList.pop(old_Index)
    print('old_Index_Pop',old_Index_Pop)

    # 插入元素
    dataList.insert(new_Index,old_Index_Pop)
    # 替换用例ID保存数据
    for sourceID ,newID in zip(data_ID_List,dataList):
        newID['testcase_id']=sourceID
        # newID['testcaseList']=[i['script_TestDataCase']==str(sourceID) for i in newID]
        _newIndexList = Testcase.objects.get(testcase_id=int(sourceID))
        _newIndexList.testcase_caseName = newID['testcase_caseName']
        _newIndexList.testcase_casePrecondition = newID['testcase_casePrecondition']
        _newIndexList.testcase_caseSteps = newID['testcase_caseSteps']
        _newIndexList.testcase_caseExpected = newID['testcase_caseExpected']
        _newIndexList.testcase_caseType = newID['testcase_caseType']
        _newIndexList.testcase_caseLeve = newID['testcase_caseLeve']
        _newIndexList.testcase_caseVersion = newID['testcase_caseVersion']
        _newIndexList.save()
        for sortId in newID['testcaseList']:
            _newScriptList=Testscript.objects.get(script_id=sortId['script_id'])
            _newScriptList.script_testDataName=sortId['script_testDataName']
            _newScriptList.script_testDataPositioning = sortId['script_testDataPositioning']
            _newScriptList.script_testDataKeyWord = sortId['script_testDataKeyWord']
            _newScriptList.script_testDataPremise = sortId['script_testDataPremise']
            _newScriptList.script_testDataElement = sortId['script_testDataElement']
            _newScriptList.script_testDataParameter = sortId['script_testDataParameter']
            _newScriptList.script_testDataAssert = sortId['script_testDataAssert']
            _newScriptList.script_testDataProject = sortId['script_testDataProject']
            _newScriptList.script_testDataVersion = sortId['script_testDataVersion']
            _newScriptList.script_TestDataCase = str(sourceID)
            _newScriptList.script_testResult = sortId['script_testResult']
            _newScriptList.save()

    # for i in request.POST:
    #     caseNameList = json.loads(i)
    #     newIndex = caseNameList["newIndex"]
    #     oldIndex = caseNameList["oldIndex"]
    #     newScript = tuple(caseNameList['newScriptList'])
    #     oldScript = tuple(caseNameList['oldScriptIdList'])
    #     if len(newScript) == 1:
    #         newScript = '(' + str(newScript[0]) + ')'
    #         print('newScript', newScript)
    #
    #     if len(oldScript) == 1:
    #         oldScript = '(' + str(oldScript[0]) + ')'
    #         print('oldScript', oldScript)
    #
    # _newIndexList = Testcase.objects.get(testcase_id=int(newIndex))
    # _oldIndexList = Testcase.objects.get(testcase_id=int(oldIndex))

    # 查询ScriptId
    # script_id_list='SELECT a.script_id,(b.script_id) FROM quality_testscript a,quality_testscript b WHERE'+' '\
    #     'a.script_TestDataCase='+newIndex+' AND b.script_TestDataCase='+oldIndex+''\

    # scriptList=commonList().getModelData(script_id_list)
    # print('获取到的scriptID',scriptList)
    # 更新用例脚本
    # newIndex_sql = 'UPDATE quality_testscript AS a JOIN quality_testscript AS b ON (a.script_id in  ' + str(
    #     newScript) + ' AND b.script_id in ' + str(oldScript) + ') OR (a.script_id in ' + str(
    #     oldScript) + ' AND b.script_id in ' + str(
    #     newScript) + ') SET a.script_TestDataCase = b.script_TestDataCase,b.script_TestDataCase = a.script_TestDataCase'
    #
    # commonList().getModelData(newIndex_sql)
    # print('newIndex_sql', newIndex_sql)
    #
    # _copynewIndexList = copy.deepcopy(_newIndexList)
    # _copyoldIndexList = copy.deepcopy(_oldIndexList)
    #
    # _copynewIndexList.testcase_caseName = _oldIndexList.testcase_caseName
    # _copynewIndexList.testcase_casePrecondition = _oldIndexList.testcase_casePrecondition
    # _copynewIndexList.testcase_caseSteps = _oldIndexList.testcase_caseSteps
    # _copynewIndexList.testcase_caseExpected = _oldIndexList.testcase_caseExpected
    # _copynewIndexList.testcase_caseType = _oldIndexList.testcase_caseType
    # _copynewIndexList.testcase_caseLeve = _oldIndexList.testcase_caseLeve
    # _copynewIndexList.testcase_caseVersion = _oldIndexList.testcase_caseVersion
    #
    # _copyoldIndexList.testcase_caseName = _newIndexList.testcase_caseName
    # _copyoldIndexList.testcase_casePrecondition = _newIndexList.testcase_casePrecondition
    # _copyoldIndexList.testcase_caseSteps = _newIndexList.testcase_caseSteps
    # _copyoldIndexList.testcase_caseExpected = _newIndexList.testcase_caseExpected
    # _copyoldIndexList.testcase_caseType = _newIndexList.testcase_caseType
    # _copyoldIndexList.testcase_caseLeve = _newIndexList.testcase_caseLeve
    # _copyoldIndexList.testcase_caseVersion = _newIndexList.testcase_caseVersion
    #
    # _copynewIndexList.save()
    # _copyoldIndexList.save()

    data = {
        "code": 0,
        "msg": "排序保存成功"
    }
    return JsonResponse(data, safe=False)


# 保存testScript排序
def saveCaseData(request):
    print("用例排序", request.POST)
    newID = request.POST.get("newID")
    currentID = request.POST.get("currentID")

    _newCaseList = Testscript.objects.get(script_id=int(newID))
    _currentCaseList = Testscript.objects.get(script_id=int(currentID))

    _copynewCaseList = copy.deepcopy(_newCaseList)
    _copycurrentCaseList = copy.deepcopy(_currentCaseList)

    # _copynewCaseList.script_id=_currentCaseList.script_id
    _copynewCaseList.script_testDataName = _currentCaseList.script_testDataName
    _copynewCaseList.script_testDataPositioning = _currentCaseList.script_testDataPositioning
    _copynewCaseList.script_testDataKeyWord = _currentCaseList.script_testDataKeyWord
    _copynewCaseList.script_testDataPremise = _currentCaseList.script_testDataPremise
    _copynewCaseList.script_testDataElement = _currentCaseList.script_testDataElement
    _copynewCaseList.script_testDataParameter = _currentCaseList.script_testDataParameter
    _copynewCaseList.script_testDataAssert = _currentCaseList.script_testDataAssert
    _copynewCaseList.script_testDataProject = _currentCaseList.script_testDataProject
    _copynewCaseList.script_testDataVersion = _currentCaseList.script_testDataVersion
    _copynewCaseList.script_TestDataCase = _currentCaseList.script_TestDataCase
    _copynewCaseList.script_testResult=''

    # _copycurrentCaseList.script_id=_newCaseList.script_id
    _copycurrentCaseList.script_testDataName = _newCaseList.script_testDataName
    _copycurrentCaseList.script_testDataPositioning = _newCaseList.script_testDataPositioning
    _copycurrentCaseList.script_testDataKeyWord = _newCaseList.script_testDataKeyWord
    _copycurrentCaseList.script_testDataPremise = _newCaseList.script_testDataPremise
    _copycurrentCaseList.script_testDataElement = _newCaseList.script_testDataElement
    _copycurrentCaseList.script_testDataAssert = _newCaseList.script_testDataAssert
    _copycurrentCaseList.script_testDataParameter = _newCaseList.script_testDataParameter
    _copycurrentCaseList.script_testDataProject = _newCaseList.script_testDataProject
    _copycurrentCaseList.script_testDataVersion = _newCaseList.script_testDataVersion
    _copycurrentCaseList.script_TestDataCase = _newCaseList.script_TestDataCase
    _copycurrentCaseList.script_testResult=''

    _copynewCaseList.save()
    _copycurrentCaseList.save()

    data = {
        "code": 0,
        "msg": "排序保存成功"
    }
    return JsonResponse(data, safe=False)






