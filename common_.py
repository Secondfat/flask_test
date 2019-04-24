# coding=utf8
# Author:guoxc
import redis
import json
import time

host = '10.134.96.54'
passwd = 'redis'
port = 5500
db = 0

redis_cli = redis.StrictRedis(host=host, password=passwd, port=port, db=db)

# 数据类型转换
def safe_convert(text, tp, default):
	try:
		return tp(text)
	except:
		return default

# 返回正确数据
def recdata(result_data):
	recdict = {}
	recdict["code"] = "ok"
	recdict["result"] = result_data
	return recdict

# 拼接错误数据
def code_error(error_code):
	recdict = {}
	recdict["code"] = "error"
	recdict["error"] = error_code
	return recdict

# 跨域访问添加headers
def cross_header(rst):
	rst.headers['Access-Control-Allow-Origin'] = '*'
	return rst

# 拆分project_id
def div_project(project_id):
	id_temp = project_id.split('|')
	return id_temp
######################################################
## redis相关

def redis_get(key):
	try:
		return redis_cli.get(key).decode(encoding='utf-8')
	except:
		return False

#取set值
def redis_smembers(name):
	try:
		return redis_cli.smembers(name).decode(encoding='utf-8')
	except:
		return False

def redis_Hget(name, key):
	try:
		return redis_cli.hget(name, key).decode(encoding='utf-8')
	except:
		return False

def redis_Hset(name, key, value):
	try:
		return redis_cli.hset(name, key, value).decode(encoding='utf-8')
	except:
		return False

def redis_keys(pattern):
	try:
		if pattern:
			keys = redis_cli.keys(pattern)
		else:
			keys = redis_cli.keys()
		#print(keys)
		if keys:
			for i in range(0, len(keys)):
				keys[i] = keys[i].decode(encoding='utf-8')
			return keys
		else:
			return False
	except:
		return False

# 增加hash
def add_hash(name, data):
	try:
		now = time.strftime("%Y-%m-%d %H:%M:%S")
		redis_cli.hmset(name, {"data": json.dumps(data), "like_num": 0, "unlike_num": 0, "like_name": "", "unlike_name": "", "creat_time": now})
	except Exception as e:
		print(e)

#从顶部增加list值
def add_list_top(name, title_id):
	try:
		redis_cli.lpush(name, title_id)
	except Exception as e:
		print(e)

#取list的值
def get_list(name, begin, end):
	try:
		keys = redis_cli.lrange(name, begin, end)
		for i in range(0, len(keys)):
			keys[i] = keys[i].decode(encoding='utf-8')
		return keys
	except Exception as e:
		print(e)

# 自加1
def auto_plus(name, key, value):
	try:
		redis_cli.hincrby(name, key, value)
	except Exception as e:
		print(e)


# 自减1
######################################################
## MySQL相关

