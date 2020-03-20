from flask import Blueprint,request,jsonify
from hew_api.admin.models import HewRoleTypes,HewAdmin
from hew_api.config import client
import datetime
import json

role_type=Blueprint('role_type',__name__)
@role_type.route('/role_type',methods=['POST'])
def add_role_type():
    roletype=request.json['roletype']
    adminId=request.json['adminId']
    data_status={"responseStatus":0,"result":""}

    if roletype and adminId and request.method=='POST':
        try:
            queryset=HewAdmin.objects.get(pk=adminId)
            if queryset:
                roletype=HewRoleTypes(
                    roletype=roletype,
                    adminId=adminId
                )
                roletype_created=roletype.save()
                if roletype_created:
                    data_status["responseStatus"]=1
                    data_status["result"]="Successfully Role Type Created"
                    return data_status
        except Exception as e:
            data_status["responseStatus"]=1
            data_status["result"]=e.args[0]
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields missing"
        return data_status

@role_type.route('/role_type',methods=['GET'])
def show_role_type():
    data_status={"responseStatus":0,"result":""}
    try:
        role_type=HewRoleTypes.objects().all()
        if role_type:
           data_status["responseStatus"]=1
           data_status["result"]="Show Roles Type Data"
           #return data_status
           return role_type.to_json()
        else:
           data_status["responseStatus"]=0
           data_status["result"]= "Not available"
           #return data_status
           return role_type.to_json()
        #return role.to_json()
    except Exception as e:
        data_status["responseStatus"]=0
        data_status["result"]=e.args[0]
        return data_status

    
@role_type.route('/role_type/<rt_id>',methods=['GET'])
def single_role_type(rt_id):
    data_status={"responseStatus":0,"result":""}
    try:
        role_type=HewRoleTypes.objects(pk=rt_id).all()
        if role_type:
           data_status["responseStatus"]=1
           data_status["result"]="Show Roles Type Data"
           #return data_status
           return role_type.to_json()
        else:
           data_status["responseStatus"]=0
           data_status["result"]= "Not available"
           #return data_status
           return role_type.to_json()
        #return role.to_json()
    except Exception as e:
        data_status["responseStatus"]=0
        data_status["result"]=e.args[0]
        return data_status
    
@role_type.route('/role_type/<rt_id>',methods=['PUT'])
def edit_role_type(rt_id):
    roletype=request.json['roletype']
    data_status={"responseStatus":0,"result":""}

    if roletype and request.method=='PUT':
        try:
            role_type=HewRoleTypes.objects(pk=rt_id).get()
            if role_type:
                role_type.roletype=roletype
                update_data=role_type.save()
                data_status["responseStatus"]=1
                data_status["result"]="Role Type Updated Successfully"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields are missing"
        return data_status

@role_type.route('/role_type/<rt_id>',methods=['DELETE'])
def delete_role_type(rt_id):
    data_status={"responseStatus":0,"result":""}

    if rt_id and request.method=='DELETE':
        try:
            role_type=HewRoleTypes.objects(pk=rt_id).get()
            if role_type:
                delete_role=role_type.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Deleted Role Type"
                return data_status
        except Exception as e :
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status
    else:
         data_status["responseStatus"]=0
         data_status["result"]="Role Type Does not existed"
         return data_status
