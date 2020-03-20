from flask import Blueprint,request,jsonify
from hew_api.admin.models import HewDepartmentUsers,HewRoles
from hew_api.config import client
import datetime

from werkzeug import generate_password_hash, check_password_hash

user=Blueprint('user',__name__)

@user.route('/user',methods=['POST'])
def add_user():
    displayName=request.json['displayName']
    userName=request.json['userName']
    email=request.json['email']
    phoneNumber=request.json['phoneNumber']
    password=request.json['password']
    roleId=request.json['roleId']
    createdOn=datetime.datetime.now()
    status=request.json['status']
    lastLogin=datetime.datetime.now()
    lastLogout =datetime.datetime.now()

    data_status={"responseStatus":0,"result":""}

    if displayName and userName and email and phoneNumber and password and roleId and createdOn and status in [0,1] and lastLogin and lastLogout and request.method=='POST':
        print(roleId)
        try:
            queryset=HewRoles.objects(pk=roleId).get()
            if queryset:
                try:
                    user=HewDepartmentUsers(
                        displayName=displayName,
                        userName=userName,
                        email=email,
                        phoneNumber=phoneNumber,
                        password=generate_password_hash(password),
                        roleId=roleId,
                        createdOn=createdOn,
                        status=status,
                        lastLogin=lastLogin,
                        lastLogout=lastLogout
                    )
                    user_created=user.save()
                    if user_created:
                        data_status["responseStatus"]=1
                        data_status["result"]="Successfully User Created"
                        return data_status
                except Exception as e:
                    data_status["responseStatus"] = 0
                    data_status["result"] = "User name already exist! " + type(e).__name__
                    return data_status
        except HewRoles.DoesNotExist as e:
            data_status["responseStatus"] = 0
            data_status["result"] = "Role id doesnot exist! " + type(e).__name__
            return data_status
        except Exception as e:
            data_status["responseStatus"] = 0
            data_status["result"] = "Invalid Role id! " + type(e).__name__
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields missing"
        return data_status

@user.route('/user',methods=['GET'])
def show_user():
    data_status = {"responseStatus": 0, "result": ""}
    if request.method == 'GET':
        try:
            queryset = HewDepartmentUsers.objects.all()
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
        
@user.route('/user/<uid>',methods=['GET'])
def single_user(uid):
    data_status = {"responseStatus": 0, "result": ""}
    if request.method == 'GET':
        try:
            queryset = HewDepartmentUsers.objects.all()
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
        

    
@user.route('/user/<uid>',methods=['PUT'])
def edit_user(uid):
    displayName=request.json['displayName']
    #userName=request.json['userName']
    email=request.json['email']
    phoneNumber=request.json['phoneNumber']
    #password=request.json['password']
    status=request.json['status']
    data_status={"responseStatus":0,"result":""}

    if displayName and email and phoneNumber and status in [0,1] and request.method=='PUT':
        try:
            user=HewDepartmentUsers.objects(pk=uid).get()
            if user:
                
                user.displayName=displayName
                #user.userName=userName
                user.email=email
                user.phoneNumber=phoneNumber
                #user.password=password
                user.status=status
                
                update_data=user.save()
                data_status["responseStatus"]=1
                data_status["result"]="User Updated Successfully"
                return data_status
        except Exception as e:
            data_status["responseStatus"] = 0
            data_status["result"] = "Invalid User id! " + type(e).__name__
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields are missing"
        return data_status

@user.route('/user/<uid>', methods=['DELETE'])
def delete_user(uid):
    data_status={"responseStatus":0,"result":""}
        
    if uid and request.method=='DELETE':

        try:
            user=HewDepartmentUsers.objects(pk=uid).get()
            
            if user:
                delete_data=user.delete()
        
                data_status["responseStatus"]=1
                data_status["result"]="Deleted User"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]="Invalid Id"
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields are missing"
        return data_status
    

@user.route('/user/<uid>',methods=['PATCH'])
def update_status(uid):
    data_status={"responseStatus":0,"result":""}
    status=request.json['status']
    if uid and status in [0,1]:
        try:
            user=HewDepartmentUsers.objects(pk=uid).get()    
            if user:
                user.status=status
                user.save()
                data_status["responseStatus"]=1
                data_status["result"]="User Status Updated"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]="Invalid Id"
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields are missing"
        return data_status
    
        

    
