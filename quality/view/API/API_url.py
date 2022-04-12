from django.urls import path,re_path
from quality.view.API import API
app_name="API"

urlpatterns = [
    # selectVersionData,selectAPIdata,deleteApiData,saveTestCase,selectTestCase,deleteTestData,apiTest,saveWebTestCase

    # deleteWebTestData,saveScriptData,deleteScript,selectScriptData,webRequest,saveModelData,selectModelList
    #selectAllModel,deleteModelData,selectAllModelTree,selectWebTestCase,readlog,getReprotList

    path('/getReprotList/$',API.getReprotList,name='getReprotList'),
    path('/readlog/$',API.readlog,name='readlog'),
    path('/selectWebTestCaselist/$',API.selectWebTestCaselist,name='selectWebTestCaselist'),
    path('/selectAllModelTree/$',API.selectAllModelTree,name='selectAllModelTree'),
    path('/deleteModelData/$',API.deleteModelData,name='deleteModelData'),
    path('/selectAllModel/$',API.selectAllModel,name='selectAllModel'),
    path('/selectModelList/$',API.selectModelList,name='selectModelList'),
    path('/saveModelData/$',API.saveModelData,name='saveModelData'),
    path('/webRequest/$',API.webRequest,name='webRequest'),

    path('/selectScriptData/$',API.selectScriptData,name='selectScriptData'),
    path('/saveScriptData/$',API.saveScriptData,name='saveScriptData'),
    path('/deleteScript/$',API.deleteScript,name='deleteScript'),

    path('/deleteWebTestData/$',API.deleteWebTestData,name='deleteWebTestData'),
    path('/selectWebTestCase/$',API.selectWebTestCase,name='selectWebTestCase'),

    path('/saveWebTestCase/$',API.saveWebTestCase,name='saveWebTestCase'),
    path('/apiTest/$',API.apiTest,name='apiTest'),
    path('/deleteTestData/$',API.deleteTestData,name='deleteTestData'),
    path('/deleteApiData/$',API.deleteApiData,name='deleteApiData'),
    path('/selectAPIdata/$',API.selectAPIdata,name='selectAPIdata'),
    path('/saveAPIdata/$',API.saveAPIdata,name='saveAPIdata'),
    path('/saveTestCase/$',API.saveTestCase,name='saveTestCase'),
    path('/selectTestCase/$',API.selectTestCase,name='selectTestCase'),
    path('/selectVersionData/$',API.selectVersionData,name='selectVersionData'),
    
]