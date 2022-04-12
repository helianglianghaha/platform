# from keywords.browsermanagement import BrowserManagement
# import sys
# sys.path.append("E:\\quality\\quality2019722\\quality\\test")
# from keywords.element import Elementkeywords
from quality.test.seleniumData.keywords.element import Elementkeywords
from quality.test.seleniumData.keywords.browsermanagement import BrowserManagement
from quality.test.seleniumData.keywords.alert import AlertKeyWord
from quality.test.seleniumData.keywords.cookies import cookiesKeywords
from quality.test.seleniumData.keywords.javascript import JavaScript
from quality.common.logger import Log
# from keywords.browsermanagement import BrowserManagement
from quality.common.logger import Log
from quality.test.seleniumData.prams import connectionList
import time
# from prams import connectionList

class FunctionList(Elementkeywords):
    '''
    --openbrowser---打开浏览器
    --clickElement---点击元素
    --sendKeys---传参
    '''
    def openbrowser(locator,command_executor):
        '''
        打开浏览器
        :param url:
        :param chrome:
        :return:
        '''
        print("locator",locator)
        print("command_executor",command_executor)
        pramsList=locator.split(" ")
        if len(pramsList)==2:
            driver=BrowserManagement().open_browser(pramsList[0],command_executor)
            return  driver
        else:
            print("返回的参数不是两个")
    def forcedWaitTime(waitTime,version):
        '''
        强制等待
        :return:
        '''
        time=int(waitTime)
        Elementkeywords().forcedWait(time)
    def impicitlyWaitTime(waitTime,version):
        '''
        隐式等待
        :param waitTime:
        :return:
        '''
        Elementkeywords().impicitlyWait(connectionList[version][-1],waitTime)
    def clickElement(locator,allElement,version):
        '''
        点击元素
        :param locator:
        :return:
        '''
        Elementkeywords().click(connectionList[version][-1],allElement,locator)
    def getRectUrl(url,version):
        '''
        访问URL
        :param version:
        :return:
        '''
        Elementkeywords().getUrl(connectionList[version][-1],url)
    def clickElements(locator,number,version):
        '''
        多个元素
        '''
        Elementkeywords().clickElements(connectionList[version][-1],locator,number)
    def closeHandle(version):
        '''关闭窗口'''
        Elementkeywords().close_handle(connectionList[version][-1])
    def changeHandle(version):
        '''
        切换窗口
        '''
        Elementkeywords().changeHandle(connectionList[version][-1])
    def changeOldHandle(version):
        Elementkeywords().change_OldHandle(connectionList[version][-1])
    def changeNewHandele(version):
        Elementkeywords().change_NewHandle(connectionList[version][-1])
    def switchIframe(locator,version):
        '''切换iframe'''
        Elementkeywords().switch_iframe(connectionList[version][-1],locator)
    def switchDefaultContent(version):
        '''切换主iframe'''
        Elementkeywords().switch_default_content(connectionList[version][-1])
    def addCookie(locator,version):
        '''
        :param locator:
        :param version:
        :return:
        '''
        value_list=locator.split(",")
        if len(value_list)==2:
            cookiesKeywords().addCookies(connectionList[version][-1],value_list[0],value_list[1])
        else:
            print("元素少于3个")
    def driverRefresh(version):
        '''刷新浏览器'''
        # print('version'version)
        BrowserManagement().fresh(connectionList[version][-1])
    def goToforward(url,version):
        '''请求浏览器'''
        BrowserManagement().gotoBroswer(connectionList[version][-1],url)



    def keyBoard(locator,Keys,version):
        '''
        调用键盘
        :param locator:
        :param version:
        :return:
        '''
        Elementkeywords().keyBoardKeys(connectionList[version][-1],locator,Keys)
    def quit(version):
        '''
        退出
        '''
        time.sleep(3)
        Elementkeywords().quit(connectionList[version][-1])
    def upload(filepath,version):
        '''
        上传文件
        :return:
        '''
        time.sleep(2)
        Elementkeywords().uploadField(filepath)
    def clearElementValue(locator,version):
        '''清空元素'''
        Elementkeywords().clear_element_vaule(connectionList[version][-1],locator)
    def assertElementIsDisplay(excepted,testCaseList,version):
        '''断言元素是否可见'''
        Elementkeywords().element_isDisplay(connectionList[version][-1],excepted,testCaseList)
    def assertElementIsSelect(excepted,testCaseList,version):
        '''断言元素是否被选择'''
        Elementkeywords().element_isSelected(connectionList[version][-1],excepted,testCaseList)
    def assertValueElement(excepted,value,testCaseList,version):
        '''判断元素值'''
        Elementkeywords().element_value_should_contains(connectionList[version][-1],excepted,value,testCaseList)
    def assertElement(excepted,testCaseList,version):
        '''
        元素断言
        '''
        Elementkeywords().element_should_contains(connectionList[version][-1],excepted,testCaseList)
    def sendKeys(locator,data,version):
        '''
        传参
        :param locator:
        :param data:
        :return:
        '''
        Elementkeywords().send_keys(connectionList[version][-1], locator, data)
    def randomPhone(locator,data,version):
        '''
        传参
        :param locator:
        :param data:
        :return:
        '''
        from quality.common.commonbase import  commonList
        data=commonList().randomPhoneBase()
        Elementkeywords().send_keys(connectionList[version][-1], locator, data)
    def randomName(locator,data,version):
        '''
        传参
        :param locator:
        :param data:
        :return:
        '''
        from quality.common.commonbase import commonList
        data = commonList().randomNameBase()
        Elementkeywords().send_keys(connectionList[version][-1], locator, data)
    def confirmAlert(action,version):
        '''
        :param acion 
        accept dismiss
        '''
        AlertKeyWord().confirm_action(connectionList[version][-1],action)
    def drapPullMouse(locator,offest,version):
        '''
        鼠标拖拽
        :param locator:
        :param offest:
        :param version:
        :return:
        '''
        print('jkl')
        Elementkeywords().mouseDrag(connectionList[version][-1],locator,offest)
        print(333)
    def actionForm(args,version):
        '''
        鼠标悬浮
        
        '''
        Elementkeywords().actionPerform(connectionList[version][-1],args)
    def switchDefaultContent(version):
        '''
        切换到主页面
        '''
        Elementkeywords().defaultContent(connectionList[version][-1])
    def elementDisplay(locator,version):
        '''
        元素是否可见
        '''
        element_display=Elementkeywords().element_disPlay(connectionList[version][-1],locator)
        print("elementDisplay=======locator是否可见",locator)
        return element_display
    def executeJavascript(locator,args,version):
        '''
        :param args
        将滚动条移动到页面的底部
        js="var q=document.documentElement.scrollTop=100000" 
        #将滚动条移动到页面的顶部  
        js="var q=document.documentElement.scrollTop=0"
        若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作 
        js="var q=document.getElementById('id').scrollTop=100000"
        '''
        JavaScript.execute_javascript(connectionList[version][-1],locator,args)


