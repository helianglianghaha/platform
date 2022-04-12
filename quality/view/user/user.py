from django.http.response import JsonResponse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
import json
import  datetime
from django.db.models import Q
import random
from django.core import serializers
from django.db import models
# from quality.model.User imp/ort  User
# from quality.model.OrganizeModel import Organize_User,Organize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from quality.view.organize import organize
from django.db import connection, transaction

def save_user(request):
    data={
        'code':200,
        'msg':'保存成功'
    }
    try:
        user_name=request.POST.get('user_name')
        user_type=request.POST.get('user_type')
        user_login_ame=request.POST.get('user_login_ame')
        user_phone=request.POST.get('user_phone')
        user_initiation_time=request.POST.get('user_initiation_time')
        user_departure_time=request.POST.get('user_departure_time')
        user_organize_id = request.POST.getlist('user_organize_id[]', '')
        user=User()
        user.user_name=user_name
        user.user_type=user_type
        user.user_login_ame=user_login_ame
        user.user_phone=user_phone
        if user_initiation_time:
            user.user_initiation_time=user_initiation_time
        if user_departure_time:
            user.user_departure_time=user_departure_time
        user.save()
        if user_organize_id:
            for organize in user_organize_id:
                organize=Organize.objects.get(organize_id=organize)
                organizeMember=Organize_User.objects.create(user_id=user,organize_id=organize)
    except Exception as e:
        data['code']=1000
        data['msg']='保存失败'
    # user=json.loads(request.POST['user'])
    return JsonResponse(data)



def edit_user(request):
    data={
        'code':200,
        'msg':'修改成功'
    }
    try:
        user_id=request.POST.get('user_id')
        user_name=request.POST.get('user_name')
        user_type=request.POST.get('user_type')
        user_login_ame=request.POST.get('user_login_ame')
        user_initiation_time=request.POST.get('user_initiation_time')
        user_departure_time=request.POST.get('user_departure_time')
        user_phone=request.POST.get('user_phone')
        user_organize_id = request.POST.getlist('user_organize_id[]', '')
        user=User.objects.get(user_id=user_id)
        user.user_organize.clear()
        if user_organize_id:
            for organize in user_organize_id:
                organize=Organize.objects.get(organize_id=organize)
                organizeMember=Organize_User.objects.create(user_id=user,organize_id=organize)
        user.user_name=user_name
        user.user_type=user_type
        user.user_login_ame=user_login_ame
        user.user_phone=user_phone
        if user_initiation_time:
            user.user_initiation_time=user_initiation_time
        if user_departure_time:
            user.user_departure_time=user_departure_time
        user.save()
    except Exception as e:
        data['code']=1000
        data['msg']='修改失败'
    return JsonResponse(data)

def delete_user(request):
    data={
        'code':200,
        'msg':'删除成功'
    }
    try:
        user_id=request.POST.get('user_id')
        User.objects.get(user_id=user_id).delete()
    except Exception as e:
        data['code']=1000
        data['msg']='删除失败'
    return JsonResponse(data)

def select_user(request):
    data = {
        "code": 200,
        'userList': [],
        'organizeLists':[]
    }
    try:
        userName=request.POST.get("userName")
        user_organize_id=request.POST.get("user_organize_id")
        user_onjob_status=request.POST.get("user_onjob_status")
        # filter_dict = dict()
        con = Q()
        q1 = Q()
        q2=Q()
        q1.connector = 'AND'
        if userName:
            # filter_dict['user_name__contains']=userName
            q1.children.append(('user_name__contains', userName))
        if user_organize_id:
            # organizes1=Organize.objects.filter(Q(parent_organize_id = user_organize_id) | Q(organize_id = user_organize_id)).values_list('organize_id',flat=True)
            organizes1sql='SELECT  GROUP_CONCAT(DISTINCT id._ids)as ids FROM(' \
                          ' SELECT @ids as _ids,' \
                          ' ( SELECT @ids := GROUP_CONCAT(organize_id)' \
                          ' FROM quality_organize WHERE FIND_IN_SET(parent_organize_id, @ids)' \
                          ') as cids, @l := @l+1 as level  FROM quality_organize,' \
                          '  (SELECT @ids :='+user_organize_id+', @l := 0) b WHERE @ids IS NOT NULL) id'
            cursor = connection.cursor()
            cursor.execute(organizes1sql)
            organizes1=cursor.fetchone()[0].split(',')
            userIds=Organize_User.objects.filter(organize_id__in=organizes1).values_list('user_id_id',flat=True)
            # filter_dict['user_id__in']=userIds
            q1.children.append(('user_id__in', userIds))
        if user_onjob_status:
            now = datetime.datetime.now()
            if user_onjob_status=='2':
                q1.children.append(('user_departure_time__isnull', False))
                q1.children.append(~Q(user_departure_time=''))
                q1.children.append(('user_departure_time__lt', now))
                # filter_dict['user_departure_time__isnull']=False
                # filter_dict['user_departure_time__lt']=now
            else:
                q2.connector = 'OR'
                q2.children.append(('user_departure_time__isnull', True))
                q2.children.append(Q(user_departure_time=''))
                q2.children.append(('user_departure_time__gt', now))
                # filter_dict[Q('user_departure_time__gt')]=str(now)
        if q1.children:
            con.add(q1, 'AND')
        if q2.children:
            con.add(q2, 'AND')
        # users=User.objects.filter(**filter_dict).order_by('-create_time')
        users=User.objects.filter(con).order_by('-create_time')
        if users:
            pageIndex=request.POST.get("pageIndex")
            pageSize=request.POST.get("pageSize")
            paginator = Paginator(users, pageSize)
            data['total'] = paginator.count
            try:
                users = paginator.page(pageIndex)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            # userList = json.loads(serializers.serialize("json", users))
            i=0
            for user in users.object_list:
                data['userList'].append(i)
                data['userList'][i] = {
                    "user_id": '',
                    "user_name": '',
                    "user_login_ame": '',
                    "user_type": '',
                    "user_phone": '',
                    'organize_name':'',
                    'user_organize_id':[],
                    'user_initiation_time':'',
                    'user_departure_time':''
                }
                # data['userList'][i]['user_id']=user['pk']
                # data['userList'][i]['user_name']=user['fields']['user_name']
                # data['userList'][i]['user_login_ame']=user['fields']['user_login_ame']
                # data['userList'][i]['user_type']=user['fields']['user_type']
                # data['userList'][i]['user_phone']=user['fields']['user_phone']
                data['userList'][i]['user_id']=user.pk
                data['userList'][i]['user_name']=user.user_name
                data['userList'][i]['user_login_ame']=user.user_login_ame
                data['userList'][i]['user_type']=user.user_type
                data['userList'][i]['user_phone']=user.user_phone
                data['userList'][i]['user_initiation_time']=user.user_initiation_time
                data['userList'][i]['user_departure_time']=user.user_departure_time
                organizeLists=json.loads(serializers.serialize("json", user.user_organize.all()))
                j=0
                for organizes in organizeLists:
                    data["userList"][i]['organize_name']+=organizes['fields']['organize_name']
                    data["userList"][i]['user_organize_id'].append(int(organizes['pk']))
                    if j.__eq__(len(organizeLists)-1) is False:
                        data["userList"][i]['organize_name']+=';'
                    j+=1
                i+=1
            organizeListss=organize.getOrganizeList()
            data['organizeLists']=organizeListss

        else:
            data['userList'] =json.loads(serializers.serialize("json", users))
    except Exception as e:
        print(e)
    return JsonResponse(data)

def selectUserAll():
    users=User.objects.all()
    data={'userList':[]}
    if users:
        i=0
        for user in users:
            data['userList'].append(i)
            data['userList'][i]={
                'label': user.user_name,
                'value':  user.user_id
            }
            i+=1
    return data['userList']

def selectUserByType(request):
    type=request.POST.get("user_type")
    users=User.objects.filter(user_type=type)
    data={'code':200,'userLists':[]}
    if users:
        i=0
        for user in users:
            data['userLists'].append(i)
            data['userLists'][i]={
                'label': user.user_name,
                # 'value':  user.user_id
                'value':  user.user_name
            }
            i+=1
    return JsonResponse(data)