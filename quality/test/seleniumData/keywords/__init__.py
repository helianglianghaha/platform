# __all__=["browsermanagement", 'webdrivertools.py', 'element']
from .alert import AlertKeyWord
from .browsermanagement import BrowserManagement
from .connectioncache import ConnectionCache
from .element import Elementkeywords
from .webdrivertools import WebDriverCreator
if __name__=="__main__":
    print("keywords作为主程序运行")
else:
    print("keywords初始化")