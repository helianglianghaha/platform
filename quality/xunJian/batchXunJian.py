import copy,time,datetime,hashlib,random,requests
from quality.common.functionlist import FunctionList
from quality.common.logger import Log
from quality.view.API_version.API_model import Executinglog
from quality.common.functionlist import FunctionList
from quality.common.commonbase import commonList
from apscheduler.scheduler import Scheduler
log=Log()
#添加定时任务
sched = Scheduler()

from quality.view.UI.UIFunction  import executSingleCase,UiFunction
from quality.view.API_version.API_model import Executinglog
from quality.test.seleniumData.prams import connectionList
class batchXunJianTestCase:
    # def __int__(self):
    #     self.xunJianBatchTestCase(batchXunJianTestCase)

    @sched.interval_schedule(seconds=60)
    def xunJianBatchTestCase(self):
        '''
        巡检接口批量执行
        :return:
        '''
        try:
            allTestCase=self.getAllXunJianTestCase()

            print('allTestCase',allTestCase)
            for key in allTestCase.keys():
                TestCasesList=allTestCase[key]
                mdStringValue = executSingleCase().Hashlib()
                for case in TestCasesList:
                    executSingleCase()._xunHuanExecutSingle(case, 0, mdStringValue)
                #根据hash获取执行结果
                testResult=self.getXunJianReport(mdStringValue)
                #执行不成功发送企信通知
                if testResult:
                    self.sendQiXin(key,mdStringValue)
        except Exception as e:
            log.info('xunJianBatchTestCase报错了%s' % e)
    def getXunJianReport(self,mdStringValue):
        '''根据md5查看测试报告'''
        try:
            sql = 'SELECT * FROM ' \
                  '(SELECT * FROM ' \
                  'quality_executinglog a,' \
                  'quality_testcase b,' \
                  'quality_testscript f,' \
                  'quality_modelversion d' \
                  ' WHERE  f.script_testDataVersion = d.Modelversion_id ' \
                  'AND a.executing_testscript_id = f.script_id ' \
                  'AND f.script_TestDataCase = b.testcase_id ' \
                  'AND a.executing_testmd = ' + '\'' + mdStringValue + '\'' \
                   ' ) temp ' \
                   'LEFT JOIN (SELECT * FROM(SELECT * FROM quality_testpicture h ORDER BY h.picture_id DESC ) w GROUP BY w.picture_scriptId) ' \
                   'e ON temp.script_id =e.picture_scriptId'
            reportValue = commonList().getModelData(sql)

            #获取结果
            valueList=[value.script_testResult for value in reportValue if value.script_testResult=='失败']
            return  valueList
        except Exception as e:
            log.info('getXunJianReport报错了%s' % e)
    def sendQiXin(self,modelVersion,hash):
        '''发送企信消息'''
        try:
            nowTime=datetime.datetime.now()
            text = "【项目】：" +modelVersion+ "-UI巡检失败请相关同事关注" + "\n" \
                "【告警时间】：" + str(nowTime) + "\n" \
                "【URL地址】：" + 'http://127.0.0.1:8080/#/UIreport?label='+hash
            #调用发送企信推送接口
            self.sendMsg(text)
        except Exception as  e:
            log.info('sendQiXin报错了%s' % e)
    def sendMsg(self,text):
        '''
        企信消息结果
        :param text:
        :return:
        '''
        try:
            url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6ffbeb41-a3b0-4f43-b270-0113abd0a615"  # 填上机器人Webhook地址
            headers = {"Content-Type": "application/json"}
            data = {
                "msgtype": "text",
                "text": {
                    "content": text,
                    "mentioned_list": [""],
                    "mentioned_mobile_list": [""]
                }
            }
            result = requests.post(url, headers=headers, json=data)
            return result
        except Exception as e:
            log.info('sendMsg报错了%s' % e)
    def getAllXunJianTestCase(self):
        '''获取所有需要巡检的项目测试用例'''
        try:
            allTestCase=[]
            modelDataList=self.getAllVersionData()
            if isinstance(modelDataList,list):
                for modeldata in modelDataList:
                    modelTestCase={}
                    modeTestCases=self.getSingleVersionTestCase(modeldata)

                    #用例数据单独处理
                    finaTestCase=UiFunction().sortList(modeTestCases)

                    modelTestCase[modeldata]=finaTestCase
                    #获取每个项目的testcases
                    allTestCase.append(modelTestCase)
            return allTestCase
        except Exception as e :
            log.info('getAllXunJianTestCase报错了%s' % e)
    def getAllVersionData(self):
        '''获取所有的巡检版本信息'''
        try:
            sql="select b.modeldata_name from quality_proaddress  a,quality_modelversion b WHERE a.Modelversion_id_id=b.Modelversion_id and  a.pro_openXunjian='true'"
            modelData=commonList.getModelData(sql)
            return  modelData
        except Exception as e :
            log.info('getAllVersionData报错了%s' % e)
    def getSingleVersionTestCase(self,modelData):
        '''获取单个版本需要执行的用例'''
        try:
            sql='select * from quality_testcase a,quality_modelversion b where a.testcase_caseVersion=b.Modelversion_id and b.modeldata_name='+"\'"+modelData+"\'"
            singleTestCase=commonList.getModelData(sql)
            return  singleTestCase
        except Exception as e :
            log.info('getAllVersionData报错了%s' % e)
sched.start()