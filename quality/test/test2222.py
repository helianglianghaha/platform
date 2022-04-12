import sys
sys.path.append("E:\\quality\\quality2019722\\quality\\test")
from seleniumData.keywords.browsermanagement import BrowserManagement
from seleniumData.keywords.element import Elementkeywords
from prams import connectionList

chrome='chrome'
url="http://fenxi.haofenshu.com/login"
t=BrowserManagement()
t.open_browser(url,chrome)
# if t.open_browser(url,chrome):
locator1="//*[@id='user']"
locator2="//*[@id='password']"
username="ndjxxyadmin"
password="chuxinjiaoyu"
button="//*[@id='login']"
Elementkeywords().click_element(locator1)
Elementkeywords().send_keys(connectionList[0],locator1,username)
Elementkeywords().send_keys(connectionList[0],locator2,password)
Elementkeywords().click(connectionList[0],button)


