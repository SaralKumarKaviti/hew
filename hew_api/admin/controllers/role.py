from flask import Blueprint,request,jsonify
from hew_api.admin.models import HewRoles,HewAdmin
from hew_api.config import client
import datetime
import json
#from admin import admin

role=Blueprint('role',__name__)
@role.route('/role',methods=['POST'])
def add_role():
    roleName=request.json['roleName']
    adminId=request.json['adminId']
    rolePermissions=request.json['rolePermissions']
    createdOn=datetime.datetime.now()
    status=request.json['status']

    data_status={"responseStatus":0,"result":""}
    
    if roleName and adminId and rolePermissions and createdOn and status in [0,1] and request.method=='POST':
        try:
            queryset=HewAdmin.objects.get(pk=adminId)
            if queryset:
                try:
                    role=HewRoles(
                        roleName=roleName,
                        adminId=adminId,
                        rolePermissions=rolePermissions,
                        createdOn=createdOn,
                        status=status
                    )
                    role_created=role.save()
        
                    if role_created:
                        data_status["status"]=1
                        data_status["result"]="Successfully Role Created"
                        return data_status
                except Exception as e:
                    data_status["responseStatus"]=1
                    data_status["result"]=e.args[0]
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
        data_status["responseStatus"]=0
        data_status["result"]="Required fields missing"
        return data_status

@role.route('/role',methods=['GET'])
def show_role():
    data_status = {"responseStatus": 0, "result": ""}
    if request.method == 'GET':
        try:
            queryset = HewRoles.objects.all()
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

@role.route('/role/<rid>',methods=['GET'])
def single_role(rid):
    data_status = {"responseStatus": 0, "result": ""}
    if request.method == 'GET':
        try:
            queryset=HewRoles.objects(pk=rid).get()
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
        
@role.route('/role/<rid>',methods=['PUT'])
def edit_role(rid):
    roleName=request.json['roleName']
    rolePermissions=request.json['rolePermissions']
    status=request.json['status']
    data_status={"responseStatus":0,"result":""}

    if roleName and rolePermissions and status in [0,1] and request.method=='PUT':
        try:
            role=HewRoles.objects(pk=rid).get()
            if role:
                role.roleName=roleName
                role.rolePermissions=rolePermissions
                role.status=status

                update_data=role.save()
                data_status["responseStatus"]=1
                data_status["result"]="Role Updated Successfully"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields are missing"
        return data_status

@role.route('/role/<rid>',methods=['DELETE'])
def delete_role(rid):
    data_status={"responseStatus":0,"result":""}

    if rid and request.method=='DELETE':
        try:
            role=HewRoles.objects(pk=rid).get()
            if role:
                delete_role=role.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Deleted Role"
                return data_status
        except Exception as e :
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status
    else:
         data_status["responseStatus"]=0
         data_status["result"]="Role Does not existed"
         return data_status

@role.route('/role/<rid>',methods=['PATCH'])
def update_status(rid):
    data_status={"responseStatus":0,"result":""}
    status=request.json['status']
    if rid and status in[0,1]:
        try:
            role=HewRoles.objects(pk=rid).get()
            if role:
                role.status=status
                role.save()
                data_status["responseStatus"]=1
                data_status["result"]="Role Status Updated"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Role Does not existed"
        return data_status


