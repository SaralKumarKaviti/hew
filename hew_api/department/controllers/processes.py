from flask import Blueprint,request,jsonify
from hew_api.admin.models import HewDepartmentUsers, HewRoles, HewCompanyPreference
from hew_api.department.models import HewProcess
from hew_api.config import client
import datetime
import json


processes = Blueprint('processes', __name__)

@processes.route('/final_cp', methods=['GET'])
def final_cp():
	
	queryset = HewProcess.objects.order_by('-id').first()
	if queryset:
		process_id = queryset.processId
		num = int(process_id[-6:]) + 1
		if len(str(num)) == 1:
			processId = "PROC" + '00000' + str(num)
			
		elif len(str(num)) == 2:
			processId = "PROC" + '0000' + str(num)
			
		elif len(str(num)) == 3:
			processId = "PROC" + '000' + str(num)
			
		elif len(str(num)) == 4:
			processId = "PROC" + '00' + str(num)
			
		elif len(str(num)) == 5:
			processId = "PROC" + '0' + str(num)
			
		else:
			processId = "PROC" + str(num)
			return processId
		return processId

	else:
		processId = "PROC" + "000001"
		return processId

@processes.route('/get_pid', methods=['GET'])
def generate_cp():
	data_status = {"responseStatus": 0, "result": ""}

	queryset = HewProcess.objects.order_by('-id').first()
	if queryset:
		process_id = queryset.processId
		num = int(process_id[-6:]) + 1
		if len(str(num)) == 1:
			processId = "PROC" + '00000' + str(num)
			# return processId
		elif len(str(num)) == 2:
			processId = "PROC" + '0000' + str(num)
			# return processId
		elif len(str(num)) == 3:
			processId = "PROC" + '000' + str(num)
			# return processId
		elif len(str(num)) == 4:
			processId = "PROC" + '00' + str(num)
			# return processId
		elif len(str(num)) == 5:
			processId = "PROC" + '0' + str(num)
			# return processId
		else:
			processId = "PROC" + str(num)
			data_status["responseStatus"] = 1
			data_status["result"] = processId
			return data_status

		data_status["responseStatus"] = 1
		data_status["result"] = processId
		return data_status

	else:
		processId = "PROC" + "000001"
		data_status["responseStatus"] = 1
		data_status["result"] = processId
		return data_status

	

	

@processes.route('/processes', methods=['POST'])
def add_process():
	data_status = {"responseStatus": 0, "result": ""}
	name = request.json['name']
	processName = request.json['processName']
	status = request.json['responseStatus']
	userId = request.json['userId']
	createdOn = datetime.datetime.now()

	if processName and status in [0, 1] and userId and request.method == 'POST':
		try:
			queryset = HewDepartmentUsers.objects.get(pk__exact=userId)
			if queryset:
				processId = name+final_cp()
				if processId != None:
					process = HewProcess(
							processName=processName,
							processId=processId,
							userId=userId,
							createdOn=createdOn,
							status=status
						)
					process.save()
					data_status["responseStatus"]=1
					data_status["result"]="Successfully Process Created"
					return data_status
				else:
					data_status["responseStatus"] = 0
					data_status["result"] = "Company Preference not exist!"
					return data_status

		except HewDepartmentUsers.DoesNotExist as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Department User id doesnot exist! " + type(e).__name__
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "All are required fields!"
		return data_status


@processes.route('/processes/<id>', methods=['PUT'])
def edit_process(id):
	data_status = {"responseStatus": 0, "result": ""}
	processName = request.json['processName']

	if processName and request.method == 'PUT':
		try:
			queryset = HewProcess.objects.get(pk__exact=id)
			if queryset:
				queryset.processName = processName
				process_data = queryset.save()
				data_status["responseStatus"]=1
				data_status["result"]= json.loads(process_data.to_json())
				return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid process id! " + type(e).__name__
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "All are required fields"
		return data_status 

@processes.route('/processes/<id>', methods=['GET'])
def get_process(id):
	data_status = {"responseStatus": 0, "result": ""}
	if id and request.method == 'GET':
		try:
			queryset = HewProcess.objects.get(pk__exact=id)
			if queryset:
				data_status["responseStatus"]=1
				data_status["result"]= json.loads(queryset.to_json())
				return data_status
		except HewProcess.DoesNotExist as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid process id! " + type(e).__name__
			return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid process id! " + type(e).__name__
			return data_status

@processes.route('/processes/all', methods=['GET'])
def all_process():
	data_status = {"responseStatus": 0, "result": ""}
	queryset = HewProcess.objects.all()
	if queryset:
		data_status["responseStatus"]=1
		data_status["result"]= json.loads(queryset.to_json())
		return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "No records are available! " 
		return data_status

@processes.route('/processes/<id>', methods=['DELETE'])
def delete_process(id):
	data_status = {"responseStatus": 0, "result": ""}
	if id and request.method == 'DELETE':
		try:
			queryset = HewProcess.objects.get(pk__exact=id)
			if queryset != None:
				queryset.delete()
				data_status["responseStatus"] = 1
				data_status["result"] = "Successfully deleted!"
				return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid Id"
			return data_status

	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status

@processes.route('/processes/<id>', methods=['PATCH'])
def update_proc_status(id):
	data_status = {"responseStatus": 0, "result": ""}
	status = request.json['status']
	if id and (status in [0,1]) and request.method == 'PATCH':
		try:
			queryset = HewProcess.objects.get(pk__exact=id)
			if queryset != None:
				queryset.status = status
				queryset.save()
				data_status["responseStatus"]=1
				data_status["result"]="Process Status Updated"
				return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid Id!"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status
