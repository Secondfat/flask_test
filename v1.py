# coding=utf8
# Author:guoxc

#import pymysql as MYSQLdb
from common_ import *
import time
import json


everypage = 12

# 增加需求
def add_requirement_redis(project_id, add_reqdict):
	try:
		if project_id != 0:
			match = str(project_id ) + "_" + "*" #匹配data数据
		else:
			return ("project_id is null")
		key_data = redis_keys(match)
		if key_data:
			name = str(project_id) + "_" + str(len(key_data) + 1)
		else:
			name = str(project_id) + "_1"
		add_reqdict["title_id"] = name
		add_hash(name, add_reqdict)
		return "OK"
	except Exception as e:
		return code_error(e)

# 取需求
def get_requirment_redis(project_id, page_num, email):
	try:
		get_requirment_data = {}
		get_requirement_list = []
		key_data = []
		sort_key_temp = []
		no_sort_key = []
		if project_id == "" or project_id == None:
			pattern = ""
			key_temp = redis_keys(pattern)
			if key_temp:
				no_sort_key.extend(redis_keys(pattern))
			else:
				pass
		elif '|' in project_id:
			for id_temp in project_id.split('|'):
				pattern = str(id_temp) + '_*'
				key_temp = redis_keys(pattern)
				if key_temp:
					no_sort_key.extend(redis_keys(pattern))
				else:
					pass
		else:
			pattern = str(project_id) + '_*'
			key_temp = redis_keys(pattern)
			if key_temp:
				no_sort_key.extend(redis_keys(pattern))
			else:
				pass
		if no_sort_key:
			for key in no_sort_key:
				value1 = {}
				if 'all' in key:
					pass
				else:
					mm_temp = time.strptime(redis_Hget(key, 'creat_time'), "%Y-%m-%d %H:%M:%S")
					value1['title_id'] = key
					value1['creat_time']= int(time.mktime(mm_temp))
					sort_key_temp.append(value1)
			sort_key = sorted(sort_key_temp, key=lambda x: x['creat_time'], reverse = True)
			begin = everypage * (page_num - 1)
			end = everypage * page_num
			if len(sort_key) < begin:
				return "nodata"
			elif len(sort_key) >= begin and len(sort_key) < end:
				for i in range(begin, len(sort_key)):
					key_data.append(sort_key[i]["title_id"])
			elif len(sort_key) >= end:
				for i in range(begin, end):
					key_data.append(sort_key[i]["title_id"])
		else:
			return recdata("")
		if key_data and key_data != None:
			for key in key_data:
				data_key = redis_Hget(key, "data")
				if data_key:
					dic_temp = json.loads(data_key)
					dic_temp["islike"] = like_unlike(key, email)
					dic_temp["like_num"] = redis_Hget(key, "like_num")
					dic_temp["unlike_num"] = redis_Hget(key, "unlike_num")
					dic_temp["creat_time"] = redis_Hget(key, "creat_time")
					get_requirement_list.append(dic_temp)
				else:
					pass
			get_requirment_data = recdata(get_requirement_list)
			return get_requirment_data
		else:
			return recdata("")
	except Exception as e:
		return code_error(e)

# like_type字段 1:赞 2:踩 3:取消赞 4:取消踩
def like_requirement_redis(like_type, email, title_id):
	try:
		if like_type == 1:
			key_change = 'like'
			value_change = 1
		elif like_type == 2:
			key_change = 'unlike'
			value_change = 1
		elif like_type == 3:
			key_change = 'like'
			value_change = -1
		elif like_type == 4:
			key_change = 'unlike'
			value_change = -1
		else:
			return False
		try:
			change_name(title_id, key_change + '_name', email, value_change)
			auto_plus(title_id, key_change + '_num', value_change)
			return "OK"
		except Exception as e:
			return code_error(e)
	except Exception as e:
		return code_error(e)


#like字段 0:无赞无踩;1:赞;2:踩
def like_unlike(key, email):
	like_name = redis_Hget(key, "like_name")
	unlike_name = redis_Hget(key, "unlike_name")
	if email in like_name:
		return 1
	elif email in unlike_name:
		return 2
	else:
		return 0

# 名字修改
def change_name(name, key, email, value):
	try:
		name_temp = redis_Hget(name, key)
		if value == 1:
			name_temp = name_temp + email + ';'
		elif value == -1:
			name_temp = name_temp.replace(email + ';', '')
		redis_Hset(name, key, name_temp)
	except Exception as e:
		print(e)


# if __name__ == '__main__':
# 	get_requirment_redis(1, "郭祥宸")


#r = redis.Redis(host='10.134.96.54', port=5500, password='redis', db=0)
#r.set('name', ['zhang'])   #添加
#print (r.get('name'))   #获取


# mysql_host = "10.144.102.31"
# mysql_user = "root"
# mysql_pw = "wuxian@123"
# db_name = "data_center"
#
# def select_datacenter(sql):
# 	###mysql connect###
# 	db = MYSQLdb.connect(mysql_host, mysql_user, mysql_pw, db_name, charset='utf8')
# 	cursor = db.cursor()
# 	try:
# 		# 执行sql语句
# 		cursor.execute(sql)
# 		data = cursor.fetchall()
# 	except Exception as e:
# 		# Rollback in case there is any error
# 		# print sql
# 		#logging.error(traceback.format_exc())
# 		return False
# 	# 关闭数据库连接
# 	db.close()
# 	return data

# def get_requirment(project_id):
# 	get_requirement_data = {}
# 	if project_id == 0:
# 		project_id = '%'
# 	get_requirement_sql = "select id,project_id,user_name,email,requirement,level,pm_name,create_time from requirement where project_id like '%s' order by create_time desc" % (
# 	project_id)
# 	get_requirement_sql_data = select_datacenter(get_requirement_sql)
# 	get_requirement_list = []
# 	for requirement in get_requirement_sql_data:
# 		id = str(requirement[0])
# 		project_id = str(requirement[1])
# 		user_name = requirement[2]
# 		email = requirement[3]
# 		content = requirement[4]
# 		level = requirement[5]
# 		pm_name = requirement[6]
# 		create_time = str(requirement[7])
# 		get_requirement_list.append(
# 			dict(id=id, project_id=project_id, user_name=user_name, email=email, content=content, level=level,
# 			     pm_name=pm_name, create_time=create_time))
# 	get_requirement_data["code"] = "ok"
# 	get_requirement_data["result"] = get_requirement_list
# 	return get_requirement_data