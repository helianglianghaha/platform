from apscheduler.schedulers.background import BackgroundScheduler
from quality.common.commonbase import commonList
from quality.common.logger import Log
from django.http.response import JsonResponse
import mysql.connector
log=Log()
#添加定时任务
scheduler = BackgroundScheduler()
import time
import datetime,json,os,shutil

def compare_and_sync(source_cursor,target_conn, target_cursor, source_table, target_table):
    '''对比数据'''
    log.info("compare_and_sync开始执行")
    target_sql='''SELECT COLUMN_NAME
        FROM information_schema.columns
        WHERE table_schema = 'testplatfrom'
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

def sync_tables(request):
    # 连接源数据库和目标数据库
    try:
        log.info('sync_tables开始执行')
        source_conn = mysql.connector.connect(
            host='120.55.13.41',
            user='zentao',
            password='X323pjDHsf6K3Fxs',
            database='zentao'
        )
        source_cursor = source_conn.cursor()

        target_conn = mysql.connector.connect(
            host='192.168.8.28',
            user='root',
            password='mysql_ciFtek',
            database='testplatfrom'
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
    except Exception as e:
        dingSendMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2','BUG同步禅道出错{}'.format(e))
        return JsonResponse('BUG同步禅道出错{}'.format(e), safe=False)

#版本信息定时通知
def update_versioninfo(request):
    '''更新版本信息'''
    try:
        # Check if today is Sunday
        if datetime.datetime.now().weekday() == 6:  # Sunday is represented by 6
            # print("Today is Sunday. Skipping interface update.")
            return
        #查询正在测试中的版本，负责人，BUG，123进度，备注
        totalVersionSql="select * from quality_versionmanager where  modelStatus like \'%测试中%\'"
        totalVersionData=commonList().getModelData(totalVersionSql)

        # 获取未解决BUG
        unsolvesql = "select count(*) as number from zt_bug where status=\'active\'"
        unsolveData = commonList().getModelData(unsolvesql)
        unsolveDataNumber=unsolveData[0]['number']

        # 每日新增BUG
        todayBug = 'select  count(*) as number from zt_bug where Date(openedDate)=CURRENT_DATE'
        todayBugData = commonList().getModelData(todayBug)
        todayBugDataNumber=todayBugData[0]['number']

        if len(totalVersionData)==0:
            return JsonResponse('没有测试中的版本，不用通知',safe=False)

        versionStart='> 来活了，以下为测试中版本信息'
        for versioninfo in totalVersionData:
            # print('获取的版本',versioninfo)
            version=versioninfo['version']
            description = versioninfo['description']
            owner = versioninfo['owner']
            development = versioninfo['development']
            status = versioninfo['status']
            testCases = versioninfo['testCases']
            product=versioninfo['product']
            testingTime=versioninfo['testingTime']
            liveTime=versioninfo['liveTime']
            testCaseReview = versioninfo['testCaseReview']
            firstRoundTest = versioninfo['firstRoundTest']
            secondRoundTest = versioninfo['secondRoundTest']
            thirdRoundTest=versioninfo['thirdRoundTest']
            remarks = versioninfo['remarks']
            tableID=versioninfo['tableID']

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

            versionInfo='''
                \n\n > 迭代 : <font color=#303133>{}</font> 
                \n\n > 版本 : <font color=#303133>{}</font> 
                \n\n > 需求 : <font color=#303133>{}</font>  
                \n\n > 负责人 : <font color=#303133>{}</font>  
                \n\n > 开发者 : <font color=#303133>{}</font>  
                \n\n > 产品 : <font color=#303133>{}</font>  
                \n\n > 需求状态 ：<font color=#303133>{}</font>  
                \n\n > 提测时间 ：<font color=#303133>{}</font>  
                \n\n > 上线时间 ：<font color=#303133>{}</font>  
                \n\n > 编写测试用例 ：<font color=#303133>{}%</font>  
                \n\n > 测试用例评审 ：<font color=#303133>{}%</font>  
                \n\n > 一轮测试进度 ：<font color=#303133>{}%</font>  
                \n\n > 二轮测试进度 ：<font color=#303133>{}%</font>  
                \n\n > 三轮测试进度 ：<font color=#303133>{}%</font>
                \n\n > 版本备注：<font color=#303133>{}</font>
                \n
                        '''.format(tableID,version, description, owner,development,product,status,testingTime,liveTime,testCases,testCaseReview,firstRoundTest, secondRoundTest,thirdRoundTest,remarks)
            versionStart=versionStart+versionInfo+'\n'
            # print('=====versionInfo======', versionInfo)

        dingSendMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2',versionStart)
        
        # totalCurl='''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
        #                 -H 'Content-Type: application/json' \
        #                 --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
        #                 --compressed
        #                 '''.format(content=versionStart)
        # print('totalCurl',totalCurl)
        import os
        # 没有获取到测试中的版本，不用执行通知
        

        return JsonResponse('版本内容更新成功',safe=False)

    except Exception as e:
        log.info(' error{}'.format(e))
        dingSendMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2','版本内容同步出出错{}'.format(e))
        return JsonResponse('版本内容更新失败{}'.format(e),safe=False)

def dingSendMessage(url,versionStart):
    '''叮叮消息通知'''
    import requests
    import json
    payload = json.dumps({
    "msgtype": "markdown",
    "markdown": {
        "title": "版本信息通知",
        "text": versionStart,
        "at": {
        "isAtAll": True
        }
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=payload)

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

        versionInfo = '''
                    \n\n<font color=#303133>====> 最新版本BUG解决情况如下 <====</font> 
                    \n\n>版本 : 【<font color=#303133>{}</font> 】
                    \n\n> 致命级别 : <font color=#303133>{}</font> 个 
                    \n\n> 严重级别 : <font color=#303133>{}</font> 个
                    \n\n> 一般级别 : <font color=#303133>{}</font> 个
                    \n\n> 提示级别 : <font color=#303133>{}</font> 个 
                    \n\n> 未解决BUG ：<font color=#303133>{}</font> 个
                    \n\n> 已解决BUG ：<font color=#303133>{}</font> 个 记得及时关闭
                            '''.format(version_report, serious_count, normal_count, prompt_count, suggestion_count, open_count, close_count
                                       )
        dingSendMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2',versionInfo)
        
        # bugCurl='''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
        #         -H 'Content-Type: application/json' \
        #         --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
        #         --compressed
        #         '''.format(content=versionInfo)
        # import os
        # os.system(bugCurl)

    except Exception as e:
        log.info('出错了{}'.format(e))
        dingSendMessage('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2','同步最近一个版本的BUG信息{}'.format(e))
        # msg = '''curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cb28dc5d-9ebc-4928-9fa0-bf0648934fba' \
        #     -H 'Content-Type: application/json' \
        #     --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{content}"，"mentioned_mobile_list":[""]}}'
        #     --compressed
        #     '''.format(content=e)
        # import os
        # os.system(msg)

def exectSingleProject(requestData,dingAddress):
    '''单个项目执行'''
    executeType=requestData["executeType"]
    buildAddress=requestData["buildAddress"]
    performanceData=requestData["performanceData"]
    scriptName=requestData["scriptName"]
    sceiptProject_id=requestData['sceiptProject_id']
    environment=requestData['environment']
    platfromName=requestData['platfromName']
    platfromType=requestData['platfromType']

    # 格式化脚本
    import ast
    scriptName = ast.literal_eval(scriptName)

    if environment=='1':
        execteEnvironment='测试环境'
    
    if environment=='2':
        execteEnvironment='生产环境'

    # 获取项目地址
    projectName_id = requestData['projectName']
    sql = 'select modelData from quality_modeldata where modeldata_id= ' + str(projectName_id)
    projectName = (commonList().getModelData(sql))


    # 获取版本地址
    modelDataId = requestData['sceiptProject_id']
    # modelDataSql = 'select modelData from quality_modeldata where modeldata_id= ' + str(modelDataId)
    # modelDataLIst = (commonList().getModelData(modelDataSql))
    modelData = platfromName
    # log.info("获取到的项目名称{},版本名称{}".format(projectName,modelData))
    UIScriptAddress='/root/platform/playwright/UI_test_framework/testcase/'

    #判断是否有删除文件
    def check_and_delete_files(folder_path, files_to_check):
        # import logging
        # logging.basicConfig(level=logging.INFO)
        # log = logging.getLogger(__name__)
        # folder_path='/Users/hll/Desktop/apache-jmeter-5.5/script/聚好麦/聚好麦-测试环境-客服系统/'
        # files_to_check=[{'name': '客服系统-聚好麦-测试环境-星期六小卖铺.jmx', 'url': '/Users/hll/Desktop/git/platform/media/客服系统-聚好麦-测试环境-星期六小卖铺.jmx'}]
        all_files = os.listdir(folder_path)
        log.info(files_to_check)
        log.info(type(files_to_check))

        for file_name in all_files:
            # 构建文件的完整路径
            file_path = os.path.join(folder_path, file_name)
        
            # 检查文件是否存在于文件名列表中
            matching_files=[]
            for file in files_to_check:
                if file["name"] == file_name and os.path.isfile(file_path):
                    matching_files.append(file)

            # matching_files = [file for file in files_to_check if file["name"] == file_name and os.path.isfile(file_path)]
            log.info(matching_files)
            # 如果没有找到匹配的文件，删除文件
            if not matching_files:
                os.remove(file_path)
                log.info("没有匹配上文件,开始删除文件{}".format(file_path))
        
    substrings_to_check=scriptName
    if executeType in  ['0','3'] or executeType == False:#接口
        log.info("======执行接口====")

        directory_path='/root/jmeter/apache-jmeter-5.4.1/script/'+projectName[0]["modelData"] + "/" + modelData + "/"
    elif executeType == '2':#UI
        directory_path='/root/platform/playwright/UI_test_framework/testcase/'+projectName[0]["modelData"] + "/" + modelData + "/UIReport/script/"
    else:
        directory_path='/root/jmeter/apache-jmeter-5.4.1/ProScript/'+projectName[0]["modelData"] + "/" + modelData + "/"


    #删除已经删除的脚本
    check_and_delete_files(directory_path,substrings_to_check)

    #获取UI
    UIdata=requestData['UIdata']
    UIExcReport=requestData['UIExcReport']
    UIReport=requestData['UIReport']
    UIScript=requestData['UIScript']

    #创建build文件目录
    ant_build="/root/ant/apache-ant-1.9.16/build/"
    log_path="/root/platform/logs/"
    if not os.path.exists(ant_build+projectName[0]["modelData"]+"/"+modelData):
        os.makedirs(ant_build+projectName[0]["modelData"]+"/"+modelData)

    #创建测试报告文件夹
    testReportAddress='/root/platform/static/'
    if not  os.path.exists(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/ApiReport/"):
        os.makedirs(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/ApiReport/")
        os.makedirs(testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/PerformanceReport/")
        log.info("==========接口测试报告文件已创建====")

    #判断UI测试文件夹是否存在
    if not  os.path.exists(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/"):
        os.makedirs(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/results")
        os.makedirs(testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/html")
        
    #判断UI测试日志是否存在
    if not  os.path.exists(log_path + projectName[0]["modelData"] + "/" + modelData + "/UILog/"):
        os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/UILog/")
        os.mknod(log_path + projectName[0]["modelData"] + "/" + modelData + "/UILog/" + "log.text")
        log.info("=====UI文件已创建======")
    
    # #创建日志文件
    
    if not os.path.exists(log_path+projectName[0]["modelData"]+"/"+modelData+"/ApiLog/"):
        #创建日志文件夹
        os.makedirs(log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/")
        os.makedirs(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/")
    
        #创建日志文件
        os.mknod(log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text")
        os.mknod(log_path + projectName[0]["modelData"] + "/" + modelData + "/ApiLog/" + "log.text")
        log.info("======接口日志文件夹已创建=====")
        

    #创建脚本目录
    #接口脚本
    apiScriptFilePath = '/root/jmeter/apache-jmeter-5.4.1/script/'

    #性能接口脚本
    performanceScriptFilePath = '/root/jmeter/apache-jmeter-5.4.1/ProScript/'


    if not os.path.exists(apiScriptFilePath+projectName[0]["modelData"] + "/" + modelData):
        os.makedirs(apiScriptFilePath+projectName[0]["modelData"] + "/" + modelData)
    if not os.path.exists(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData):
        os.makedirs(performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData)
    if not os.path.exists(UIScriptAddress + projectName[0]["modelData"] + "/" + modelData+"/UIReport/script/"):
        os.makedirs(UIScriptAddress + projectName[0]["modelData"] + "/" + modelData+"/UIReport/script/") 
        log.info("UI文件不存在开始创建")

    
    #复制脚本到对应的文件夹
    fileUrlList=[i["url"] for i in scriptName]
    if executeType in ['0','3']  or executeType == False:#接口
        for fileUrl in fileUrlList:
            fileName = os.path.split(fileUrl)[1]  # 读取文件名
            fullFilePath = apiScriptFilePath + projectName[0]["modelData"] + "/" + modelData + "/" + fileName
            if os.path.exists(fullFilePath):
                pass
            else:
                log.info("=========================复制接口脚本=======================")
                sourceFilePath='/root/platform/media/'+fileName
                shutil.copyfile(sourceFilePath,fullFilePath)
                log.info("复制接口脚本成功{}".format(fullFilePath))
    elif executeType == '2':
        log.info("========开始复制文件=======")
        for fileUrl in fileUrlList:
            fileName = os.path.split(fileUrl)[1]  # 读取文件名
            fullFilePath = UIScriptAddress + projectName[0]["modelData"] + "/" + modelData+"/UIReport/script/"+ fileName
            if os.path.exists(fullFilePath):
                pass
            else:
                log.info("=========================开始复制UI脚本=======================")
                sourceFilePath='/root/platform/media/'+fileName
                shutil.copyfile(sourceFilePath,fullFilePath)
                log.info("=======复制UI脚本成功{}=========".format(fullFilePath))

    else:
        for fileUrl in fileUrlList:
            fileName = os.path.split(fileUrl)[1]  # 读取文件名
            fullFilePath = performanceScriptFilePath + projectName[0]["modelData"] + "/" + modelData + "/" + fileName
            if os.path.exists(fullFilePath):
                pass
            else:
                log.info("========================复制性能脚本=================")
                sourceFilePath = '/root/platform/media/' + fileName
                shutil.copyfile(sourceFilePath, fullFilePath)
                log.info("复制接口脚本成功{}".format(fullFilePath))

    testReportAddress = '/root/platform/static/'
    buildSourceFilePath = '/root/ant/apache-ant-1.9.16/build/build.xml'

    # 执行脚本前清除报告数据
    performanceReportPath = testReportAddress + projectName[0]["modelData"] + '/' + modelData + '/PerformanceReport/*'
    apiReportPatb = testReportAddress + projectName[0]["modelData"] + '/' + modelData + '/ApiReport/*'
    UIHtml=testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/html/*"

    #执行脚本前清理日志文件-jmeter执行日志文件-ant执行日志文件
    #Jmeter执行文件地址
    jmeterAPiLogPath=log_path+projectName[0]["modelData"]+"/"+modelData+"/ApiLog/"+"log.text"
    jmeterPerforLogPath=log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text"

    #执行UI脚本前清理日志- results数据-测试报告文件- log日志
    UIResult=testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/results/*"
    UILog=testReportAddress+projectName[0]["modelData"]+"/"+modelData+"/UIReport/logs/*"
    
    #Ant执行日志文件
    antApiLogPath=log_path+projectName[0]["modelData"]+"/"+modelData+"/ApiLog/"+"log.text"
    antPerForLogPath=log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text"

    if executeType in ['0','3'] or executeType==False :
        os.system("rm -rf " + jmeterAPiLogPath)
        os.system("rm -rf " + antApiLogPath)
        os.system("rm -rf " + apiReportPatb)
        log.info("接口测试执行数据清理完成")

    if executeType == '1' or executeType == True:
        os.system("rm -rf " + jmeterPerforLogPath)
        os.system("rm -rf " + antPerForLogPath)
        os.system("rm -rf " + performanceReportPath)
        log.info("性能测试执行数据清理完成")

    if executeType == '2':
        os.system("rm -rf " + UIResult)
        os.system("rm -rf " + UIHtml)
        os.system("rm -rf " + UILog)
        os.system("rm -rf "+log_path+projectName[0]["modelData"]+"/"+modelData+"/UILog/*")
        log.info("UI测试执行数据清理完成")


    os.system("rm -rf " + '/root/ant/apache-ant-1.9.16/build/' +projectName[0]["modelData"] + "/" + modelData+"/build.xml")
    log.info("=====删除日志和报告文件=====")
    # 复制build文件

    destFilePath = '/root/ant/apache-ant-1.9.16/build/' +projectName[0]["modelData"] + "/" + modelData+"/build.xml"
    shutil.copyfile(buildSourceFilePath, destFilePath)
    log.info("=======复制build文件{}======".format(destFilePath))

    # 修改build文件内容
    buildJtlData = "sed -i 's|<property name=\"jmeter.result.jtl.dir\" value=\"/root/ant/report/jtl\" />|<property name=\"jmeter.result.jtl.dir\" value="+"\"" + testReportAddress + \
    projectName[0]["modelData"] + '/' + modelData + "/ApiReport/jtl\" />|' " + destFilePath

    buildHtmlData = "sed -i 's|<property name=\"jmeter.result.html.dir\" value=\"/root/ant/report/html\" />|<property name=\"jmeter.result.html.dir\" value=" + "\"" + testReportAddress + \
                projectName[0]["modelData"] + '/' + modelData + "/ApiReport/html\" />|' " + destFilePath

    buildScriptData = "xmlstarlet ed --inplace -u '//testplans/@dir' -v '/root/jmeter/apache-jmeter-5.4.1/script/"+projectName[0]["modelData"] + '/' + modelData +"' " + destFilePath

    os.system(buildJtlData)
    os.system(buildHtmlData)
    os.system(buildScriptData)

    log.info("=====修改build文件内容=========")

    #执行前更新项目状态
    sql = 'update quality_scriptproject set runstatus=1 where sceiptProject_id='+str(sceiptProject_id)
    commonList().getModelData(sql)

    if executeType in ['0','3'] or executeType==False :
        os.system("rm -rf " + apiReportPatb)
        shellData='ant -file '+buildAddress+" run  >>"+log_path+projectName[0]["modelData"]+"/"+modelData+"/ApiLog/"+"log.text"
        log.info('shellData:{}'.format(shellData))
        

    if executeType=='1' or executeType==True:
        os.system("rm -rf " + performanceReportPath)
        shellData=performanceData+" >> "+log_path+projectName[0]["modelData"]+"/"+modelData+"/PerformanceLog/"+"log.text"
        log.info('shellData:{}'.format(shellData))


    if executeType=='2':
        os.system("rm -rf " + UIHtml)
        shellData=UIdata+" >> "+log_path+projectName[0]["modelData"]+"/"+modelData+"/UILog/"+"log.text"
        log.info('shellData:{}'.format(shellData))
    

    os.system(shellData)
    log.info("脚本已执行完成")

    #判断是否是UI自动化，根据已执行的数据生成测试报告
    if executeType=='2':
        shellData=UIExcReport+" >> "+log_path+projectName[0]["modelData"]+"/"+modelData+"/UILog/"+"log.text"
        log.info('shellData:{}'.format(shellData))
        os.system(shellData)
        log.info("=====UI测试报告已生成==========")

    #获取企信消息通知-开启状态-企信地址
    dingMessageSql = 'select ding_address,ding_version,ding_message,ding_people  from quality_dingmessage'
    dingMessageLIst = (commonList().getModelData(dingMessageSql))
    
    # # selectUserNameSql="select first_name from auth_user where username=\'{}\'".format(username)
    # # returnUserNamedata=commonList().getModelData(selectUserNameSql)
    # # if returnUserNamedata:
    # #     username=returnUserNamedata[0]['first_name']
    # # else:
    # username="自动化巡检"
    if len(dingMessageLIst)==0:
        log.info("====企信通知地址配置为空======")
    else:
        for dingmessage in dingMessageLIst:
            log.info("dingMessageLIst==={}".format(dingMessageLIst))
            # log.info("modelDataId==={}".format(modelDataId))
            import ast
            modelDataList=ast.literal_eval(dingmessage['ding_version'])
            openDingMessAge=dingmessage["ding_message"]
            dingAddress=dingmessage['ding_address']
            dingPeople=dingmessage['ding_people']
            if len(modelDataList)==0:
                log.info("====版本配置为空=====")
            else:
                if int(modelDataId) in  modelDataList:
                    reportAddress = requestData['reportAddress']
                    performanceReport = requestData['performanceReport']


                    # 根据测试报告是否生成,巡检状态,开启群通知
                    if int(executeType) in [0,3] and openDingMessAge=="True" :
                        number=0
                        while True:
                            if number>20:
                                break
                            fileExist=os.path.exists('/root/platform'+reportAddress)
                            if fileExist :
                                log.info("=======测试报告已经生成，开始企信通知======")
                                testReportAddress = '/root/platform/static/'
                                performanceJtlAddress = testReportAddress + projectName[0]["modelData"] + "/" + modelData + "/ApiReport/jtl/TestReport.jtl"

                                with open(performanceJtlAddress, 'r') as file:
                                    content = file.read()
                                # 统计总数
                                total_count = content.count('<failure>true</failure>') + content.count(
                                    '<failure>false</failure>')
                                # 统计 <failure>true</failure> 的数量
                                success_cont=content.count(
                                    '<failure>false</failure>')
                                true_count = content.count('<failure>true</failure>')

                                if true_count>0:
                                    result="构建失败"
                                else:
                                    result="构建成功"

                                # 计算占比
                                true_percentage =(success_cont / total_count) * 100 if total_count > 0 else 0
                                true_percentage = round(true_percentage, 2)
                                dingScriptMessage(dingAddress, projectName[0]["modelData"], modelData, total_count, true_count, true_percentage, result,reportAddress,execteEnvironment,platfromType)
                                
                                break
                            else:
                                import time
                                time.sleep(5)
                                log.info("没有生成测试报告，5s后台重试")
                                number+=1
                
                    else:
                        log.info("=====不满足企信推送条件=====")
                else:
                    log.info("=====没有配置该项目企信通知=======")

def XunJianExecuteScript(request):
    '''执行脚本'''
    # try:
        #查询所有需要走巡检的项目
    xunJian_sql='''
    select ding_version,ding_address from quality_dingmessage where  ding_xunjian = \'True\' AND ding_message = \'True\'
    '''
    log.info("========巡检项目开始执行========")
    ding_version=commonList().getModelData(xunJian_sql)
    for versioon_list in ding_version:
        version_id_list=eval(versioon_list['ding_version'])
        version_ding_message=versioon_list['ding_address']

        tuple_version_id_list=tuple(version_id_list)
        if len(tuple_version_id_list)==1:
            tuple_version_id_list=tuple_version_id_list[0]
            select_scriptProject_sql='''
                        select * from quality_scriptproject where sceiptProject_id = {}
            '''.format(tuple_version_id_list)
            print(select_scriptProject_sql)
            select_scriptProject_data=commonList().getModelData(select_scriptProject_sql)
            if len(select_scriptProject_data)==0:
                log.info('没有查到可执行的项目，暂不执行')
            else:
                exectSingleProject(select_scriptProject_data[0],version_ding_message)


        else:
            select_scriptProject_sql='''
                        select * from quality_scriptproject where sceiptProject_id in {}
            '''.format(tuple_version_id_list)
            print(select_scriptProject_sql)
            select_scriptProject_data=commonList().getModelData(select_scriptProject_sql)
            if len(select_scriptProject_data)==0:
                log.info('没有查到可执行的项目，暂不执行')
            else:
                for singleProjectData in select_scriptProject_data:
                    exectSingleProject(singleProjectData,version_ding_message)

    log.info("=======巡检项目结束=======")
    data = {
        "code": 200,
        "msg": "脚本开始执行，请查看日志及测试报告"
    }
    # except Exception as e:
    #     curlData = '''curl '{}' \
    #                 -H 'Content-Type: application/json' \
    #                 --data-raw '{{"msgtype": "markdown", "markdown": {{"content": "{}","mentioned_mobile_list":[]}}'
    #                 --compressed
    #                 '''.format('https://oapi.dingtalk.com/robot/send?access_token=77ea408f02f921a87f5ee61fd4fb9763581ded15d9627a3b1c1387f64d6fe3b2',e)
    #     os.system(curlData)
    #     data = {
    #         "code": 200,
    #         "msg": "脚本执行报错：{}".format(e)
    #     }
    return JsonResponse(data, safe=False)

def dingTaskMessage(request):
    '''每日任务通知'''
    import requests
    import json
    log.info("=====每日任务通知========")

    content='''
            \n\n><font color=#303133>【每日任务通知】</font> 
            \n\n><font color=#303133>今天上线需求  汇总下目前手里需求进度情况</font>
            \n\n><font color=#67C23A>今天上线需求：</font>
            \n\n><font color=#E6A23C>未提测需求数量：</font>
            \n\n><font color=#409EFF>测试中需求数量：</font>
            '''
    url = "https://oapi.dingtalk.com/robot/send?access_token=31769b8f6c90bd0270fd2a1bcaf8b0b48e0f40ef07998a9da5b18db9f084d8cb"

    payload = json.dumps({
    "msgtype": "markdown",
    "markdown": {
        "title": "任务通知",
        "text": content,
        "at": {
        "isAtAll": True
        }
    }
    })
    headers = {
    'Content-Type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=payload)

    return JsonResponse('通知成功', safe=False)


def dingScriptMessage(dingAddress,projectName,modelData, total_count, true_count, true_percentage, result,reportAddress,execteEnvironment,platfromType):
        '''叮叮消息通知'''
        import requests
        import json
        log.info("=====版本更新触发接口执行======开始推送接口自动化企信消息========")

        content='''
                \n\n><font color=#303133>本消息由系统自动发出，无需回复！</font> 
                \n\n>各位同事，大家好，以下为【<font color=#E6A23C>{}</font>】-【<font color=#E6A23C>{}</font>】项目构建信息
                \n\n>触发事件 : <font color=#409EFF>自动化巡检</font>
                \n\n>执行环境 : <font color=#E6A23C>{}</font>
                \n\n>执行平台 : <font color=#E6A23C>{}</font>
                \n\n>执行接口 : <font color=#409EFF>{}</font>个 
                \n\n>失败接口 : <font color=#F56C6C>{}</font>个
                \n\n>执行成功率 : <font color=#67C23A>{}</font>%
                \n\n>构建结果 : <font color=#E6A23C>{}</font>
                \n\n>[查看接口测试报告](http://192.168.8.22:8050{})
                '''.format(projectName,modelData,execteEnvironment,platfromType,total_count, true_count, true_percentage, result,reportAddress)
        url = dingAddress

        payload = json.dumps({
        "msgtype": "markdown",
        "markdown": {
            "title": "接口自动化",
            "text": content,
            "at": {
            "isAtAll": True
            }
        }
        })
        headers = {
        'Content-Type': 'application/json'
        }

        requests.request("POST", url, headers=headers, data=payload)
