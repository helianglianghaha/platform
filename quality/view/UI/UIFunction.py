import copy,time,datetime,hashlib,random,requests
from quality.common.functionlist import FunctionList
from quality.common.logger import Log
from quality.view.API_version.API_model import Executinglog
from quality.common.functionlist import FunctionList
from quality.common.commonbase import commonList
from quality.view.API_version.API_model import Executinglog
from quality.test.seleniumData.prams import connectionList
# from quality.view.UI.UI_data import  getSingleHubVersion

class UiFunction:
    '''
    用例列表过滤
    '''
    def __init__(self):
        self.BrowserList=['IE','CHROME','FIREFOX']
        # self.log=Log()
        # self.function=FunctionList.__dict__
        # self.nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def sortList(self,val):
        '''
        主要入口
        '''
        # print("val==================",val)
        pramsList=[]
        for i_val in val:
            print('i_val',i_val)
            # print('i_val[\'script_testDataParameter\']',i_val['script_testDataParameter'])
            if i_val['script_testDataKeyWord']=='drapPullMouse':
                break
            if i_val['script_testDataKeyWord']=='addCookie':
                break
            if i_val['script_testDataKeyWord']=='executeJavascript':
                pramsList.append(copy.deepcopy([i_val['script_testDataParameter']]))
            if len(i_val['script_testDataParameter'])>0 and i_val['script_testDataKeyWord'] not in['drapPullMouse','executeJavascript'] :
                dataList=i_val['script_testDataParameter'].split(" ")
                for k in range(0,len(dataList)):
                    if ',' in dataList[k]:
                        k_list=dataList[k].split(",")
                        dataList[k]=k_list
                    else:
                        pass
                pramsList.append(copy.deepcopy(dataList))
            if len(i_val['script_testDataParameter'])==0:
                # print("字符串为空")
                pass

        if len(pramsList)>0:
            # print("获取到的pramsList",pramsList)
            sortList=self._sortListObject(pramsList)
            _sortBrowserList=self._sortListObjectAgainst(sortList)
            #参数列表
            BrowserAll=self._sortBrowserAll(_sortBrowserList)
            list_All=self.sortpramers(val,BrowserAll)
            list_All_Second=self._sortSecondPramers(list_All)
        else:
            list_All_Second=val
        return  list_All_Second
    def _sortSecondPramers(self,val):
        sortList=[]
        for i in val:
            for k in i:
                sortList.append(k)
        return sortList
    def sortpramers(self,val,prams):
        '''
        将排序好的参数放入用例中
        '''
        new_list=[]
        all_list=[]
        # print('sortpramers====val',val)
        # print('sortpramers====prams',prams)
        for pramsList in prams:
            n=0
            for k_val in pramsList:
                # print('k_val============',k_val)
                # print('pramsList==============',pramsList)
                # print('val===================',val)
                # print('len(val)',len(val))
                # print(val[n]['script_testDataParameter'])
                if n==len(val):
                    # print("检查val",val)
                    break
                if len(val[n]['script_testDataParameter'])>0:
                    val[n]['script_testDataParameter']=k_val
                else:
                    for i in val[n+1:]:
                        if len(i['script_testDataParameter'])>0:
                            # i['script_testDataParameter']=copy.deepcopy(k_val)
                            n=val.index(i)
                            break
                n+=1
            all_list.append(copy.deepcopy(val))
        return all_list
    def _sortBrowserAll(self,val):
        '''
        将所有值排序为单个值，依次取值
        [['http://testkbdrm.yunxiao.com/login ie', ['123456', 'qwertyui'], ['8910456789', 'qwertyui'], ['ABC', 'jhjkl', 'tyuiop']]
        ['http://testkbdrm.yunxiao.com/login ie','123456','8910456789','ABC']

        [['http://testkbdrm.yunxiao.com/login ie', ['123456', 'qwertyui'], ['8910456789', 'qwertyui'], ['ABC', 'jhjkl', 'tyuiop']]
        [['http://testkbdrm.yunxiao.com/login ie', '123456', '8910456789','ABC']

        '''
        # print('_sortBrowserAll====val',val)
        number_list=self._list_number_second(val,0)
        # print('_sortBrowserAll===number_list',type(number_list))
        temp=self._list_max(val)
        temp_browser_all=[]
        if number_list>2:
            temp_browser_all=self._double_list(val)
            return temp_browser_all
        else:
            for i in range(0,temp):
                print('_sortBrowserAll=====i',i)
                temp_browser_list=[]
                for k in val:
                    # print('_sortBrowserAll_k',k)
                    if i<len(k):
                        temp_browser_list.append(k[i])
                    else:
                        temp_browser_list.append(k[-1])
                    print('temp_browser_list_loading',temp_browser_list)
                temp_browser_all.append(temp_browser_list)
            # print('temp_browser_all',temp_browser_all)
            return temp_browser_all
    def _double_list(self,val):
        '''
        列表层数超过3层
        '''
        # print("_double_list=====val",val)
        temp=self._list_max(val)
        temp_browser_all_second=[]
        for i in range(0,temp):
            # print('_sortBrowserAll=====i',i)
            for k in val:
                temp_browser_list_second=[]
                for true_list in k:
                    # print("_double_list=======val",val)
                    # print("_double_list====k",k)
                    # print("_double_list====true_list",true_list)
                    if i<len(true_list):
                        temp_browser_list_second.append(true_list[i])
                    else:
                        temp_browser_list_second.append(true_list[-1])
                    # print('temp_browser_list_loading',temp_browser_list_second)
                temp_browser_all_second.append(temp_browser_list_second)
                # print('temp_browser_all_second',temp_browser_all_second)
            # print('temp_browser_all',temp_browser_all_second)
        return temp_browser_all_second
    def _list_number_second(self,val,number):
        '''
        判断是否是列表
        '''
        _number=number
        if isinstance(val,list):
            _number+=1
            return self._list_number_second(val[0],_number)
        else:
            # print('_list_number_second=====_number',_number)
            return _number

    def _list_max(self,val):
        '''
        返回列表个数最大值
        '''
        # print("_list_max===val",val)
        temp=0
        for i in val:
            # print('_list_max===i',i)
            if isinstance(i,list):
                max_number=self._max_number(i) 
                if max_number>temp:
                    temp=max_number
                else:
                    pass               
            else:
                # print('该项不是列表')
                pass
        # print("获取的列表最大值",temp)
        return temp
    def _max_number(self,val):
        # print('_max_number===val',val)
        max_number_list=[]
        trueTy=[False for i in val if isinstance(i,list)]
        if trueTy:
            for i in val:
                if isinstance(i,list):
                    max_number_list.append(len(i))
                else:
                    pass
            # print('max_number_list=======',max_number_list)
            return max(max_number_list)
        else:
            return len(val)
    def _sortListObjectAgainst(self,val):
        '''
        再次过滤列表，浏览器登录列表合并
        ['http://testkbdrm.yunxiao.com/login', 'ie']=》['http://testkbdrm.yunxiao.com/login ie']
        '''
        for i in val:
            val[val.index(i)]=self._sortBrowser(i)
        # print("获取到的_sortListObjectAgainst=====val",val)
        return val

    def _sortBrowser(self,val):
        '''
        判断列表是否为浏览器登录
        '''
        BrowserList=['IE','CHROME','FIREFOX']
        temp=val
        for i in val:
            # print('_sortBrowser====i',i)
            if isinstance(i,list):
                val[val.index(i)]=copy.deepcopy(self._sortBrowserXunHuan(i))
            else:
                if i.upper() in self.BrowserList:
                    val=' '.join(val)
                    temp=copy.deepcopy(val)
                    if isinstance(temp,list):
                        pass
                    else:
                        temp=[temp]
                else:
                    pass
        # print("_sortBrowser======val",val)

        return temp
    def _sortBrowserXunHuan(self,val):
        '''
        合并 ['http://testkbdrm.yunxiao.com/login', 'ie']=》['http://testkbdrm.yunxiao.com/login ie']
        '''
        if isinstance(val,list):
            for i in val:
                if i.upper() in self.BrowserList:
                    val=' '.join(val)
                    val=[copy.deepcopy(val)]
                else:
                    pass
        return val
    def _sortListObject(self,args):
        '''
        拆分多个浏览器返回列表
        ['http://testkbdrm.yunxiao.com/login', ['ie', 'chrome', 'firefox']]拆分为['http://testkbdrm.yunxiao.com/login', 'ie']
        '''
        merge=[]
        otherMerge=[]
        for i in args:  #
            for k in range(0,len(i)):
                if isinstance(i[k],list):#['ie', 'chrome', 'firefox']
                    for j in i[k]:
                        i[k]=j
                        merge.append(copy.deepcopy(args))
                else:
                    pass
            if len(merge)==0:
                otherMerge.append(i)
            else:
                print("列表中没有在嵌套列表可以直接append")
        if len(merge)>0:
            return merge
        else:
            return otherMerge
class batchXunJianTestCase:
    # def __int__(self):
    #     self.log=Log()
    # @sched.interval_schedule(seconds=60)
    def xunJianBatchTestCase(self):
        '''
        巡检接口批量执行
        :return:
        '''
        # try:
        allTestCase=self.getAllXunJianTestCase()
        for scriptCase in allTestCase:
            TestCasesList=scriptCase.items()
            for key,value in TestCasesList:
                mdStringValue = executSingleCase().Hashlib()
                for case in value:
                    executSingleCase()._xunHuanExecutSingle(case, 0, mdStringValue)
                #根据hash获取执行结果
                testResult=self.getXunJianReport(mdStringValue)

                #获取版本,根据版本查找企信ID
                caseVersion=value[0]["script_testDataVersion"]
                sql='SELECT a.pro_qixin,a.pro_openQiXin FROM quality_proaddress a WHERE  a.Modelversion_id_id='+str(caseVersion)
                qiXinData=commonList().getModelData(sql)
                qiXinQun=qiXinData[0]["pro_qixin"]

                #执行不成功且填写了企信群ID
                if len(qiXinData[0]["pro_qixin"])>0 and len(testResult)>0 and qiXinData[0]["pro_openQiXin"]=='true':
                    self.sendQiXin(key, mdStringValue, qiXinQun)

    def getXunJianReport(self,mdStringValue):
        '''根据md5查看测试报告'''
        # try:
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
        print('reportValue',reportValue)
        #获取结果

        valueList=[ value['script_testResult'] for value in reportValue if value['script_testResult']=='失败']

        print("获取到的执行结果",valueList)
        return  valueList
        # except Exception as e:
        #     print('getXunJianReport报错了%s' % e)
    def sendQiXin(self,modelVersion,hash,qiXinQun):
        '''发送企信消息'''
        try:
            nowTime=datetime.datetime.now()
            text = "【项目】：" +modelVersion+ "-UI巡检失败请相关同事关注" + "\n" \
                "【告警时间】：" + str(nowTime) + "\n" \
                "【URL地址】：" + 'http://172.17.32.253:8080/#/UIreport?label='+hash
            #调用发送企信推送接口
            self.sendMsg(text,qiXinQun)
        except Exception as  e:
            print('sendQiXin报错了%s' % e)
    def sendMsg(self,text,qiXinQun):
        '''
        企信消息结果
        :param text:
        :return:
        '''
        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "msgtype": "text",
                "text": {
                    "content": text,
                    "mentioned_list": [""],
                    "mentioned_mobile_list": [""]
                }
            }
            #拆分企信群ID
            if ',' in qiXinQun:
            #多个微信群
                qiXinIdList=qiXinQun.split(',')
                for qiXin in qiXinIdList:
                    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="+qiXin
                    result = requests.post(url, headers=headers, json=data)
            else:
            #单个微信群
                url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="+qiXinQun
                result = requests.post(url, headers=headers, json=data)
            return result
        except Exception as e:
            print('sendMsg报错了%s' % e)
    def getAllXunJianTestCase(self):
        '''获取所有需要巡检的项目测试用例'''
        # try:
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
        # except Exception as e :
        #     print('getAllXunJianTestCase报错了%s' % e)
    def getAllVersionData(self):
        '''获取所有的巡检版本信息'''
        # try:
        sql="select b.modeldata_name from quality_proaddress  a,quality_modelversion b WHERE a.Modelversion_id_id=b.Modelversion_id and  a.pro_openXunjian=\'true\'"
        modelData=commonList().getModelData(sql)
        print("===========modelData======",modelData)
        modelDataList=[]
        for i in modelData:
            modelDataList.append(i['modeldata_name'])
        return  modelDataList
        # except Exception as e :
        #     print ('getAllVersionData报错了%s' % e)
    def getSingleVersionTestCase(self,modelData):
        '''获取单个版本需要执行的用例'''
        # try:
        sql='select a.testcase_id from quality_testcase a,quality_modelversion b where a.testcase_caseVersion=b.Modelversion_id and b.modeldata_name='+"\'"+modelData+"\'"
        print('sql',sql)
        singleTestCase=commonList().getModelData(sql)

        # 循环获取每个用例对应的脚本步骤
        sortListBefore = []
        for testScriptID in singleTestCase:
            sql = 'select * from quality_testscript where script_TestDataCase =' + str(testScriptID['testcase_id'])
            print('testScriptID',sql)
            CaseList = commonList().getModelData(sql)
            sortListBefore.extend((CaseList))

        return  sortListBefore
        # except Exception as e :
        #     print('getAllVersionData报错了%s' % e)
class executSingleCase:
    '''
    单条用例执行
    '''
    def __init__(self):
        self.log=Log()
        self.assertList=['assertElement','assertValueElement','assertElementIsSelect','assertElementIsDisplay']

    def _xunHuanExecutSingle(self,val,tryNumber,mdString,userName,versionName):
        functionList=FunctionList.__dict__
        function=functionList[val['script_testDataKeyWord']]
        nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(1)
        temp=tryNumber
        if val['script_testDataElement']!='' and  val['script_testDataParameter']!='':
            self.log.info('********既有元素又有参数*******script_testDataName:%s-函数%s()-prams：%s'% (val['script_testDataName'],function.__name__,val['script_testDataParameter']))
            # try:
            if val['script_testDataKeyWord'] in self.assertList:
                function(val['script_testDataElement'], val['script_testDataParameter'],val,
                         val['script_testDataVersion'])
            else:
                function(val['script_testDataElement'],val['script_testDataParameter'],val['script_testDataVersion'])
            # except Exception as  e:
            #     self.log.info('接口报错了%s'%e)
                # return False
                # self._errorExecuting(tryNumber,temp,val,function,mdString)
            self._executing(val['script_id'],nowtime,mdString,userName,versionName)
        elif val['script_testDataElement']!='' and val['script_testDataParameter']=='':
            self.log.info('*********只有元素没有参数*******script_testDataName：%s-函数：%s()'% (val['script_testDataName'],function.__name__))
            # try:
            if val['script_testDataKeyWord'] in self.assertList:
                function(val['script_testDataElement'],val,val['script_testDataVersion'])
            elif val['script_testDataKeyWord']=='clickElement':
                function(val['script_testDataElement'], val,val['script_testDataVersion'])
            else:
                function(val['script_testDataElement'],val['script_testDataVersion'])
            # except Exception as  e:
            #     self.log.info('接口报错了%s'%e)
            #     # return  False
            #     # self._errorExecuting(tryNumber,temp,val,function,mdString)
            self._executing(val['script_id'],nowtime,mdString,userName,versionName)
        elif val['script_testDataElement']=='' and val['script_testDataParameter']!='':
            self.log.info('*********没有元素只有参数******* 函数:%s()prams:%s'% (function.__name__,val['script_testDataParameter']))
            # try:
            if val['script_testDataKeyWord']=='openbrowser':
                #获取运行版本对应的Hub地址
                huaVersion=val['script_testDataVersion']
                command_executor=self._getSingleHubVersion(huaVersion)
                if command_executor:
                    driverList=function(val['script_testDataParameter'],command_executor)
                    self._connectDriver(val['script_testDataVersion'],driverList)
                else:
                    self.log.info("获取的浏览器代理节点为空")
            else:
                function(val['script_testDataParameter'],val['script_testDataVersion'])
            # except Exception as  e:
            #     self.log.info('接口报错了%s'%e)
            #     return False
            #     self._errorExecuting(tryNumber,temp,val,function,mdString)
            self._executing(val['script_id'],nowtime,mdString,userName,versionName)

        else:
            self.log.info('******即没有元素也没有参数********script_testDataName:%s-函数:%s()' % (val['script_testDataName'], function.__name__))
            try:
                function(val['script_testDataVersion'])
            except Exception as  e:
                self.log.info('接口报错了%s'%e)
                # return  False
                # self._errorExecuting(tryNumber,temp,val,function,mdString)
            self._executing(val['script_id'],nowtime,mdString,userName,versionName)

    def _getSingleHubVersion(self,testDataVersion):
        '''获取单个节点地址'''

        sql = 'select * from quality_proaddress where Modelversion_id_id=' + testDataVersion
        print('=======================获取单个节点地址======================执行了', sql)
        pro_address = commonList().getModelData(sql)
        return pro_address[0]['pro_address']

    def _connectDriver(self,version,driver):
        '''
        :param version: 运行版本
        :param driver: 版本对应的driver
        :return:
        '''
        if version in connectionList.keys():
            connectionList[version].append(driver)
            # print('_connectDriver',connectionList)
        else:
            connectionList[version]=[]
            connectionList[version].append(driver)
            # print('_connectDriver', connectionList)
    def _errorExecuting(self,tryNumber,temp,val,function,mdString):
        '''
        异常捕获重新请求
        prams:
        tryNumber:重试次数(重试3次)
        val：用例信息
        function:执行函数
        '''
        self.log.info('******第%s执行失败********script_testDataName:%s-函数:%s()'% (tryNumber,val['script_testDataName'],function.__name__))
        temp+=1
        if temp>1:
            temp=copy.deepcopy(0)
            return None
        else:
            return self._xunHuanExecutSingle(val,temp,mdString)
    def Hashlib(self):
        '''
        生成md5
        '''
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        m2=hashlib.md5()
        m2.update(now.encode("utf8"))
        return m2.hexdigest()
    def _executing(self,script_id,script_time,mdString,userName,versionName):
        '''
        保存执行时间
        '''
        executingLog=Executinglog()
        executingLog.executing_name=script_time
        executingLog.executing_testscript_id=script_id
        executingLog.executing_testmd=mdString
        executingLog.executing_endtime=datetime.datetime.now()
        executingLog.executing_userName=userName
        executingLog.executing_versionName=versionName
        executingLog.save()
        # self.log.info('script_id:%s===time:%s'%(script_id,script_time))
    
if __name__=="__main__":
    # parms=[['http://testkbdrm.yunxiao.com/login', 'Chrome'], ['13526429390', '13526429391'], ['429390', '429391'], ['幼儿园']]
    # UiFunction()._list_max(parms)
    batchXunJianTestCase().getAllXunJianTestCase()





                
 