from django.db import models


class documentMan(models.Model):
    doc_id = models.AutoField(verbose_name="文档管理ID", primary_key=True)
    id = models.IntegerField(max_length=50, verbose_name="文档ID", default=None)
    name = models.CharField(max_length=100, verbose_name="分组名称", default=None)
    children = models.CharField(max_length=100, verbose_name="文件列表", default=None)
    parentName=models.CharField(max_length=100, verbose_name="父节点名称", default=None)