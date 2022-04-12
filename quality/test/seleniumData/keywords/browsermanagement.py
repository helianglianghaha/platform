import time
import types

from selenium import webdriver
import  sys
from quality.test.seleniumData.keywords.webdrivertools import WebDriverCache,WebDriverCreator
from quality.common.logger import Log
from selenium import  webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# from keywords.webdrivertools import WebDriverCreator,WebDriverCache
# from keywords.connectioncache import ConnectionCache
# from webdrivertools import WebDriverCreator
from quality.test.seleniumData.prams import connectionList
# from prams import connectionList
class BrowserManagement(WebDriverCache):
    def __int__(self):
        self.log=Log()
    def open_browser(self, url,command_executor, browser='firefox',alias=None,
                     remote_url=False, desired_capabilities=None,
                     ff_profile_dir=None):
        # command_executor = {'command_executor': 'http://172.17.82.102:6006/wd/hub'}
        # driver = self._make_driver(browser, desired_capabilities,
        #                            ff_profile_dir, remote_url)
        driver=webdriver.Remote(command_executor=command_executor,
                          desired_capabilities=DesiredCapabilities.CHROME)
        try:
            driver.get(url)
            driver.maximize_window()
            print('connectionList_browser',connectionList)
            return driver
        except Exception:
            print("初始化浏览器失败")
    def gotoBroswer(self,driver,url):
        driver.get(url)
    def fresh(self,driver):
        driver.refresh()
    def _make_driver(self, browser,desired_capabilities=None,
                     profile_dir=None, remote=None):
        driver=WebDriverCreator().create_driver(
            browser=browser, desired_capabilities=desired_capabilities,
            remote_url=remote, profile_dir=profile_dir)
        driver.maximize_window()
        driver.set_script_timeout(30)
        driver.implicitly_wait(10)
        return driver
    def close_broswer(self,driver):
        '''关闭浏览器'''
        try:
            driver.quit()
            self.log.info("关闭浏览器成功")
        except:
            self.log.error(self.close_broswer.__name__+self.close_broswer.__doc__+":执行出错")
    def switch_browser(self,driver,index_alias):
        '''
        切换浏览器
        '''
        try:
            driver.switch(index_alias)
        except:
            self.log.error("no browser with index_alias %s found"%index_alias)
