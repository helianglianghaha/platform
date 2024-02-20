import mysql.connector

class selectSqlData:
    def check_if_data_exists(self,cursor, new_data):
        # 执行查询操作，检查数据库中是否存在相同的数据
        query = "SELECT * FROM testplatform.quality_buganalysis WHERE short_id = %s"
        # print("======数据存在===={}".format(new_data))
        cursor.execute(query, (new_data['short_id'],))
        existing_data = cursor.fetchone()
        return existing_data

    def insert_or_update_data(self,cursor, connection, new_data):
        existing_data = self.check_if_data_exists(cursor, new_data)
        if existing_data:
            new_data_list=new_data.values()
            old_data_list=existing_data
            # print("=============已存在的数据=new_data_list=================", new_data_list)
            # print("================新数据==old_data_list============", old_data_list)

            for newData in new_data_list:
                if newData not in old_data_list:
                    # 如果数据不同，执行更新操作
                    columns = ', '.join(new_data.keys())
                    values_template = ', '.join(['%s'] * len(new_data))
                    update_query = f"UPDATE testplatform.quality_buganalysis SET {columns} = ({values_template}) WHERE short_id = %s"
                    print("update_query", (new_data.values()))

                    # 执行查询
                    cursor.execute(update_query, (new_data['short_id'],))
                    connection.commit()
                    print("Data updated successfully.")
                    break

                else:
                    pass
        else:
            columns = ', '.join(new_data.keys())
            values_template = ', '.join(['%s'] * len(new_data))
            insert_query = f"INSERT INTO testplatform.quality_buganalysis ({columns}) VALUES ({values_template})"
            # 如果数据库中不存在相同的数据，执行插入操作
            cursor.execute(insert_query, tuple(new_data.values()))
            connection.commit()
            print("Data inserted successfully.")
