from django.db import connection, transaction
from django.http.response import JsonResponse
from django.utils import timezone
from django.utils import dateparse,datastructures
import datetime
from quality.view.report import report
import logging
logger = logging.getLogger('django')

#巡检质量分析
def select_testResult_analysis(request):
    data={'code':200}
    try:
        cursor = connection.cursor()
        project_id=request.POST.get('project_id')
        day=request.POST.getlist('day', '')
        day=day[0].split(',')
        startdate=day[0]
        enddate=day[1]
        condition=''
        if project_id:
            # condition=' and p.project_id='+project_id
            condition=' and  p.project_id in (' \
                      ' select np.project_id from quality_project np right join (' \
                      ' select GROUP_CONCAT(id._ids) as ids FROM(' \
                      ' SELECT @ids as _ids' \
                      ', ( SELECT @ids := GROUP_CONCAT(project_id)' \
                      ' FROM quality_project' \
                      ' WHERE FIND_IN_SET(parent_project_id, @ids)' \
                      ' ) as cids' \
                      ' FROM quality_project,' \
                      '(SELECT @ids :="'+project_id+'") b' \
                                        ' WHERE @ids IS NOT NULL' \
                                        ')id' \
                                        ')ids on  FIND_IN_SET(np.project_id, ids.ids)' \
                                        ')  '
        pageSize=int(request.POST.get('pageSize'))
        pageIndex=int(request.POST.get('pageIndex'))
        start=str((pageIndex-1)*pageSize)
        end=str(pageSize)
        sql='select p.project_id, p.project_name,tr.project_name as programme_name,tr.test_type,tr.build_start_time as date' \
            ',COUNT(tr.project_name)as allcount '\
            ',COUNT(p1.project_name)as successcount' \
            ',COUNT(p2.project_name)as failurecount' \
            ',COUNT(p3.project_name)as warncount'\
            ',case when COUNT(p1.project_name)=0 then 0 else ROUND(COUNT(p1.project_name)/COUNT(tr.project_name), 4) end as successrate' \
            ' from quality_test_result tr'\
            ' inner join quality_project p on tr.project_key=p.project_jira_key' \
            ' left join quality_project p1 on tr.project_key=p1.project_jira_key and tr.build_status="SUCCESS"'\
            ' left join quality_project p2 on tr.project_key=p2.project_jira_key and tr.build_status!="SUCCESS"' \
            ' left join quality_project p3 on tr.project_key=p3.project_jira_key and tr.warn="YES"' \
            ' WHERE DATE_FORMAT(tr.build_start_time, "%Y-%m-%d %H:%i:%S" )>="'+startdate+'" and DATE_FORMAT(tr.build_start_time, "%Y-%m-%d %H:%i:%S" )<="'+enddate+'"'+condition+''\
            ' group by tr.project_name'\
            ' LIMIT '+start+','+end
        logger.info('sql------'+sql)
        cursor.execute(sql)
        row1=report.dictfetchall(cursor)
        countsql='select count(0) from('\
                 'select  p.project_id'\
                 ' from quality_test_result tr' \
                 ' inner join quality_project p on tr.project_key=p.project_jira_key' \
                  ' WHERE DATE_FORMAT(tr.build_start_time, "%Y-%m-%d %H:%i:%S" )>="'+startdate+'" and DATE_FORMAT(tr.build_start_time, "%Y-%m-%d %H:%i:%S" )<="'+enddate+'"'+condition+'' \
                   ' group by tr.project_name' \
                 ')t'
        cursor.execute(countsql)
        count=cursor.fetchone()
        data={'code':200,'row':row1,'totals':count}
    except Exception as e:
        logger.error('巡检质量分析异常：'+e)
        data={'code':500}
    return JsonResponse(data)


def testResult_analysis_detailed(request):
    try:
        cursor = connection.cursor()
        project_id=request.POST.get('project_id')
        day=request.POST.getlist('day', '')
        day=day[0].split(',')
        startdate=day[0]
        enddate=day[1]
        condition=''
        if project_id:
            condition=' and  p.project_id in (' \
                      ' select np.project_id from quality_project np right join (' \
                      ' select GROUP_CONCAT(id._ids) as ids FROM(' \
                      ' SELECT @ids as _ids' \
                      ', ( SELECT @ids := GROUP_CONCAT(project_id)' \
                      ' FROM quality_project' \
                      ' WHERE FIND_IN_SET(parent_project_id, @ids)' \
                      ' ) as cids' \
                      ' FROM quality_project,' \
                      '(SELECT @ids :="'+project_id+'") b' \
                                                    ' WHERE @ids IS NOT NULL' \
                                                    ')id' \
                                                    ')ids on  FIND_IN_SET(np.project_id, ids.ids)' \
                                                    ')  '
        pageSize=int(request.POST.get('pageSize'))
        pageIndex=int(request.POST.get('pageIndex'))
        start=str((pageIndex-1)*pageSize)
        end=str(pageSize)
        sql='select tr.id,p.project_name,tr.project_name as programme_name,tr.test_type,tr.total, tr.build_status,tr.build_cause,' \
            'tr.build_user,tr.success,tr.failed,tr.failed_type,tr.failed_analysis' \
            ' from quality_test_result tr' \
            ' left join quality_project p on tr.project_key=p.project_jira_key' \
            ' WHERE DATE_FORMAT(tr.build_start_time, "%Y-%m-%d %H:%i:%S" )>="'+startdate+'" and DATE_FORMAT(tr.build_start_time, "%Y-%m-%d %H:%i:%S" )<="'+enddate+'"'+condition+'' \
            ' ORDER BY tr.build_start_time DESC ' \
            ' LIMIT '+start+','+end
        logger.info('sql------'+sql)
        cursor.execute(sql)
        row1=report.dictfetchall(cursor)
        countsql='select count(0)' \
                 ' from quality_test_result tr' \
                 ' left join quality_project p on tr.project_key=p.project_jira_key' \
                 ' WHERE DATE_FORMAT(tr.build_start_time, "%Y-%m-%d %H:%i:%S" )>="'+startdate+'" and DATE_FORMAT(tr.build_start_time, "%Y-%m-%d %H:%i:%S" )<="'+enddate+'"'+condition
        logger.info('countsql------'+countsql)
        cursor.execute(countsql)
        count=cursor.fetchone()
        data={'code':200,'detailRow':row1,'detailTotals':count}
    except Exception as e:
        logger.error('巡检质量分析明细异常：'+e)
        data={'code':500}
    return JsonResponse(data)