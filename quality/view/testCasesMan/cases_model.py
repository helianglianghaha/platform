from django.db import models


class testcasemanager(models.Model):
    case_id = models.AutoField(verbose_name="用例ID", primary_key=True)
    prdName = models.CharField(max_length=50, verbose_name="需求名称", default=None)
    firstModel = models.CharField(max_length=100, verbose_name="一级模块", default=None)
    secondModel = models.CharField(max_length=100, verbose_name="二级模块", default=None)
    thirdModel=models.CharField(max_length=100, verbose_name="三级模块", default=None)
    caseName = models.CharField(max_length=100, verbose_name="用例标题", default=None)
    condition = models.CharField(max_length=100, verbose_name="前置条件", default=None)
    steps = models.CharField(max_length=100, verbose_name="操作步骤", default=None)
    exceptResult = models.CharField(max_length=100, verbose_name="预期结果", default=None)
    actualResult = models.CharField(max_length=100, verbose_name="实际结果", default=None)
    caseType = models.CharField(max_length=100, verbose_name="用例类型", default=None)
    creater = models.CharField(max_length=100, verbose_name="编写人", default=None)
    executor = models.CharField(max_length=100, verbose_name="执行人", default=None)
    createrTime = models.CharField(max_length=100, verbose_name="编写时间", default=None)
    versionName=models.CharField(max_length=100, verbose_name="版本名称", default=None)
    remark = models.CharField(max_length=200, verbose_name="备注", default=None)
