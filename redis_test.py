import redis
import json
import common_
import time
import string

host = '10.134.96.54'
passwd = 'redis'
port = 5500
db = 0


# hh = "a@c;b;c;d;"
# hh = hh.replace('a@c;', '')
# print(hh)


redis_cli = redis.Redis(host=host, password=passwd, port=port, db=db)
#print(redis_cli.keys())
# key_temp = common_.redis_keys(pattern='[1|2]_*')
# sort_list = []
# for key in key_temp:
# 	value1 = {}



key_temp = common_.redis_keys("")
sort_time = []
for key in key_temp:
	value1 = {}
	#print(key)
	if 'all' in key:
		pass
	else:
		mm = json.loads(redis_cli.hget(key, 'data').decode(encoding='utf-8'))
		value1['title_id'] = mm['title_id']
		mm_temp = time.strptime(mm['creat_time'], "%Y-%m-%d %H:%M:%S")
		mm_time = mm['creat_time']
		redis_cli.hset(key, 'creat_time', mm_time)
		value1['creat_time']= int(time.mktime(mm_temp))
		print(value1)
		sort_time.append(value1)
		#print(sort_time)
print('OK')
#print(sort_time)
temp = sorted(sort_time, key = lambda x : x['creat_time'])
#redis_cli.lpush('all', '2_1')
print(temp)
for i in range(1,5):
	print(temp[i]["title_id"])
# for mm1 in temp:
# 	common_.add_list_top('all', mm1['title_id'])
# 	project_id = mm1['title_id'].split('_')[0]
# 	common_.add_list_top('all_' + str(project_id), mm1['title_id'])
# print("over")
