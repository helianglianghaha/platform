from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
class Page():
    def __init__(self):
        '''
            定义driver
        '''
        print('初始化')
        self.driver=webdriver.Chrome()
    
    def openUrl(self,url):
        '''
            打开URL
        '''
        self.driver.get(url)
        self.driver.maxmize_window()
    def quitBrowser(self):
        '''
            退出浏览器
        '''
        self.driver.quit()
    def find_element(self,method,*loc):
        ''' 
            元素定位方法
            {"value":"1","label":"ID"},
            {"value":"2","label":"Name"},
            {"value":"3","label":"ClassName"},
            {"value":"4","label":"TagName"},
            {"value":"5","label":"LinkText"},
            {"value":"6","label":"Xpath"},
            {"value":"7","label":"CssSelector"},        
        '''
        wait=WebDriverWait(self.driver,timeout=10)
        wait.until(lambda x:x.find_element(*loc).is_displayed())
        if method=='1':
            return self.driver.find_element_by_id(*loc)
        elif method=='2':
            return self.driver.find_element_by_name(*loc)
        elif method=='3':
            return self.driver.find_element_by_class_name(*loc)
        elif method=='4':
            return self.driver.find_element_by_tag_name(*loc)
        elif method=='5':
            return self.driver.find_element_by_link_text(*loc)
        elif method=='6':
            return self.driver.find_element_by_xpath(*loc)
        else:
            return self.driver.find_element_by_css_selector(*loc)
    def clearElement(self,method,*loc):
        '''
            清空
        '''
        element=self.find_element(method,*loc)
        element.clear()
    def clickElement(self,method,*loc):
        '''
            点击单个元素
        '''
        element=self.find_element(method,*loc)
        element.click()
    def sendKeys(self,method,*loc,parmeter):
        '''
            输入值
        '''
        element=self.find_element(method,*loc)
        element.send_keys(parmeter)