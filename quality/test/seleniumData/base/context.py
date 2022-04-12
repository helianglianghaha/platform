import sys
sys.path.append("E:\\quality\\quality2019722\\quality\\test")
# print(sys.path)
# from ..locators.elementfinder import ElementFinder
# from keywords.webdrivertools import WebDriverCache
from quality.test.seleniumData.keywords.webdrivertools import WebDriverCache

class ContextList():
    # def __int__(self):
    #     self._drivers = WebDriverCache()
    @property
    def driver(self):
        if not WebDriverCache().current:
            print('No browser is open.')
        return WebDriverCache().current
    # def find_element(self, locator, tag=None, required=True, parent=None):
    #     return ElementFinderList().find(locator, tag, True, required, parent)