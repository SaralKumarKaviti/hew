from flask import Blueprint, jsonify, request
from hew_api.admin.models import HewAdmin, HewDesignation
from hew_api.config import client
import datetime
import json


designation = Blueprint('designation', __name__)

@designation.route('/designation', methods=['POST'])
def create_designation():
	name = request.json['name']
	adminId = request.json['adminId']
	createdOn = datetime.datetime.now()
	status = request.json['status']
	data_status = {"responseStatus":0,"result":""}

	if name and adminId and (status in [0,1]) and request.method == 'POST':
		try:
			queryset = HewAdmin.objects.get(pk__exact=adminId)
			if queryset:
				try:
					designation_data = HewDesignation(
							name = name,
							adminId = adminId,
							status = status,
							createdOn = createdOn
						)
					designation_data.save()
					if designation_data:
						data_status["responseStatus"] = 1
						data_status["result"] = json.loads(designation_data.to_json())
						return data_status
				except Exception as e:
					data_status["responseStatus"] = 0
					data_status["result"] = "Designation name already exist! " + type(e).__name__
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

@designation.route('/designation/<id>', methods=['PUT'])
def update_designation(id):
	name = request.json['name']
	status = request.json['status']
	data_status = {"responseStatus":0,"result":""}

	if name and (status in [0,1]) and request.method == 'PUT':
		try:
			queryset = HewDesignation.objects.get(pk__exact=id)
			if queryset:
				queryset.name = name
				queryset.status = status
				designation_data = queryset.save()

				data_status["responseStatus"] = 1
				data_status["result"] = json.loads(designation_data.to_json())
				return data_status
	
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid designation id! " + type(e).__name__
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "All are required fields"
		return data_status


@designation.route('/designation', methods=['GET'])
def view_designation():
	data_status = {"responseStatus": 0, "result": ""}
	if request.method == 'GET':
		try:
			queryset = HewDesignation.objects.all()
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


@designation.route('/designation/<id>', methods=['DELETE'])
def delete_designation(id):
	data_status = {"responseStatus": 0, "result": ""}
	if id and request.method == 'DELETE':
		try:
			queryset = HewDesignation.objects.get(pk__exact=id)
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

@designation.route('/designation/<id>', methods=['PATCH'])
def update_status(id):
	data_status = {"responseStatus": 0, "result": ""}
	status = request.json['status']

	if id and (status in [0,1]) and request.method == 'PATCH':
		try:
			queryset = HewDesignation.objects.get(pk__exact=id)
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