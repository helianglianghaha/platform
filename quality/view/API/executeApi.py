import logging,os,shutil,traceback
from quality.common.commonbase import commonList
from quality.common.logger import Log
log=Log()
class versionUpdateApi:
    def mainExecuteApi(self,newData,username):
        '''主执行'''
        try:
            import logging
            logging.info("新数据=={}".format("开始执行脚本对比"))
            self._executeApi(newData,username)
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            print("捕获的异常：", str(e))
            print("完整堆栈信息如下：")
            traceback.print_exc()

    def _executeApi(self,newData,username):
        '''执行接口脚本'''
        # [{'autoTableID': 477, 'onlinModel': ['聚好麦', '好又多', '量多多'], 'platfromType': ['商户后台', '客服', '小程序'], 'modelStatus': ['聚好麦>开发中', '好又多>开发中', '量多多>开发中']}]
        try:
            juhaomaiVersionList=[]#聚好麦
            haoyouduoVersionList=[]#好又多
            liangDuoDuoVersionList=[]#量多多
            xiaoYunVersionList=[]#小云
            touFangVersionList=[]#投放
            jiHuaSuanVersionList=[]#寄划算
            jiaFengBaoVersionList=[]#加粉宝
            gongZuoShouJiVersionList=[]#工作手机

            platfromList=[]

            #合并所有项目的数据
            for version in newData:
                logging.info("===版本更新触发接口执行=======开始执行接口项目=============")
                for status in version['modelStatus']:
                    if '聚好麦' in status:
                        juhaomaiVersionList.append(status)
                    if '好又多' in status:
                        haoyouduoVersionList.append(status)
                    if '量多多' in status:
                        liangDuoDuoVersionList.append(status)
                    if '小云' in status:
                        xiaoYunVersionList.append(status)
                    if '投放' in status:
                        touFangVersionList.append(status)
                    if '寄划算' in status:
                        jiHuaSuanVersionList.append(status)
                    if '加粉宝' in status:
                        jiaFengBaoVersionList.append(status)
                    if '工作手机' in status:
                        gongZuoShouJiVersionList.append(status)
                for plType in version['platfromType']:
                    # if plType=="小程序":
                        # platfromList.append(plType)
                    # if plType=="客服":
                        platfromList.append(plType)

            # print("=======juhaomaiVersionList========",juhaomaiVersionList)
            # print("==========platfromList============",platfromList)
                #对比平台和需求进度

            #所有列表去重
            juhaomaiVersionList=set(juhaomaiVersionList)#聚好麦
            haoyouduoVersionList=set(haoyouduoVersionList)#好又多
            liangDuoDuoVersionList=set(liangDuoDuoVersionList)#量多多
            # xiaoYunVersionList=set(xiaoYunVersionList)#小云-废弃
            touFangVersionList=set(touFangVersionList)#投放
            jiHuaSuanVersionList=set(jiHuaSuanVersionList)#寄划算
            jiaFengBaoVersionList=set(jiaFengBaoVersionList)#加粉宝
            gongZuoShouJiVersionList=set(gongZuoShouJiVersionList)#工作手机

            platfromList=set(platfromList)#执行平台类型
            platfromList=tuple(platfromList)

            logging.info("===版本类型更新触发接口执行===执行平台类型==={}".format(platfromList))


            # 聚好麦测试环境和生存环境
            # environment =1 测试&  2是生产
            juhaomaiTestEnvironment = any('测试中' in versionStatus or '已测试待上线' in versionStatus for versionStatus in juhaomaiVersionList)
            juhaomaiPrdEnvironment = any('已上线' in versionStatus for versionStatus in juhaomaiVersionList)
            #聚好麦测试环境
            if len(juhaomaiVersionList)!=0 and juhaomaiTestEnvironment:
                logging.info("版本更新触发接口执行===开始执行>执行聚好麦测试环境接口脚本")
                self._sortScript('聚好麦','1',platfromList,username)

            #聚好麦生产环境
            if len(juhaomaiVersionList)!=0 and juhaomaiPrdEnvironment:
                logging.info("版本更新触发接口执行===开始执行>执行聚好麦生产环境接口脚本")
                self._sortScript('聚好麦','2',platfromList,username)


            # 好又多测试环境和生存环境
            # environment =1 测试&  2是生产
            haoYouDuoTestEnvironment = any('测试中' in versionStatus or '已测试待上线' in versionStatus for versionStatus in haoyouduoVersionList)
            haoYouDuoPrdEnvironment = any('已上线' in versionStatus for versionStatus in haoyouduoVersionList)
            #好又多测试环境
            if len(haoyouduoVersionList)!=0 and haoYouDuoTestEnvironment:
                logging.info("开始执行>执行好又多测试环境接口脚本")
                self._sortScript('好又多','1',platfromList,username)
                
            #好又多生产环境
            if len(haoyouduoVersionList)!=0 and haoYouDuoPrdEnvironment:
                logging.info("开始执行>执行好又多生产环境接口脚本")
                self._sortScript('好又多','2',platfromList,username)



            # 量多多测试环境和生存环境
            # environment =1 测试&  2是生产
            liangDuoDuoTestEnvironment = any('测试中' in versionStatus or '已测试待上线' in versionStatus for versionStatus in liangDuoDuoVersionList)
            liangDuoDuoPrdEnvironment = any('已上线' in versionStatus for versionStatus in liangDuoDuoVersionList)
            #量多多测试环境
            if len(liangDuoDuoVersionList)!=0 and liangDuoDuoTestEnvironment:
                logging.info("开始执行>执行量多多测试环境接口脚本")
                self._sortScript('量多多','1',platfromList,username)
                
            #量多多生产环境
            if len(liangDuoDuoVersionList)!=0 and liangDuoDuoPrdEnvironment:
                logging.info("开始执行>执行量多多生产环境接口脚本")
                self._sortScript('量多多','2',platfromList,username)



            # 投放测试环境和生存环境
            # environment =1 测试&  2是生产
            touFangTestEnvironment = any('测试中' in versionStatus or '已测试待上线' in versionStatus for versionStatus in touFangVersionList)
            touFangPrdEnvironment = any('已上线' in versionStatus for versionStatus in touFangVersionList)
            #投放测试环境
            if len(touFangVersionList)!=0 and touFangTestEnvironment:
                logging.info("开始执行>执行投放测试环境接口脚本")
                self._sortScript('投放','1',platfromList,username)
                
            #投放生产环境
            if len(touFangVersionList)!=0 and touFangPrdEnvironment:
                logging.info("开始执行>执行投放生产环境接口脚本")
                self._sortScript('投放','2',platfromList,username)

            # 寄划算测试环境和生存环境
            # environment =1 测试&  2是生产
            jiHuaSuanTestEnvironment = any('测试中' in versionStatus or '已测试待上线' in versionStatus for versionStatus in jiHuaSuanVersionList)
            jiHuaSuanPrdEnvironment = any('已上线' in versionStatus for versionStatus in jiHuaSuanVersionList)
            #寄划算测试环境
            if len(jiHuaSuanVersionList)!=0 and jiHuaSuanTestEnvironment:
                logging.info("开始执行>执行寄划算测试环境接口脚本")
                self._sortScript('寄划算','1',platfromList,username)
                
            #寄划算生产环境
            if len(jiHuaSuanVersionList)!=0 and jiHuaSuanPrdEnvironment:
                logging.info("开始执行>执行寄划算生产环境接口脚本")
                self._sortScript('寄划算','2',platfromList,username)

            # 加粉宝测试环境和生存环境
            # environment =1 测试&  2是生产
            jiaFengBaoTestEnvironment = any('测试中' in versionStatus or '已测试待上线' in versionStatus for versionStatus in jiaFengBaoVersionList)
            jiaFengBaoEnvironment = any('已上线' in versionStatus for versionStatus in jiaFengBaoVersionList)
            #加粉宝测试环境
            if len(jiaFengBaoVersionList)!=0 and jiaFengBaoTestEnvironment:
                logging.info("开始执行>执行加粉宝测试环境接口脚本")
                self._sortScript('加粉宝','1',platfromList,username)
                
            #加粉宝生产环境
            if len(jiaFengBaoVersionList)!=0 and jiaFengBaoEnvironment:
                logging.info("开始执行>执行工作手机生产环境接口脚本")
                self._sortScript('工作手机','2',platfromList,username)

            # 工作手机测试环境和生存环境
            # environment =1 测试&  2是生产
            gongZuoShouJiTestEnvironment = any('测试中' in versionStatus or '已测试待上线' in versionStatus for versionStatus in gongZuoShouJiVersionList)
            gongZuoShouJiPrdEnvironment = any('已上线' in versionStatus for versionStatus in gongZuoShouJiVersionList)

            #工作手机测试环境
            if len(gongZuoShouJiVersionList)!=0 and gongZuoShouJiTestEnvironment:
                logging.info("开始执行>执行工作手机测试环境接口脚本")
                self._sortScript('工作手机','1',platfromList,username)
                
            #工作手机生产环境
            if len(gongZuoShouJiVersionList)!=0 and gongZuoShouJiPrdEnvironment:
                logging.info("开始执行>执行工作手机生产环境接口脚本")
                self._sortScript('工作手机','2',platfromList,username)
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            print("捕获的异常：", str(e))
            print("完整堆栈信息如下：")
            traceback.print_exc()

        
    def _sortScript(self,platfrom,environment,platfromTpyeList,username):
        '''筛选项目和平台类型'''
        if len(platfromTpyeList)==1:
            sql='''
            SELECT
            a.*, 
            c.*, 
            d.modeldata
            FROM
                quality_scriptproject a
            JOIN
                auth_user c ON a.creater = c.username
            JOIN
                quality_modeldata d ON a.projectName=d.modeldata_id
            WHERE
                a.environment = \'{}\'
                and d.modelData=\'{}\'
                and a.platfromType = \'{}\'
                and a.status=\'True\'
            ORDER BY
                a.createtime DESC
                '''.format(environment,platfrom,platfromTpyeList[0])
            
        else:
            sql='''
            SELECT
            a.*, 
            c.*, 
            d.modeldata
            FROM
                quality_scriptproject a
            JOIN
                auth_user c ON a.creater = c.username
            JOIN
                quality_modeldata d ON a.projectName=d.modeldata_id
            WHERE
                a.environment = \'{}\'
                and d.modelData=\'{}\'
                and a.platfromType in {}
            ORDER BY
                a.createtime DESC
                '''.format(environment,platfrom,platfromTpyeList)
        # print(sql)
        # log.info("版本更新同步sql={}".format(sql))
        scriptList=commonList().getModelData(sql)
        if len(scriptList)>0:
            for script in scriptList:
                log.info(script)
                self._executeScript(script,username)

    def _executeScript(self,requestData,username):
        '''执行接口脚本'''
        try:
            import json
            logging.info("=======版本更新触发接口执行======开始执行脚本=============")
            log.info("======自动化开始执行======")
            log.info(requestData)
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
                try:
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
                except Exception as e:
                    # 获取异常详细信息
                    logging.error("Exception occurred", exc_info=True)
                    print("捕获的异常：", str(e))
                    print("完整堆栈信息如下：")
                    traceback.print_exc()
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
            
            selectUserNameSql="select first_name from auth_user where username=\'{}\'".format(username)
            returnUserNamedata=commonList().getModelData(selectUserNameSql)
            # if returnUserNamedata:
            #     username=returnUserNamedata[0]['first_name']
            # else:
            #     username="猜猜我是谁，一个来自外太空M78星云的陌生人"
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
                                        self.dingScriptMessage(dingAddress, projectName[0]["modelData"], modelData, total_count, true_count, true_percentage, result,reportAddress,execteEnvironment,username,platfromType)
                                        
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

        except Exception as e:
            # 获取异常详细信息
            logging.error("Exception occurred", exc_info=True)
            print("捕获的异常：", str(e))
            print("完整堆栈信息如下：")
            traceback.print_exc()

    def dingScriptMessage(self,dingAddress,projectName,modelData, total_count, true_count, true_percentage, result,reportAddress,execteEnvironment,username,platfromType):
        '''叮叮消息通知'''
        import requests
        import json
        log.info("=====版本更新触发接口执行======开始推送接口自动化企信消息========")

        content='''
                \n\n><font color=#303133>本消息由系统自动发出，无需回复！</font> 
                \n\n>各位同事，大家好，以下为【<font color=#E6A23C>{}</font>】-【<font color=#E6A23C>{}</font>】项目构建信息
                \n\n>更新人 : <font color=#E6A23C>{}</font>
                \n\n>触发事件 : <font color=#409EFF>需求版本更新</font>
                \n\n>执行环境 : <font color=#E6A23C>{}</font>
                \n\n>执行平台 : <font color=#E6A23C>{}</font>
                \n\n>执行接口 : <font color=#409EFF>{}</font>个 
                \n\n>失败接口 : <font color=#F56C6C>{}</font>个
                \n\n>执行成功率 : <font color=#67C23A>{}</font>%
                \n\n>构建结果 : <font color=#E6A23C>{}</font>
                \n\n>[查看接口测试报告](http://192.168.8.22:8050{})
                '''.format(projectName,modelData,username,execteEnvironment,platfromType,total_count, true_count, true_percentage, result,reportAddress)
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
    def dingUIMessage(self,dingAddress,projectName,modelData,reportAddress):
        '''叮叮消息通知'''
        import requests
        import json

        content='''
                \n\n><font color=#303133>本消息由系统自动发出，无需回复！</font> 
                \n\n>各位同事，大家好，以下为【<font color=#E6A23C>{}</font>】-【<font color=#E6A23C>{}</font>】项目构建信息
                \n\n>执行人 : <font color=#E6A23C>版本更新触发接口执行</font>
                \n\n>构建结果 : <font color=#E6A23C>执行成功</font>
                \n\n>[查看UI测试报告](http://192.168.8.22:8050{})
                '''.format(projectName,modelData,reportAddress)
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
    def executeSingleScript(self,requestData):
        try:
            import json
            logging.info("=======执行测试点接口======开始执行脚本=============")
            log.info("======执行测试点接口脚本======")
            executeType=requestData["executeType"]
            buildAddress=requestData["buildAddress"]
            performanceData=requestData["performanceData"]
            scriptName=requestData["scriptName"]
            sceiptProject_id=requestData['sceiptProject_id']
            environment=requestData['environment']
            platfromName=requestData['platfromName']
            platfromType=requestData['platfromType']

            # 执行前清空脚本执行状态
            createSql='''
                        update quality_scriptproject set totalNumber=0,successNumber=0,failNumber=0,result='未执行' where sceiptProject_id={}
                        '''.format(sceiptProject_id)
            commonList().getModelData(createSql)


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
                try:
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
                except Exception as e:
                    # 获取异常详细信息
                    logging.error("Exception occurred", exc_info=True)
                    print("捕获的异常：", str(e))
                    print("完整堆栈信息如下：")
                    traceback.print_exc()
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
            
            # selectUserNameSql="select first_name from auth_user where username=\'{}\'".format(username)
            # returnUserNamedata=commonList().getModelData(selectUserNameSql)
            # if returnUserNamedata:
            #     username=returnUserNamedata[0]['first_name']
            # else:
            username="自动化用例执行"
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
                                            
                                        # 统计接口成功/时候/运行结果
                                        updateSql='''
                                                    update quality_scriptproject set totalNumber={},successNumber={},failNumber={},result='{}' where sceiptProject_id={}
                                                  '''.format(total_count,success_cont,true_count,result,sceiptProject_id)
                                        commonList().getModelData(updateSql)
                                        # 计算占比
                                        true_percentage =(success_cont / total_count) * 100 if total_count > 0 else 0
                                        true_percentage = round(true_percentage, 2)
                                        self.dingScriptMessage(dingAddress, projectName[0]["modelData"], modelData, total_count, true_count, true_percentage, result,reportAddress,execteEnvironment,username,platfromType)
                                        
                                        
                                        
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

        except Exception as e:
            # 获取异常详细信息
            logging.error("Exception occurred", exc_info=True)
            print("捕获的异常：", str(e))
            print("完整堆栈信息如下：")
            traceback.print_exc()
            data={
                "code":20001,
                "msg":e
            }
            return data




    

    


