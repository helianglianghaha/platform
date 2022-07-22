import  threading
from quality.common.commonbase import commonList
from quality.view.API.APIClass import APITest
# from quality.view.API_version.API_function import createData
from quality.view.API_version.API_function import responseExecuting
from quality.view.API_version.API_model import Executinglog
from quality.view.API_version.API_model import Testapi
from apscheduler.scheduler import Scheduler
from quality.common.logger import Log

log = Log()

#添加定时任务
sched = Scheduler()
class batchApiCases:
    '''接口巡检'''

    def selectAllApiTestCase(self):
        '''查询所有开启巡检项目用例'''

        dingMessageSql='select ding_xunjian,ding_version,ding_message,ding_address,ding_people from quality_dingmessage WHERE ding_xunjian =\'True\''
        Log.info("查询dingMessageSql%s"%dingMessageSql)
        dingMessage=commonList().getModelData(dingMessageSql)
        if len(dingMessage)>0:
            for dingSingle in dingMessage:
                Log.info("dingSingle%s"%dingSingle)
                dingVersion=tuple(eval(dingSingle['ding_version']))
                dingMessage=dingSingle['ding_message']
                dingAddress=dingSingle['ding_address']
                dingPeople=dingSingle['ding_people']
                if len(eval(dingSingle['ding_version']))==1:
                    dingVersion='('+str(eval(dingSingle['ding_version'])[0])+')'

                #版本名称
                versionNameSql='select modelData from quality_modelData where modeldata_id in'+str(dingVersion)
                Log.info('versionNameSql%s'%versionNameSql)
                versionNameList=commonList().getModelData(versionNameSql)
                finallyVersion = []
                for version in versionNameList:
                    print('modelData',version['modelData'])
                    finallyVersion.append(version['modelData'])

                versionName='-'.join(tuple(finallyVersion))

                #查询所有要执行的接口用例
                apiTestCasesSql='select * from quality_testapi where Modelversion_id_id in' \
                             ' (SELECT Modelversion_id from quality_modeldata a,quality_modelversion b WHERE  a.modeldata_id=b.modeldata_id_id and ' \
                             ' (a.modeldata_id in'+str(dingVersion)+'))'
                apiTestCases=commonList().getModelData(apiTestCasesSql)

                #用例不为空调用新线程
                if len(apiTestCases)>0:
                    Log.info('开始执行接口用例')
                    MyThreading(apiTestCases,versionName,dingMessage,dingAddress,dingPeople).start()

                    #为线程开启同步
                    # MyThreading(apiTestCases, versionName, dingMessage, dingAddress,dingPeople).join()
                else:
                    Log.info('接口测试用例为空')
threadLock=threading.Lock()
class MyThreading(threading.Thread):
    def __init__(self,apiTestCases,versionName,dingMessage,dingAddress,dingPeople):
        super(MyThreading,self).__init__()
        self.apiTestCases=apiTestCases
        self.versionName=versionName
        self.dingMessage=dingMessage
        self.dingAddress=dingAddress
        self.dingPeople=dingPeople
    def run(self):
        threadLock.acquire()
        self.runApiTestCases()
        threadLock.release()
    def runApiTestCases(self):
        '''执行接口测试用例'''
        Log.info('开始执行接口自动化')
        import  datetime
        username="自动化巡检"
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        executing_testmd = APITest().Hashlib()
        for caseData in self.apiTestCases:
            # 过滤参数存在变量重新赋值
            from quality.view.API_version.API_function import responseExecuting
            caseDataSort = responseExecuting().sortVariable(caseData)

            testapi_id = caseDataSort['testapi_id']
            testmodelData = caseDataSort['testmodelData']
            Modelversion_id_id = caseDataSort['Modelversion_id_id']
            testapiRequest = caseDataSort['testapiRequest']
            testapiHost = caseDataSort['testapiHost']

            print('testapiHeader',caseDataSort['testapiHeader'])
            print(type(caseDataSort['testapiHeader']))
            testapiHeader = eval(caseDataSort['testapiHeader'])
            testapiAssert = eval(caseDataSort["testapiAssert"])

            # testapiname=caseData['testapiname']
            testapiMethod = str(caseData['testapiMethod'])
            testapiUrl = caseData['testapiUrl']

            testapiBody = caseData['testapiBody']
            testapiExtract = eval(caseData['testapiExtract'])
            testapiAssert = caseData['testapiAssert']
            url = testapiRequest + "://" + testapiHost + testapiUrl
            # print('testapiExtract', testapiExtract)

            if caseData['testcookiesValue'] == 'true':
                # 查询登录接口
                sql = "select * from quality_testapi where testapiname='登录' and Modelversion_id_id=" + str(
                    Modelversion_id_id)
                loginData = commonList().getModelData(sql)

                login_url = "https://" + loginData[0]['testapiHost'] + loginData[0]['testapiUrl']
                login_data = loginData[0]['testapiBody']
                response = APITest().updataCookies(login_url, login_data)
                testapiResponse = APITest().apiRequest(url, testapiBody, testapiMethod, response)

                _testCases = Testapi.objects.get(testapi_id=testapi_id)
                _testCases.teststatuscode = testapiResponse.status_code
                _testCases.testencoding = testapiResponse.encoding
                _testCases.testurl = testapiResponse.url
                _testCases.testheader = testapiResponse.headers
                _testCases.testapiResponse = str(bytes.decode(testapiResponse.content))[0:980]

                returnDataList = responseExecuting().assertApiData(testapiResponse, testapiAssert,
                                                                   testapiResponse.status_code)
                _testCases.testapiAssert = returnDataList["assertData"]

                if len(testapiAssert) != 0 and "fail" not in returnDataList["resultList"]:
                    _testCases.testresult = 1
                else:
                    _testCases.testresult = 2
                _testCases.save()

                _executing = Executinglog()
                _executing.executing_name = nowtime
                _executing.executing_testmd = executing_testmd
                _executing.executing_testapi_id = testapi_id
                _executing.executing_starttime = datetime.datetime.now()
                _executing.save()

            else:
                testapiResponse = APITest().requestNoCookie(url, testapiBody, testapiMethod, testapiHeader)
                testapiExtract = responseExecuting().extractApiData(testapiResponse, testapiExtract)
                _testCases = Testapi.objects.get(testapi_id=testapi_id)
                _testCases.testapiResponse = bytes.decode(testapiResponse.content)[0:980]
                _testCases.teststatuscode = testapiResponse.status_code
                _testCases.testencoding = testapiResponse.encoding
                _testCases.testheader = testapiResponse.headers
                _testCases.testurl = testapiResponse.url
                _testCases.testapiExtract = testapiExtract

                returnDataList = responseExecuting().assertApiData(testapiResponse, testapiAssert,
                                                                   testapiResponse.status_code)
                _testCases.testapiAssert = returnDataList["assertData"]

                if len(testapiAssert) != 0 and "fail" not in returnDataList["resultList"]:
                    _testCases.testresult = 1
                else:
                    _testCases.testresult = 2
                _testCases.save()

                _executing = Executinglog()
                _executing.executing_name = nowtime
                _executing.executing_testmd = executing_testmd
                _executing.executing_testapi_id = testapi_id
                _executing.executing_starttime = datetime.datetime.now()
                _executing.executing_userName = username
                _executing.executing_versionName = self.versionName
                _executing.save()

        #钉钉消息通知
        if self.dingMessage=='True':
            # 机器人地址
            ding_url = self.dingAddress
            # 测试报告地址
            testReportAddress = 'http://192.168.100.118:8050/#/reportManage?label=' + executing_testmd
            Log.info("开始发送消息")
            createData().sendDingMessageTotal(ding_url, testReportAddress, executing_testmd, self.versionName,
                                      username,self.dingPeople)

        Log.info("接口自动化执行结束")
