from django.http.response import JsonResponse
from quality.common.logger import Log
log = Log()
import json, re, requests, ast, datetime
from quality.common.commonbase import commonList
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler

#添加定时任务
scheduler = BackgroundScheduler()
def selectReportTotal(request):
    '''查询测试报告数据'''
    requestData = json.loads(request.body)
    versionName=requestData['versionName']

    versiondata='''
            SELECT 
            SUM(CASE WHEN status = '开发中' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN status = '已上线' THEN 1 ELSE 0 END) AS ready_count,
            SUM(CASE WHEN status = '规划中' THEN 1 ELSE 0 END) AS guihua_count,
            SUM(CASE WHEN status = '待测试' THEN 1 ELSE 0 END) AS test_count,
            SUM(CASE WHEN status = '暂停' THEN 1 ELSE 0 END) AS stop_count,
            SUM(CASE WHEN status = '已测试待上线' THEN 1 ELSE 0 END) AS already_count,
            SUM(CASE WHEN status = '测试中' THEN 1 ELSE 0 END) AS testing_count,
            SUM(CASE WHEN status = '部分上线' THEN 1 ELSE 0 END) AS bufenReady_count,
            count(tableID is not NULL) AS total_version_count
            FROM quality_versionmanager
            where tableID=\'{}\'
    '''.format(versionName)

    testCasesData = '''
                SELECT 
                COALESCE(SUM(CASE WHEN actualResult = '成功' THEN 1 ELSE 0 END), 0) AS success_count,
                COALESCE(SUM(CASE WHEN actualResult = '未执行' THEN 1 ELSE 0 END), 0) AS undo_count,
                COALESCE(SUM(CASE WHEN actualResult = '阻塞' THEN 1 ELSE 0 END), 0) AS pending_count,
                COALESCE(SUM(CASE WHEN actualResult = '失败' THEN 1 ELSE 0 END), 0) AS failed_count,
                COALESCE(COUNT(versionName), 0) AS total_case_count
                FROM quality_testcasemanager
                where versionName=\'{}\'
        '''.format(versionName)

    # 获取需求的版本
    versionSql="SELECT DISTINCT(version) from quality_versionmanager WHERE tableID=\'{}\'".format(versionName)
    versionList=commonList().getModelData(versionSql)

    print(versionList)
    for version in versionList:
        bug_id_sql="select * from zt_build where name=\'{}\'".format(version['version'])
        bug_id_list=commonList().getModelData(bug_id_sql)
        if bug_id_list:
            bugs_sql="select bugs from zt_build"
            bugs_sql_list=commonList().getModelData(bugs_sql)
            print('bugs_sql_list',bugs_sql_list)
            for bug_info in bugs_sql_list:
                if bug_info['bugs']!='':
                    print('bug_info',bug_info['bugs'])
                    bug_list=bug_info['bugs'].split(",")
                    bug_tuple = tuple(int(num) for num in bug_list)

                    # bug解决情况
                    resolve_bugs_sql='''
                    SELECT 
                    COALESCE(SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END), 0) AS active_bug_count,
                    COALESCE(SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END), 0) AS resolved_bug_count,
                    COALESCE(SUM(CASE WHEN status = 'closed' THEN 1 ELSE 0 END), 0) AS closed_bug_count,
                    count(id) as total_bugs_count
                    FROM zt_bug
                    WHERE  id IN {}
                    '''.format(bug_tuple)
                    print('resolve_bugs_sql',resolve_bugs_sql)
                    resolve_bugs_list=commonList().getModelData(resolve_bugs_sql)

                    # 获取该版本周期内每天的BUG数
                    numbers_bugs_sql = '''
                    SELECT openedBy, COUNT(*) AS bug_count
                    FROM zt_bug
                    where id in {}
                    GROUP BY openedBy
                    ORDER BY bug_count DESC
                                '''.format(bug_tuple)
                    numbers_bugs_data = commonList().getModelData(numbers_bugs_sql)

                    # 获取该版本周期内每天的解决BUG数
                    bugs_count_sql='''
                    SELECT DATE(resolvedDate) AS resolved_date, COUNT(*) AS resolved_bug_count
                    FROM zt_bug
                    WHERE status = 'resolved' AND resolvedDate IS NOT NULL and id in {}
                    GROUP BY resolved_date
                    ORDER BY resolved_date
                    '''.format(bug_tuple)
                    status_sql_list=commonList().getModelData(bugs_count_sql)
                else:
                    resolve_bugs_list=[]
                    status_sql_list=[]
                    numbers_bugs_data=[]
                    log.info("no bugs found")
        else:
            resolve_bugs_list = []
            status_sql_list = []
            numbers_bugs_data = []
            log.info("版本没有关联BUGID，为空")
    versionListData=commonList().getModelData(versiondata)
    testCaseList = commonList().getModelData(testCasesData)

    data={
        "code":200,
        "version":versionListData, #版本信息
        "testCasefInfo":testCaseList, #用例执行信息
        "bugList":resolve_bugs_list,  #该版本所有BUG解决状态
        "solvedBugList":status_sql_list, #每日已解决BUG数
        "bugNumList":numbers_bugs_data #每日新增BUG数
    }

    return  JsonResponse(data, safe=False)