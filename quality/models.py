# _*_ coding:utf-8_*_
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# name = models.CharField(max_length=40, blank=True, verbose_name="姓名")
#  gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="secret", verbose_name="性别")
#  age = models.IntegerField(default=0, verbose_name="年龄")
#  rank = models.PositiveIntegerField(default=1, verbose_name="排名", unique=True)
#  discount = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="折扣", default=1.0)
#  school = models.ForeignKey(to=School, verbose_name="学校", on_delete=models.CASCADE)
#  message = models.OneToOneField(to=Message, verbose_name="信息", on_delete=models.CASCADE)
#  teacher = models.ManyToManyField(verbose_name="老师", to=Teacher, blank=True)
#  introduce = models.TextField(blank=True, verbose_name="介绍")
#  grade = models.FloatField(default=0.0, verbose_name="成绩")
#  url = models.URLField(verbose_name="个人主页", max_length=100)
#  email = models.EmailField(verbose_name="邮箱")
#  image = models.ImageField(upload_to='img/%Y/%m/%d/', verbose_name='上传图片', null=True)
#  file = models.FileField(upload_to="file/%Y/%m/%d/", verbose_name="上传文件", blank=True)
#  is_deleted = models.BooleanField(verbose_name="已删除", default=False, blank=True)
#  time_added = models.DateTimeField(verbose_name="添加时间", auto_now_add=True, blank=True)



# Create your models here.
# class UserProfile():
#     nick_name = models.CharField(max_length=50,verbose_name="昵称",default="")
#     birday = models.DateField(verbose_name="生日",null=True,blank=True)
#     gender = models.CharField(max_length=6,choices=(("male","男"),("female","女")),default="female")
#     address = models.CharField(max_length=100, default="")
#     mobile = models.CharField(max_length=11,null=True,blank=True)
#     image = models.ImageField(upload_to='image/%Y/%m',default="image/default.png",max_length=100)

#     class Meta:
#         verbose_name = "用户信息"
#         verbose_name_plural = verbose_name

#     def __str__(self):
#         return self.username

class PostList(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    # objects=models.Manager()
    class Meta:
        ordering = ('-pub_date',)

    def __unicode__(self):
        return self.title


# class Project(models.Model):
#     project_id = models.AutoField(verbose_name="项目ID", primary_key=True)
#     parent_project_id = models.IntegerField(verbose_name="父项目节点", null=True)
#     project_name = models.CharField(max_length=100, verbose_name="项目名称")
#     tester = models.CharField(max_length=100, verbose_name="测试人员")
#     producter = models.CharField(max_length=100, verbose_name="产品人员")
#     programmer = models.CharField(max_length=1000, verbose_name="开发人员")
#     projecter = models.CharField(max_length=50, verbose_name="PMO")
#     project_jira_id = models.CharField(max_length=11,default='', verbose_name="项目在jira上的id")
#     project_jira_key = models.CharField(max_length=11,default='', verbose_name="项目在jira上的key")
#     project_jira_type_key = models.CharField(max_length=11,default='', verbose_name="项目在jira上的typekey")
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
#     update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")


# class Version(models.Model):
#     version_id = models.AutoField(primary_key=True, verbose_name="版本ID")
#     version_name = models.CharField(max_length=50, default='', verbose_name="版本名称")
#     version_manager = models.CharField(max_length=50, default='', verbose_name="版本负责人")
#     version_type = models.CharField(max_length=50, default='', verbose_name="版本类型")
#     project_id = models.ForeignKey('Project',related_name="versionID", on_delete=models.CASCADE)
#     #jira上版本的属性信息
#     version_jira_project_id = models.CharField(max_length=11, default='', verbose_name="版本在jira上的id")
#     version_jira_id = models.CharField(max_length=11, default='', verbose_name="版本在jira上的id")
#     version_released = models.CharField(max_length=11, default='', verbose_name="版本是否发布")
#     version_archived = models.CharField(max_length=11, default='', verbose_name="版本是否归档")
#     create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
#     update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")


# class Version_Time(models.Model):
#     time_id = models.AutoField(primary_key=True, verbose_name="时间轴ID")
#     # version_id = models.ForeignKey('Version', on_delete=models.CASCADE)
#     version_id = models.OneToOneField('Version', on_delete=models.CASCADE,to_field='version_id', null=True)
#     review_time = models.CharField(blank=True,default='',max_length=100,verbose_name="需求评审时间")
#     begindevelop_time = models.CharField(blank=True,default='',max_length=100,verbose_name="研发开始时间")
#     begintest_time = models.CharField(blank=True,default='',max_length=100,verbose_name="研发开始提测时间")
#     enddevelop_time = models.CharField(blank=True,default='',max_length=100,verbose_name="研发最后提测时间")
#     signoff_time = models.CharField(blank=True,default='',max_length=100,verbose_name="测试通过时间")
#     release_time = models.CharField(blank=True,default='',max_length=100,verbose_name="发布时间")
#     delay = models.CharField(blank=True,default='',max_length=100,verbose_name="是否延期")
#     delivery_cycle = models.IntegerField(verbose_name="交付周期")
#     develop_cycle = models.IntegerField(verbose_name="开发周期")
#     test_cycle = models.IntegerField(verbose_name="测试周期")



# class Version_Bug(models.Model):
#     version_bug_id=models.AutoField(verbose_name="VERSIONBUGID", primary_key=True)
#     version_id = models.ForeignKey('Version',  on_delete=models.CASCADE)
#     bug_num = models.IntegerField(default=0,verbose_name="BUG总数")
#     buga_num = models.IntegerField(default=0,verbose_name="A级BUG数")
#     bugb_num = models.IntegerField(default=0,verbose_name="B级BUG数")
#     bugc_num = models.IntegerField(default=0,verbose_name="C级BUG数")
#     bugd_num = models.IntegerField(default=0,verbose_name="D级BUG数")
#     buge_num = models.IntegerField(default=0,verbose_name="D级BUG数")
#     bug_test_num = models.IntegerField(default=0,verbose_name="测试环境BUG数")
#     bug_leave_num = models.IntegerField(default=0,verbose_name="遗留BUG数")
#     bug_produce_num = models.IntegerField(default=0,verbose_name="生产环境BUG数")
#     bug_omit_num = models.IntegerField(default=0,verbose_name="遗漏BUG数")

# class Version_Bug_Leave(models.Model):
#     bug_leave_id=models.AutoField(verbose_name="BUGLEAVEID", primary_key=True)
#     version_id = models.ForeignKey('Version', on_delete=models.CASCADE)
#     bug_name = models.CharField(max_length=100,default='', verbose_name="BUG名称")
#     bug_url = models.CharField(max_length=100,default='', verbose_name="BUG地址")
#     bug_type = models.CharField(max_length=100,default='', verbose_name="BUG等级")
#     bug_status2=models.CharField(max_length=100,default='', verbose_name="BUG状态")
#     bug_impact_assessment = models.CharField(max_length=1000,default='', verbose_name="BUG影响评估")

# class Version_Bug_Analysis(models.Model):
#     version_id = models.ForeignKey('Version', on_delete=models.CASCADE)
#     bug_id = models.AutoField(verbose_name="BUGID", primary_key=True)
#     bug_name = models.CharField(max_length=100, default='',verbose_name="BUG名称")
#     bug_url = models.CharField(max_length=100,default='', verbose_name="BUG地址")
#     bug_type = models.CharField(max_length=100,default='', verbose_name="BUG等级")
#     bug_reason = models.CharField(max_length=100,default='', verbose_name="BUG原因")
#     bug_analysis = models.CharField(max_length=1000,default='', verbose_name="BUG分析")
#     bug_status=models.CharField(max_length=100,default='', verbose_name="BUG状态")
#     bug_omit_num = models.FloatField(default=0, verbose_name="遗漏bug数")
#     bug_person_liable = models.CharField(default='', max_length=100,verbose_name="责任人")
#     performance_deduction = models.FloatField(default=0, verbose_name="绩效扣减")


# class Version_Code(models.Model):
#     code_id=models.AutoField(primary_key=True,verbose_name="ID")
#     version_id = models.ForeignKey('Version', on_delete=models.CASCADE)
#     code_num = models.IntegerField(default=0,verbose_name="代码总行数")
#     code_change_num = models.IntegerField(default=0,verbose_name="代码变更行数")
#     code_defect_rate = models.FloatField(default=0,verbose_name="千行代码缺陷率")


# class Version_delay(models.Model):
#     delay_id = models.AutoField(primary_key=True, verbose_name="延期ID")
#     version_id = models.ForeignKey('Version', on_delete=models.CASCADE)
#     delay_cycle1 = models.CharField(max_length=100, verbose_name="延期环节")
#     delay_time1 = models.FloatField(verbose_name="延期时间")
#     delay_reason1 = models.CharField(max_length=1000, verbose_name="延期原因")


# class Version_engineer(models.Model):
#     engineer_id=models.AutoField('ID',primary_key=True)
#     version_id = models.ForeignKey('Version',  on_delete=models.CASCADE)
#     # engineer_type=models.CharField(max_length=100,verbose_name="人员类型")
#     test_bug_num = models.CharField(max_length=1000,default='',verbose_name="测试人员")
#     productor_bug_num = models.CharField(max_length=1000,default='',verbose_name="研发人员")
#     programer_bug_num = models.CharField(max_length=1000,default='',verbose_name="产品人员")


# class Version_release(models.Model):
#     release_id = models.AutoField(primary_key=True,verbose_name="发布ID")
#     version_id = models.ForeignKey('Version', on_delete=models.CASCADE)
#     release_num = models.IntegerField(default=0,verbose_name="发布次数")
#     release_consume_time = models.CharField(max_length=32,default=0,verbose_name="结束回归时间")
#     release_time = models.CharField(max_length=32,verbose_name="开始发布时间")
#     release_back_time = models.CharField(max_length=32,verbose_name="开始回归时间")
#     release_result = models.IntegerField(default='',verbose_name="发布结果1：成功、2：失败")
#     release_analysis = models.CharField(max_length=1000,default='',null=True, verbose_name="备注")

# class Version_overall_evaluation(models.Model):
#     overall_id=models.AutoField(primary_key=True,verbose_name="总体评价ID")
#     version_id = models.ForeignKey('Version', on_delete=models.CASCADE)
#     test_overall_evaluation=models.CharField(max_length=1000,default='',null=True, verbose_name="测试环境总体评价")
#     produce_overall_evaluation=models.CharField(max_length=1000,default='',null=True, verbose_name="发布环境总体评价")
# class NewTable(models.Model):
#     bight_f = models.BigIntegerField()  # 64位整数
#     bool_f = models.BooleanField()  # 布林值
#     date_f = models.DateField(auto_now=True)  # 日期格式
#     char_f = models.CharField(max_length=20, unique=True)  # 单行的文字资料
#     datetime_f = models.DateTimeField(auto_now_add=True)  # 日期格式
#     decimal_f = models.DecimalField(max_digits=10, decimal_places=2)
#     flost_f = models.FloatField(null=True)  # 浮点数栏位
#     int_f = models.IntegerField(default=2010)  # 整数栏位
#     text_f = models.TextField()  # 长文字格式

