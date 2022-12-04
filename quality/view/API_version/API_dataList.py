class DataList:
	def __int__(self,project_id,year,month,location_code):
		self.MqSqlAddress={
            'host': '192.168.100.89',
            'user': 'apm',
            'password': 'persagy@2021',
            'port': 9934,
            'database':'persagy_test',
            'charset':'utf8',
        }
		self.project_id=project_id
		self.year=year
		self.month=month
		self.location_code=location_code
	def selectMysql(self,sql):
		'''mysql查询'''
		import pymysql
		from pymysql.constants import CLIENT
		# sql='show tables'
		connection = pymysql.connect(db='lzzk', user='lzzk', password='v0eKCUDZ7RpX8Ff', host='192.168.100.102',
									 port=31009, charset='utf8', client_flag=CLIENT.MULTI_STATEMENTS)
		cursor = connection.cursor()
		cursor.execute(sql)
		result=cursor.fetchall()
		return result

	def conectMysql(self,sql):
		import  pymysql
		from pymysql.constants import CLIENT
		# sql='show tables'
		connection = pymysql.connect(db='lzzk', user='lzzk', password='v0eKCUDZ7RpX8Ff', host='192.168.100.102',
									 port=31009, charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
		cursor = connection.cursor()

		#转译字符串
		if isinstance(sql,list):
			for sql_list in sql:
				# sql_list=escape_string(sql_list)

				print('sql_list',sql_list)
				result = cursor.execute(sql_list)
			connection.commit()
			connection.close()
		else:
			# sql=escape_string(sql)
			result=cursor.execute(sql)
			connection.commit()
			connection.close()

			return  result
		print('sql',sql)
		# print('result',result)
		print(9999999)
		#查询多条数据



	def returnTables(self):
		'''返回所有的表'''
		return_table='show tables'
		result = self.selectMysql(return_table)
		print(result)
		total_tables_columns={
			"tableList":[],
			# "tableListConlumns":[]
		}

		for i in range(len(result)):
			tableList={"value":"","label":""}
			columnsList={}
			tableList["value"]=result[i][0]
			tableList["label"]=str(i)
			total_tables_columns["tableList"].append(tableList)
			# columns=self.returnColumns(result[0])
			# columnsList[result[0]]=columns
			# total_tables_columns["tableListConlumns"].append(columnsList)

		return total_tables_columns



	def returnColumns(self,table):
		'''返回所有的列'''
		print('table',table)
		return_column='show FIELDS from '+table
		result=self.selectMysql(return_column)
		columnList = []
		for column in result:
			columnList.append(column[0])
		return columnList

	def tb_coldstation_features_environment_in(self,project_id,year,month,location_code):
		'''
		:param project_id: 项目名称
		:param month: 月
		:param location_code:楼层编码
		:return:
		'''

		tb_coldstation_features_environment_in_sql='INSERT INTO tb_coldstation_features_environment_in_'+str(year)+'0'+str(month)+\
			' (project_id,'\
			'collection_time,'\
			'date,'\
			'location_code,'\
			'temperature,'\
			'create_time) VALUES'
		day=1
		if month in [4,6,9,11]:
			maxDay=30
		else:
			maxDay=31
		import  random
		temperature=random.randint(1,10)
		for i  in range(maxDay):
			startString='(\''+project_id+'\',\''+year+'-0'+str(month)+'-0'+str(day)+' 00:00:00\',2022'+str(month)+',\''+location_code+'\','+temperature+',\'2022-05-17 00:00:00\'),'
			tb_coldstation_features_environment_in_sql+=startString
			day = day + 1
		return tb_coldstation_features_environment_in_sql
	def executeSql(self,sqlString):
		'''执行sql语句'''
		import pymysql
		from pymysql.cursors import DictCursor  # 结果以字典的形式返回
		# 创建连接
		conn = pymysql.connect(**self.MqSqlAddress)

		# 创建游标
		cursor = conn.cursor(DictCursor)

		# 执行sql语句
		cursor.execute(sqlString)
		sqlData = cursor.fetchall()

		# print(type(sqlData['energy_data']))
		print("获取到的sql语句是", sqlString)
		print("断言sql自查询获取到的数据是：", (sqlData))
		# 关闭游标和数据库
		cursor.close()
		conn.close()
		return sqlData

	def mainSql(self):
		'''总执行接口'''
		sqlString=self.tb_coldstation_features_environment_in(self.project_id,self.year,self.month,self.location_code)

		self.executeSql(sqlString)