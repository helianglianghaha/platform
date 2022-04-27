import requests,re
# import cookieslib,urll
# from quality.common.commonbase
from quality.common.commonbase import commonList
from quality.common.logger import Log
from quality.common.msg import msglogger
from ..API.APIClass import  APITest
from django.db import connection
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
        # conv=converters.conversions
        # conv[246]=float
        # conv[10] = str
        # conv[7]  = str
        # conv[12] = str
        # conv[11] = str
        self.db_config={
            'host': 'rm-uf60nso6wlf92lhtjzo.mysql.rds.aliyuncs.com',
            'user': 'root1',
            'password': 'Goodlearning2021@@',
            'port': 3306,
            'database':'lz_ems',
            'charset':'utf8',
            # 'conv':'conv'
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
                    jsonData=jsonpath.jsonpath(sourceData,oneAssertData['assertVariable'])
                    if len(jsonData)>0:
                        if str(jsonData[0])==oneAssertData["assertVariAbleValue"]:
                            oneAssertData['assertResult'] = "success"
                            resultData["resultList"].append("success")
                        else:
                            oneAssertData['assertResult'] ="预期json值是"+str(oneAssertData["assertVariAbleValue"])+"实际json值是"+str(jsonData)
                            resultData["resultList"].append("fail")
                    else:
                        oneAssertData['assertResult'] = "提取的值为空"
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
        conn=pymysql.connect(**self.db_config)

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
    def executing(self,response,passWordFree,addPassWordFree,apiExtractName,apiExtractExpression):
        print('executing')
        log.info('passWordFree=%s&&&addPassWordFree=%s&&&apiExtractName=%s&&&apiExtractExpression=%s'%(passWordFree,addPassWordFree,apiExtractName,apiExtractExpression))
        if passWordFree and not addPassWordFree:
            self._execuPassWord(response,apiExtractName,apiExtractExpression)
        elif addPassWordFree and not passWordFree:
            self._execuAddPass(response,apiExtractName,apiExtractExpression)
        elif passWordFree and addPassWordFree:
            self._execuPassAddWord(response,apiExtractName,apiExtractExpression)
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
class requestObject(responseExecuting):
    '''
    url:请求URL
    header:请求头
    data:请求参数
    cookies：请求cookies
    '''
    def __init__(self,url,header,data,method,cookies,apiExtractName,apiExtractExpression,passWordFree,addPassWordFree):
        # print('初始化request')
        self.url=url
        self.header=header
        self.data=data
        self.method = method
        self.cookies=cookies
        self.apiExtractName=apiExtractName
        self.apiExtractExpression=apiExtractExpression
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
            self.executing(__response,self.passWordFree,self.addPassWordFree,self.apiExtractName,self.apiExtractExpression)
            return __response
        elif self.data=='' and self.cookies!='':
            __response=self._requestCookies()
            self.executing(__response,self.passWordFree,self.addPassWordFree,self.apiExtractName,self.apiExtractExpression)
            return __response
        elif self.cookies=='' and self.data!='':
            __response=self._requestData(self.method)
            self.executing(__response,self.passWordFree,self.addPassWordFree,self.apiExtractName,self.apiExtractExpression)
            return __response
        else:
            __response=requests.get(url=self.url,headers=self.header,data=self.data,cookies=self.cookies)
            self.executing(__response,self.passWordFree,self.addPassWordFree,self.apiExtractName,self.apiExtractExpression)
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