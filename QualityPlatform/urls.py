from django.contrib import admin
from django.urls import path,re_path as url
# from django.config.urls import include,url
from django.views.generic import  TemplateView
from django.urls import get_resolver
from django.urls import  resolvers
# from django.views
from quality.view.project import login
from quality.view.API import API
from quality.view.UI import UI_data
from quality.view.API_version import API_data

urlpatterns = [
   url('admin/',admin.site.urls),
   # url('quality/admin/', admin.site.urls),
   path('',TemplateView.as_view(template_name='index.html')),
   url('quality/saveScriptData/',API.saveScriptData, name='saveScriptData'),
   url('quality/deleteScript/',API.deleteScript, name='deleteScript'),
   url('quality/upload/',API.upload, name='upload'),
   url('quality/saveScriptFile/',API.saveScriptFile, name='saveScriptFile'),
   url('quality/deleteScriptFile/',API.deleteScriptFile, name='deleteScriptFile'),
   url('quality/selectScriptFile/',API.selectScriptFile, name='selectScriptFile'),
   url('quality/executeScript/',API.executeScript, name='executeScript'),
   url('quality/readScriptLog/',API.readScriptLog, name='readScriptLog'),
   url('quality/readHtmlReport/',API.readHtmlReport, name='readHtmlReport'),
   url('quality/deleteApiScript/',API.deleteApiScript, name='deleteApiScript'),
   url('quality/getReportFileData/',API.getReportFileData, name='getReportFile'),
   url('quality/download_files/',API.download_files, name='download_files'),
   url('quality/sqlcat/',API.sqlcat, name='sqlcat'),
   url('quality/readLog/',API.readLog, name='readLog'),
   url('quality/selectTableList/',API.selectTableList, name='selectTableList'),
   url('quality/selectTableDegion/',API.selectTableDegion, name='selectTableDegion'),
   url('quality/selectProScriptFile/',API.selectProScriptFile, name='selectProScriptFile'),
   url('quality/createScriptFile/',API.createScriptFile, name='createScriptFile'),
   url('quality/selectTagsManger/',API.selectTagsManger, name='selectTagsManger'),
   url('quality/selectVersionManger/',API.selectVersionManger, name='selectVersionManger'),
   url('quality/saveSingleVersionManger/',API.saveSingleVersionManger, name='saveSingleVersionManger'),
   url('quality/delVersionManger/',API.delVersionManger, name='delVersionManger'),



   url('quality/readlog/',API.readlog, name='readlog'),
   url('quality/selectAllModelTree/',API.selectAllModelTree, name='selectAllModelTree'),
   url('quality/deleteModelDataList/',API.deleteModelDataList, name='deleteModelDataList'),
   url('quality/selectAllModel/',API.selectAllModel, name='selectAllModel'),
   url('quality/selectModelList/',API.selectModelList, name='selectModelList'),
   url('quality/saveModelData/',API.saveModelData, name='saveModelData'),
   url('quality/addModelVersion/',API.addModelVersion, name='addModelVersion'),
   url('quality/selectModelVersion/',API.selectModelVersion, name='selectModelVersion'),
   url('quality/saveProAddress/',UI_data.saveProAddress, name='saveProAddress'),
   url('quality/selectProAddress/',UI_data.selectProAddress, name='selectProAddress'),
   url('quality/deleteProAddress/',UI_data.deleteProAddress, name='deleteProAddress'),
   url('quality/selectTestCaseList/',UI_data.selectTestCaseList, name='selectTestCaseList'),

   url('quality/selectCookiesSelection/',API_data.selectCookiesSelection, name='selectCookiesSelection'),
   url('quality/delCookies/',API_data.delCookies, name='delCookies'),
   url('quality/selectCookies/',API_data.selectCookies, name='selectCookies'),
   url('quality/saveCookies/',API_data.saveCookies, name='saveCookies'),
   url('quality/saveTestSort/',API_data.saveTestSort, name='saveTestSort'),
   url('quality/delVariable/',API_data.delVariable, name='delVariable'),
   url('quality/selectGlobalVariable/',API_data.selectGlobalVariable, name='selectGlobalVariable'),
   url('quality/apiRequest/',API_data.apiRequest, name='apiRequest'),
   url('quality/saveGlobalVari/',API_data.saveGlobalVari, name='saveGlobalVari'),
   url('quality/selectVersionList/',API_data.selectVersionList, name='selectVersionList'),
   url('quality/selectVersionData/',API_data.selectVersionData, name='selectVersionData'),
   url('quality/saveApiTestCase/',API_data.saveApiTestCase, name='saveApiTestCase'),
   url('quality/selectApiCases/',API_data.selectApiCases, name='selectApiCases'),
   url('quality/deleteApiTestCases/',API_data.deleteApiTestCases, name='deleteApiTestCases'),
   url('quality/selectSingleVersion/',API_data.selectSingleVersion, name='selectSingleVersion'),
   url('quality/deletaSingleVersion/',API_data.deletaSingleVersion, name='deletaSingleVersion'),
   url('quality/todoBatchExection/',API_data.todoBatchExection, name='todoBatchExection'),
   url('quality/executeBatchExection/',API_data.executeBatchExection, name='executeBatchExection'),
   url('quality/selectExecuting/',API_data.selectExecuting, name='selectExecuting'),
   url('quality/deleteExecutingLog/',API_data.deleteExecutingLog, name='deleteExecutingLog'),
   url('quality/selectReportList/',API_data.selectReportList, name='selectReportList'),
   url('quality/selectCaseTime/',API_data.selectCaseTime, name='selectCaseTime'),
   url('quality/copyApiTestCases/',API_data.copyApiTestCases, name='copyApiTestCases'),
   url('quality/executTools/',API_data.executTools, name='copyApiTestCases'),
   url('quality/saveDingMessage/',API_data.saveDingMessage, name='saveDingMessage'),
   url('quality/selectDingMessage/',API_data.selectDingMessage, name='selectDingMessage'),
   url('quality/delDingMessage/',API_data.delDingMessage, name='delDingMessage'),
   url('quality/checkEnergySaving/',API_data.checkEnergySaving, name='checkEnergySaving'),
   url('quality/createData/',API_data.createData, name='createData'),
   url('quality/selectTablesColumns/',API_data.selectTablesColumns, name='selectTablesColumns'),
   url('quality/selectColumns/',API_data.selectColumns, name='selectColumns'),
   url('quality/selectDianWei/',API_data.selectDianWei, name='selectDianWei'),
   url('quality/saveVersionManger/',API.saveVersionManger, name='saveVersionManger'),


   url('quality/readLog/',UI_data.readLog, name='readLog'),
   url('quality/selectUiTestCase/',UI_data.selectUiTestCase, name='selectUiTestCase'),
   url('quality/saveTestCase/',UI_data.saveTestCase, name='saveTestCase'),
   url('quality/saveKeyWord/',UI_data.saveKeyWord, name='saveKeyWord'),
   url('quality/selectTestKey/',API_data.selectTestKey, name='selectTestKey'),
   url('quality/saveTestScript/',UI_data.saveTestScript, name='saveTestScript'),
   url('quality/delUITestCase/',UI_data.delUITestCase, name='delUITestCase'),
   url('quality/delScriptCase/',UI_data.delScriptCase, name='delScriptCase'),
   url('quality/selectTestReportDetail/',UI_data.selectTestReportDetail, name='selectTestReportDetail'),
   url('quality/addScript/',UI_data.addScript, name='addScript'),

   url('quality/saveEmailConfig/',UI_data.saveEmailConfig, name='saveEmailConfig'),
   url('quality/selectEmailConfig/',UI_data.selectEmailConfig, name='selectEmailConfig'),
   url('quality/saveCaseData/',UI_data.saveCaseData, name='saveCaseData'),
   url('quality/saveTestCaseSort/',UI_data.saveTestCaseSort, name='saveTestCaseSort'),
   url('quality/copyTestUITestCase/',UI_data.copyTestUITestCase, name='copyTestUITestCase'),
   url('quality/copyTestUiScript/',UI_data.copyTestUiScript, name='copyTestUiScript'),
   url('quality/saveUpLoad/',UI_data.saveUpLoad, name='saveUpLoad'),
   url('quality/userRegister/',UI_data.userRegister, name='userRegister'),

   url('quality/LogOut/',UI_data.LogOut, name='LogOut'),
   url('quality/selectUserInfo/',UI_data.selectUserInfo, name='selectUserInfo'),

   url('quality/batchExecutingCases/',UI_data.batchExecutingCases, name='batchExecutingCases'),
   url('quality/batchCopyScript/',UI_data.batchCopyScript, name='batchCopyScript'),

   url('quality/deleteWebTestData/',API.deleteWebTestData, name='deleteWebTestData'),
   url('quality/apiTest/',API.apiTest, name='apiTest'),
   url('quality/deleteTestData/',API.deleteTestData, name='deleteTestData'),
   url('quality/selectTestCase/',API.selectTestCase, name='selectTestCase'),
   url('quality/saveTestCase/',API.saveTestCase, name='saveTestCase'),
   url('quality/deleteApiData/',API.deleteApiData, name='deleteApiData'),
   url('quality/selectAPIdata/',API.selectAPIdata, name='selectAPIdata'),
   url('quality/saveAPIdata/',API.saveAPIdata, name='saveAPIdata'),
   url('quality/selectVersionData/',API.selectVersionData, name='selectVersionData'),
   url('quality/Login/',login.Login, name='Login'),
    ]
# from apscheduler.scheduler import Scheduler
from quality.xunJian.batchApiXunJian import batchApiCases
# from quality.view.UI.UIFunction import batchXunJianTestCase
# sched = Scheduler()
#
#
# @sched.interval_schedule(seconds=120)
# def my_task():
#    batchApiCases().selectAllApiTestCase()
# sched.start()
