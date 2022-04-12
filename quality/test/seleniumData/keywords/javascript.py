from quality.common.logger import Log
from selenium import  webdriver
class JavaScript():
    def __init__(self):
        self.log=Log()
    def execute_javascript(driver,locator,args):
        '''
        JS执行
        prams:args
        '''
        # try:
        # Log().log.info("execute_javascript执行的参数为",args)
        # targent=driver.find_element_by_xpath(args)s
        # print('targent',targent)
        # args="var q=document.getElementByXpath('//*[@id=\'dropdown-menu-2483\']').scrollTop=100000"    //*[@id="app-m1"]/div[1]
        print("开始执行下滑")
        target = driver.find_element_by_xpath(locator)
        driver.execute_script(args,target)
        print("执行下滑结束")
        # except Exception as e:
        #     raise e
        #     self.log.error("execute_javascript执行出错")