# from base.context import ContextList
# from base.context import ContextList
from quality.test.seleniumData.base.context import ContextList
# from selenium.webdriver.remote.webelement import webE
from selenium.webdriver.remote.webelement import WebElement
class ElementFinderList(ContextList):
    # def __init__(self,webelement):
    #     self.webelement=webelement
    def find(self, locator, tag=None, first_only=True, required=True,
             parent=None):
        element_type = 'Element' if not tag else tag.capitalize()
        if self._is_webelement(locator):
            return locator
        criteria = self._parse_locator(locator) 
        elements = criteria
        if required and not elements:
            data={
                "code":1000,
                "msg":"%s with locator '%s' not found."% (element_type, locator)
            }
            return data
        if first_only:
            if not elements:
                return None
            return elements[0]
        return elements
    def _is_webelement(self, element):
        return isinstance(element,WebElement)
    def _parse_locator(self, locator):
        if locator.startswith(('//', '(//')):
            return 'xpath', locator
        index = self._get_locator_separator_index(locator)
        if index != -1:
            prefix = locator[:index].strip()
            if prefix:
                return prefix, locator[index+1:].lstrip()
        return locator
    def _get_locator_separator_index(self, locator):
        if '=' not in locator:
            return locator.find(':')
        if ':' not in locator:
            return locator.find('=')
        return min(locator.find('='), locator.find(':'))