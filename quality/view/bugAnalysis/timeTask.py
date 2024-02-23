from apscheduler.schedulers.background import BackgroundScheduler
from quality.common.commonbase import commonList
#添加定时任务
scheduler = BackgroundScheduler()
import time
import datetime

#版本信息定时通知
def update_versioninfo():
    # Check if today is Sunday
    if datetime.datetime.now().weekday() == 6:  # Sunday is represented by 6
        print("Today is Sunday. Skipping interface update.")
        return
    #查询正在测试中的版本，负责人，BUG，123进度，备注
    totalVersionSql="select * from quality_versionmanager where  status=\'测试中\'"
    totalVersionData=commonList().getModelData(totalVersionSql)


    print('totalVersionData',totalVersionData)

    # 获取未解决BUG
    unsolvesql = 'select count(*) as number from quality_buganalysis where status_alias=\'新\''
    unsolveData = commonList().getModelData(unsolvesql)
    unsolveDataNumber=unsolveData[0]['number']

    # 每日新增BUG

    todayBug = 'select  count(*) as number from quality_buganalysis where Date(created)=CURRENT_DATE'
    todayBugData = commonList().getModelData(todayBug)
    todayBugDataNumber=todayBugData[0]['number']

    versionStart='> 各位烙铁，大家好，以下为测试中版本信息'
    for versioninfo in totalVersionData:
        print('获取的版本',versioninfo)
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

        versionInfo='''\n>版本 : {} \n>需求 : {}\n>负责人 : {}\n>开发者 : {}\n>需求状态 ：{} \n>编写测试用例 ：{}%\n>测试用例评审 ：{}%\n>一轮测试进度 ：{}%\n>二轮测试进度 ：{}%\n>三轮测试进度 ：{}%\n>版本备注 ：{}
                    '''.format(version, description, owner,development,status,testCases,testCaseReview,firstRoundTest, secondRoundTest,thirdRoundTest,remarks)
        versionStart=versionStart+versionInfo+'\n'
        # print('=====versionInfo======', versionInfo)
    versionStart=versionStart+'''
    \n>所有版本未解决BUG : {}个\n>今日新增BUG : {}个
    '''.format(unsolveDataNumber,todayBugDataNumber)
    totalCurl='''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
                    -H 'Content-Type: application/json' \
                    --data-raw '{{"msgtype": "text", "text": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
                    --compressed
                    '''.format(content=versionStart)
    print('totalCurl',totalCurl)

    import os
    os.system(totalCurl)

def update_bug_info():
    '''同步最近一个版本的BUG信息'''
    sql='''
        SELECT 
            version_report,
            SUM(CASE WHEN severity = 'suggestion' THEN 1 ELSE 0 END) AS suggestion_count,
            SUM(CASE WHEN severity = 'prompt' THEN 1 ELSE 0 END) AS prompt_count,
            SUM(CASE WHEN severity = 'normal' THEN 1 ELSE 0 END) AS normal_count,
            SUM(CASE WHEN severity = 'serious' THEN 1 ELSE 0 END) AS serious_count,
            SUM(CASE WHEN severity = 'critical' THEN 1 ELSE 0 END) AS critical_count,
            SUM(CASE WHEN status_alias = '新' THEN 1 ELSE 0 END) AS open_count,
            SUM(CASE WHEN status_alias = '已解决' THEN 1 ELSE 0 END) AS close_count,
            SUM(CASE WHEN status_alias = '已关闭' THEN 1 ELSE 0 END) AS closed_count,
            count(*) AS total_count,
        FROM quality_buganalysis
        GROUP BY version_report;
    '''
    bugData=commonList().getModelData(sql)

    suggestion_count=bugData[0]['suggestion_count']
    prompt_count = bugData[0]['prompt_count']
    normal_count = bugData[0]['normal_count']
    serious_count = bugData[0]['serious_count']
    critical_count = bugData[0]['critical_count']
    open_count = bugData[0]['open_count']
    close_count = bugData[0]['close_count']
    version_report=bugData[0]['version_report']

    versionInfo = '''\n====>最新版本BUG解决情况如下<====\n>版本 : 【{}】\n>致命级别 : {}个 \n>严重级别 : {}个\n>一般级别 : {}个\n>提示级别 : {}个\n>建议 ：{}个 \n>未解决BUG ：{}个\n>已解决BUG ：{}个 记得及时关闭
                        '''.format(version_report,critical_count, serious_count, normal_count, prompt_count, suggestion_count, open_count, close_count
                                   )

    bugCurl='''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
                    -H 'Content-Type: application/json' \
                    --data-raw '{{"msgtype": "text", "text": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
                    --compressed
                    '''.format(content=versionInfo)

    print('bugCurl',bugCurl)

    import os
    os.system(bugCurl)


# Schedule updates at 9:00 AM, 11:00 AM, and 6:00 PM on non-Sundays
scheduler.add_job(update_versioninfo, 'cron', hour=9)
scheduler.add_job(update_versioninfo, 'cron', hour=12)
scheduler.add_job(update_versioninfo, 'cron', hour=20)

scheduler.add_job(update_bug_info, 'cron', hour=9)
scheduler.add_job(update_bug_info, 'cron', hour=12)
scheduler.add_job(update_bug_info, 'cron', hour=20)

# scheduler.start()
  # Check every minute