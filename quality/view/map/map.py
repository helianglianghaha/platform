# from django.core import serializers
# from django.db import models
# from django.http.response import JsonResponse
# from django.db import models
# from django.db import connection
# # from quality.models import Version_overall_evaluation,Version
# import json,datetime

# #查询总体评价
# def selectOverAll(request):
#     try:
#         print(request.POST)
#         version_id_id=request.POST.get("version_id_id")
#         selectList="select * from quality_version_overall_evaluation where version_id_id="+str(version_id_id)
#         cursor = connection.cursor()
#         cursor.execute(selectList)
#         data=dictfetchall(cursor)
#         data1={
#             "code":200,
#             "msg":"总体评价查询成功",
#             "data":data
#         }
#         return JsonResponse(data1)
#     except Exception as e:
#         data1={
#             "code":10000,
#             "msg":e
#         }
#         return JsonResponse(data1)

# #保存总体评价
# def saveOverAll(request):
#     try:
#         print(request.POST)
#         overall_id=request.POST.get("overall_id")
#         version_id_id=request.POST.get("version_id_id",'')
#         test_overall_evaluation=request.POST.get("test_overall_evaluation",'')
#         produce_overall_evaluation=request.POST.get("produce_overall_evaluation",'')
#         print("获取的overall_id值为",overall_id)
#         if overall_id=='' or overall_id==None:
#             # print(1111111111111)
#             _versionOver=Version_overall_evaluation()
#             _versionOver.version_id=Version.objects.get(version_id=version_id_id)
#             _versionOver.test_overall_evaluation=test_overall_evaluation
#             _versionOver.produce_overall_evaluation=produce_overall_evaluation
#             _versionOver.save()
#         else:
#             # print(2222222222222222)
#             _versionOver=Version_overall_evaluation()
#             _versionOver.overall_id=overall_id
#             _versionOver.version_id=Version.objects.get(version_id=version_id_id)
#             _versionOver.test_overall_evaluation=test_overall_evaluation
#             _versionOver.produce_overall_evaluation=produce_overall_evaluation
#             _versionOver.save()
#         data={
#             "code":200,
#             "msg":"保存成功"
#         }
#         return JsonResponse(data)
#     except Exception as e:
#         data={
#             "code":1000,
#             "msg":e
#         }
#         return JsonResponse(data)
# def getMapData(request):
#     # print(1111)
#     versionId=request.GET.get("versionId")
#     # print("versionid",versionId)
#     projectId=request.GET.get("projectId")
#     # print("projectid",projectId)
#     cursor = connection.cursor()
#     cursor2=connection.cursor()
#     cursor3=connection.cursor()

#     sql="SELECT * FROM quality_version a,quality_version_time b,quality_project c WHERE a.version_id=b.version_id_id AND c.project_id="+str(projectId)+" "+"AND a.project_id_id="+str(projectId) +" "+"AND b.version_id_id BETWEEN 0 AND"+" "+str(versionId)+" ORDER BY version_id DESC LIMIT 0,5"
#     sql2="SELECT * FROM quality_version a RIGHT OUTER JOIN quality_version_bug b ON a.version_id=b.version_id_id WHERE a.project_id_id="+str(projectId)+" "+"AND a.version_id BETWEEN 0 AND"+" "+str(versionId)+" "+"ORDER BY version_id DESC LIMIT 0,5"
#     # SELECT * FROM quality_project a WHERE a.project_id=(SELECT parent_project_id FROM quality_project WHERE project_id=28) OR a.project_id=28
#     sql3="SELECT * FROM quality_project a WHERE a.project_id=(SELECT parent_project_id FROM quality_project WHERE project_id="+str(projectId)+")"+" "+"OR a.project_id="+str(projectId)
#     # print('sql数据为',sql3)
#     cursor.execute(sql)#查询项目发布过程
#     cursor2.execute(sql2)#查询版本BUG
#     cursor3.execute(sql3)#查询项目信息
#     data=dictfetchall(cursor)
#     data2=dictfetchall(cursor2)
#     data3=dictfetchall(cursor3)
#     dataFrom={
#         "code":200,
#         "dataTime":data,
#         "dataBug":data2,
#         "dataProject":data3,
#     }
#     print(data)
#     return JsonResponse(dataFrom,safe=False)
# def getMapProjectData(request):
#     versionId=request.GET.get("versionId")
#     projectId=request.GET.get("projectId")
#     sql="SELECT * FROM quality_project a,quality_version b,quality_version_time c WHERE b.version_id=c.version_id_id AND a.project_id=b.project_id_id AND b.project_id_id="+str(projectId)+" "+"AND b.version_id="+str(versionId)

#     sql2="SELECT priorityName,COUNT(*) 'nums' FROM quality_issues WHERE versionsId in (SELECT version_jira_id FROM quality_version WHERE version_id="+str(versionId)+") GROUP BY priorityName"
#     sql3="SELECT * FROM quality_version a,quality_version_release b WHERE a.version_id=b.version_id_id AND a.version_id="+str(versionId)
#     sql4="SELECT * FROM quality_version a,quality_version_code b WHERE a.version_id=b.version_id_id and a.version_id="+str(versionId)
#     sql5="SELECT * FROM quality_project a WHERE a.project_id=(SELECT parent_project_id FROM quality_project WHERE project_id="+str(projectId)+")"+" "+"OR a.project_id="+str(projectId) 
#     sql6="SELECT * FROM quality_version a,quality_version_bug_leave b WHERE a.version_id=b.version_id_id AND a.version_id="+str(versionId)
#     sql7="SELECT * FROM quality_version a,quality_version_engineer b WHERE a.version_id=b.version_id_id AND a.version_id="+str(versionId)
#     sql9="SELECT * FROM quality_version a,quality_version_bug_analysis b WHERE a.version_id=b.version_id_id AND a.version_id="+str(versionId)
#     sql10="SELECT user_name 'name',COUNT(*) 'value' FROM quality_user a,quality_issues b WHERE a.user_login_ame=b.assigneeName AND b.versionsId=(SELECT version_jira_id FROM quality_version WHERE version_id="+str(versionId)+") GROUP BY user_name ORDER BY COUNT(*) DESC"
#     sql11="SELECT user_name 'name',COUNT(*) 'value' FROM quality_user a,quality_issues b WHERE a.user_login_ame=b.creatorName AND b.versionsId=(SELECT version_jira_id FROM quality_version WHERE version_id="+str(versionId)+") GROUP BY creatorName"
#     cursor = connection.cursor()#获取发布时间
#     cursor2 = connection.cursor()#获取BUG数
#     cursor3=connection.cursor()#获取发布时间
#     cursor4=connection.cursor()#获取发布代码
#     cursor5=connection.cursor()#查询版本及项目信息
#     cursor6=connection.cursor()#查询遗留BUG
#     cursor7=connection.cursor()#查询参与人员信息
#     cursor9=connection.cursor()#遗漏BUG分析
#     cursor10=connection.cursor()#获取研发人员对应的BUG
#     cursor11=connection.cursor()#获取测试人员对应BUG

#     cursor.execute(sql)
#     cursor2.execute(sql2)
#     cursor3.execute(sql3)
#     cursor4.execute(sql4)
#     cursor5.execute(sql5)
#     cursor6.execute(sql6)
#     cursor7.execute(sql7)
#     cursor9.execute(sql9)
#     cursor10.execute(sql10)
#     cursor11.execute(sql11)


#     data=dictfetchall(cursor)
#     if data==[]:
#         submitBuglist=[]
#         solveBuglist=[]
#     else:
#         startTime=data[0]["begintest_time"]
#         endTime=data[0]["signoff_time"]
#         dataStartTime=datetime.datetime.strptime(startTime,"%Y-%m-%d")#字符串转成datetime
#         dataEndTime=datetime.datetime.strptime(endTime,"%Y-%m-%d")#字符串转成datetime
#         dataStart=getDateTime2(startTime)
#         dataEnd=getDateTime2(endTime)
#         datatimelist=[]
#         days=(datetime.datetime(dataEnd[0],dataEnd[1],dataEnd[2])-datetime.datetime(dataStart[0],dataStart[1],dataStart[2])).days
#         for i in range(days+2):
#             dataTime=dataStartTime+ datetime.timedelta(days=i)
#             dataTimeToString=dataTime.strftime("%Y-%m-%d")
#             datatimelist.append(dataTimeToString)
#             # print("获取到相加的时间为",dataTime)
#         # print("获取到的时间列表是",datatimelist)
#         submitBuglist=[]#提交BUG数
#         solveBuglist=[]#解决BUG数
#         list2={}
#         list3={}
#         for j in range(len(datatimelist)-1):
#             #提BUG数量
#             sql12="SELECT count(*) 'nums' FROM quality_issues WHERE"+" "+"\'"+datatimelist[j]+"\'"+"< created and created <="+"\'"+datatimelist[j+1]+"\'"+"AND versionsId=(SELECT version_jira_id FROM quality_version WHERE version_id="+str(versionId)+")"
#             #解决BUG数量
#             sql13="SELECT count(*) 'nums' FROM quality_issues WHERE"+" "+"\'"+datatimelist[j]+"\'"+"< resolutiondate and resolutiondate <="+"\'"+datatimelist[j+1]+"\'"+"AND versionsId=(SELECT version_jira_id FROM quality_version WHERE version_id="+str(versionId)+")"

#             cursor12=connection.cursor()#提取BUG数
#             cursor12.execute(sql12)
#             data12=dictfetchall(cursor12)
#             list2[datatimelist[j]]=data12[0]["nums"]

#             cursor13=connection.cursor()#解决BUG数
#             cursor13.execute(sql13)
#             data13=dictfetchall(cursor13)
#             list3[datatimelist[j]]=data13[0]["nums"]

#         submitBuglist.append(list2)
#         solveBuglist.append(list3)
#         # print("获取的提交BUG列表",submitBuglist)
#         # print("获取的解决BUG列表",solveBuglist)




#     data2=dictfetchall(cursor2)
#     priorityName=['A致命','B严重','C一般','D细微','E建议']
#     priorityName2=[]
#     for i in range(len(data2)):
#         priorityName2.append(data2[i]["priorityName"])
#     for j in priorityName:
#         if j in priorityName2:
#             pass
#         else:
#             priorityName3={}
#             priorityName3["priorityName"]=j
#             priorityName3["nums"]=0
#             data2.append(priorityName3)
#     data3=dictfetchall(cursor3)

#     data4=dictfetchall(cursor4)
#     data5=dictfetchall(cursor5)
#     data6=dictfetchall(cursor6)
#     data7=dictfetchall(cursor7)
#     data9=dictfetchall(cursor9)
#     data10=dictfetchall(cursor10)
#     data11=dictfetchall(cursor11)


#     dataFrom={
#         "code":200,
#         "dataTime":data,
#         "dataBug":data2,
#         "dataRealese":data3,
#         "dataCode":data4,
#         "dataProject":data5,
#         "dataBugLeave":data6,
#         "dataEngineer":data7,
#         "dataBugAnalysis":data9,
#         "dataUserBUGs":data10,
#         "dataTestBug":data11,
#         "dataSubmitBug":submitBuglist,
#         "dataSolveBug":solveBuglist,
#     }
#     return JsonResponse(dataFrom)
# def getDateTime(request):
#     data={
#         "code":200,
#         "msg":"获取成功了"
#     }
#     return JsonResponse(data)
# def getDateTime2(time):
#     print(11111111111111111111)
#     startTime1=time.split("-")
#     startTimeList=[]
#     for i in startTime1:
#         startTimeList.append(int(i))
#     print('startTimeList',startTimeList)
#     return startTimeList
# def dictfetchall(cursor):
#     "将游标返回的结果保存到一个字典对象中"
#     desc = cursor.description
#     return [dict(zip([col[0] for col in desc], row))for row in cursor.fetchall()]
