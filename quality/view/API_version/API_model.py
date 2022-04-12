from django.db import models
from django.utils import timezone
import django.utils.timezone as timezone


#接口管理
class Testcase(models.Model):
    testcase_id=models.AutoField(verbose_name="测试用例ID", primary_key=True)
    testcase_caseName=models.CharField(max_length=100, verbose_name="测试用例名称",default=None)
    testcase_casePrecondition=models.CharField(max_length=100, verbose_name="前置条件",default=None)
    testcase_caseSteps=models.CharField(max_length=500, verbose_name="操作步骤",default=None)
    testcase_caseExpected=models.CharField(max_length=500, verbose_name="预期结果",default=None)
    testcase_caseType=models.CharField(max_length=10, verbose_name="用例类型",default=None)
    testcase_caseLeve=models.CharField(max_length=10, verbose_name="用例等级",default=None)
    testcase_caseVersion=models.CharField(max_length=50, verbose_name="所属版本",default=None)
class Testapi(models.Model):
    testapi_id=models.AutoField(verbose_name="接口ID", primary_key=True)
    testmodelData=models.IntegerField(verbose_name="所属项目")
    Modelversion_id=models.ForeignKey('Modelversion',  on_delete=models.CASCADE)
    testapiHost=models.CharField(max_length=100, verbose_name="域名")
    testapiname = models.CharField(max_length=500, verbose_name="API名称")
    testapiMethod = models.CharField(max_length=50, verbose_name="请求方法")
    testapiUrl = models.CharField(max_length=1000, verbose_name="请求URL")
    testapiBody = models.CharField(max_length=1000, verbose_name="请求参数")
    testaddCookiesValue=models.CharField(max_length=50, verbose_name="添加cookies")
    testapiExtractName= models.CharField(max_length=50, verbose_name="正则名称") 
    testapiExtractExpression=models.CharField(max_length=100, verbose_name="正则表达式")
    testapiExtractResponse=models.CharField(max_length=1000, verbose_name="提取响应值")

    testapiAssert = models.CharField(max_length=1000, verbose_name="断言")
    testapiResponse = models.CharField(max_length=1000, verbose_name="响应值")
    testcookiesValue =models.CharField(max_length=50,verbose_name="是否添加cookies")
    testapiRequest=models.CharField(max_length=50,verbose_name="请求协议")
    testaddPassWordFree =models.CharField(max_length=50,verbose_name="添加免密配置")
    testpassWordFree =models.CharField(max_length=50,verbose_name="免密配置")
    teststatuscode=models.CharField(max_length=10,verbose_name="请求状态码")
    testencoding=models.CharField(max_length=10,verbose_name="编码方式")
    testheader=models.CharField(max_length=1000,verbose_name="请求头")
    testresult=models.IntegerField(default=0,verbose_name="测试结果")
    testurl=models.CharField(max_length=500,verbose_name="测试url")

#执行日志
class Executinglog(models.Model):
    executing_id=models.AutoField(verbose_name="日志ID", primary_key=True)
    executing_name=models.CharField(max_length=100, verbose_name="执行名称")
    executing_testmd=models.CharField(max_length=50,verbose_name="接口用例")
    executing_testscript_id=models.IntegerField(verbose_name="接口脚本")
    executing_testapi_id = models.IntegerField(verbose_name="API用例")
    executing_testui_id = models.IntegerField(verbose_name="UI用例")
    executing_starttime=models.DateTimeField('保存日期',auto_now_add=True)
    executing_endtime=models.DateTimeField('最后修改日期',auto_now=True)
    executing_userName = models.CharField(max_length=50, verbose_name="执行人")
    executing_versionName = models.CharField(max_length=50, verbose_name="版本信息")


#关键字
class Keyword(models.Model):
    key_id=models.AutoField(verbose_name="关键字ID", primary_key=True)
    key_name=models.CharField(max_length=100, verbose_name="关键字名称")
#UI脚本配置
class Testscript(models.Model):
    script_id=models.AutoField(verbose_name="脚本ID", primary_key=True)
    script_testDataName=models.CharField(max_length=100, verbose_name="脚本名称")
    script_testDataPositioning=models.CharField(max_length=50, verbose_name="定位方法")
    script_testDataKeyWord=models.CharField(max_length=50, verbose_name="关键字")
    script_testDataPremise=models.CharField(max_length=1000, verbose_name="前置条件")
    script_testDataElement=models.CharField(max_length=1000, verbose_name="元素信息")
    script_testDataParameter=models.CharField(max_length=1000, verbose_name="参数信息")
    script_testDataAssert=models.CharField(max_length=1000, verbose_name="断言信息")
    script_testDataProject=models.CharField(max_length=50, verbose_name="项目")
    script_testDataVersion=models.CharField(max_length=50, verbose_name="版本")
    script_TestDataCase=models.CharField(max_length=50, verbose_name="用例")
    script_testResult=models.CharField(max_length=50,verbose_name="测试结果")
#保存图片
class Testpicture(models.Model):
    picture_id=models.AutoField(verbose_name="新增图片id", primary_key=True)
    picture_testcaseId=models.IntegerField(verbose_name="用例id")
    picture_scriptId=models.IntegerField(verbose_name="脚本id")
    picture_file=models.CharField(max_length=100,verbose_name="保存图片地址")
#全局变量
class Testvariable(models.Model):
    variable_id=models.AutoField(verbose_name="变量ID", primary_key=True)
    variableKey=models.CharField(max_length=50, verbose_name="key")
    variableValue=models.CharField(max_length=1000, verbose_name="value")

class Testextract(models.Model):
    extract_id=models.AutoField(verbose_name="提取变量ID", primary_key=True)
    extract_apiName=models.CharField(max_length=50, verbose_name="用例名称")
    extract_apiExtractExpression=models.CharField(max_length=50, verbose_name="提取表达式")
    extract_apiExtractResponse=models.CharField(max_length=1000, verbose_name="提取值")
class Testcookies(models.Model):
    cookie_id=models.AutoField(verbose_name="cookieId", primary_key=True)
    cookie_name=models.CharField(max_length=50, verbose_name="cookie名称")
    cookie_value=models.CharField(max_length=1000, verbose_name="cookie值")
    cookie_domain=models.CharField(max_length=50, verbose_name="cookiehost")
    cookie_path=models.CharField(max_length=50, verbose_name="cookie路径")

class Testemail(models.Model):
    email_id=models.AutoField(verbose_name="emailID", primary_key=True)
    email_serverAddress=models.CharField(max_length=50, verbose_name="邮件服务器地址")
    email_emailTeam=models.CharField(max_length=50, verbose_name="项目")
    email_fromAddr=models.CharField(max_length=50, verbose_name="发件人地址")
    email_toAddr=models.CharField(max_length=100, verbose_name="收件人地址")
    email_account=models.CharField(max_length=100, verbose_name="账号")
    email_password=models.CharField(max_length=50, verbose_name="密码")

    