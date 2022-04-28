import sys,traceback

sys.path.append("E:\\quality\\quality2019722\\quality\\test")
# from locatorsList.elementfinderList import ElementFinderList
from quality.test.seleniumData.locatorsList.elementfinderList import ElementFinderList
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # 导入keys
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
from quality.common.logger import Log
from quality.view.API_version.API_model import Testpicture, Testscript
#import time, os, win32gui, win32con
from quality.test.seleniumData.prams import connectionList, handles
from selenium.common.exceptions import TimeoutException
# from prams import connectionList
# from utils.typeslist import is_falsy
# from base.context import ContextList
# from keywords.webdrivertools import WebDriverCache
from quality.test.seleniumData.keywords.connectioncache import ConnectionCache


class Elementkeywords(ConnectionCache):
    def __init__(self):
        self.log = Log()

    def click_element(self, driver, locators, modifier=False):
        if self._find_element(locators):
            driver._find_element(locators).click()
        else:
            driver._click_with_modifier(locators)

    def keyBoardKeys(self, driver, loctor, sendKeys):
    #     NULL = '\ue000'
    #     CANCEL = '\ue001'  # ^break
    #     HELP = '\ue002'
    #     BACKSPACE = '\ue003'
    #     BACK_SPACE = BACKSPACE  # 删除键
    #     TAB = '\ue004'  # TAB键
    #     CLEAR = '\ue005'
    #     RETURN = '\ue006'  # 键盘返回键
    #     ENTER = '\ue007'  # 回车键
    #     SHIFT = '\ue008'  # Shift键
    #     LEFT_SHIFT = SHIFT
    #     CONTROL = '\ue009'
    #     LEFT_CONTROL = CONTROL  # Ctrl 键
    #     ALT = '\ue00a'  # Alt 键
    #     LEFT_ALT = ALT
    #     PAUSE = '\ue00b'
    #     ESCAPE = '\ue00c'  # ECS键
    #     SPACE = '\ue00d'  # 空格键
    #     PAGE_UP = '\ue00e'  # PgUp 键
    #     PAGE_DOWN = '\ue00f'  # PgDwon 键
    #     END = '\ue010'  # END 键
    #     HOME = '\ue011'  # HOME 键
    #     LEFT = '\ue012'  # 左键
    #     ARROW_LEFT = LEFT
    #     UP = '\ue013'  # 上键
    #     ARROW_UP = UP
    #     RIGHT = '\ue014'
    #     ARROW_RIGHT = RIGHT  # 右键
    #     DOWN = '\ue015'  # 下键
    #     ARROW_DOWN = DOWN  # 键盘向下的箭头
    #     INSERT = '\ue016'  # insert键
    #     DELETE = '\ue017'  # del键
    #
    #     SEMICOLON = '\ue018'  # ';'键
    #     EQUALS = '\ue019'  # '='键
    #
    # 　　  # 数字键盘
    # NUMPAD0 = '\ue01a'  # number pad keys
    # NUMPAD1 = '\ue01b'
    # NUMPAD2 = '\ue01c'
    # NUMPAD3 = '\ue01d'
    # NUMPAD4 = '\ue01e'
    # NUMPAD5 = '\ue01f'
    # NUMPAD6 = '\ue020'
    # NUMPAD7 = '\ue021'
    # NUMPAD8 = '\ue022'
    # NUMPAD9 = '\ue023'
    # MULTIPLY = '\ue024'  # '*' 键
    # ADD = '\ue025'  # '+' 键
    # SEPARATOR = '\ue026'  # ','键
    # SUBTRACT = '\ue027'  # '-' 键
    # DECIMAL = '\ue028'  # '.'键
    # DIVIDE = '\ue029'  # '/'键
    #
    # F1 = '\ue031'  # function  keys
    # F2 = '\ue032'
    # F3 = '\ue033'
    # F4 = '\ue034'
    # F5 = '\ue035'
    # F6 = '\ue036'
    # F7 = '\ue037'
    # F8 = '\ue038'
    # F9 = '\ue039'
    # F10 = '\ue03a'
    # F11 = '\ue03b'
    # F12 = '\ue03c'
    #
    # META = '\ue03d'
    # COMMAND = '\ue03d'
        try:
            if sendKeys.upper() == 'ADD':
                driver.find_element_by_xpath(loctor).send_keys(Keys.ADD)
            if sendKeys.upper() == 'ALT':
                driver.find_element_by_xpath(loctor).send_keys(Keys.ALT)
            if sendKeys.upper() == 'ARROW_DOWN':
                driver.find_element_by_xpath(loctor).send_keys(Keys.ARROW_DOWN)
            if sendKeys.upper() == 'ARROW_LEFT':
                driver.find_element_by_xpath(loctor).send_keys(Keys.ARROW_LEFT)
            if sendKeys.upper() == 'ARROW_RIGHT':
                driver.find_element_by_xpath(loctor).send_keys(Keys.ARROW_RIGHT)
            if sendKeys.upper() == 'ARROW_UP':
                driver.find_element_by_xpath(loctor).send_keys(Keys.ARROW_UP)
            if sendKeys.upper() == 'BACK_SPACE':
                driver.find_element_by_xpath(loctor).send_keys(Keys.BACK_SPACE)
            if sendKeys.upper() == 'CANCEL':
                driver.find_element_by_xpath(loctor).send_keys(Keys.CANCEL)
            if sendKeys.upper() == 'DELETE':
                driver.find_element_by_xpath(loctor).send_keys(Keys.DELETE)
            if sendKeys.upper() == 'ENTER':
                driver.find_element_by_xpath(loctor).send_keys(Keys.ENTER)
            if sendKeys.upper() == 'DOWN':
                driver.find_element_by_xpath(loctor).send_keys(Keys.DOWN)
        except:
            self.log.info(traceback.format_exc())

    def getUrl(self, driver, url):
        try:
            driver.get(url)
        except:
            self.log.info(traceback.format_exc())

    def element_is_displayed(self, driver, locator):
        '''元素是否可见'''
        try:
            self.log.info('driver信息为' + str(driver) + "------" + "定位的元素是：" + locator)
            is_display = driver.find_element_by_xpath(locator).is_displayed()
            return is_display
        except:
            self.log.info(traceback.format_exc())

    def element_is_selected(self, driver, locator):
        '''元素是否被选中'''
        try:
            self.log.info('driver信息为' + str(driver) + "------" + "定位的元素是：" + locator)
            is_selected = driver.find_element_by_xpath(locator).is_selected()
            print('element_is_selected', is_selected)
            return is_selected
        except:
            self.log.info(traceback.format_exc())

    def clear_element_vaule(self, driver, loctor):
        '''清除元素信息'''
        try:
            self.log.info('driver信息为' + str(driver) + "------" + "清除的元素是：" + loctor)
            driver.find_element_by_xpath(loctor).clear()
        except:
            self.log.info(traceback.format_exc())

    def send_keys(self, driver, loctor, sendKeys):
        # if method=="xpath":
        try:
            self.log.info('driver信息为' + str(driver) + "------" + "定位的元素是：" + loctor + "------" + "传参" + sendKeys)
            driver.find_element_by_xpath(loctor).send_keys(sendKeys)
        except:
            self.log.info(traceback.format_exc())

    def click(self, driver, allElement, loctor):
        '''
        ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"
        :param driver:
        :param allElement:
        :param loctor:
        :return:
        '''
        try:
            print('========element', allElement)
            self.log.info('driver信息为' + str(driver) + "------" + "定位的元素是：" + loctor + "------")
            if allElement['script_testDataPositioning'] == 'Xpath':
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, loctor))).click()
            if allElement['script_testDataPositioning'] == 'ID':
                WebDriverWait(driver, 8, 1).until(EC.presence_of_element_located((By.ID, loctor))).click()
            if allElement['script_testDataPositioning'] == 'LINK_TEXT':
                WebDriverWait(driver, 8, 1).until(EC.presence_of_element_located((By.LINK_TEXT, loctor))).click()
            if allElement['script_testDataPositioning'] == 'PARTIAL_LINK_TEXT':
                WebDriverWait(driver, 8, 1).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, loctor))).click()
            if allElement['script_testDataPositioning'] == 'NAME':
                WebDriverWait(driver, 8, 1).until(EC.presence_of_element_located((By.NAME, loctor))).click()
            if allElement['script_testDataPositioning'] == 'TAG_NAME':
                WebDriverWait(driver, 8, 1).until(EC.presence_of_element_located((By.TAG_NAME, loctor))).click()
            if allElement['script_testDataPositioning'] == 'CLASS_NAME':
                WebDriverWait(driver, 8, 1).until(EC.presence_of_element_located((By.CLASS_NAME, loctor))).click()
            if allElement['script_testDataPositioning'] == 'CSS_SELECTOR':
                WebDriverWait(driver, 8, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, loctor))).click()
        except:
            self.log.info(traceback.format_exc())
    def forcedWait(self, waitTime):
        '''强制等待'''
        try:
            time.sleep(waitTime)
        except:
            self.log.info(traceback.format_exc())

    def impicitlyWait(self, driver, waitTime):
        '''隐式等待'''
        try:
            driver.implicitly_wait(waitTime)
        except:
            self.log.info(traceback.format_exc())
    def uploadField(self, filePath, browser_type="chrome"):
        '''
        通过pywin32模块实现文件上传的操作
        :param filePath: 文件的绝对路径
        :param browser_type: 浏览器类型（默认值为chrome）
        :return:
        '''
        print("1234567890-====================")
        if browser_type.lower() == "chrome":
            title = "打开"
        elif browser_type.lower() == "firefox":
            title = "文件上传"
        elif browser_type.lower() == "ie":
            title = "选择要加载的文件"
        else:
            title = ""  # 这里根据其它不同浏览器类型来修改
            # 找元素
        # 一级窗口"#32770","打开"
        dialog = win32gui.FindWindow("#32770", title)
        # 向下传递
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, "ComboBoxEx32", None)  # 二级
        comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, "ComboBox", None)  # 三级
        # 编辑按钮
        edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)  # 四级
        # 打开按钮
        button = win32gui.FindWindowEx(dialog, 0, 'Button', "打开(&O)")  # 二级
        # 输入文件的绝对路径，点击“打开”按钮
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, filePath)  # 发送文件路径
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 点击打开按钮

    def element_isSelected(self, driver, excepted, testCaseList):
        '''
        断言元素是否被选择
        :param driver:
        :param excepted:
        :param testCaseList:
        :return:
        '''
        try:
            self._savePictureFile()
            picture_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
            isSelected = self.element_is_selected(driver, excepted)
            print('isSelected', isSelected)
            if isSelected:
                self._saveTestResult(testCaseList['script_id'], testResult="成功")
            else:
                self.log.error('**********断言元素失败元素不可见**********' + '定位的元素为' + excepted)
                picture_dir = os.getcwd() + 'static' + '\\' + picture_time + "-" + testCaseList[
                    'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                    testCaseList['script_TestDataCase']) + '.png'
                driver.save_screenshot(picture_dir)
                picture_name = 'http://172.17.32.253:8030/static/' + picture_time + "-" + testCaseList[
                    'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                    testCaseList['script_TestDataCase']) + '.png'
                self._savePicture(testCaseList['script_id'], testCaseList['script_TestDataCase'], picture_name)
                self._saveTestResult(testCaseList['script_id'], testResult="失败")
        except:
            self.log.error('**********断言元素失败元素不可见**********' + '定位的元素为' + excepted)
            self.log.info(traceback.format_exc())
            picture_dir = os.getcwd() + 'static' + '\\' + picture_time + "-" + testCaseList[
                'script_testDataName'] + "-" + str(
                testCaseList['script_id']) + "-" + str(testCaseList['script_TestDataCase']) + '.png'
            driver.save_screenshot(picture_dir)
            picture_name = 'http://172.17.32.253:8030/static/' + picture_time + "-" + testCaseList[
                'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                testCaseList['script_TestDataCase']) + '.png'
            self._savePicture(testCaseList['script_id'], testCaseList['script_TestDataCase'], picture_name)
            self._saveTestResult(testCaseList['script_id'], testResult="失败")

    def element_isDisplay(self, driver, excepted, testCaseList):
        '''
        断言元素是否可见
        :param driver:
        :param excepted:
        :param testCaseList:
        :return:
        '''
        try:
            self._savePictureFile()
            picture_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
            isDisplay = self.element_is_displayed(driver, excepted)
            if isDisplay:
                self._saveTestResult(testCaseList['script_id'], testResult="成功")
            else:
                self.log.error('**********断言元素失败元素不可见**********' + '定位的元素为' + excepted)
                picture_dir = '.\\' + 'static' + '\\' + picture_time + "-" + testCaseList[
                    'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                    testCaseList['script_TestDataCase']) + '.png'
                driver.save_screenshot(picture_dir)
                picture_name = 'http://172.17.32.253:8030/static/' + picture_time + "-" + testCaseList[
                    'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                    testCaseList['script_TestDataCase']) + '.png'
                self._savePicture(testCaseList['script_id'], testCaseList['script_TestDataCase'], picture_name)
                self._saveTestResult(testCaseList['script_id'], testResult="失败")
        except :
            self.log.error('**********断言元素失败元素不可见**********' + '定位的元素为' + excepted)
            self.log.info(traceback.format_exc())
            picture_dir = '.\\' + 'static' + '\\' + picture_time + "-" + testCaseList[
                'script_testDataName'] + "-" + str(
                testCaseList['script_id']) + "-" + str(testCaseList['script_TestDataCase']) + '.png'
            driver.save_screenshot(picture_dir)
            picture_name = 'http://172.17.32.253:8030/static/' + picture_time + "-" + testCaseList[
                'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                testCaseList['script_TestDataCase']) + '.png'
            self._savePicture(testCaseList['script_id'], testCaseList['script_TestDataCase'], picture_name)
            self._saveTestResult(testCaseList['script_id'], testResult="失败")

    def element_value_should_contains(self, driver, excepted, value, testCaseList):
        '''
        断言元素的值，断言失败保存图片到数据库
        :param driver:
        :param excepted:
        :param testCaseList:
        :return:
        '''
        self._saveTestResult(testCaseList['script_id'], testResult=" ")
        try:
            self.log.info(
                "=================================element_value_should_contains  start begin working============================")
            self.log.info('driver信息为' + str(driver) + "------" + "断言元素：" + excepted + "------")
            picture_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
            File_Path = os.getcwd() + '\\' + 'screenshotPicture' + '\\'
            if not os.path.exists(File_Path):
                os.makedirs(File_Path)
            element_value = self._findValueElement(driver, testCaseList, excepted)
            print('返回的值为', element_value)
            print('预期的返回值为', value)
            self.log.info('返回的值为'+element_value+"预期的返回值为"+value)
            if element_value == value:
                self._saveTestResult(testCaseList['script_id'], testResult="成功")
            else:
                self.log.error('**********断言元素失败**********' + '定位的元素为' + excepted)
                picture_dir = 'C:\\TestPlat\\platForm\\static' + '\\' + picture_time + "-" + testCaseList[
                    'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                    testCaseList['script_TestDataCase']) + '.png'
                driver.save_screenshot(picture_dir)
                picture_name = 'http://172.17.32.253:8030/static/' + picture_time + "-" + testCaseList[
                    'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                    testCaseList['script_TestDataCase']) + '.png'
                self._savePicture(testCaseList['script_id'], testCaseList['script_TestDataCase'], picture_name)
                self._saveTestResult(testCaseList['script_id'], testResult="失败")
            self.log.info(
                "=================================element_value_should_contains  ending working============================")
        except :
            self.log.info(traceback.format_exc())
            picture_dir = 'C:\\TestPlat\\platForm\\static' + '\\' + picture_time + "-" + testCaseList[
                'script_testDataName'] + "-" + str(
                testCaseList['script_id']) + "-" + str(testCaseList['script_TestDataCase']) + '.png'
            driver.save_screenshot(picture_dir)
            picture_name = 'http://172.17.32.253:8030/static/' + picture_time + "-" + testCaseList[
                'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                testCaseList['script_TestDataCase']) + '.png'
            self._savePicture(testCaseList['script_id'], testCaseList['script_TestDataCase'], picture_name)
            self._saveTestResult(testCaseList['script_id'], testResult="失败")

    def _savePictureFile(self):
        '''创建文件夹'''
        File_Path = os.getcwd() + '\\' + 'screenshotPicture' + '\\'
        if not os.path.exists(File_Path):
            os.makedirs(File_Path)

    def element_should_contains(self, driver, excepted, testCaseList):
        '''
        断言失败保存图片到数据库
        prams:
        driver:驱动信息
        excepted:预期元素信息
        testCaseList：用例信息
        '''
        try:
            self.log.info('driver信息为' + str(driver) + "------" + "断言元素：" + excepted + "------")
            picture_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
            # print(os.getcwd())
            self._savePictureFile()
            self._findElement(driver, testCaseList, excepted)
            self._saveTestResult(testCaseList['script_id'], testResult="成功")
        except:
            self.log.error('**********断言元素失败**********' + '定位的元素为' + excepted)
            self.log.info(traceback.format_exc())
            picture_dir = '.\\' + 'static' + '\\' + picture_time + "-" + testCaseList[
                'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                testCaseList['script_TestDataCase']) + '.png'
            driver.save_screenshot(picture_dir)
            picture_name = 'http://172.17.32.253:8030/static/' + picture_time + "-" + testCaseList[
                'script_testDataName'] + "-" + str(testCaseList['script_id']) + "-" + str(
                testCaseList['script_TestDataCase']) + '.png'
            self._savePicture(testCaseList['script_id'], testCaseList['script_TestDataCase'], picture_name)
            self._saveTestResult(testCaseList['script_id'], testResult="失败")

    def _saveTestResult(self, script_id, testResult):
        '''
        保存测试结果
        '''
        try:
            _testResult = Testscript.objects.get(script_id=script_id)
            _testResult.script_testResult = testResult
            _testResult.save()
        except:
            self.log.info(traceback.format_exc())

    def _savePicture(self, picture_scriptId, picture_testcaseId, picture_file):
        '''
        保存图片到数据库
        '''
        # _picture=Testpicture.objects.get(picture_testcaseId=picture_testcaseId)
        # if _picture:
        #     _picture.picture_file = picture_file
        #     _picture.save()
        # else:
        try:
            _picture = Testpicture()
            _picture.picture_scriptId = picture_scriptId
            _picture.picture_testcaseId = picture_testcaseId
            _picture.picture_file = picture_file
            _picture.save()
        except:
            self.log.info(traceback.format_exc())

    def _findValueElement(self, driver, allElement, locator):
        '''
        查找元素值
        :param driver:
        :param allElement:
        :param locator:
        :return:
        '''
        try:
            if allElement['script_testDataPositioning'] == 'Xpath':
                text = (WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, locator)))).text
                return text
            if allElement['script_testDataPositioning'] == 'ID':
                text = (WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located((By.ID, locator)))).text
                return text
            if allElement['script_testDataPositioning'] == 'LINK_TEXT':
                text = (WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located((By.LINK_TEXT, locator)))).text
                return text
            if allElement['script_testDataPositioning'] == 'PARTIAL_LINK_TEXT':
                text = (
                    WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, locator)))).text
                return text
            if allElement['script_testDataPositioning'] == 'NAME':
                text = (WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located((By.NAME, locator)))).text
                return text
            if allElement['script_testDataPositioning'] == 'TAG_NAME':
                text = (WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located((By.TAG_NAME, locator)))).text
                return text
            if allElement['script_testDataPositioning'] == 'CLASS_NAME':
                text = (WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located((By.CLASS_NAME, locator)))).text
                return text
            if allElement['script_testDataPositioning'] == 'CSS_SELECTOR':
                text = (WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))).text
                return text
        except:
            self.log.info(traceback.format_exc())

    def _findElement(self, driver, allElement, locator):
        '''
        查找元素
        '''
        try:
            if allElement['script_testDataPositioning'] == 'Xpath':
                WebDriverWait(driver, 6, 1).until(EC.presence_of_element_located((By.XPATH, locator)))
            if allElement['script_testDataPositioning'] == 'ID':
                WebDriverWait(driver, 6, 1).until(EC.presence_of_element_located((By.ID, locator)))
            if allElement['script_testDataPositioning'] == 'LINK_TEXT':
                WebDriverWait(driver, 6, 1).until(EC.presence_of_element_located((By.LINK_TEXT, locator)))
            if allElement['script_testDataPositioning'] == 'PARTIAL_LINK_TEXT':
                WebDriverWait(driver, 6, 1).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, locator)))
            if allElement['script_testDataPositioning'] == 'NAME':
                WebDriverWait(driver, 6, 1).until(EC.presence_of_element_located((By.NAME, locator)))
            if allElement['script_testDataPositioning'] == 'TAG_NAME':
                WebDriverWait(driver, 6, 1).until(EC.presence_of_element_located((By.TAG_NAME, locator)))
            if allElement['script_testDataPositioning'] == 'CLASS_NAME':
                WebDriverWait(driver, 6, 1).until(EC.presence_of_element_located((By.CLASS_NAME, locator)))
            if allElement['script_testDataPositioning'] == 'CSS_SELECTOR':
                WebDriverWait(driver, 6, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))
        except:
            self.log.info(traceback.format_exc())
    def changeHandle(self, driver):
        try:
            now_handle = driver.current_window_handle
            all_handles_list = driver.window_handles
            for handle in all_handles_list:
                if handle != now_handle:
                    driver.switch_to.window(handle)
        except:
            self.log.info(traceback.format_exc())

    def change_OldHandle(self, driver):
        '''切换到老窗口'''
        try:
            all_handles_list = driver.window_handles
            driver.switch_to.window(all_handles_list[-2])
        except:
            self.log.info(traceback.format_exc())
    def close_handle(self, driver):
        '''关闭窗口'''
        try:
            driver.close()
        except:
            self.log.info(traceback.format_exc())

    def change_NewHandle(self, driver):
        try:
            all_handles_list = driver.window_handles
            driver.switch_to.window(all_handles_list[-1])
        except:
            self.log.info(traceback.format_exc())
    def switch_iframe(self,driver,locator):
        '''切换iframe'''
        try:
            driver.switch_to.frame(locator)
        except:
            self.log.info(traceback.format_exc())
    def switch_default_content(self,driver):
        '''切换到主iframe'''
        try:
            driver.switch_to.default_content()
        except:
            self.log.info(traceback.format_exc())
    def quit(self, driver):
        try:
            driver.quit()
        except:
            self.log.info(traceback.format_exc())

    def clickElements(self, driver, locator, number):
        try:
            driver.find_elements_by_xpath(locator)[int(number)].click()
        except:
            self.log.info(traceback.format_exc())

    def _find_element(self, locator, parent=None):
        try:
            ElementFinderList().find(locator, parent=parent)
        except:
            self.log.info(traceback.format_exc())

    def defaultContent(self, driver):
        '''
        切换到主页面
        '''
        try:
            driver.switch_to.default_content()
        except:
            self.log.info(traceback.format_exc())

    def element_disPlay(self, driver, locator):
        '''
        判断元素是否可见
        '''
        try:
            return driver.find_element_by_xpath(locator).is_display()
        except:
            self.log.info(traceback.format_exc())
    def actionPerform(self, driver, locator):
        '''
        鼠标悬浮
        '''
        try:
            action = ActionChains(driver)
            element = driver.find_element_by_xpath(locator)
            action.click(element)
            action.perform()
        except:
            self.log.info(traceback.format_exc())

    def mouseDrag(self, driver, locator, offest):
        '''
        鼠标拖拽
        click(on_element=None)  　　                #单击鼠标左键
        click_and_hold(on_element=None) 　　  #点击鼠标左键，按住不放
        context_click(on_element=None)           #点击鼠标右键
        double_click(on_element=None)            #双击鼠标左键
        drag_and_drop(source, target)              #拖拽到某个元素然后松开
        drag_and_drop_by_offset(source, xoffset, yoffset)          #拖拽到某个坐标然后松开
        move_by_offset(xoffset, yoffset)             #鼠标移动到距离当前位置（x,y）
        move_to_element(to_element)               #鼠标移动到某个元素
        move_to_element_with_offset(to_element, xoffset, yoffset) #将鼠标移动到距某个元素多少距离的位置
        release(on_element=None)                     #在某个元素位置松开鼠标左键
        perform()                                             #执行链中的所有动作
        '''
        try:
            Action = ActionChains(driver)
            element = driver.find_element_by_id(locator)
            offestList = offest.split(' ')
            xoffset = int(offestList[0])
            yoffset = int(offestList[1])
            Action.click_and_hold(element)
            Action.move_to_element_with_offset(element, xoffset, yoffset)
            Action.perform()
        except:
            self.log.info(traceback.format_exc())






