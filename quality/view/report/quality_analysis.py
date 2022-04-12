from django.db import connection, transaction
from django.http.response import JsonResponse
from django.utils import timezone
from django.utils import dateparse,datastructures
import datetime
from quality.view.report import report
import logging

logger = logging.getLogger('django')
# logger = logging.getLogger(__name__)

#质量分析图表：按月统计bug人占比、人均bug
def select_quality_analysis(request):
    data={'code':200}
    try:
        cursor = connection.cursor()
        user_organize_id=request.POST.get('user_organize_id', '')
        day=request.POST.getlist('day', '')
        day=day[0].split(',')
        startdate=day[0]
        enddate=day[1]
        condition=''
        if user_organize_id:
            condition=' WHERE o1.organize_id='+user_organize_id
            level='0'
        else:
            user_organize_id='0'
            level='-1'
        sql2=report.sqlCondition(user_organize_id,level)
        sql=' SELECT o.organize_id,o.organize_name, o.parent_organize_id,o.dates ,' \
            ' COUNT(o.organize_id)as usercount,(CASE WHEN sum(o.bugcount) is null THEN 0 ELSE sum(o.bugcount) END)as bugcount' \
            ',count(o.assigneeName)as bugusercount' \
            ', ROUND(count(o.assigneeName)/COUNT(o.organize_id)*100,2)as numberOfBugs' \
            ',(CASE WHEN ROUND(sum(o.bugcount)/count(o.organize_id),2) is null THEN 0 ELSE ROUND(sum(o.bugcount)/count(o.organize_id),2)END)as perCapitaAll' \
            ',(CASE WHEN ROUND(sum(o.bugcount)/count(o.assigneeName),2) is null THEN 0 ELSE ROUND(sum(o.bugcount)/count(o.assigneeName),2)END)as perCapita' \
            ' from '\
            ' (SELECT DISTINCT ou.user_id_id,o1.organize_id,o1.organize_name,us.user_id,o1.parent_organize_id,us.user_login_ame, B.dates,iss.assigneeName,iss.bugcount'\
            ' from quality_organize o1'+sql2+'' \
            ' left join quality_user us on  ou.user_id_id=us.user_id' \
            ' inner join (SELECT @num :=@num+1,DATE_FORMAT(ADDDATE(DATE_SUB("'+startdate+'",INTERVAL 1 month),INTERVAL @num+1 month),"%Y-%m") AS dates' \
            ' FROM quality_user,(SELECT @num := -1) t' \
            ' WHERE ADDDATE("'+startdate+'",INTERVAL @num month) <= DATE_FORMAT("'+enddate+'", "%Y-%m")'\
            ' ORDER BY dates'\
            ') B on B.dates>=date_format(us.user_initiation_time, "%Y-%m")'\
            ' and IF (ISNULL(us.user_departure_time) || LENGTH(trim(us.user_departure_time))<1, 0 = 0,date_format(us.user_departure_time, "%Y-%m")>=B.dates) ' \
            ' left join (select qiss.assigneeName,COUNT(qiss.assigneeName)as bugcount,DATE_FORMAT( qiss.created, "%Y-%m" )as date' \
            ' from quality_issues qiss' \
            ' WHERE DATE_FORMAT( qiss.created, "%Y-%m" )>=DATE_FORMAT("'+startdate+'", "%Y-%m" ) and DATE_FORMAT( qiss.created, "%Y-%m" )<=DATE_FORMAT("'+enddate+'", "%Y-%m" )' \
            ' and qiss.assigneeName is not null and LENGTH(trim(qiss.assigneeName))>0'\
            ' GROUP BY DATE_FORMAT( qiss.created, "%Y-%m" ),qiss.assigneeName) iss on us.user_login_ame=iss.assigneeName and iss.date=B.dates'\
            ''+condition+''\
            ' GROUP BY B.dates,o1.organize_id,us.user_id'\
            ') o'\
            ' GROUP BY o.dates,o.organize_id'

        # print(sql)
        logger.info('质量分析图表：按月统计bug人占比、人均bug语句------'+sql)
        cursor.execute(sql)
        row1=report.dictfetchall(cursor)
        data={'code':200,'row':row1}
    except Exception as e:
        # print(e)
        logger.error('质量分析图表异常：'+e)
        data={'code':500}
    return JsonResponse(data)

# sql='select  isss.organize_name,isss.organize_id, isss.parent_organize_id,COUNT(isss.organize_id)as usercount, count(isss.assigneeName)as bugusercount,sum(isss.bugcount)as bugCount ,' \
#     ' ROUND(count(isss.assigneeName)/COUNT(isss.organize_id)*100,2)as numberOfBugs,ROUND(sum(isss.bugcount)/COUNT(isss.organize_id),2)as perCapitaAll,' \
#     '(CASE WHEN ROUND(sum(isss.bugcount)/count(isss.assigneeName),2) is null THEN 0 ELSE ROUND(sum(isss.bugcount)/count(isss.assigneeName),2)END)as perCapita ,isss.dates '\
#     ' from(' \
#     ' SELECT o.organize_id,o.organize_name, iss.assigneeName,count(iss.assigneeName)as bugcount,o.parent_organize_id,o.dates from '\
#     ' (SELECT DISTINCT ou.user_id_id,o1.organize_id,o1.organize_name,us.user_id,o1.parent_organize_id,us.user_login_ame, B.dates'\
#     ' from quality_organize o1'+sql2+'' \
#     ' left join quality_user us on  ou.user_id_id=us.user_id' \
#     ' inner join (SELECT @num :=@num+1,DATE_FORMAT(ADDDATE(DATE_SUB("'+startdate+'",INTERVAL 1 month),INTERVAL @num+1 month),"%Y-%m") AS dates' \
#     ' FROM quality_user,(SELECT @num := -1) t' \
#     ' WHERE ADDDATE("'+startdate+'",INTERVAL @num month) <= DATE_FORMAT("'+enddate+'", "%Y-%m")'\
#     ' ORDER BY dates'\
#     ') B on B.dates>=date_format(us.user_initiation_time, "%Y-%m")'\
#     ' and IF (ISNULL(us.user_departure_time) || LENGTH(trim(us.user_departure_time))<1, 0 = 0,date_format(us.user_departure_time, "%Y-%m")>=B.dates) ' \
#     ' left join (select qiss.assigneeName,COUNT(qiss.assigneeName)as bugcount,DATE_FORMAT( qiss.created, "%Y-%m" )as date' \
#     ' from quality_issues qiss' \
#     ' WHERE DATE_FORMAT( qiss.created, "%Y-%m" )>="'+startdate+'" and DATE_FORMAT( qiss.created, "%Y-%m" )<="'+enddate+'"' \
#     ' and qiss.assigneeName is not null || LENGTH(trim(qiss.assigneeName))>0'\
#     ' GROUP BY DATE_FORMAT( qiss.created, "%Y-%m" ),qiss.assigneeName) iss on us.user_login_ame=iss.assigneeName and iss.date=B.date'\
#     ''+condition+''\
#     ' GROUP BY B.dates,o1.organize_id,us.user_id'\
#     ') o'\
#     ' GROUP BY o.dates,o.organize_id,o.user_id_id'\
#     ') isss'\
#     ' GROUP BY isss.dates,isss.organize_id  '

#按月统计每个人的bug数
def findBugByUser(request):
    data={'code':200,'userBugList': [],'totals':0}
    try:
        cursor = connection.cursor()
        user_organize_id=request.POST.get('user_organize_id', '')
        pageSize=int(request.POST.get('pageSize'))
        pageIndex=int(request.POST.get('pageIndex'))
        day=request.POST.getlist('day', '')
        monthData=request.POST.getlist('monthData', '')
        day=day[0].split(',')
        monthData=monthData[0].split(',')
        startdate=day[0]
        enddate=day[1]
        start=0 #分页
        start=str((pageIndex-1)*pageSize)
        end=str(pageSize)
        condition=''
        if user_organize_id:
            condition=' WHERE o1.organize_id='+user_organize_id
            level='0'
        else:
            user_organize_id='0'
            level='-1'
        sql2=report.sqlCondition(user_organize_id,level)
        sql=' select news.*,IFNULL(isss.bugcount,0)as bugcount,isss.date from ('\
            ' SELECT DISTINCT us.user_id,us.user_login_ame, us.user_name,us.bugallcount from quality_organize o1'+sql2+'' \
            ' left join (' \
            ' SELECT u.user_login_ame,u.user_name,u.user_id,IFNULL(iss.bugallcount,0)as bugallcount from  quality_user u' \
            ' left join (' \
            ' select qiss.assigneeName,COUNT(qiss.assigneeName)as bugallcount' \
            ' from quality_issues qiss ' \
            ' WHERE DATE_FORMAT( qiss.created, "%Y-%m" )>="'+startdate+'" and DATE_FORMAT( qiss.created, "%Y-%m" )<="'+enddate+'" ' \
            ' and qiss.assigneeName is not null and LENGTH(trim(qiss.assigneeName))>0 ' \
            ' GROUP BY qiss.assigneeName ' \
            ')iss on u.user_login_ame=iss.assigneeName' \
            ')us on ou.user_id_id=us.user_id'+condition+'' \
            ' order by us.bugallcount desc' \
            ' limit '+start+','+end+''\
            ' )news ' \
            ' left join (select qis.assigneeName,COUNT(qis.assigneeName)as bugcount,DATE_FORMAT( qis.created, "%Y-%m" )as date '\
            ' from quality_issues qis  '\
            ' WHERE DATE_FORMAT( qis.created, "%Y-%m" )>="'+startdate+'" and DATE_FORMAT( qis.created, "%Y-%m" )<="'+enddate+'"  '\
            ' GROUP BY qis.assigneeName, DATE_FORMAT( qis.created, "%Y-%m" ))isss on news.user_login_ame=isss.assigneeName  '
        # print(sql)
        logger.info('质量分析：按月统计每个人的bug数 sql语句------'+sql)
        cursor.execute(sql)
        row1=report.dictfetchall(cursor)
        i=0
        # data['userBugList'].append(i)
        for row in row1:
            name=row['user_login_ame']
            flag=False
            if row1.index(row)==0:
                data['userBugList'].append(i)
                data['userBugList'][i]={
                    'name':'',
                    'loginname':'',
                    'bugallcount':0,
                }
                for month in monthData:
                    data['userBugList'][i][month]=0
                data['userBugList'][i]['loginname']=name
                data['userBugList'][i]['name']=row['user_name']
                data['userBugList'][i]['bugallcount']=row['bugallcount']
                data['userBugList'][i][row['date']]=row['bugcount']
            else:
                for user in data['userBugList']:
                    if name==user['loginname']:
                        flag=True
                        user[row['date']]=row['bugcount']
                        break
                if flag is False:
                    i+=1
                    data['userBugList'].append(i)
                    data['userBugList'][i]={
                        'name':'',
                        'loginname':'',
                        'bugallcount':0,
                    }
                    for month in monthData:
                        data['userBugList'][i][month]=0
                    data['userBugList'][i]['loginname']=name
                    data['userBugList'][i]['name']=row['user_name']
                    data['userBugList'][i]['bugallcount']=row['bugallcount']
                    data['userBugList'][i][row['date']]=row['bugcount']
        #查询总条数
        sqlcount='  SELECT count(DISTINCT ou.user_id_id) from quality_organize o1'+sql2+condition
        cursor.execute(sqlcount)
        data['totals']=cursor.fetchone()
    except Exception as e:
        # print(e)
        logger.error('质量分析按月统计每个人的bug数异常------'+e)
        data={'code':500}
    return JsonResponse(data)