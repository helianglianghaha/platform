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
from quality.view.bugAnalysis import analysis
from quality.view.bugAnalysis import timeTask
from quality.view.documentMan import doc_api
from quality.view.testCasesMan import  cases_api
from quality.view.report import  testTeport
from quality.view.API import apiDetail

urlpatterns = [
   url('admin/',admin.site.urls),
   path('',TemplateView.as_view(template_name='index.html')),

   url('quality/casesfilesupload/',cases_api.casesfilesupload, name='casesfilesupload'),
   url('quality/selectXmindData/',cases_api.selectXmindData, name='selectXmindData'),
   
   url('quality/ximdfilesupload/',cases_api.ximdfilesupload, name='ximdfilesupload'),
   url('quality/testXmindCasesUpload/',cases_api.testXmindCasesUpload, name='testXmindCasesUpload'),
   url('quality/testCasesUpload/',cases_api.testCasesUpload, name='testCasesUpload'),
   url('quality/selectCasesData/',cases_api.selectCasesData, name='selectCasesData'),
   url('quality/selectSingleTest/',cases_api.selectSingleTest, name='selectSingleTest'),

   url('quality/delXmindDataList/',cases_api.delXmindDataList, name='delXmindDataList'),
   url('quality/selectPrd/',cases_api.selectPrd, name='selectPrd'),

   
   url('quality/selectTotalXmindCases/',cases_api.selectTotalXmindCases, name='selectTotalXmindCases'),
   url('quality/selectXminData/',cases_api.selectXminData, name='selectXminData'),
   url('quality/saveXmindCase/',cases_api.saveXmindCase, name='saveXmindCase'),
   url('quality/configCaseOwner/',cases_api.configCaseOwner, name='configCaseOwner'),
   url('quality/selectScriptFile/',cases_api.selectScriptFile, name='selectScriptFile'),
   
   
   
   url('quality/selectTotalCases/',cases_api.selectTotalCases, name='selectTotalCases'),
   url('quality/saveTestCase/',cases_api.saveTestCase, name='saveTestCase'),
   url('quality/detTestCase/',cases_api.detTestCase, name='detTestCase'),

   url('quality/delXmindCase/',cases_api.delXmindCase, name='delXmindCase'),
   url('quality/selectSortXmind/',cases_api.selectSortXmind, name='selectSortXmind'),

   url('quality/copyTestCase/',cases_api.copyTestCase, name='copyTestCase'),
   url('quality/downloadTemFiles/',cases_api.downloadTemFiles, name='downloadTemFiles'),
   url('quality/selectReportTotal/',testTeport.selectReportTotal, name='selectReportTotal'),



   # 文件导入
   url('quality/jsonfilesupload/',apiDetail.jsonfilesupload, name='jsonfilesupload'),
   url('quality/uploadApi/',apiDetail.uploadApi, name='uploadApi'),
   url('quality/selectAllApiData/',apiDetail.selectAllApiData, name='selectAllApiData'),








   url('quality/saveScriptData/',API.saveScriptData, name='saveScriptData'),
   url('quality/deleteScript/',API.deleteScript, name='deleteScript'),
   url('quality/upload/',API.upload, name='upload'),
   url('quality/saveScriptFile/',API.saveScriptFile, name='saveScriptFile'),
   url('quality/saveXmindScriptFile/',API.saveXmindScriptFile, name='saveXmindScriptFile'),

   url('quality/deleteScriptFile/',API.deleteScriptFile, name='deleteScriptFile'),
   url('quality/selectScriptFile/',API.selectScriptFile, name='selectScriptFile'),
   url('quality/executeScript/',API.executeScript, name='executeScript'),
   url('quality/saveTaskInfo/',API.saveTaskInfo, name='saveTaskInfo'),#保存任务信息
   url('quality/delTaskInfo/',API.delTaskInfo, name='delTaskInfo'),
   

   
   url('quality/readScriptLog/',API.readScriptLog, name='readScriptLog'),
   url('quality/readHtmlReport/',API.readHtmlReport, name='readHtmlReport'),
   url('quality/deleteApiScript/',API.deleteApiScript, name='deleteApiScript'),
   url('quality/getReportFileData/',API.getReportFileData, name='getReportFile'),
   url('quality/download_files/',API.download_files, name='download_files'),
   url('quality/seleMainScript/',API.seleMainScript, name='seleMainScript'),
   url('quality/seleMainXmindScript/',API.seleMainXmindScript, name='seleMainXmindScript'),  
   

   url('quality/selectTaskInfo/',API.selectTaskInfo, name='selectTaskInfo'),
   url('quality/selectVersionTotalData/',API.selectVersionTotalData, name='selectVersionTotalData'),
   url('quality/executeAllScript/',API.executeAllScript, name='executeAllScript'),
   url('quality/selectSortVersion/',API.selectSortVersion, name='selectSortVersion'),
   
   

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
   url('quality/BUGAnalysis/',analysis.BUGAnalysis, name='BUGAnalysis'),
   url('quality/updateVersion/',analysis.updateVersion, name='updateVersion'),
   url('quality/compare_trees/',analysis.compare_trees, name='compare_trees'),
   url('quality/sortReportApi/',analysis.sortReportApi, name='sortReportApi'),
   
   
   url('quality/sync_tables/',timeTask.sync_tables, name='sync_tables'),
   url('quality/XunJianExecuteScript/',timeTask.XunJianExecuteScript, name='XunJianExecuteScript'),
   url('quality/saveTestResults/',analysis.saveTestResults, name='saveTestResults'),
   url('quality/clearTestBugs/',analysis.clearTestBugs, name='clearTestBugs'),
   url('quality/selectReportBugList/',analysis.selectReportBugList, name='selectReportBugList'),

   url('quality/selectBugDataList/',analysis.selectBugDataList, name='selectBugDataList'),
   url('quality/selectTopBugData/',analysis.selectTopBugData, name='selectTopBugData'),
   url('quality/savefileData/',doc_api.savefileData, name='savefileData'),
   url('quality/selectFiles/',doc_api.selectFiles, name='selectFiles'),
   url('quality/delFileName/',doc_api.delFileName, name='delFileName'),
   url('quality/editFiles/',doc_api.editFiles, name='editFiles'),
   url('quality/filesupload/',doc_api.filesupload, name='filesupload'),
   url('quality/saveFilsList/',doc_api.saveFilsList, name='saveFilsList'),
   url('quality/selectFileLists/',doc_api.selectFileLists, name='selectFileLists'),
   url('quality/delFilsList/',doc_api.delFilsList, name='delFilsList'),
   url('quality/downFiles/',doc_api.downFiles, name='downFiles'),


   url('quality/selectSigleVersionBugData/',analysis.selectSigleVersionBugData, name='selectSigleVersionBugData'),
   url('quality/update_versioninfo/',timeTask.update_versioninfo, name='totalVersionData'),
   url('quality/update_bug_info/',timeTask.update_bug_info, name='update_bug_info'),

   url('quality/readlog/',API.readlog, name='readlog'),
   url('quality/selectAllModelTree/',API.selectAllModelTree, name='selectAllModelTree'),
   url('quality/deleteModelDataList/',API.deleteModelDataList, name='deleteModelDataList'),
   url('quality/selectAllModel/',API.selectAllModel, name='selectAllModel'),
   url('quality/selectModelList/',API.selectModelList, name='selectModelList'),
   url('quality/saveModelData/',API.saveModelData, name='saveModelData'),
   url('quality/addModelVersion/',API.addModelVersion, name='addModelVersion'),
   url('quality/selectModelVersion/',API.selectModelVersion, name='selectModelVersion'),
   url('quality/selectSortModelVersion/',API.selectSortModelVersion, name='selectSortModelVersion'),
   url('quality/createTodoTask/',API.createTodoTask, name='createTodoTask'),
   url('quality/selectTodoTask/',API.selectTodoTask, name='selectTodoTask'),
   url('quality/updateTodoTask/',API.updateTodoTask, name='updateTodoTask'),

   url('quality/selectPeople/',API.selectPeople, name='selectPeople'),
   url('quality/selectVersionList/',API.selectVersionList, name='selectVersionList'),
   url('quality/selectReportVersionList/',API.selectReportVersionList, name='selectReportVersionList'),

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
   url('quality/saveDingMessage/',API_data.saveDingMessage, name='saveDingMessage'),
   url('quality/selectDingMessage/',API_data.selectDingMessage, name='selectDingMessage'),
   url('quality/delDingMessage/',API_data.delDingMessage, name='delDingMessage'),
   url('quality/selectColumns/',API_data.selectColumns, name='selectColumns'),
   url('quality/selectDianWei/',API_data.selectDianWei, name='selectDianWei'),
   url('quality/saveVersionManger/',API.saveVersionManger, name='saveVersionManger'),
   url('quality/sync_tables/',timeTask.sync_tables, name='sync_tables'),

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
   url('quality/copyVersionManger/',API.copyVersionManger, name='selectVersionData'),

   url('quality/Login/',login.Login, name='Login'),
    ]
