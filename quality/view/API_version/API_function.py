import requests,re,json,jsonpath
# import cookieslib,urll
# from quality.common.commonbase
from quality.common.commonbase import commonList
from quality.common.logger import Log
from quality.common.msg import msglogger
from ..API.APIClass import  APITest
from django.db import connection
from quality.view.API_version.API_model import Testvariable
from pymysql import  converters
log=Log()
class responseExecuting():
    '''
    正则提取
    apiExtractName：提取名称
    apiExtractExpression：提取表达式
    responseData：返回值
    passWordFree：URL提取
    addPassWordFree：提取cookies
    '''
    def __init__(self):
        self.db_config={
            'host': 'rm-uf60nso6wlf92lhtjzo.mysql.rds.aliyuncs.com',
            'user': 'root1',
            'password': 'Goodlearning2021@@',
            'port': 3306,
            'database':'lz_ems',
            'charset':'utf8',
        }
        self.test_db_config={
            'host': '192.168.100.89',
            'user': 'apm',
            'password': 'persagy@2021',
            'port': 9934,
            'database':'persagy_test',
            'charset':'utf8',
        }


    @msglogger
    def sortVariable(self,variableList):
        '''重新赋值参数'''
        print(variableList)
        #判断数据类型
        for variable in variableList:
            if isinstance(variableList[variable],str) and  variableList[variable].find('${')>=0:

                #获取截取字符串
                stringStartIndex=variableList[variable].find('$')
                stringEndIndex=variableList[variable].find('}')
                stringValiable=variableList[variable][stringStartIndex:stringEndIndex+1]

                #查找要替换的字符串
                srcString=variableList[variable]
                parameter = stringValiable[2:-1]
                sql = 'select * from quality_testvariable where variableKey=' + "'" + parameter + "'"
                parameterSpl = commonList().getModelData(sql)
                afterParameter = parameterSpl[0]['variableValue']

                variableList[variable]=srcString.replace(stringValiable,afterParameter)

                #替换后再次查找字符串
                if variableList[variable].find('${')>=0:
                    variableList[variable]=(APITest()._sortString(variableList[variable]))

        return  variableList
    def extractApiData(self,response,testapiExtract):
        '''
        返回结果提取
        1:jsonpath提取数据
        2:URL提取数据
        3:提取cookies
        '''
        print('extractApiData++++++testapiExtract',testapiExtract)
        if len(testapiExtract)!=0:
            for extractData in testapiExtract:
                if extractData['apiExtractType']=='1':
                    sourceData = json.loads(bytes.decode(response.content))
                    jsonData = jsonpath.jsonpath(sourceData, extractData['apiExtractExpression'])
                    print('jsonData',jsonData)
                    if len(jsonData)==0:
                        extractData['apiExtractResponse']="提取的值为空"
                    else:
                        extractData['apiExtractResponse']=jsonData[0]

                        #提取的值非空可以保存
                        self.saveExtractData(extractData)
                if extractData['apiExtractType']=='2':
                    pass
                if extractData['apiExtractType'] == '3':
                    extractCookie=response.cookies
                    extractCookie=requests.utils.dict_from_cookiejar(extractCookie)
                    print('extractCookie',extractCookie)
                    if len(extractCookie)==0:
                        extractData['apiExtractResponse'] = "提取的cookies为空"
                    else:
                        extractData['apiExtractResponse']=str(extractCookie)

                        # 提取的值非空可以保存
                        self.saveExtractData(extractData)
            #保存提取全局变量
            # self.saveExtractData(testapiExtract)
        else:
            log.info("提取列表为空")
        return  testapiExtract
    def saveExtractData(self,extractdata):
        '''提取保存的值放到全局变量'''
        # for extract in extractdata:
        print('extractdata',extractdata)
        extractList=Testvariable.objects.filter(variableKey=extractdata['apiExtractName'])
        if len(extractList)==0:
            _saveVariable = Testvariable()
            _saveVariable.variableKey=extractdata['apiExtractName']
            _saveVariable.variableValue=str(extractdata['apiExtractResponse'])
            _saveVariable.save()
        else:
            print('extractdata', extractdata)
            _saveVariable=Testvariable.objects.get(variableKey=extractdata['apiExtractName'])
            _saveVariable.variableKey = extractdata['apiExtractName']
            _saveVariable.variableValue = (extractdata['apiExtractResponse'])
            _saveVariable.save()

    @msglogger
    def assertApiData(self,response,assertData,responseCode):
        '''
        接口断言
        1：code状态码
        2：字段是否存在
        3：字段值是否一致
        4：字段总个数是否正确
        5：Sql自查询
        '''
        assertData=eval(assertData)
        resultData={
            "assertData":[],
            "resultList":[]
        }
        #处理返回值信息
        if isinstance(assertData,list):
            for oneAssertData in assertData:
                if oneAssertData["assertType"]=='1':
                    # print('开始处理断言信息',oneAssertData)
                    if oneAssertData["assertVariable"]==str(responseCode):
                        oneAssertData['assertResult']="success"
                        resultData["resultList"].append("success")
                    else:
                        oneAssertData['assertResult']="预期的状态码是"+str(oneAssertData["assertVariable"])+"实际的状态码是"+str(responseCode)
                        resultData["resultList"].append("fail")
                if oneAssertData["assertType"] == '2':

                    if oneAssertData['assertVariable'] in str(bytes.decode(response.content)):
                        oneAssertData['assertResult'] = "success"
                        resultData["resultList"].append("success")
                    else:
                        oneAssertData['assertResult']="字段不在返回值中"
                        resultData["resultList"].append("fail")
                if oneAssertData["assertType"]=='3':
                    import re,jsonpath,json
                    sourceData=json.loads(bytes.decode(response.content))
                    print(oneAssertData)
                    jsonData=jsonpath.jsonpath(sourceData,oneAssertData['assertVariable'])
                    print('jsonData',jsonData)
                    if not isinstance(jsonData,bool):
                        if len(jsonData)>0:
                            if str(jsonData[0])==oneAssertData["assertVariAbleValue"]:
                                oneAssertData['assertResult'] = "success"
                                resultData["resultList"].append("success")
                            else:
                                oneAssertData['assertResult'] ="预期json值是"+str(oneAssertData["assertVariAbleValue"])+"实际json值是"+str(jsonData)
                                resultData["resultList"].append("fail")
                        else:
                            oneAssertData['assertResult'] = "提取的值为空"
                            resultData["resultList"].append("fail")
                    else:
                        oneAssertData['assertResult'] = "提取的表达式有问题"
                if oneAssertData["assertType"]=='5':
                    returnData=self.assertSelectSqlData(oneAssertData['assertVariable'])
                    if str(returnData)==oneAssertData["assertVariAbleValue"]:
                        oneAssertData['assertResult'] = "success"
                        resultData["resultList"].append("success")
                    else:
                        oneAssertData['assertResult'] = "预期sql查询值是" + str(
                        oneAssertData["assertVariAbleValue"]) + "实际sql查询值是" + str(returnData)
                        resultData["resultList"].append("fail")
            resultData["assertData"]=assertData
            return  resultData
        else:
            log.info("assertData不为list，请校验数据后再试试吧")
    def assertSelectSqlData(self,assertData):
        '''sql查询断言'''
        import  pymysql
        from pymysql.cursors import DictCursor#结果以字典的形式返回
        #创建连接
        conn=pymysql.connect(**self.test_db_config)

        #创建游标
        cursor=conn.cursor(DictCursor)

        #执行sql语句
        cursor.execute(assertData)

        sqlData=cursor.fetchall()

        # print(type(sqlData['energy_data']))
        print("获取到的sql语句是",assertData)
        print("断言sql自查询获取到的数据是：",(sqlData))

        #关闭游标和数据库
        cursor.close()
        conn.close()
        return  sqlData












    @msglogger
    def executing(self,response,passWordFree,addPassWordFree,apiExtractName):
        print('executing')
        log.info('passWordFree=%s&&&addPassWordFree=%s&&&apiExtractName=%s&&&apiExtractExpression=%s'%(passWordFree,addPassWordFree,apiExtractName,apiExtractExpression))
        if passWordFree and not addPassWordFree:
            self._execuPassWord(response,apiExtractName)
        elif addPassWordFree and not passWordFree:
            self._execuAddPass(response,apiExtractName)
        elif passWordFree and addPassWordFree:
            self._execuPassAddWord(response,apiExtractName)
        else:
            print('不需要提取')
    @msglogger
    def _execuPassWord(self,response,apiExtractName,apiExtractExpression):
        '''URL提取'''
        url=response.url
        log.info('【URL】:%s'%url)
        self._execuData(apiExtractName,apiExtractExpression,url)
    @msglogger
    def _execuAddPass(self,response,apiExtractName,apiExtractExpression):
        '''response_cookies'''
        url=response.url
        log.info('【URL】:%s'%url)
        cookieslist=response.cookies
        log.info('response_cookies=%s'%cookieslist)
        cookie=requests.utils.dict_from_cookiejar(cookieslist) #将cookies转换成字典
    @msglogger
    def _execuPassAddWord(self,response,apiExtractName,apiExtractExpression):
        '''提取URL和和response_cookies'''
        url=response.url
        log.info('【URL】:%s'%url)
        variableVarr=self._execuData(apiExtractName,apiExtractExpression,url)
        log.info('保存的提取值是:%s'%variableVarr)
        cookieslist=response.cookies
        log.info('获取到的cookies是'%cookieslist)
        cookie=requests.utils.dict_from_cookiejar(cookieslist) #将cookies转换成字典
    @msglogger
    def _execuData(self,apiExtractName,apiExtractExpression,apiResponse):
        '''提取数据'''
        print('apiExtractName',apiExtractName)
        print('apiExtractExpression',apiExtractExpression)
        variable=re.findall(apiExtractExpression,apiResponse)
        self._saveData(apiExtractName,variable)
        return variable
    @msglogger
    def _saveData(self,ExtractName,varr):
        '''保存提取的变量'''
        if len(varr)==0:
            print('获取的token为空')
        else:
            sql='select * from quality_testvariable where variableKey='+"\'"+ExtractName+"\'"
            exitVaribale=commonList().getModelData(sql)
            log.info('exitVaribale%s'%exitVaribale)
            if len(exitVaribale)!=0:
                sql='update quality_testvariable set variableValue='+"\'"+varr[0] +"\'"+'where variableKey='+"\'"+ExtractName+"\'"
                print(sql)
                self._saveVariable(sql)
            else:
                sql='insert into quality_testvariable (variableKey,variableValue) values ('+ExtractName+','+varr[0]+")"
                print(sql)
                self._saveVariable(sql)
    @msglogger
    def _saveVariable(self,varr):
        ''''''
        cursor = connection.cursor()
        cursor.execute(varr)
        print(cursor)
class createDataFinally():
    '''冷站智控造数据'''
    def createSqlData(self,requestType):
        '''执行sql造数据'''
        from .API_dataList import DataList
        if requestType=='1':#tb_coldstation_features_environment_in_202205
            DataList().tb_coldstation_features_environment_in()
        #     tb_coldstation_features_environment_in_202205_string=tb_coldstation_features_environment_in_202205_sql
        #
        # sql=''
    def executeTime(self,sqlTime):
        '''时间处理'''
        pass
    def sortDingMessage(self,totalData,Modelversion_id_id,executing_testmd,versionName,executName):
        '''分类处理信息'''
        print("开始执行分类处理信息")
        for versionList in range(len(totalData)):
            for version in eval(totalData[versionList]['version']):
                print('Modelversion_id_id',Modelversion_id_id)
                print('version',version)
                if Modelversion_id_id == version:
                    # 机器人地址
                    ding_url = totalData[versionList]["robotAddress"]
                    ding_people=totalData[versionList]["people"]
                    if ',' in ding_people:
                        ding_people=ding_people.split(',')
                    else:
                        ding_people=list(ding_people)
                    print('钉钉通知人',ding_people)
                    # 测试报告地址
                    testReportAddress = 'http://192.168.100.118:8050/#/reportManage?label=' + executing_testmd
                    print("开始发送消息")
                    self.sendDingMessageTotal(ding_url, testReportAddress, executing_testmd, versionName,
                                                      executName,ding_people)
    def sendDingMessageTotal(self,url,testReportUrl,executing_testmd,versionName,executName,ding_people):
        '''
        发送钉钉消息
        url:机器人地址
        testReportUrl:测试报告地址
        executing_testmd：测试报告md5值
        versionName：版本名称
        executName：执行人
        '''
        Log().info("开始执行消息通知")

        Log().info("钉钉通知人%s"%ding_people)

        HEADERS={
            "Content-Type":"application/json;charset=utf-8"
        }
        # 获取用例执行后的通过率，返回成功或失败
        sql_num = "SELECT SUM(CASE WHEN a.testresult = 1 THEN 1 ELSE 0 END) count_success,SUM(CASE WHEN a.testresult = 2 THEN 1 ELSE 0 END) count_fail,SUM(CASE WHEN a.testresult is  null THEN 1 ELSE 0 END) count_null,count(*) total from quality_testapi a," \
                  + "quality_executinglog b WHERE a.testapi_id=b.executing_testapi_id AND b.executing_testmd=" + "\'" + executing_testmd + "\'"
        TestcaseNum = commonList().getModelData(sql_num)
        Log().info("TestcaseNum%s"%TestcaseNum)
        if int(TestcaseNum[0]['count_fail'])!=0:
            exectResult='执行失败'
        else:
            exectResult='执行成功'
        excutePassRate=(int(TestcaseNum[0]['count_success'])/int(TestcaseNum[0]['total']))
        excutePassRate=(round(excutePassRate,2))*100
        print('通过率',excutePassRate)
        message='【'+versionName+'】'+"接口自动化巡检\n"\
                '【执行人】'+executName+'\n'\
                '【运行结果】'+exectResult+'\n'\
                '【执行通过率】'+str(excutePassRate)+'%\n'\
                '【运行URL地址】'+testReportUrl+'\n'
        passRate=(TestcaseNum[0]['count_success'])/int(TestcaseNum[0]['total'])
        String_message={
            "msgtype":"text",
            "text":{"content":message},
            "at":{
                "atMobiles": [ding_people],
                "isAtAll":0
            }
        }
        String_textMsg=json.dumps(String_message)
        print("获取到的String_textMsg",String_textMsg)
        print(type(passRate))
        print("endString",int(int(passRate)/100))

        if int(excutePassRate)<100:
            # response=requests.post(url,data=String_textMsg,headers=HEADERS)
            print("执行用例失败注意查看通知")
            # pass
        else:
            print("没有失败执行的用例可以不用发通知")

class requestObject(responseExecuting):
    '''
    url:请求URL
    header:请求头
    data:请求参数
    cookies：请求cookies
    '''
    def __init__(self,url,header,data,method,cookies,apiExtractName,passWordFree,addPassWordFree):
        # print('初始化request')
        self.url=url
        self.header=header
        self.data=data
        self.method = method
        self.cookies=cookies
        self.apiExtractName=apiExtractName
        self.passWordFree=passWordFree
        self.addPassWordFree=addPassWordFree
        responseExecuting.__init__(self)
        # print((data))
        # log.info('url=%s;header=%s;data=%s;cookies=%s;apiExtractName=%s;apiExtractExpression=%s;passWordFree=%s;addPassWordFree=%s;'%(url,header,data,cookies,apiExtractName,apiExtractExpression,passWordFree,addPassWordFree))


    @msglogger
    def requestApi(self):
        '''request请求'''
        if self.url=='':
            return ("url为空")
        elif self.header=='':
            return ("header为空")
        elif self.data=='' and self.cookies=='':
            __response=self._requestDataCookies()
            # self.executing(__response,self.passWordFree,self.addPassWordFree,self.apiExtractName)
            return __response
        elif self.data=='' and self.cookies!='':
            __response=self._requestCookies()
            # self.executing(__response,self.passWordFree,self.addPassWordFree,self.apiExtractName)
            return __response
        elif self.cookies=='' and self.data!='':
            __response=self._requestData(self.method)
            # self.executing(__response,self.passWordFree,self.addPassWordFree,self.apiExtractName)
            return __response
        else:
            __response=requests.get(url=self.url,headers=self.header,data=self.data,cookies=self.cookies)
            # self.executing(__response,self.passWordFree,self.addPassWordFree,self.apiExtractName)
            return __response
    @msglogger
    def _requestDataCookies(self):
        '''不包含请求参数和cookies'''
        # print('url',self.url)
        s=requests.Session()
        response=s.get(url=self.url,headers=self.header,allow_redirects=False)
        # print('缓存的cookies=%s'%requests.cookies)
        # print('获取响应设置的cookies=%s'%response.headers['Set-Cookie'])
        return response
    @msglogger
    def _requestData(self,requestMethod):
        '''仅包含请求参数'''
        if requestMethod=='1':
            response=requests.get(url=self.url,data=self.data.encode(),headers=self.header)
        if requestMethod == '2':
            response = requests.post(url=self.url, data=self.data.encode(), headers=self.header)
        if requestMethod=='3':
            response=requests.put(url=self.url,data=self.data.encode(),headers=self.header)
        if requestMethod=='4':
            response=requests.delete(url=self.url,data=self.data.encode(),headers=self.header)
        return response
    @msglogger
    def _requestCookies(self):
        '''仅包含请求cookies'''
        response=requests.get(url=self.url,headers=self.header,cookies=self.cookies,allow_redirects=False)
        print('cookies=%s'%response.cookies)
        return response

if __name__=='__main__':
    url='http://a.iyunxiao.com/mkp?go=http://2Fmkp.yunxiao.com'
    header={'Content-Type':'application/json;charset=UTF-8'}
    cookies={"GO_TOKEN":"93a756c6064e29c0adb73409940f8c103cef8ec41f0234cfdeda682ed641dded00ce15cb0692e4245d5f32e0047db884"}
    apiExtractName='token'
    apiExtractExpression='token=(.+?)&go='
    requestObject(url,header,data=None,cookies=cookies,apiExtractName=apiExtractName,apiExtractExpression=None,passWordFree=True,addPassWordFree=False).requestApi()