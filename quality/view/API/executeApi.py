import logging
class versionUpdateApi:
    def mainExecuteApi(self,newData):
        '''主执行'''
        import logging
        # print("新数据=={}".format(newData))
        self._executeApi(newData)

    def _executeApi(self,newData):
        '''执行接口脚本'''
        # [{'autoTableID': 477, 'onlinModel': ['聚好麦', '好又多', '量多多'], 'platfromType': ['商户后台', '客服', '小程序'], 'modelStatus': ['聚好麦>开发中', '好又多>开发中', '量多多>开发中']}]

        juhaomaiVersionList=[]#聚好麦
        haoyouduoVersionList=[]#好又多
        liangDuoDuoVersionList=[]#量多多
        xiaoYunVersionList=[]#小云
        touFangVersionList=[]#投放
        jiHuaSuanVersionList=[]#寄划算
        jiaFengBaoVersionList=[]#加粉宝
        gongZuoShouJiVersionList=[]#工作手机

        platfromList=[]

        #合并所有项目的数据
        for version in newData:
            logging.info("==========开始执行接口项目=============")
            for status in version['modelStatus']:
                if '聚好麦' in status:
                    juhaomaiVersionList.append(status)
            # juhaomaiVersionList = [status for status in version['modelStatus'] if '聚好麦' in status]
            # haoyouduoVersionList=[status for status in version['modelStatus'] if '好又多' in status]
            # liangDuoDuoVersionList=[status for status in version['modelStatus'] if '量多多' in status]
            # xiaoYunVersionList=[status for status in version['modelStatus'] if '小云' in status]
            # touFangVersionList=[status for status in version['modelStatus'] if '投放' in status]
            # jiHuaSuanVersionList=[status for status in version['modelStatus'] if '寄划算' in status]
            # jiaFengBaoVersionList=[status for status in version['modelStatus'] if '加粉宝' in status]
            # gongZuoShouJiVersionList=[status for status in version['modelStatus'] if '工作手机' in status]

            platfromList=[plType for plType in version['platfromType']]
        
        print("=======juhaomaiVersionList========",juhaomaiVersionList)
        print("==========platfromList============",platfromList)
            #对比平台和需求进度

        # status_conditions = ["platfromType LIKE '%{}%'".format(s) for s in platfromType]

        # # 聚好麦
        # if platfrom=="聚好麦" :
        #     logging.info("开始执行>执行聚好麦测试环境接口脚本")
        #     sql='''
        #             SELECT
        #                     a.*, 
        #                     b.*, 
        #                     c.*, 
        #                     d.modeldata
        #             FROM
        #                     quality_scriptproject a
        #             JOIN
        #                     quality_modeldata b ON a.versionName = b.modeldata_id
        #             JOIN
        #                     auth_user c ON a.creater = c.username
        #             JOIN
        #                     quality_modeldata d ON b.subModelData = d.modeldata_id
        #             WHERE
        #                     a.environment = '1'
        #                     and d.modelData=\'{}\'
        #                     and a.`status`='TRUE'
        #                     and {}
        #             ORDER BY
        #                     a.createtime DESC

        #     '''.format(platfrom,status_conditions)
        #     print("聚好麦执行sql==={}".format(sql))

        # if platfrom=="聚好麦" and environmentType=="生产环境":
        #     logging.info("开始执行>执行聚好麦生产环境接口脚本")


        # # 好又多
        # if platfrom=="好又多" and environmentType=="测试环境":
        #     logging.info("开始执行>执行好又多测试环境接口脚本")


        # if platfrom=="好又多" and environmentType=="生产环境":
        #     logging.info("开始执行>执行好又多生产环境接口脚本")



        # # 量多多
        # if platfrom=="量多多" and environmentType=="测试环境":
        #     logging.info("开始执行>执行量多多测试环境接口脚本")


        # if platfrom=="量多多" and environmentType=="生产环境":
        #     logging.info("开始执行>执行量多多生产环境接口脚本")



        # # 小云
        # if platfrom=="小云" and environmentType=="测试环境":
        #     logging.info("开始执行>执行小云测试环境接口脚本")


        # if platfrom=="小云" and environmentType=="生产环境":
        #     logging.info("开始执行>执行小云生产环境接口脚本")


        # # 投放
        # if platfrom=="投放" and environmentType=="测试环境":
        #     logging.info("开始执行>执行投放测试环境接口脚本")


        # if platfrom=="投放" and environmentType=="生产环境":
        #     logging.info("开始执行>执行投放生产环境接口脚本")



        # # 寄划算
        # if platfrom=="寄划算" and environmentType=="测试环境":
        #     logging.info("开始执行>执行寄划算测试环境接口脚本")


        # if platfrom=="寄划算" and environmentType=="生产环境":
        #     logging.info("开始执行>执行寄划算生产环境接口脚本")


    

    


