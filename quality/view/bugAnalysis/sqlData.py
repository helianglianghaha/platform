import mysql.connector
from quality.common.commonbase import commonList

class selectSqlData:
    def check_if_data_exists(self,cursor, new_data):
        # 执行查询操作，检查数据库中是否存在相同的数据
        query = "SELECT id, title, version_report, severity, priority, status, current_owner, reporter, created, project_id, template_id, created_from, follower, due, BugStoryRelation_relative_id, BugStoryRelation_story_name, is_delay, delay, resolution, resolved, closed, modified, lastmodify, closer, in_progress_time, verify_time, reject_time, assigned_time, short_id, status_alias FROM testplatform.quality_buganalysis WHERE short_id ={}".format(new_data['short_id'])
        print('query',query)
        existing_data = commonList().getModelData(query)
        return existing_data

    def insert_or_update_data(self,cursor, connection, new_data):
        existing_data = self.check_if_data_exists(cursor, new_data)
        if existing_data:
            new_data_list=new_data.values()
            old_data_list=existing_data[0].values()
            # print('newData',new_data)
            print("=============已存在的数据=old_data_list=================", old_data_list)
            print("================新数据==new_data_list============", new_data_list)
            for newData in new_data_list:
                if newData not in old_data_list:
                    # 如果数据不同，执行更新操作
                    print("数据不同需要更新")
                    columns = ', '.join(new_data.keys())
                    values_template = ', '.join(['%s'] * len(new_data))

                    update_query = "UPDATE testplatform.quality_buganalysis SET "
                    update_query += ", ".join([f"{key} = %s" for key in new_data.keys()])
                    update_query += " WHERE short_id = %s"  # Assuming 'id' is the unique identifier

                    # 执行查询
                    # cursor.fetchall()
                    cursor.execute(update_query, tuple(new_data.values()) + (new_data['short_id'],))

                    connection.commit()
                    print("Data updated successfully.")
                    break
                else:
                    print("数据相同，不用更新")
        else:
            columns = ', '.join(new_data.keys())
            values_template = ', '.join(['%s'] * len(new_data))
            insert_query = f"INSERT INTO testplatform.quality_buganalysis ({columns}) VALUES ({values_template})"
            # 如果数据库中不存在相同的数据，执行插入操作
            cursor.execute(insert_query, tuple(new_data.values()))
            connection.commit()
            print("Data inserted successfully.")
