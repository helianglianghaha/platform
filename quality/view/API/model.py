from django.db import models
from django.utils import timezone


#接口管理
# class Api(models.Model):
#     api_id = models.AutoField(verbose_name="接口管理ID", primary_key=True)
#     version_id=models.ForeignKey('Version',  on_delete=models.CASCADE)
#     api_host=models.CharField(max_length=100, verbose_name="域名")
#     api_name = models.CharField(max_length=500, verbose_name="API名称")
#     api_method = models.CharField(max_length=50, verbose_name="请求方法")
#     api_url = models.CharField(max_length=100, verbose_name="请求URL")
#     api_request = models.CharField(max_length=100, verbose_name="请求路径")
#     api_response = models.CharField(max_length=1000, verbose_name="返回值")
#API用例
# class Testcase(models.Model):
#     test_id=models.AutoField(verbose_name="用例ID", primary_key=True)
#     api_id=models.ForeignKey('Api',  on_delete=models.CASCADE)
#     test_host=models.CharField(max_length=100, verbose_name="域名")
#     test_name = models.CharField(max_length=500, verbose_name="API名称")
#     test_method = models.CharField(max_length=50, verbose_name="请求方法")
#     test_url = models.CharField(max_length=100, verbose_name="请求URL")
#     test_assert = models.CharField(max_length=100, verbose_name="断言")
#     test_request = models.CharField(max_length=100, verbose_name="请求参数")
#     test_exresponse = models.CharField(max_length=1000, verbose_name="预期结果")
#     test_acesponse= models.CharField(max_length=1000, verbose_name="实际结果")
#     test_results=models.IntegerField(default=0,verbose_name="执行结果")

#web测试用例
# class Webtestcase(models.Model):
    # webtestcase_id=models.AutoField(verbose_name="web用例ID", primary_key=True)
    # modeldata_id=models.ForeignKey('Modeldata',  on_delete=models.CASCADE)
    # webtestcase_name=models.CharField(max_length=500, verbose_name="用例名称")
    # webtestcase_request=models.CharField(max_length=100, verbose_name="前置条件")
    # webtestcase_steps=models.CharField(max_length=1000, verbose_name="操作步骤")
    # webtestcase_exresponse=models.CharField(max_length=1000, verbose_name="预期结果")
    # webtestcase_acesponse=models.CharField(max_length=1000, verbose_name="实际结果")
    # webtestcase_assert=models.CharField(max_length=100, verbose_name="断言")
    # webtestcase_result=models.IntegerField(default=0,verbose_name="执行结果")
#测试脚本
# class Script(models.Model):
#     script_id=models.AutoField(verbose_name="脚本ID", primary_key=True)
#     webtestcase_id=models.ForeignKey('Webtestcase',  on_delete=models.CASCADE)
#     script_name=models.CharField(max_length=50, verbose_name="名称")
#     script_method=models.CharField(max_length=50, verbose_name="元素定位方法")
#     script_element=models.CharField(max_length=500, verbose_name="元素")
#     script_action=models.CharField(max_length=500, verbose_name="动作")
#     script_data=models.CharField(max_length=500, verbose_name="请求参数")
#     script_assert=models.CharField(max_length=100, verbose_name="断言")
#     script_timeout=models.CharField(max_length=100, verbose_name="超时")
#     script_keyword=models.CharField(max_length=100, verbose_name="关键字")
#模块信息
class Modeldata(models.Model):
    modeldata_id=models.AutoField(verbose_name="模块ID", primary_key=True)
    modelData=models.CharField(max_length=50, verbose_name="模块名称")
    subModelData=models.IntegerField(verbose_name="所属模块")
    modelData_pripeople=models.CharField(max_length=50, verbose_name="负责人")
    modelData_testenvironment=models.CharField(max_length=50, verbose_name="测试环境")
    modelData_proenvironment=models.CharField(max_length=50, verbose_name="生产环境")

#模块-版本信息
class Modelversion(models.Model):
    Modelversion_id=models.AutoField(verbose_name="版本ID", primary_key=True)
    modeldata_name=models.CharField(max_length=50, verbose_name="版本名称")
    modeldata_id=models.ForeignKey('Modeldata',  on_delete=models.CASCADE)
#代理地址
class Proaddress(models.Model):
    proxyid=models.AutoField(verbose_name="代理地址ID", primary_key=True)
    Modelversion_id = models.ForeignKey('Modelversion', on_delete=models.CASCADE)
    pro_address=models.CharField(max_length=1000, verbose_name="版本名称")
    pro_openXunjian=models.CharField(max_length=50, verbose_name="开启巡检")
    pro_qixin = models.CharField(max_length=50, verbose_name="企信群")
    pro_openQiXin = models.CharField(max_length=50, verbose_name="是否开启通知")

#接口脚本
class Scriptproject(models.Model):
    sceiptProject_id=models.AutoField(verbose_name="接口脚本id", primary_key=True)
    projectName=models.CharField(max_length=50, verbose_name="项目名称")
    versionName = models.CharField(max_length=50, verbose_name="版本名称-废弃")
    platfromName = models.CharField(max_length=100, verbose_name="版本名称")
    buildAddress = models.CharField(max_length=100, verbose_name="build文件地址")
    reportAddress = models.CharField(max_length=100, verbose_name="报告地址")
    scriptName = models.CharField(max_length=1000, verbose_name="脚本文件地址")
    executeType=models.CharField(max_length=50, verbose_name="执行类型")
    performanceData=models.CharField(max_length=1000, verbose_name="性能测试命令")
    performanceReport=models.CharField(max_length=100, verbose_name="性能测试报告")

    UIdata=models.CharField(max_length=1000, verbose_name="UI测试命令")
    UIExcReport=models.CharField(max_length=1000, verbose_name="UI测试报告生成命令")
    UIReport=models.CharField(max_length=1000, verbose_name="UI测试报告地址")
    UIScript=models.CharField(max_length=1000, verbose_name="UI测试脚本地址")

    creater=models.CharField(max_length=100, verbose_name="创建人")
    environment = models.CharField(max_length=10, verbose_name="执行环境")
    status=models.CharField(max_length=100, verbose_name="项目状态")
    owner=models.CharField(max_length=50, verbose_name="负责人")
    updater=models.CharField(max_length=50, verbose_name="更新人")
    remark=models.CharField(max_length=200, verbose_name="备注")
    status=models.CharField(max_length=100, verbose_name="项目状态")
    runstatus = models.CharField(max_length=100, verbose_name="运行状态")
    platfromType=models.CharField(max_length=50, verbose_name="执行端")
    createtime=models.DateTimeField()
    modifytime=models.DateTimeField()

#新增版本管理
class Versionmanager(models.Model):
    autoTableID=models.AutoField(verbose_name="版本管理ID", primary_key=True)
    tableID=models.CharField(max_length=50, verbose_name="新增表ID")
    version=models.CharField(max_length=50, verbose_name="项目名称")
    description = models.CharField(max_length=50, verbose_name="需求描述")
    priority = models.CharField(max_length=50, verbose_name="优先级")
    owner = models.CharField(max_length=50, verbose_name="负责人")
    development = models.CharField(max_length=50, verbose_name="开发者")
    product = models.CharField(max_length=50, verbose_name="产品")
    status = models.CharField(max_length=50, verbose_name="需求状态")
    testCases = models.CharField(max_length=50, verbose_name="编写测试用例进度")
    testCaseReview = models.CharField(max_length=50, verbose_name="测试用例评审进度")
    firstRoundTest = models.CharField(max_length=50, verbose_name="一轮测试进度")
    secondRoundTest = models.CharField(max_length=50, verbose_name="二轮测试进度")
    thirdRoundTest = models.CharField(max_length=50, verbose_name="三轮测试进度")
    testingTime = models.CharField(max_length=50, verbose_name="上线时间")
    liveTime = models.CharField(max_length=50, verbose_name="上线时间")
    remarks = models.CharField(max_length=50, verbose_name="备注")
    yueLinProgress = models.CharField(max_length=50, verbose_name="悦邻严选上线进度")
    yueLinRemarks = models.CharField(max_length=50, verbose_name="备注")
    juHaoMaiProgress = models.CharField(max_length=50, verbose_name="聚好麦上线进度")
    juHaoMaiRemarks = models.CharField(max_length=50, verbose_name="备注")
    editable = models.BooleanField(max_length=50, verbose_name="项目名称")
    tableName=models.CharField(max_length=50, verbose_name="周计划名称")
    onlinModel=models.CharField(max_length=50, verbose_name="上线平台")
    modelStatus=models.CharField(max_length=50, verbose_name="平台上线状态")
    platfromType=models.CharField(max_length=50, verbose_name="执行端")

#新增任务信息管理
class taskmanager(models.Model):
    id=models.AutoField(verbose_name="任务管理ID", primary_key=True)
    taskName=models.CharField(max_length=50, verbose_name="任务名称")
    status=models.CharField(max_length=50, verbose_name="任务状态")
    owner=models.CharField(max_length=50, verbose_name="任务负责人")
    remark=models.CharField(max_length=50, verbose_name="备注")
    beginTime=models.DateTimeField()
    endTime=models.DateTimeField()
    updateTime=models.DateTimeField()
    createTime=models.DateTimeField()


#新增待办任务
class todutasklist(models.Model):
    id=models.AutoField(verbose_name="任务管理ID", primary_key=True)
    toDoTaskName=models.CharField(max_length=255, verbose_name="待办任务名称")
    status=models.CharField(max_length=50, verbose_name="任务状态")
    createTime=models.DateTimeField()
    updateTime=models.DateTimeField()
    ownerAccount=models.CharField(max_length=255, verbose_name="账户")
    ownerName=models.CharField(max_length=255, verbose_name="负责人")
    taskType=models.CharField(max_length=255, verbose_name="任务类型")
    description=models.CharField(max_length=255, verbose_name="任务描述")
