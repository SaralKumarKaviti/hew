from flask import Blueprint, jsonify, request
from hew_api.admin.models import HewAdmin, HewDepartment
from hew_api.config import client
import datetime
import json


department = Blueprint('department', __name__)

@department.route('/department', methods=['POST'])
def add_department():
	name = request.json['name']
	adminId = request.json['adminId']
	createdOn = datetime.datetime.now()
	status = request.json['status']
	data_status = {"responseStatus":0,"result":""}

	if name and adminId and (status in [0,1]) and request.method == 'POST':
		try:
			queryset = HewAdmin.objects.get(pk=adminId)
			if queryset:
				try:
					department_data = HewDepartment(
							name = name,
							adminId = adminId,
							status = status,
							createdOn = createdOn
						)
					department_data.save()
					if department_data:
						data_status["responseStatus"] = 1
						data_status["result"] = json.loads(department_data.to_json())
						return data_status
				except Exception as e:
					data_status["responseStatus"] = 0
					data_status["result"] = "Department name already exist! " + type(e).__name__
					return data_status

		except HewAdmin.DoesNotExist as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Admin id doesnot exist! " + type(e).__name__
			return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid Admin id! " + type(e).__name__
			return data_status
		
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "All are required fields"
		return data_status

@department.route('/department/<dept_id>', methods=['PUT'])
def edit_department(dept_id):
	name = request.json['name']
	status = request.json['status']
	data_status = {"responseStatus":0,"result":""}

	if name and (status in [0,1]) and request.method == 'PUT':
		try:
			queryset = HewDepartment.objects.get(pk=dept_id)
			if queryset:
				queryset.name = name
				queryset.status = status
				department_data = queryset.save()

				data_status["responseStatus"] = 1
				data_status["result"] = json.loads(department_data.to_json())
				return data_status
	
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid department id! " + type(e).__name__
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "All are required fields"
		return data_status


@department.route('/department', methods=['GET'])
def show_department():
	data_status = {"responseStatus": 0, "result": ""}
	if request.method == 'GET':
		try:
			queryset = HewDepartment.objects.all()
			if queryset != None:
				data_status["responseStatus"] = 1
				data_status["result"] = json.loads((queryset.to_json()))
				return data_status

		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "No records available"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "No records available"
		return data_status

@department.route('/department/<dept_id>', methods=['GET'])
def show_single_department(dept_id):
	data_status = {"responseStatus": 0, "result": ""}
	if request.method == 'GET':
		try:
			queryset = HewDepartment.objects(pk=dept_id).get()
			if queryset != None:
				data_status["responseStatus"] = 1
				data_status["result"] = json.loads((queryset.to_json()))
				return data_status

		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "No records available"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "No records available"
		return data_status


@department.route('/department/<dept_id>', methods=['DELETE'])
def delete_department(dept_id):
	data_status = {"responseStatus": 0, "result": ""}
	if dept_id and request.method == 'DELETE':
		try:
			queryset = HewDepartment.objects.get(pk=dept_id)
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

@department.route('/department/<dept_id>', methods=['PATCH'])
def update_status(dept_id):
	data_status = {"responseStatus": 0, "result": ""}
	status = request.json['status']

	if id and (status in [0,1]) and request.method == 'PATCH':
		try:
			queryset = HewDepartment.objects.get(pk=id)
			if queryset != None:
				queryset.status = status
				queryset.save()
				data_status["responseStatus"] = 1
				data_status["result"] = "Successfully updated!"
				return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid Id!"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status