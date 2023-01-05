from quality.common.logger import Log
class TestTools:
    def conectMysql(self, sql):
        import pymysql
        connection = pymysql.connect(db='dc_dic_yl', user='persagy', password='17pkBLum44Px', host='bj-cdb-hv5uh8zm.sql.tencentcdb.com',
                                         port=59750, charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        # 查询多条数据
        result = cursor.fetchall()
        return result

    def selectSourceID(self, id):
        '''数据库查询'''
        try:
            # print("获取到的id",id)
            sql = 'select infos from dt_object where id=' + "'" + str(id) + "'"

            result = self.conectMysql(sql)
            # print('result',result[0][0])
            result = result[0][0]
            if 'null' in result:
                result = result.replace('null', '\'null\'')
            return eval(result)
        except Exception as e:
            Log().info("错误", str(e))