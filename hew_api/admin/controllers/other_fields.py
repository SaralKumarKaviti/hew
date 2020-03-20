from flask import Blueprint,request,jsonify
from hew_api.admin.models import HewOtherFields
from hew_api.config import client
import datetime
import json

other_fields = Blueprint('other_fields',__name__)
@other_fields.route('/add_other_fields',methods=['POST'])
def add_other_fields():
    '''This will create a Hew Other Fields '''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'POST':
        name    = request.json['name']
        adminId = request.json['adminId']
        status  = request.json['status']
        try:
            if name and adminId and status in [0,1]:
                other_field = HewOtherFields(
                    name      =   name,
                    adminId   =   adminId,
                    createdOn = datetime.datetime.now(),
                    status    = status
                )
                other_field_created = other_field.save()
                data_status["responseStatus"]=1
                data_status["result"]="Other Field created Successfully"
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@other_fields.route('/other_fields',methods=['GET'])
def get_all_other_fields():
    ''''This will give a list of other fields'''
    if request.method == 'GET':
        data_status={"responseStatus":0,"result":""}
        try:
            other_field = HewOtherFields.objects()
            if other_field:
                data_status["responseStatus"]=1
                data_status["result"]="Measurements list fetched successfully"
                data_status["other_fields"] = json.loads(other_field.to_json())
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Data not available"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status
    
@other_fields.route('/other_fields/<oid>',methods=['PUT'])
def edit_other_fields(oid):
    '''This edit Hew Other Fields'''
    if request.method == 'PUT':
        otherFieldId = oid
        data_status={"responseStatus":0,"result":""}
        try:
            name = request.json['name']
            status = request.json['status']
            if name and status in [0,1]:
                other_field = HewOtherFields.objects(id=otherFieldId).get()
                if other_field:
                    other_field.update(name = name, status = status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Other Field Updated Successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except HewOtherFields.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]= "Other Field does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@other_fields.route('/other_fields/<oid>',methods=['GET'])
def get_other_fields(oid):
    '''This Method get Hew Other Field based on Id'''
    if request.method == 'GET':
        otherFieldId = oid
        data_status={"responseStatus":0,"result":""}
        try:
            other_field = HewOtherFields.objects(id=otherFieldId).get()
            if other_field:
                data_status["responseStatus"]=1
                data_status["result"]="success"
                data_status["other_field_info"] = json.loads(other_field.to_json())
                return data_status
        except HewOtherFields.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Other Field does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@other_fields.route('/other_fields/<oid>',methods=['DELETE'])
def del_other_fields(oid):
    '''This Method delete Hew Other Fields based on Id'''
    if request.method == 'DELETE':
        otherFieldId = oid
        data_status={"responseStatus":0,"result":""}
        try:
            other_field = HewOtherFields.objects(id=otherFieldId).get()
            if other_field:
                other_field.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Successfully deleted"
                return data_status
        except HewOtherFields.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Other Field does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@other_fields.route('/other_fields_status/<oid>',methods=['PATCH'])
def update_other_fields_status(oid):
    ''' This updates status '''
    if request.method == 'PATCH':
        otherFieldId = oid
        data_status={"responseStatus":0,"result":""}
        status = request.json['status']
        try:
            if status in [0,1]:
                other_field = HewOtherFields.objects(id=otherFieldId).get()
                if other_field:
                    other_field.update(status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Status updated successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except HewOtherFields.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Other Field does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status