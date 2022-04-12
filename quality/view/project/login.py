from django.http.response import JsonResponse
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.backends import ModelBackend
from quality.common.commonbase import commonList
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# from django.contrib.auth.decorators import login_required
from functools import wraps




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def Login(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user =authenticate(username=username, password=password)
    if user is not None and user.is_active:
        try:
            token=Token.objects.get(user=user)
            token.delete()
            token = Token.objects.create(user=user)
            request.session['username']=username
        except:
            token = Token.objects.create(user=user)
        sql='select * from auth_user where username='+"\'"+username+"\'"
        userInfo=commonList().getModelData(sql)
        data={
            "code":0,
            "userInfo":userInfo,
            "token":str(token)
        }
        return JsonResponse(data,safe=False)
    else:
        try:
            User.objects.get(username=username)
            case="密码错误"
        except User.DoesNotExist:
            case="用户不存在"
        data={
            "code":1000,
            "msg":case
        }
        return JsonResponse(data,safe=False)



