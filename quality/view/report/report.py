from django.http.response import JsonResponse
from django.utils import timezone
from django.utils import dateparse,datastructures
import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
import json
import random
from django.core import serializers
from django.db import models
from quality.model.OrganizeModel import Organize,Organize_User
from quality.model.User import User
from quality.view.user import user
from django.db import connection, transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def selectStatistics(request):
    try:
        cursor = connection.cursor()
        user_organize_id=request.POST.get('user_organize_id', '')
        day=request.POST.get('day', '')
        result=getParams(user_organize_id,day)
        user_organize_id=result['user_organize_id']
        day=result['day']
        level=result['level']
        month=result['month']
        lastmonth=result['lastmonth']
        sql2=sqlCondition(user_organize_id,level)
        # ' left join quality_organize oo on (o1.organize_id=oo.organize_id or oo.parent_organize_id=o1.organize_id)' \
        # ' left join quality_organize o2 on (o1.organize_id=o2.organize_id or o2.parent_organize_id=o1.organize_id)' \
        # 'left join quality_organize o3 on (o2.organize_id=o3.organize_id or o3.parent_organize_id=o2.organize_id)' \
        # ' left join quality_organize_user ou on ou.organize_id_id=o3.organize_id' \
            # ' inner join (SELECT id.level, DATA.organize_id FROM(' \
        # ' SELECT @ids as _ids,' \
        # ' ( SELECT @ids := GROUP_CONCAT(organize_id)' \
        # ' FROM quality_organize WHERE FIND_IN_SET(parent_organize_id, @ids)' \
        # ') as cids, @l := @l+1 as level  FROM quality_organize,' \
        # '  (SELECT @ids :='+user_organize_id+', @l := '+level+') b WHERE @ids IS NOT NULL' \
        #                                                       ') id, quality_organize DATA WHERE FIND_IN_SET(DATA.organize_id, id._ids)ORDER BY level)oo on oo.organize_id=o1.organize_id' \

        currentMonthSql= 'SELECT o.organize_id,o.organize_name, o.parent_organize_id' \
                        ',COUNT(o.organize_id)as usercount' \
                        ',(CASE WHEN sum(o.bugcount) is null THEN 0 ELSE sum(o.bugcount) END)as bugcount,count(o.assigneeName)as bugusercount' \
                        ', ROUND(count(o.assigneeName)/COUNT(o.organize_id)*100,2)as numberOfBugs' \
                ',(CASE WHEN ROUND(sum(o.bugcount)/count(o.organize_id),2) is null THEN 0 ELSE ROUND(sum(o.bugcount)/count(o.organize_id),2)END)as perCapitaAll' \
            ',(CASE WHEN ROUND(sum(o.bugcount)/count(o.assigneeName),2) is null THEN 0 ELSE ROUND(sum(o.bugcount)/count(o.assigneeName),2)END)as perCapita' \
             ',(CASE  WHEN MONTH( o.date) is null  THEN '+month+' else MONTH( o.date) end) as month,o.level' \
            ' from (SELECT DISTINCT ou.user_id_id,o1.organize_id,o1.organize_name,us.user_id,o1.parent_organize_id,us.user_login_ame,oo.level, iss.bugcount,iss.assigneeName,iss.date' \
            ' from quality_organize o1 '+sql2+'' \
             ' inner join (SELECT id.level, DATA.organize_id FROM(' \
            ' SELECT @ids as _ids,' \
             ' ( SELECT @ids := GROUP_CONCAT(organize_id)' \
             ' FROM quality_organize WHERE FIND_IN_SET(parent_organize_id, @ids)' \
             ') as cids, @l := @l+1 as level  FROM quality_organize,' \
            '  (SELECT @ids :='+user_organize_id+', @l := '+level+') b WHERE @ids IS NOT NULL' \
            ') id, quality_organize DATA WHERE FIND_IN_SET(DATA.organize_id, id._ids)ORDER BY level)oo on o1.organize_id=oo.organize_id' \
            ' inner join quality_user us on  ou.user_id_id=us.user_id ' \
           ' and  IF (ISNULL(us.user_initiation_time) || LENGTH(trim(us.user_initiation_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_initiation_time, "%Y%m") ,"'+day+'") <=0 )' \
            ' AND IF (ISNULL(us.user_departure_time) || LENGTH(trim(us.user_departure_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_departure_time, "%Y%m") ,"'+day+'") >=0 )' \
          ' left join (select qiss.assigneeName,COUNT(qiss.assigneeName)as bugcount,DATE_FORMAT( qiss.created, "%Y-%m" )as date' \
          ' from quality_issues qiss' \
          ' WHERE DATE_FORMAT( qiss.created, "%Y%m" )="'+day+'"'\
         ' and qiss.assigneeName is not null and LENGTH(trim(qiss.assigneeName))>0' \
         ' GROUP BY DATE_FORMAT( qiss.created, "%Y-%m" ),qiss.assigneeName) iss on us.user_login_ame=iss.assigneeName ' \
         ' WHERE 1=1 '\
             ' GROUP BY o1.organize_id,us.user_id) o' \
            '  GROUP BY o.organize_id'
            # ' union'
        lastMonthSql= 'SELECT o.organize_id,o.organize_name,o.parent_organize_id' \
                      ' ,COUNT(o.organize_id)as usercount' \
                      ',(CASE WHEN sum(o.bugcount) is null THEN 0 ELSE sum(o.bugcount) END)as bugcount' \
                      ',count(o.assigneeName)as bugusercount' \
                      ', ROUND(count(o.assigneeName)/COUNT(o.organize_id)*100,2)as numberOfBugs' \
                      ',(CASE WHEN ROUND(sum(o.bugcount)/count(o.organize_id),2) is null THEN 0 ELSE ROUND(sum(o.bugcount)/count(o.organize_id),2)END)as perCapitaAll' \
                      ',(CASE WHEN ROUND(sum(o.bugcount)/count(o.assigneeName),2) is null THEN 0 ELSE ROUND(sum(o.bugcount)/count(o.assigneeName),2)END)as perCapita' \
                     ',(CASE  WHEN MONTH( o.date) is null  THEN '+lastmonth+' else MONTH( o.date) end) as month,o.level' \
                   ' from (SELECT DISTINCT ou.user_id_id,o1.organize_id,o1.organize_name,us.user_id,o1.parent_organize_id,us.user_login_ame,oo.level, iss.bugcount,iss.assigneeName,iss.date' \
                   ' from quality_organize o1'+sql2+'' \
                    '  left join (SELECT id.level, DATA.organize_id FROM(' \
                     ' SELECT @ids as _ids,' \
                   ' ( SELECT @ids := GROUP_CONCAT(organize_id)' \
                   ' FROM quality_organize WHERE FIND_IN_SET(parent_organize_id, @ids)' \
                   ') as cids, @l := @l+1 as level  FROM quality_organize,' \
                   '  (SELECT @ids :='+user_organize_id+', @l := '+level+') b WHERE @ids IS NOT NULL' \
                   ') id, quality_organize DATA WHERE FIND_IN_SET(DATA.organize_id, id._ids)ORDER BY level)oo on oo.organize_id=o1.organize_id' \
                   ' inner join quality_user us on  ou.user_id_id=us.user_id ' \
                   ' and  IF (ISNULL(us.user_initiation_time) || LENGTH(trim(us.user_initiation_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_initiation_time, "%Y%m") ,"'+day+'") <=-1 )' \
                   ' AND IF (ISNULL(us.user_departure_time) || LENGTH(trim(us.user_departure_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_departure_time, "%Y%m") ,"'+day+'") >=-1 )' \
                 ' left join (select qiss.assigneeName,COUNT(qiss.assigneeName)as bugcount,DATE_FORMAT( qiss.created, "%Y-%m" )as date' \
                 ' from quality_issues qiss' \
                 ' WHERE PERIOD_DIFF( "'+day+'", date_format(qiss.created, "%Y%m") ) =1' \
                ' and qiss.assigneeName is not null and LENGTH(trim(qiss.assigneeName))>0' \
                ' GROUP BY DATE_FORMAT( qiss.created, "%Y-%m" ),qiss.assigneeName) iss on us.user_login_ame=iss.assigneeName' \
                    ' GROUP BY o1.organize_id,us.user_id) o' \
                                              ' GROUP BY o.organize_id'
        # print(currentMonthSql)
        # print(lastMonthSql)
        cursor.execute(currentMonthSql)
        currentrow=dictfetchall(cursor)
        cursor.execute(lastMonthSql)
        lastMonthRow=dictfetchall(cursor)
        # row1+=row2
        # row = cursor.fetchall()
        # desc = cursor.description
        data={'code':200,'currentrow':currentrow,'lastMonthRow':lastMonthRow}
    except Exception as e:
        print(e)
        data={'code':500}
    return JsonResponse(data)

def selectUserMoreBugCount(request):
    cursor = connection.cursor()
    sql1=''
    user_organize_id=request.POST.get('user_organize_id', '')
    if user_organize_id:
        sql1=' and o1.organize_id='+user_organize_id
    day=request.POST.get('day', '')
    result=getParams(user_organize_id,day)
    user_organize_id=result['user_organize_id']
    day=result['day']
    level=result['level']
    sql2=sqlCondition(user_organize_id,level)
    currrntsql='SELECT o.user_login_ame,o.user_id,o.user_name' \
        ',count(iss.assigneeName)as bugcount' \
        ',(CASE  WHEN MONTH( iss.created) is null  THEN 6 else MONTH( iss.created) end) as month' \
        ' from (' \
        ' SELECT DISTINCT us.user_id,us.user_login_ame,us.user_name' \
        ' from quality_organize o1'+sql2+'' \
        ' left join quality_user us on  ou.user_id_id=us.user_id' \
        ' WHERE 1=1 '+sql1+' and  IF (ISNULL(us.user_initiation_time) || LENGTH(trim(us.user_initiation_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_initiation_time, "%Y%m") ,"'+day+'") <=0 ) ' \
        ' AND IF (ISNULL(us.user_departure_time) || LENGTH(trim(us.user_departure_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_departure_time, "%Y%m") ,"'+day+'") >=0 )' \
        ')o' \
        ' inner join quality_issues iss on iss.assigneeName=o.user_login_ame and  DATE_FORMAT( iss.created, "%Y%m" ) = "'+day+'"' \
        ' GROUP BY o.user_id' \
        ' order by bugcount desc'
    # 当月人员bug数，倒序
    # print(currrntsql)
    cursor.execute(currrntsql)
    row1=dictfetchall(cursor)
    lastmonthsql='SELECT o.user_login_ame,o.user_id,o.user_name' \
               ',count(iss.assigneeName)as bugcount' \
               ',(CASE  WHEN MONTH( iss.created) is null  THEN 6 else MONTH( iss.created) end) as month' \
               ' from (' \
               ' SELECT DISTINCT us.user_id,us.user_login_ame,us.user_name' \
               ' from quality_organize o1'+sql2+'' \
                ' left join quality_user us on  ou.user_id_id=us.user_id' \
                ' WHERE 1=1 '+sql1+' and  IF (ISNULL(us.user_initiation_time) || LENGTH(trim(us.user_initiation_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_initiation_time, "%Y%m") ,"'+day+'") <=-1 ) ' \
                ' AND IF (ISNULL(us.user_departure_time) || LENGTH(trim(us.user_departure_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_departure_time, "%Y%m") ,"'+day+'") >=-1 )' \
               ')o' \
               ' inner join quality_issues iss on iss.assigneeName=o.user_login_ame and  PERIOD_DIFF( "'+day+'", date_format(iss.created, "%Y%m") ) =1' \
                 ' GROUP BY o.user_id' \
                 ' order by bugcount desc'
    cursor.execute(lastmonthsql)
    row2=dictfetchall(cursor)
    data={'code':200,'row':row1,'lastmonthrow':row2}
    return JsonResponse(data)

def sqlCondition(user_organize_id,level):
    cursor = connection.cursor()
    gradeSql='SELECT MAX(id.level)as level FROM(' \
             ' SELECT @ids as _ids,' \
             ' ( SELECT @ids := GROUP_CONCAT(organize_id)' \
             ' FROM quality_organize WHERE FIND_IN_SET(parent_organize_id, @ids)' \
             ') as cids, @l := @l+1 as level  FROM quality_organize,' \
             '  (SELECT @ids :='+user_organize_id+', @l :='+ level+') b WHERE @ids IS NOT NULL) id'
    cursor.execute(gradeSql)
    grade=int(cursor.fetchone()[0])
    sql2=''
    if grade>=1:
        for i in range(grade):
            if i>0:
                sql2+=' left join quality_organize o'+str(i+1)+' on (o'+str(i)+'.organize_id=o'+str(i+1)+'.organize_id or o'+str(i+1)+'.parent_organize_id=o'+str(i)+'.organize_id)'
    sql2+= ' left join quality_organize_user ou on ou.organize_id_id=o'+str(i+1)+'.organize_id'
    return sql2

def getParams(user_organize_id,day):
    if user_organize_id:
        level='0'
    else:
        user_organize_id='0'
        level='-1'
    if day is  '':
        year = str(timezone.now().year)
        month=timezone.now().month
        if month<10:
            months="0"+str(month)
            day=str(year+months)
    else:
        if '-' in day:
            days = datetime.datetime.strptime(day,'%Y-%m')
        else:
            days = datetime.datetime.strptime(day,'%Y%m')
        month=days.month
        day=days.strftime("%Y%m")
    lastmonth=str(month-1)
    month=str(month)
    data={'level':level,'user_organize_id':user_organize_id,'day':day,'month':month,'lastmonth':lastmonth}
    return data

def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row))for row in cursor.fetchall()]



# currentMonthSql='select isss.level, isss.organize_name,isss.organize_id, isss.parent_organize_id,COUNT(isss.organize_id)as usercount, isss.month,   count(isss.assigneeName)' \
#     'as bugusercount,sum(isss.bugcount)as bugCount ,' \
#     'ROUND(count(isss.assigneeName)/COUNT(isss.organize_id)*100,2)as numberOfBugs,' \
#     'ROUND(sum(isss.bugcount)/COUNT(isss.organize_id),2)as perCapitaAll,' \
#     '(CASE WHEN ROUND(sum(isss.bugcount)/count(isss.assigneeName),2) is null THEN 0 ELSE ROUND(sum(isss.bugcount)/count(isss.assigneeName),2)END)as perCapita from' \
#     '(SELECT o.organize_id,o.organize_name, iss.assigneeName,count(iss.assigneeName)as bugcount,o.parent_organize_id,' \
#     '(CASE  WHEN MONTH( iss.created) is null  THEN '+month+' else MONTH( iss.created) end) as month,o.level' \
#     ' from (SELECT DISTINCT ou.user_id_id,o1.organize_id,o1.organize_name,us.user_id,o1.parent_organize_id,us.user_login_ame,oo.level' \
#     ' from quality_organize o1 '+sql2+'' \
#      ' inner join (SELECT id.level, DATA.organize_id FROM(' \
#     ' SELECT @ids as _ids,' \
#      ' ( SELECT @ids := GROUP_CONCAT(organize_id)' \
#      ' FROM quality_organize WHERE FIND_IN_SET(parent_organize_id, @ids)' \
#      ') as cids, @l := @l+1 as level  FROM quality_organize,' \
#     '  (SELECT @ids :='+user_organize_id+', @l := '+level+') b WHERE @ids IS NOT NULL' \
#     ') id, quality_organize DATA WHERE FIND_IN_SET(DATA.organize_id, id._ids)ORDER BY level)oo on o1.organize_id=oo.organize_id' \
#     ' inner join quality_user us on  ou.user_id_id=us.user_id ' \
#    ' and  IF (ISNULL(us.user_initiation_time) || LENGTH(trim(us.user_initiation_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_initiation_time, "%Y%m") ,"'+day+'") <=0 )' \
#     ' AND IF (ISNULL(us.user_departure_time) || LENGTH(trim(us.user_departure_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_departure_time, "%Y%m") ,"'+day+'") >=0 )' \
#    ' WHERE 1=1 '\
#      ' GROUP BY o1.organize_id,us.user_id) o' \
#     ' left join quality_issues iss on o.user_login_ame=iss.assigneeName' \
#     ' and   DATE_FORMAT( iss.created, "%Y%m" ) = "'+day+'" GROUP BY o.organize_id,o.user_id_id) isss' \
#         ' GROUP BY isss.organize_id'


# lastMonthSql=' select isss.level, isss.organize_name,isss.organize_id, isss.parent_organize_id,COUNT(isss.organize_id)as usercount, isss.month,'\
#     ' count(isss.assigneeName)as bugusercount,sum(isss.bugcount)as bugCount ,'\
#     'ROUND(count(isss.assigneeName)/COUNT(isss.organize_id)*100,2)as numberOfBugs,'\
#     'ROUND(sum(isss.bugcount)/COUNT(isss.organize_id),2)as perCapitaAll,' \
#     '(CASE WHEN ROUND(sum(isss.bugcount)/count(isss.assigneeName),2) is null THEN 0 ELSE ROUND(sum(isss.bugcount)/count(isss.assigneeName),2)END)as perCapita' \
#     ' from (SELECT o.organize_id,o.organize_name, iss.assigneeName,count(iss.assigneeName)as bugcount,o.parent_organize_id,' \
#     '(CASE  WHEN MONTH( iss.created) is null  THEN '+lastmonth+' else MONTH( iss.created) end) as month,o.level' \
#            ' from (SELECT DISTINCT ou.user_id_id,o1.organize_id,o1.organize_name,us.user_id,o1.parent_organize_id,us.user_login_ame,oo.level' \
#            ' from quality_organize o1'+sql2+'' \
#             '  left join (SELECT id.level, DATA.organize_id FROM(' \
#              ' SELECT @ids as _ids,' \
#            ' ( SELECT @ids := GROUP_CONCAT(organize_id)' \
#            ' FROM quality_organize WHERE FIND_IN_SET(parent_organize_id, @ids)' \
#            ') as cids, @l := @l+1 as level  FROM quality_organize,' \
#            '  (SELECT @ids :='+user_organize_id+', @l := '+level+') b WHERE @ids IS NOT NULL' \
#            ') id, quality_organize DATA WHERE FIND_IN_SET(DATA.organize_id, id._ids)ORDER BY level)oo on oo.organize_id=o1.organize_id' \
#            ' inner join quality_user us on  ou.user_id_id=us.user_id ' \
#            ' and  IF (ISNULL(us.user_initiation_time) || LENGTH(trim(us.user_initiation_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_initiation_time, "%Y%m") ,"'+day+'") <=-1 )' \
#            ' AND IF (ISNULL(us.user_departure_time) || LENGTH(trim(us.user_departure_time))<1, 0 = 0,PERIOD_DIFF(date_format(us.user_departure_time, "%Y%m") ,"'+day+'") >=-1 )' \
#            ' WHERE 1=1 '\
#             ' GROUP BY o1.organize_id,us.user_id) o' \
#            ' left join quality_issues iss on o.user_login_ame=iss.assigneeName' \
#            ' and   PERIOD_DIFF( "'+day+'", date_format(iss.created, "%Y%m") ) =1 ' \
#                                       ' GROUP BY o.organize_id,o.user_id_id) isss' \
#                                       ' GROUP BY isss.organize_id'