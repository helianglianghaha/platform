import functools
from functools import wraps
from quality.common.logger import Log
from django.http.response import JsonResponse

def loginRequired(func):
    @wraps(func)
    def decorated_view(request):
        is_login=request.session.get('username',False)
        if is_login:
            return func(request)
        else:
            data={
                "code":1000,
                "msg":"登录超时，请重新登录"
            }
            return JsonResponse(data,safe=False)
    return decorated_view

def msgMessage(func):
    @functools.wraps(func)
    def wrapper(request):
        Log().info('call %s()；document：%s；args:%s' % (func.__name__,func.__doc__,request.POST))
        return func(request)
    return wrapper
def msglogger(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        Log().info('args={}'.format(*args))
        Log().info('call %s()；document：%s；' % (func.__name__,func.__doc__))
        return func(*args,**kwargs)
    return wrapper
