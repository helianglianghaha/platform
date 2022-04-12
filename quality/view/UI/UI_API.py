import copy
from quality.common.logger import Log
class SortList:
    def __init__(self):
        self.log=Log()
    def StringSplit(self,val):
        '''
        多个参数：a:[]
        Description:多个参数，需要进行分片
        '''
        

    def _sortCaseList(self,val):
        '''
        单个参数:[]
        Parameter：val
        Description：返回的是参数列表，顺序取值，index不够取最后一位
        '''
        try:
            if isinstance(val,dict):
                for i in val:
                    funList={}
                    copyFunList={}
                    temp=0
                    for j in i:
                        if type(i[j])==list:
                            funList[j]=i[j]
                            if len(i[j])>temp:
                                temp=len(i[j])
                            copyFunList[j]=i[j][0]
                        else:
                            copyFunList[j]=i[j]
                totalList=[]
                copy_j_list=copy.deepcopy(copyFunList)
                for k in range(0,temp):
                    for coyp_k in funList:
                        if len(funList[coyp_k])>k:
                            copy_j_list[coyp_k]=funList[coyp_k][k]
                        else:
                            copy_j_list[coyp_k]=funList[coyp_k][-1]
                    totalList.append(copy.deepcopy(copy_j_list))
                return (totalList)
            else:
                 self.log.info("获取的用例列表不是%s"%val)
        except Exception as e:
            raise e
            self.log.error("列表执行出错")
        