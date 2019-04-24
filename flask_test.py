# coding=utf8
# Author:guoxc

from flask import Flask,jsonify,request
from v1 import *
from common_ import *
from urllib.request import quote, unquote
import logging

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route('/add_requirement', methods=['POST'])
def add_requirement():
	add_requirement_data = {}
	try:
		if request.method == 'POST':
			body_value = unquote(request.get_data().decode(encoding='utf-8')).split('&')
			#body_value = unquote(request.get_data().decode(encoding='utf-8')).split('&')
		else:
			return jsonify(code_error("Method error"))
		add_reqdict = {}
		project_id = 0
		for value_temp in body_value:
			arg_key = value_temp.split('=')[0]
			if len(value_temp.split('=')) != 1:
				arg_value = value_temp.split('=')[1]
			else:
				arg_value = ""
			if arg_key == 'project_id':
				project_id = safe_convert(arg_value, int, 0)
			elif arg_key == 'user_name':
				user_name = safe_convert(arg_value, str, "")
				add_reqdict['user_name'] = user_name
			elif arg_key == 'email':
				email = safe_convert(arg_value, str, "")
				add_reqdict['email'] = email
			elif arg_key == 'requirement':
				requirement = safe_convert(arg_value, str, "")
				add_reqdict['requirement'] = requirement
		insert_status = add_requirement_redis(project_id, add_reqdict)
		rst = cross_header(jsonify(recdata(insert_status)))
		return rst
	except Exception as e:
		return jsonify(code_error(e))


@app.route('/get_requirement', methods=['GET', 'POST'])
def get_requirement():
	start_time = time.time()
	requirement_data = {}
	visit_ip, visit_ua = get_visitor_info()
	try:
		project_id = get_para('project_id', str)
		user_name = get_para('user_name', str)
		page_num = get_para('page_num', int)
		email = get_para('email', str)
		if user_name == ""or user_name == None:
			return err_rec("user_name数据错误")
		if page_num == 0 or page_num == None:
			return err_rec("page_num数据错误")
		if email == "" or email == None:
			return err_rec("email数据错误")
		#requirement_data = get_requirment(project_id)
		# project_id = safe_convert(project_id, int, 0)
		# user_name = safe_convert(user_name, str, "")
		# page_num = safe_convert(page_num, int, 0)
		requirement_data = get_requirment_redis(project_id, user_name, page_num, email)
		rst = cross_header(jsonify(requirement_data))
		status = 'ok'
		return rst
	except Exception as e:
		status = 'fail'
		return jsonify(code_error(e))
	cost = (time.time()-start_time)*1000
	logging.info("ip=%s,op=get_requirement,ua=%s,cost=%.2fms,status=%s" % (visit_ip, visit_ua, cost, status))


@app.route('/like_requirement', methods=['GET','POST'])
def like_requirement():
	try:
		#print(request.args.keys())
		like_type = get_para('like_type', int)
		user_name = get_para('user_name', str)
		title_id = get_para('title_id', str)
		email = get_para('email', str)
		# like_type = safe_convert(like_type, int, 0)
		# user_name = safe_convert(user_name, str, "")
		# title_id = safe_convert(title_id, str, "")
		if user_name == "" or user_name == None:
			return err_rec("user_name数据错误")
		if title_id == "" or title_id == None:
			return err_rec("title_id数据错误")
		if like_type == 0 or like_type == None:
			return err_rec("like_type数据错误")
		if email == "" or email == None:
			return err_rec("like_type数据错误")
		like_do = like_requirement_redis(like_type, email, title_id)
		rst = cross_header(jsonify(recdata(like_do)))
		return rst
	except Exception as e:
		return jsonify(code_error(e))

@app.errorhandler(404)
def catch_404(error):
	print()
	return request.url + "\n error %s" % 404, 404

# 参数错误
def err_rec(log):
	return cross_header(jsonify(code_error(log)))

# 取url参数
def get_para(para, type):
	if type == int:
		return request.values.get(para, default=0, type=int)
	elif type == str:
		return request.values.get(para, default='', type=str)

def get_visitor_info():
	return request.remote_addr, request.user_agent

if __name__ == '__main__':
	#app.run(host = '10.134.96.54', port=5600, debug=True)
	app.run()
