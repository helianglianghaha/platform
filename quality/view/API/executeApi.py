import logging
class versionUpdateApi:
    def mainExecuteApi(self,oldData,newData):
        '''主执行'''
        import logging
        print("老数据=={}".format(oldData))
        print("新数据=={}".format(newData))

        # 返回修改的版本和执行端
        if len(newData)==0:
            logging.info("进度为空，不用执行脚本")
            return
        versions_status_list=self.compareVersion(oldData,newData)
        if len(versions_status_list['version_status_list'])==0:
            logging.info("进度没有修改，不用执行脚本")
            return
        else:
            self.firstExecuteApi(versions_status_list)
    def compareVersion(self,oldData,newData):
        '''对比版本数据'''
        # 1. 组合所有 oldData 中的 status 为一个集合
        print("老数据{}".format(oldData))
        print("新数据{}".format(newData))
        missing_status_list = {
            "version_status_list":[],
            "all_old_platfromType":[]
        }

        all_old_status = set()
        all_old_platfromType=set()
        for item in oldData:
            if len(item["modelStatus"])>0:
                all_old_status.update(item["modelStatus"])
            if len(item["platfromType"]>0):
                all_old_platfromType.update(item["platfromType"])

        missing_status_list['all_old_platfromType']=all_old_platfromType

        for item in newData:
            for status in item["modelStatus"]:
                if status not in all_old_status:
                    missing_status_list['version_status_list'].append(status)

        # 打印结果
        logging.info('需求进度有变更{}'.format(missing_status_list))
        return missing_status_list
    

    def firstExecuteApi(self, status_list):
        '''执行修改状态后的项目的脚本'''
        logging.info("==========开始匹配接口项目=============")
        env_map = {
            '聚好麦': ['测试中', '已测试待上线', '已上线'],
            '好又多': ['测试中', '已测试待上线', '已上线'],
            '量多多': ['测试中', '已测试待上线', '已上线'],
            '小云': ['测试中', '已测试待上线', '已上线'],
            '投放': ['测试中', '已测试待上线', '已上线'],
            '寄划算': ['测试中', '已测试待上线', '已上线'],
        }
        platfromType=status_list["all_old_platfromType"]


        for status_version in status_list:
            for platform, stages in env_map.items():
                if status_version.startswith(platform):
                    environment = '测试环境' if any(stage in status_version for stage in stages[:-1]) else '生产环境'
                    logging.info(f"版本更新触发>执行{platform}{environment}接口脚本")
                    self._executeApi(platform, environment,platfromType)
                    break


    def _executeApi(self,platfrom,environmentType,platfromType):
        '''执行接口脚本'''
        logging.info("==========开始执行接口项目=============")
        logging.info("平台=={},执行环境=={},执行脚本类型==={}".format(platfrom,environmentType,platfromType))

        status_conditions = ["platfromType LIKE '%{}%'".format(s) for s in platfromType]
        # 聚好麦
        if platfrom=="聚好麦" and environmentType=="测试环境":
            logging.info("开始执行>执行聚好麦测试环境接口脚本")
            sql='''
                    SELECT
                            a.*, 
                            b.*, 
                            c.*, 
                            d.modeldata
                    FROM
                            quality_scriptproject a
                    JOIN
                            quality_modeldata b ON a.versionName = b.modeldata_id
                    JOIN
                            auth_user c ON a.creater = c.username
                    JOIN
                            quality_modeldata d ON b.subModelData = d.modeldata_id
                    WHERE
                            a.environment = '1'
                            and d.modelData=\'{}\'
                            and a.`status`='TRUE'
                            and {}
                    ORDER BY
                            a.createtime DESC

            '''.format(platfrom,status_conditions)
            print("聚好麦执行sql==={}".format(sql))

        if platfrom=="聚好麦" and environmentType=="生产环境":
            logging.info("开始执行>执行聚好麦生产环境接口脚本")


        # 好又多
        if platfrom=="好又多" and environmentType=="测试环境":
            logging.info("开始执行>执行好又多测试环境接口脚本")


        if platfrom=="好又多" and environmentType=="生产环境":
            logging.info("开始执行>执行好又多生产环境接口脚本")



        # 量多多
        if platfrom=="量多多" and environmentType=="测试环境":
            logging.info("开始执行>执行量多多测试环境接口脚本")


        if platfrom=="量多多" and environmentType=="生产环境":
            logging.info("开始执行>执行量多多生产环境接口脚本")



        # 小云
        if platfrom=="小云" and environmentType=="测试环境":
            logging.info("开始执行>执行小云测试环境接口脚本")


        if platfrom=="小云" and environmentType=="生产环境":
            logging.info("开始执行>执行小云生产环境接口脚本")


        # 投放
        if platfrom=="投放" and environmentType=="测试环境":
            logging.info("开始执行>执行投放测试环境接口脚本")


        if platfrom=="投放" and environmentType=="生产环境":
            logging.info("开始执行>执行投放生产环境接口脚本")



        # 寄划算
        if platfrom=="寄划算" and environmentType=="测试环境":
            logging.info("开始执行>执行寄划算测试环境接口脚本")


        if platfrom=="寄划算" and environmentType=="生产环境":
            logging.info("开始执行>执行寄划算生产环境接口脚本")


        

        


