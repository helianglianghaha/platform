from selenium import webdriver
# import sys
# sys.path.append("E:\\quality\\quality2019722\\quality\\test")
# print(sys.path)
# from types import is_truthy
# from utils.typeslist import is_string,is_truthy
from quality.test.seleniumData.keywords.connectioncache import ConnectionCache
# from keywords.connectioncache import ConnectionCache




class WebDriverCreator():

    browser_names = {
        'googlechrome': "chrome",
        'gc': "chrome",
        'chrome': "chrome",
        'headlesschrome': 'headless_chrome',
        'ff': 'firefox',
        'firefox': 'firefox',
        'headlessfirefox': 'headless_firefox',
        'ie': 'ie',
        'internetexplorer': 'ie',
        'edge': 'edge',
        'opera': 'opera',
        'safari': 'safari',
        'phantomjs': 'phantomjs',
        'htmlunit': 'htmlunit',
        'htmlunitwithjs': 'htmlunit_with_js',
        'android': 'android',
        'iphone': 'iphone'
    }
    def __int__(self,command_executor):
        self.command_executor=command_executor
    def create_driver(self, browser, desired_capabilities, remote_url,
                      profile_dir=None):
        creation_method = self._get_creator_method(browser)
        return creation_method(desired_capabilities, remote_url)
    def _get_creator_method(self, browser):
        browser = browser.lower().replace(' ', '')
        print('browser',browser)
        if browser in self.browser_names:
            return getattr(self, 'create_{}'.format(self.browser_names[browser]))
        raise ValueError('{} is not a supported browser.'.format(browser))
    def create_chrome(self, desired_capabilities, remote_url, options=None):
        desired_capabilities = {'desired_capabilities': webdriver.DesiredCapabilities.CHROME.copy()}
        command_executor={'command_executor':'http://172.17.85.7:6006/wd/hub'}
        # return webdriver.Remote(**desired_capabilities,**command_executor)
        # return webdriver.Remote(**desired_capabilities)
        return webdriver.Chrome(**desired_capabilities)
    def create_ie(self, desired_capabilities, remote_url, options=None):
        desired_capabilities = {'desired_capabilities': webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()}
        return webdriver.Ie(**desired_capabilities)
    def create_firefox(self, desired_capabilities, remote_url, options=None):
        desired_capabilities = {'desired_capabilities': webdriver.DesiredCapabilities.FIREFOX.copy()}
        return webdriver.Firefox(**desired_capabilities)
class WebDriverCache(ConnectionCache):
    def __init__(self):
        ConnectionCache.__init__(self, no_current_msg='No current browser')
        self._closed = set()

    @property
    def drivers(self):
        return self._connections

    @property
    def active_drivers(self):
        open_drivers = []
        for driver in self._connections:
            if driver not in self._closed:
                open_drivers.append(driver)
        return open_drivers

    def close(self):
        if self.current:
            driver = self.current
            driver.quit()
            self.current = self._no_current
            self._closed.add(driver)

    def close_all(self):
        for driver in self._connections:
            if driver not in self._closed:
                driver.quit()
        self.empty_cache()
        return self.current