import requests,datetime,hashlib
from quality.common.commonbase import commonList
class APITest:
    '''
        -login--登录获取cookies
        -apiRequest--request请求
    '''

    # @msglogger
    def _sortString(self, stringList):
        '''替换字符串'''
        print('stringList', stringList)
        import copy
        stringStartIndex = stringList.find('$')
        stringEndIndex = stringList.find('}')
        stringValiable = stringList[stringStartIndex:stringEndIndex + 1]
        print("==============stringValiable======================", stringValiable)

        # 查找要替换的字符串
        srcString = stringList
        parameter = stringValiable[2:-1]
        sql = 'select * from quality_testvariable where variableKey=' + "'" + parameter + "'"

        parameterSpl = commonList().getModelData(sql)
        afterParameter = parameterSpl[0]['variableValue']
        print("afterParameter", afterParameter)

        stringList = srcString.replace(stringValiable, afterParameter)
        import copy
        finallyString = copy.deepcopy(stringList)
        print("======replaceParameter=====", stringList)
        # 替换后再次查找字符串
        print("======num========", finallyString.find('${'))
        if "${"  in finallyString:
            return self._sortString(finallyString)
        return  finallyString

    def Hashlib(self):
        '''
        生成md5
        '''
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        m2=hashlib.md5()
        m2.update(now.encode("utf8"))
        return m2.hexdigest()
    def requestNoCookie(self,url,data,requestMethod,testapiHeader):
        '''接口请求没有cookies'''
        #处理请求头数据
        header=self._sortHeader(testapiHeader)
        # header = {
        #     'Content-Type': 'application/json'
        # }
        if requestMethod=='1':
            response=requests.get(url=url,data=data.encode(),headers=header)
        if requestMethod == '2':
            response = requests.post(url=url, data=data.encode(), headers=header)
        if requestMethod=='3':
            response=requests.put(url=url,data=data.encode(),headers=header)
        if requestMethod=='4':
            response=requests.delete(url=url,data=data.encode(),headers=header)
        return  response
    def _sortHeader(self,testapiHeader):
        '''过滤请求头'''
        if len(testapiHeader)==0:
            header = {
                'Content-Type': 'application/json'
            }
            return  header
        else:
            finalHeader={}
            for headerData in testapiHeader:
                print('headerData',headerData)
                if  headerData['key']=='':
                    pass
                else:
                    header={}
                    header[headerData['key']]=headerData['value']
                    finalHeader.update(header)
            if  'Content-Type' not in finalHeader.keys():
                finalHeader['Content-Type']='application/json'
            return finalHeader
    def login(self,url,data):
        '''登录获取cookies'''
        global cookies
        header={
                    'Content-Type':'application/json'
                }
        s = requests.Session()
        # s.post(url,data=data,headers=header)
        data=s.post(url,data=data,headers=header,verify=False,allow_redirects=True)
        # cookies=s.cookies
        return data
    def updataCookies(self,url,data):
        '''更新cookies'''
        header={
                    'Content-Type':'application/json;charset=UTF-8'
                }
        s = requests.Session()
        s.post(url,data=data,headers=header,verify=False)
        return s.cookies


    def apiRequest(self,url,data,method,cookies):
        '''request请求'''
        try:
            s = requests.Session()
            s.cookies.update(cookies)
            if s.cookies:
                header={

                    'Content-Type': 'application/json;charset=UTF-8;'
                }
                if method=="1":
                    print("get方法")
                    response=s.get(url,headers=header)
                    responseData=response
                elif method=="2":
                    print("post方法")
                    response=s.post(url,data=data,headers=header,allow_redirects=True)
                    responseData=response
                else:
                    responseData={}
            else:
                responseData="获取的cookies为空"
        except Exception as e:
            responseData=e   
        return responseData
        
