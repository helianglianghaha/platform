from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.common.exceptions import WebDriverException
from quality.test.seleniumData.prams import connectionList
from quality.common.logger import Log

class AlertKeyWord():
    def __init__(self):
        self.Accept='ACCEPT'
        self.DissMiss='DISSMISS'
        self.log=Log()
        self.timeout=5
    def confirm_action(self,driver,action):
        '''确定Alert'''
        text = self.handle_alert(driver,action)
        self._next_alert_action = self.ACCEPT
        return text
    def handle_alert(self,driver,action):
        alert = self._wait_alert(driver,self.timeout)
        return self._handle_alert(alert, action)
    def _handle_alert(self,alert,action):
        action=action.upper()
        if action==self.Accept:
            alert.accept()
        elif action==self.DissMiss:
            alert.dismiss()
        else:
            self.log.info("Invaild alert action %s"%action)

    def _wait_alert(self,driver,timeout=None):
        try:
            return WebDriverWait(driver,timeout).until(EC.alert_is_present())
        except WebDriverException:
            return False
            self.log.info('Alert not found')
if __name__=="__main__":
    action="accept"
    alert=AlertKeyWord().confirm_action(connectionList[-1],action)
            

