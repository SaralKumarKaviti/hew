from flask import Blueprint,request,jsonify
from hew_api.admin.models import HewDepartmentUsers, HewRoles
from hew_api.config import client
import datetime
import json
from flask import Flask

from werkzeug import generate_password_hash, check_password_hash

# Email Configuration
import secrets
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'amarkr.lue@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
secret_val = secrets.token_urlsafe(20)


department_users = Blueprint('department_users', __name__)

@department_users.route('/login', methods=['POST'])
def department_login():
	email = request.json['email']
	password = request.json['password']
	data_status = {"responseStatus": 0, "result": ""}

	if email and password and request.method == 'POST':
		try:
			queryset = HewDepartmentUsers.objects.get(email__exact=email)
			if check_password_hash(queryset.password, password):
				queryset.lastLogin = datetime.datetime.now()
				queryset.save()
				dataset = {
					"id": str(queryset.id),
                    "displayName": queryset.displayName,
                    "userName": queryset.userName,
                    "email": queryset.email,
                    "phoneNumber": queryset.phoneNumber,
                    "roleId": str(queryset.roleId),
                    "createdOn": queryset.createdOn,
                    "status": queryset.status,
                    "lastLogin": queryset.lastLogin,
                    "lastLogout": queryset.lastLogout
				}
				data_status["responseStatus"] = 1
				data_status["result"] = dataset
				return data_status
			else: 
			    data_status["responseStatus"] = 0
			    data_status["result"] = "Invalid Password!"
			    return data_status
		except HewDepartmentUsers.DoesNotExist:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid Email Id"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "All are required fields!"
		return data_status
@department_users.route('/view_profile/<id>', methods=['GET'])
def view_profile(id):
	data_status = {"responseStatus": 0, "result": ""}
	if id and request.method == 'GET':
		try:
			queryset = HewDepartmentUsers.objects.get(pk__exact=id)
			if queryset:
				dataset = {
					"id": str(queryset.id),
	                "displayName": queryset.displayName,
	                "userName": queryset.userName,
	                "email": queryset.email,
	                "phoneNumber": queryset.phoneNumber,
	                "roleId": str(queryset.roleId),
	                "createdOn": queryset.createdOn,
	                "status": queryset.status,
	                "lastLogin": queryset.lastLogin,
	                "lastLogout": queryset.lastLogout
				}
				data_status["responseStatus"] = 1
				data_status["result"] = dataset
				return data_status
		except HewDepartmentUsers.DoesNotExist:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid user id!"
			return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "User id should be 24 characters!"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status

@department_users.route('/change_password', methods=['PATCH'])
def change_password():
	id = request.json['id']
	password = request.json['password']
	newPassword = request.json['newPassword']
	confirmNewPassword = request.json['confirmNewPassword']
	data_status = {"responseStatus": 0, "result": ""}

	if id and password and newPassword and confirmNewPassword and request.method == 'PATCH':
		if newPassword == confirmNewPassword:
			queryset = HewDepartmentUsers.objects.get(pk__exact=id)
			if queryset:
				if check_password_hash(queryset.password, password):
					queryset.password = generate_password_hash(newPassword)
					queryset.save()
					data_status["responseStatus"] = 1
					data_status["result"] = "Password successfully changed!"
					return data_status
				else:
					data_status["responseStatus"] = 0
					data_status["result"] = "Wrong Password!"
					return data_status
			else:
				data_status["responseStatus"] = 0
				data_status["result"] = "Invalid User!"
				return data_status
		else:
			data_status["responseStatus"] = 0
			data_status["result"] = "New Password Miss-matched!"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status


@department_users.route('/edit_profile', methods=['PUT'])
def edit_profile():
	data_status = {"responseStatus": 0, "result": ""}
	id = request.json['id']
	displayName = request.json['displayName']
	phoneNumber = request.json['phoneNumber']
	status = request.json['status']

	if id and displayName and phoneNumber and (status in [0,1]) and request.method == 'PUT':
		try:
			queryset = HewDepartmentUsers.objects.get(pk__exact=id)
			if queryset:
				queryset.displayName = displayName
				queryset.phoneNumber = phoneNumber
				queryset.status = status
				queryset.save()
				data_status["responseStatus"] = 1
				data_status["result"] = "Profile updated successfully!"
				return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid user id! " + type(e).__name__
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status


@department_users.route('/email_verification', methods=['GET', 'POST'])
def email_verification():
	data_status = {"responseStatus": 0, "result": ""}
	id = request.json['id']
	email = request.json['email']

	if id and email:
		queryset = HewDepartmentUsers.objects.get(pk__exact=id)
		queryset.verification = str(secret_val)
		queryset.save()
		msg = Message('Forgot Password Email Verification',sender='amarkr.lue@gmail.com',recipients=[email])
		msg.body = 'http://192.168.0.154:5000/api/department/forgot_password/'+str(secret_val)
		mail.send(msg)

		data_status["responseStatus"] = 1
		data_status["result"] = "Sent successfully!"
		return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status


@department_users.route('/forgot_password/<verification>', methods=['GET', 'PATCH'])
def forgot_password(verification):
	id = request.json['id']
	newPassword = request.json['newPassword']
	confirmPassword = request.json['confirmPassword']
	data_status = {"responseStatus":0,"result":""}

	if id and newPassword and confirmPassword and verification:
		try:
			queryset = HewDepartmentUsers.objects.get(verification=verification)
			if queryset:
				if newPassword and confirmPassword and request.method == 'PATCH':
					if newPassword == confirmPassword:
						try:
							queryset = HewDepartmentUsers.objects.get(pk__exact=id)
							if queryset:
								queryset.password = generate_password_hash(newPassword)
								queryset.save()
								data_status["responseStatus"] = 1
								data_status["result"] = "Password successfully changed!"
								return data_status
						except Exception as e:
							data_status["responseStatus"] = 0
							data_status["result"] = e.args[0]
							return data_status
					else:
						data_status["responseStatus"] = 0
						data_status["result"] = "Password Miss-matched!"
						return data_status
				else:
					data_status["responseStatus"] = 0
					data_status["result"] = "All are required fields!"
					return data_status

		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = e.args[0]
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status 
