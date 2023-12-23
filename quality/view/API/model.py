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
    versionName = models.CharField(max_length=50, verbose_name="版本名称")
    buildAddress = models.CharField(max_length=100, verbose_name="build文件地址")
    reportAddress = models.CharField(max_length=100, verbose_name="报告地址")
    scriptName = models.CharField(max_length=1000, verbose_name="脚本文件地址")
    executeType=models.BooleanField(verbose_name="切换性能和接口数据类型", default=False, blank=True)
    performanceData=models.CharField(max_length=1000, verbose_name="性能测试命令")
    performanceReport=models.CharField(max_length=100, verbose_name="性能测试报告")
    creater=models.CharField(max_length=100, verbose_name="创建人")
    status=models.CharField(max_length=100, verbose_name="项目状态")
    runstatus = models.CharField(max_length=100, verbose_name="运行状态")
    createtime=models.DateTimeField()
    modifytime=models.DateTimeField()