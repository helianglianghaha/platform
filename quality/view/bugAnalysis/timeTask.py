from apscheduler.schedulers.background import BackgroundScheduler
from quality.common.commonbase import commonList
from quality.common.logger import Log
from django.http.response import JsonResponse
import mysql.connector
log=Log()
#添加定时任务
scheduler = BackgroundScheduler()
import time
import datetime

def compare_and_sync(source_cursor,target_conn, target_cursor, source_table, target_table):
    '''对比数据'''
    log.info("compare_and_sync开始执行")
    target_sql='''SELECT COLUMN_NAME
        FROM information_schema.columns
        WHERE table_schema = 'testplatform'
        AND table_name = '{target_table}'
    '''.format(target_table=target_table)

    result_rows=commonList().getModelData(target_sql)
    columns = [column['COLUMN_NAME'] for column in result_rows]
    columns_str = ','.join(columns)
    source_query=f"SELECT {columns_str} FROM {source_table}".format(columns_str,source_table)
    import  re
    if target_table=='zt_bug':
        source_query=re.sub(r'\b(case|status|lines)\b(?!Version)', r'`\1`', source_query)
        source_query = source_query + " order by id desc"
    if target_table=='zt_module':
        source_query = re.sub(r'\b(name|order|from|owner)\b(?!Version)', r'`\1`', source_query)
        source_query=source_query+" order by id desc"
    if target_table == 'zt_product':
        source_query = re.sub(r'\b(name|code|status|desc|order)\b(?!Version)', r'`\1`', source_query)
        source_query = source_query + " order by id desc"
    if target_table == 'zt_build':
        source_query = re.sub(r'\b(name|date|desc|order)\b(?!Version)', r'`\1`', source_query)
        source_query = source_query + " order by id desc"

    if target_table=='zt_project':
        source_query = re.sub(r'\b(name|code|end|firstEnd|parallel|realBegan|begin|desc|left|order)\b(?!Version)', r'`\1`', source_query)
        # source_query =source_query+" order by id desc"
        print("=====source_query=====",source_query)

    source_rows = commonList().getSignModeldata(source_cursor,source_query)

    # try:
    if target_table=="zt_bug":
        number = 1
        for row in source_rows:
            # print("当前执行的数据", row)
            from .sqlData import selectSqlData
            selectSqlData().insert_or_update_data(target_cursor, target_conn, row,target_table)
            number += 1
            if number >= 400:
                break

    else:
        for row in source_rows:
            # print("当前执行的数据", row)
            from .sqlData import selectSqlData
            selectSqlData().insert_or_update_data(target_cursor, target_conn, row,target_table)

def sync_tables():
    # 连接源数据库和目标数据库
    log.info('sync_tables开始执行')
    source_conn = mysql.connector.connect(
        host='120.55.13.41',
        user='zentao',
        password='X323pjDHsf6K3Fxs',
        database='zentao'
    )
    source_cursor = source_conn.cursor()

    target_conn = mysql.connector.connect(
        host='118.178.255.171',
        user='store',
        password='UUueBYYs9U4uptj',
        database='testplatform'
    )
    target_cursor = target_conn.cursor()

    # try:
    # 同步 zt_bug 表
    compare_and_sync(source_cursor,target_conn, target_cursor, 'zt_bug', 'zt_bug')

    # 同步 zt_module 表
    compare_and_sync(source_cursor,target_conn, target_cursor, 'zt_module', 'zt_module')

    # 同步 zt_product 表
    compare_and_sync(source_cursor,target_conn, target_cursor, 'zt_product', 'zt_product')

    # 同步 zt_build 表
    compare_and_sync(source_cursor, target_conn, target_cursor, 'zt_build', 'zt_build')

    # 同步 zt_project 表
    compare_and_sync(source_cursor,target_conn, target_cursor, 'zt_project', 'zt_project')


    source_cursor.close()
    source_conn.close()
    target_cursor.close()
    target_conn.close()

    data = {
        "code": 200,
        "data": "同步成功"
    }
    return JsonResponse(data, safe=False)

#版本信息定时通知
def update_versioninfo(request):
    '''更新版本信息'''
    try:
        # Check if today is Sunday
        if datetime.datetime.now().weekday() == 6:  # Sunday is represented by 6
            # print("Today is Sunday. Skipping interface update.")
            return
        #查询正在测试中的版本，负责人，BUG，123进度，备注
        totalVersionSql="select * from quality_versionmanager where  status=\'测试中\'"
        totalVersionData=commonList().getModelData(totalVersionSql)

        # 获取未解决BUG
        unsolvesql = "select count(*) as number from zt_bug where status=\'active\'"
        unsolveData = commonList().getModelData(unsolvesql)
        unsolveDataNumber=unsolveData[0]['number']

        # 每日新增BUG
        todayBug = 'select  count(*) as number from zt_bug where Date(openedDate)=CURRENT_DATE'
        todayBugData = commonList().getModelData(todayBug)
        todayBugDataNumber=todayBugData[0]['number']

        versionStart='> 来活了，以下为测试中版本信息'
        for versioninfo in totalVersionData:
            # print('获取的版本',versioninfo)
            version=versioninfo['version']
            description = versioninfo['description']
            owner = versioninfo['owner']
            development = versioninfo['development']
            status = versioninfo['status']
            testCases = versioninfo['testCases']
            testCaseReview = versioninfo['testCaseReview']
            firstRoundTest = versioninfo['firstRoundTest']
            secondRoundTest = versioninfo['secondRoundTest']
            thirdRoundTest=versioninfo['thirdRoundTest']
            remarks = versioninfo['remarks']

            if len(testCases)==0:
                testCases=0
            if len(testCaseReview)==0:
                testCaseReview=0
            if len(firstRoundTest)==0:
                firstRoundTest=0
            if len(secondRoundTest)==0:
                secondRoundTest=0
            if len(thirdRoundTest)==0:
                thirdRoundTest=0

            versionInfo='''\n> 版本 : {} \n> 需求 : {}\n> 负责人 : {}\n> 开发者 : {}\n> 需求状态 ：{} \n> 编写测试用例 ：{}%\n> 测试用例评审 ：{}%\n> 一轮测试进度 ：{}%\n> 二轮测试进度 ：{}%\n> 三轮测试进度 ：{}%\n> 版本备注 ：{}
                        '''.format(version, description, owner,development,status,testCases,testCaseReview,firstRoundTest, secondRoundTest,thirdRoundTest,remarks)
            versionStart=versionStart+versionInfo+'\n'
            # print('=====versionInfo======', versionInfo)
        versionStart=versionStart+'''
        \n>所有版本未解决BUG : {}个\n>今日新增BUG : {}个
        '''.format(unsolveDataNumber,todayBugDataNumber)
        totalCurl='''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
                        -H 'Content-Type: application/json' \
                        --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
                        --compressed
                        '''.format(content=versionStart)
        # print('totalCurl',totalCurl)
        import os
        # 没有获取到测试中的版本，不用执行通知
        if len(totalVersionData)==0:
            totalCurl = '''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
                        -H 'Content-Type: application/json' \
                        --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
                        --compressed
                        '''.format(content="一个测试中的版本都没有，今天是个平安夜")
            os.system(totalCurl)
        else:
            os.system(totalCurl)
    except Exception as e:
        msg = '''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
                -H 'Content-Type: application/json' \
                --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
                --compressed
                '''.format(content=e)
        import os
        os.system(msg)

def update_bug_info(request):
    '''同步最近一个版本的BUG信息'''
    try:
        sql='''
            SELECT 
            b.name,
            SUM(CASE WHEN a.severity = '4' THEN 1 ELSE 0 END) AS suggestion_count,
            SUM(CASE WHEN a.severity = '3' THEN 1 ELSE 0 END) AS prompt_count,
            SUM(CASE WHEN a.severity = '2' THEN 1 ELSE 0 END) AS normal_count,
            SUM(CASE WHEN a.severity = '1' THEN 1 ELSE 0 END) AS serious_count,
            SUM(CASE WHEN a.status = 'active' THEN 1 ELSE 0 END) AS active_count,
            SUM(CASE WHEN a.status = 'resolved' THEN 1 ELSE 0 END) AS resolved_count,
            SUM(CASE WHEN a.status = 'closed' THEN 1 ELSE 0 END) AS closed_count,
            COUNT(*) AS total_count
            FROM zt_bug a
            LEFT JOIN zt_project b ON a.execution = b.id
            where b.name is NOT NULL
            GROUP BY b.name
            ORDER BY MAX(a.openedDate) DESC
        '''

        bugData=commonList().getModelData(sql)
        suggestion_count=bugData[0]['suggestion_count']
        prompt_count = bugData[0]['prompt_count']
        normal_count = bugData[0]['normal_count']
        serious_count = bugData[0]['serious_count']
        open_count = bugData[0]['active_count']
        close_count = bugData[0]['resolved_count']
        version_report=bugData[0]['name']

        versionInfo = '''\n====> 最新版本BUG解决情况如下 <====\n>版本 : 【{}】\n> 致命级别 : {}个 \n> 严重级别 : {}个\n> 一般级别 : {}个\n> 提示级别 : {}个 \n> 未解决BUG ：{}个\n> 已解决BUG ：{}个 记得及时关闭
                            '''.format(version_report, serious_count, normal_count, prompt_count, suggestion_count, open_count, close_count
                                       )
        bugCurl='''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
                -H 'Content-Type: application/json' \
                --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
                --compressed
                '''.format(content=versionInfo)
        import os
        os.system(bugCurl)

    except Exception as e:
        msg = '''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
            -H 'Content-Type: application/json' \
            --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
            --compressed
            '''.format(content=e)
        import os
        os.system(msg)


# Schedule updates at 9:00 AM, 11:00 AM, and 6:00 PM on non-Sundays
# scheduler.add_job(update_versioninfo, 'cron', hour=9)
# scheduler.add_job(update_versioninfo, 'cron', hour=11)
# scheduler.add_job(update_versioninfo, 'cron', hour=20)
#
scheduler.add_job(sync_tables, 'interval', minutes=10)
#
# scheduler.add_job(update_bug_info, 'cron', hour=9)
# scheduler.add_job(update_bug_info, 'cron', hour=12)
# scheduler.add_job(update_bug_info, 'cron', hour=20)
#
scheduler.start()
