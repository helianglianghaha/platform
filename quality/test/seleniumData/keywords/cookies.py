class cookiesKeywords:
    def addCookies(self,driver,name,value):
        '''
        :param name:
        :param value:
        :return:
        '''
        new_cookie={'name':name,'value':value}
        driver.add_cookie(new_cookie)