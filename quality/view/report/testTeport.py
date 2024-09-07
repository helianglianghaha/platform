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


    #根据版本内容查询禅道实际版本
    actlSql='''
            SELECT DISTINCT(version) from quality_versionmanager where tableID=\'{}\'
            '''.format(versionName)
    versionList=commonList().getModelData(actlSql)
    singleVersion=versionList[0]['version']

    versiondata='''
            SELECT 
            SUM(CASE WHEN modelStatus LIKE '%开发中%' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN modelStatus LIKE '%测试中%' THEN 1 ELSE 0 END) AS testing_count,
            SUM(CASE WHEN modelStatus LIKE '%已测试待上线%' THEN 1 ELSE 0 END) AS already_count,
            SUM(CASE WHEN modelStatus LIKE '%已上线%' THEN 1 ELSE 0 END) AS ready_count,
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
       SELECT
            * 
        FROM
            zt_bug
            where execution =
        ( SELECT a.id FROM zt_project a LEFT JOIN zt_project b ON a.project = b.id WHERE a.project != 0 AND a.team = \'{}\' )
            ) AS zt_bug
            GROUP BY DATE(closedDate)
            ORDER BY event_date
            '''.format(singleVersion)
    print('resolve_bugs_sql',resolve_bugs_sql)
    resolve_bugs_list=commonList().getModelData(resolve_bugs_sql)

    #获取测试点的信息
    xmindCasesSql='''
        SELECT
            COUNT(id) AS total_num,
            SUM(CASE WHEN result = '成功' THEN 1 ELSE 0 END) AS success_count,
            SUM(CASE WHEN result = '未执行' THEN 1 ELSE 0 END) AS undo_count,
            SUM(CASE WHEN result = '阻塞' THEN 1 ELSE 0 END) AS pending_count,
            SUM(CASE WHEN result = '失败' THEN 1 ELSE 0 END) AS failed_count
        FROM
            quality_xmind_data 
        WHERE
            version = \'{}\'
        '''.format(versionName)
    ximdData=commonList().getModelData(xmindCasesSql)



    # 获取该版本周期内每天新增的BUG数
    numbers_bugs_sql = '''
    SELECT DATE(openedDate) AS event_date, COUNT(*) AS bug_count
    FROM (SELECT DISTINCT b.id m,b.title, b.`status`,b.openedDate
    FROM zt_bug b
    where execution =
    ( SELECT a.id FROM zt_project a LEFT JOIN zt_project b ON a.project = b.id WHERE a.project != 0 AND a.team = \'{}\' )
    ) as zt_bug
    GROUP BY DATE(openedDate)
    ORDER BY event_date'''.format(singleVersion)
    numbers_bugs_everydata = commonList().getModelData(numbers_bugs_sql)

    # 获取该版本周期内BUG总体解决情况
    bugs_count_sql='''
        SELECT 
        COUNT(*) AS bug_count,
        SUM(CASE WHEN `status` = 'active' THEN 1 ELSE 0 END) AS active_bug_count,
        SUM(CASE WHEN `status` = 'resolved' THEN 1 ELSE 0 END) AS resolved_bug_count,
        SUM(CASE WHEN `status` = 'closed' THEN 1 ELSE 0 END) AS closed_bug_count
        FROM (
            SELECT
            * 
        FROM
            zt_bug
            where execution =
        ( SELECT a.id FROM zt_project a LEFT JOIN zt_project b ON a.project = b.id WHERE a.project != 0 AND a.team = \'{}\' )
                ) AS zt_bug
            '''.format(singleVersion)
    print("获取该版本周期内BUG总体解决情况",bugs_count_sql)

    #获取最近五个版本的测试点执行情况
    versionXmindSql='''
        SELECT
		version,
		COUNT(*) as total_num,
		SUM(CASE WHEN result = '成功' THEN 1 ELSE 0 END) AS success_count,
		SUM(CASE WHEN result = '未执行' THEN 1 ELSE 0 END) AS undo_count,
		SUM(CASE WHEN result = '阻塞' THEN 1 ELSE 0 END) AS pending_count,
		SUM(CASE WHEN result = '失败' THEN 1 ELSE 0 END) AS failed_count
		FROM
				quality_xmind_data
		where 
			version=\'{}\'
		GROUP BY
				version
		ORDER BY
				version DESC
        '''.format(versionName)
    versionXmindList=commonList().getModelData(versionXmindSql)

    versionNameList=[]
    total_num_list=[]
    success_count_list=[]
    undo_count_list=[]
    pending_count_list=[]
    failed_count_list=[]
    BUG_Cases_Rate=[]
    BUG_number_list=[]

    #分类处理版本数据
    if len(versionXmindList)!=0:
        for versionInfo in versionXmindList:
            print("99999999999{}".format(versionInfo))
            versionNameList.append(versionInfo['version'])
            total_num_list.append(int(versionInfo['total_num']))
            success_count_list.append(int(versionInfo['success_count']))
            undo_count_list.append(int(versionInfo['undo_count']))
            pending_count_list.append(int(versionInfo['pending_count']))
            failed_count_list.append(int(versionInfo['failed_count']))
            totalBugNumList='''
                        SELECT 
                        COUNT(*) AS bug_count,
                        SUM(CASE WHEN `status` = 'active' THEN 1 ELSE 0 END) AS active_bug_count
                        FROM (
                            SELECT DISTINCT b.id AS m, b.title, b.`status`, b.openedDate
                            FROM zt_bug b
                            where execution =
                            ( SELECT a.id FROM zt_project a LEFT JOIN zt_project b ON a.project = b.id WHERE a.project != 0 AND a.team = \'{}\' )
                        ) AS zt_bug
                    '''.format(singleVersion)
            print("分类处理版本数据",totalBugNumList)
            everyOwnerDataList=commonList().getModelData(totalBugNumList)
            BugTotalNum=everyOwnerDataList[0]['bug_count']
            BUG_number_list.append(BugTotalNum)
            total_count=int(versionInfo['success_count'])+int(versionInfo['pending_count'])+int(versionInfo['failed_count'])
            if total_count!=0:
                BugCasesRate=round((BugTotalNum/total_count)*100,2)
            else:
                BugCasesRate=0
            BUG_Cases_Rate.append(BugCasesRate)


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
                (
                SELECT
                    * 
                FROM
                    zt_bug
                    where execution =
                ( SELECT a.id FROM zt_project a LEFT JOIN zt_project b ON a.project = b.id WHERE a.project != 0 AND a.team = \'{}\' )
                ) b
                LEFT JOIN auth_user j ON j.username = b.openedBy
            WHERE
                j.username IS NOT NULL
        ) AS j 
    GROUP BY
        j.first_name
    '''.format(singleVersion)
    everyOwnerDataList=commonList().getModelData(everyOwnerSql)


    # 获取负责人
    ownerSql='''
        select owner,development,product from quality_versionmanager  where tableID=\'{}\'
    '''.format(versionName)
    ownerTotalData=commonList().getModelData(ownerSql)
    print('ownerTotalData',ownerTotalData)

    all_owners = list(set(owner for item in ownerTotalData for owner in eval(item['owner']) if item['owner'] and item['owner'] != '[]'))

    all_developments = list(set(dev for item in ownerTotalData for dev in eval(item['development']) if item['development'] and item['development'] != '[]'))

    all_prd = list(set(prd for item in ownerTotalData for prd in eval(item['product']) if item['product'] and item['product'] != '[]'))


    unique_owners = list(set(all_owners))
    unique_developments = list(set(all_developments))
    unique_prd=list(set(all_prd))
    owner_string=', '.join(unique_owners)
    development_string=', '.join(unique_developments)
    prd_string=', '.join(unique_prd)
    print(unique_owners)
    print(unique_developments)


    status_sql_list=commonList().getModelData(bugs_count_sql)
    versionListData=commonList().getModelData(versiondata)
    testCaseList = commonList().getModelData(testCasesData)

    data={
        "code":200,
        "version":versionListData, #版本信息
        "testCasefInfo":testCaseList, #用例执行信息
        "ximdDataInfo":ximdData,
        "resolve_bugList":resolve_bugs_list,  #该版本每天所有BUG解决情况
        "totalBugList":status_sql_list, #该版本所有BUG解决情况
        "addBugNumList":numbers_bugs_everydata, #每日新增BUG数
        "ownerList":owner_string, #获取负责人
        "developmentList":development_string,#获取研发人员
        "product":prd_string,
        "everyOwnerList":everyOwnerDataList, #获取每个人提的BUG
        "versionList":versionNameList,
        "totalNumList":total_num_list,
        "successNumList":success_count_list,
        "undoNumList":undo_count_list,
        "pendingNumList":pending_count_list,
        "failedNumList":failed_count_list,
        "BugCasesRate":BUG_Cases_Rate,
        "BugNumList":BUG_number_list
    }

    return  JsonResponse(data, safe=False)