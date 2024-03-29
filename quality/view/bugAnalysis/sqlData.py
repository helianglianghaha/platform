import mysql.connector
from quality.common.commonbase import commonList

class selectSqlData:
    def check_if_data_exists(self,cursor, new_data,target_table):
        # 执行查询操作，检查数据库中是否存在相同的数据
        print("check_if_data_exists已执行")
        print(new_data)
        query = "SELECT * FROM testplatform.{} WHERE id ={}".format(target_table,new_data['id'])
        print('query',query)
        existing_data = commonList().getModelData(query)
        return existing_data

    def insert_or_update_data(self,cursor, connection, new_data,target_table):
        print('insert_or_update_data已执行')
        existing_data = self.check_if_data_exists(cursor, new_data,target_table)
        if existing_data:
            new_data_list=new_data.values()
            old_data_list=existing_data[0].values()
            print('newData',new_data)
            print("=============已存在的数据=old_data_list=================", old_data_list)
            print("================新数据==new_data_list============", new_data_list)
            for newData in new_data_list:
                if newData not in old_data_list:
                    update_query = "UPDATE testplatform.{} SET ".format(target_table)
                    update_query += ", ".join([f"{key} = %s" for key in new_data.keys()])
                    update_query += " WHERE id = %s"
                    print('=======update_query====',update_query)
                    import re
                    if target_table == 'zt_bug':
                        update_query = re.sub(r'\b(case|status|lines)\b(?!Version)', r'`\1`', update_query)
                    if target_table == 'zt_module':
                        update_query = re.sub(r'\b(name|order|from|owner)\b(?!Version)', r'`\1`', update_query)
                    if target_table == 'zt_product':
                        update_query = re.sub(r'\b(name|code|status|desc|order)\b(?!Version)', r'`\1`', update_query)
                    if target_table == 'zt_project':
                        update_query = re.sub(r'\b(name|code|end|begin|desc|left|order)\b(?!Version)', r'`\1`',update_query)
                    if target_table == 'zt_build':
                        update_query = re.sub(r'\b(name|date|desc|order)\b(?!Version)', r'`\1`', update_query)
                        update_query = update_query + " order by id desc"

                    cursor.execute(update_query, tuple(new_data.values()) + (new_data['id'],))
                    connection.commit()
                    break
                else:
                    pass
                    # print("数据相同，不用更新")

        else:
            print("数据不存在开始执行更新")
            columns = ', '.join(new_data.keys())
            values_template = ', '.join(['%s'] * len(new_data))
            print(new_data.values())
            insert_query = f"INSERT INTO testplatform.{target_table} ({columns}) VALUES ({values_template})"

            import  re
            if target_table == 'zt_bug':
                insert_query = re.sub(r'\b(case|status|lines)\b(?!Version)', r'`\1`', insert_query)
            if target_table == 'zt_module':
                insert_query = re.sub(r'\b(name|order|from|owner)\b(?!Version)', r'`\1`', insert_query)
            if target_table == 'zt_product':
                insert_query = re.sub(r'\b(name|code|status|desc|order)\b(?!Version)', r'`\1`', insert_query)
            if target_table == 'zt_project':
                insert_query = re.sub(r'\b(name|code|begin|end|desc|left|order)\b(?!Version)', r'`\1`', insert_query)
            if target_table == 'zt_build':
                insert_query = re.sub(r'\b(name|date|desc)\b(?!Version)', r'`\1`', insert_query)
            print('insert_query', insert_query)
            cursor.execute(insert_query, tuple(new_data.values()))
            connection.commit()
