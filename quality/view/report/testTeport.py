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

    # bug每天的解决情况
    resolve_bugs_sql='''
    SELECT DATE(closedDate) AS event_date, 
    COUNT(*) AS bug_count,
    SUM(CASE WHEN `status` = 'active' THEN 1 ELSE 0 END) AS active_bug_count,
    SUM(CASE WHEN `status` = 'resolved' THEN 1 ELSE 0 END) AS resolved_bug_count,
    SUM(CASE WHEN `status` = 'closed' THEN 1 ELSE 0 END) AS closed_bug_count
    FROM (
        SELECT DISTINCT b.id AS m, b.title, b.`status`, b.closedDate
        FROM zt_bug b
        LEFT JOIN zt_project a ON a.id = b.execution 
            AND a.project = 2 
            AND a.type = 'stage' 
            AND a.name LIKE '%v%'
        LEFT JOIN quality_versionmanager c ON c.version = a.name 
            AND c.tableID=\'{}\'
            WHERE c.version is not NULL and b.`status`='closed'
    ) AS zt_bug
    GROUP BY DATE(closedDate)
    ORDER BY event_date
    '''.format(versionName)
    print('resolve_bugs_sql',resolve_bugs_sql)
    resolve_bugs_list=commonList().getModelData(resolve_bugs_sql)


    # 获取该版本周期内每天新增的BUG数
    numbers_bugs_sql = '''
    SELECT DATE(openedDate) AS event_date, COUNT(*) AS bug_count
    FROM (SELECT DISTINCT b.id m,b.title, b.`status`,b.openedDate
    FROM zt_bug b
    LEFT JOIN zt_project a ON a.id = b.execution AND a.project = 2 AND a.type = 'stage' AND a.name LIKE '%v%'
    LEFT JOIN quality_versionmanager c ON c.version = a.name and c.tableID=\'{}\' WHERE c.version is not NULL) as zt_bug
    GROUP BY DATE(openedDate)
    ORDER BY event_date'''.format(versionName)
    numbers_bugs_everydata = commonList().getModelData(numbers_bugs_sql)


    # 获取该版本周期内BUG总体解决情况
    bugs_count_sql='''
        SELECT 
        COUNT(*) AS bug_count,
        SUM(CASE WHEN `status` = 'active' THEN 1 ELSE 0 END) AS active_bug_count,
        SUM(CASE WHEN `status` = 'resolved' THEN 1 ELSE 0 END) AS resolved_bug_count,
        SUM(CASE WHEN `status` = 'closed' THEN 1 ELSE 0 END) AS closed_bug_count
        FROM (
            SELECT DISTINCT b.id AS m, b.title, b.`status`, b.openedDate,c.version
            FROM zt_bug b
            LEFT JOIN zt_project a ON a.id = b.execution 
                AND a.project = 2 
                AND a.type = 'stage' 
                AND a.name LIKE '%v%'
            LEFT JOIN quality_versionmanager c ON c.version = a.name 
                AND c.tableID=\'{}\'
                WHERE c.version is not NULL
        ) AS zt_bug
    '''.format(versionName)

    # 获取每个人提的BUG
    everyOwnerSql='''
    SELECT
        j.first_name AS name,
        COUNT(*) AS value
    FROM
        (
            SELECT
                DISTINCT b.id m,
                b.title,
                b.`status`,
                b.openedDate,
                j.first_name,
                b.openedBy
            FROM
                zt_bug b
                LEFT JOIN zt_project a ON a.id = b.execution
                AND a.project = 2
                AND a.type = 'stage'
                AND a.NAME LIKE '%v%'
                LEFT JOIN quality_versionmanager c ON c.version = a.NAME
                LEFT JOIN auth_user j ON j.username = b.openedBy
                AND c.tableID = \'{}\'
            WHERE
                c.version IS NOT NULL
                AND j.username IS NOT NULL
        ) AS j 
    GROUP BY
        j.first_name
    '''.format(versionName)
    everyOwnerDataList=commonList().getModelData(everyOwnerSql)


    # 获取负责人
    ownerSql='''
        select owner,development from quality_versionmanager  where tableID=\'{}\'
    '''.format(versionName)
    ownerTotalData=commonList().getModelData(ownerSql)

    all_owners = [eval(item['owner'])[0] for item in ownerTotalData if item['owner'] != '[]']
    all_developments = [eval(item['development'])[0] for item in ownerTotalData if item['development'] != '[]']

    unique_owners = list(set(all_owners))
    unique_developments = list(set(all_developments))
    owner_string=', '.join(unique_owners)
    development_string=', '.join(unique_developments)
    print(unique_owners)
    print(unique_developments)


    status_sql_list=commonList().getModelData(bugs_count_sql)
    versionListData=commonList().getModelData(versiondata)
    testCaseList = commonList().getModelData(testCasesData)

    data={
        "code":200,
        "version":versionListData, #版本信息
        "testCasefInfo":testCaseList, #用例执行信息
        "resolve_bugList":resolve_bugs_list,  #该版本每天所有BUG解决情况
        "totalBugList":status_sql_list, #该版本所有BUG解决情况
        "addBugNumList":numbers_bugs_everydata, #每日新增BUG数
        "ownerList":owner_string, #获取负责人
        "developmentList":development_string,#获取研发人员
        "everyOwnerList":everyOwnerDataList #获取每个人提的BUG

        #     获取产品
    }

    return  JsonResponse(data, safe=False)