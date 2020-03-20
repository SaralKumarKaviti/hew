from flask import Blueprint, jsonify, request
from hew_api.admin.models import HewAdmin
from hew_api.config import client
from werkzeug import generate_password_hash, check_password_hash
import datetime
import json
from flask import Flask

# Email Configuration
import secrets
from flask_mail import Mail, Message

# Upload Images
import base64
from io import BytesIO
from PIL import Image
import os

admin = Blueprint('admin', __name__)

app = Flask(__name__)
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'amarkr@gmail.com'
app.config['MAIL_PASSWORD'] = '@!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
secret_val = secrets.token_urlsafe(20)

# -----------------------------------------------

UPLOAD_FOLDER = '/home/apptrinity10/development/flask/hew_project/hew_api/admin/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @admin.route('/convert_and_save',methods=['POST'])
def convert_and_save(userName, email, image_data):
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))
    rgb_im = im.convert('RGB')
    imageName = userName + '.png'
    rgb_im.save(os.path.join(app.config['UPLOAD_FOLDER'], imageName))
    queryset = HewAdmin.objects.get(email__iexact=email)
    queryset.image = imageName
    queryset.save()
    return imageName
# ------------------------------------------------

@admin.route('/create_admin',methods=['POST'])
def create_admin():
    displayName = request.json['displayName']
    userName = request.json['userName']
    email = request.json['email']
    password = request.json['password']
    permissionId = request.json['permissionId']
    createdOn = datetime.datetime.now()
    status = request.json['status']
    image = request.json['image']
    data_status = {"responseStatus":0,"result":""}

    if displayName and userName and email and password and permissionId and (status in [0,1]) and image and request.method == 'POST':
        try:
            queryset = HewAdmin.objects.get(email__iexact=email)
            if queryset:
                data_status["responseStatus"] = 0
                data_status["result"] = "Email id already registered!"
                return data_status
        except Exception as e:
            pass

        admin = HewAdmin(
            displayName = displayName,
            userName = userName,
            email = email,
            password = generate_password_hash(password),
            permissionId = permissionId,
            createdOn = createdOn,
            status = status
        )
        admin_created = admin.save()
        if admin_created:
            convert_and_save(userName, email, image)
            data_status["responseStatus"] = 1
            data_status["result"] = "User added successfully!"
            return data_status
            
    else:
        data_status["responseStatus"] = 0
        data_status["result"] = "All are required fields"
        return data_status


@admin.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.json['email']
    password = request.json['password']
    data_status = {"responseStatus":0,"result":""}

    if email and password and request.method == 'POST':
        try:
            queryset = HewAdmin.objects.get(email__exact=email)
            if (check_password_hash(queryset.password, password)):
                queryset.lastLogin = datetime.datetime.now()
                queryset.lastLogout = datetime.datetime.now()
                queryset.save()
                dataset = {
                    "id": str(queryset.id),
                    "displayName": queryset.displayName,
                    "userName": queryset.userName,
                    "email": queryset.email,
                    "permissionId": queryset.permissionId,
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

        except HewAdmin.DoesNotExist:
            data_status["responseStatus"] = 0
            data_status["result"] = "Invalid Email Id!"
            return data_status
    else:
        data_status["responseStatus"] = 0
        data_status["result"] = "All are required fields!"
        return data_status

@admin.route('/email_verify', methods=['GET', 'POST'])
def email_verify():
    data_status = {"responseStatus": 0, "result": ""}
    uid = request.json['uid']
    email = request.json['email']

    if uid and email:
        queryset = HewAdmin.objects.get(pk=uid)
        if queryset:
            queryset.verification = str(secret_val)
            queryset.save()
            msg = Message('Forgot Password Email Verification',sender='amarkr.lue@gmail.com',recipients=[email])
            msg.body = 'http://127.0.0.1:5000/api/admin/admin_forgot_password/'+str(secret_val)
            mail.send(msg)
            
            data_status["responseStatus"] = 1
            data_status["result"] = "Sent successfully!"
            return data_status
    else:
        data_status["responseStatus"] = 0
        data_status["result"] = "Required fields are missing!"
        return data_status

@admin.route('/admin_forgot_password/<verification>', methods=['GET','PATCH'])
def admin_forgot_password(verification):
    uid = request.json['uid']
    newPassword = request.json['newPassword']
    confirmPassword = request.json['confirmPassword']
    data_status = {"responseStatus":0,"result":""}

    try:
        queryset = HewAdmin.objects.get(verification=verification)
        if queryset:
            if newPassword and confirmPassword and request.method == 'PATCH':
                if newPassword == confirmPassword:
                    try:
                        queryset = HewAdmin.objects.get(pk__exact=uid)
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


@admin.route('/admin_profile/<uid>', methods=['GET'])
def admin_profile(uid):
    # uid = request.json['uid'] 
    data_status = {"responseStatus": 0, "result": ""}

    if uid and request.method == 'GET':

        try:
            queryset = HewAdmin.objects.get(pk__exact=uid)
            # print(queryset)
            if queryset:
                dataset = {
                    "id": str(queryset.id),
                    "displayName": queryset.displayName,
                    "userName": queryset.userName,
                    "email": queryset.email,
                    "permissionId": queryset.permissionId,
                    "createdOn": queryset.createdOn,
                    "status": queryset.status
                }
                data_status["responseStatus"] = 1
                data_status["result"] = dataset
                return data_status
        except HewAdmin.DoesNotExist as e:
            data_status["responseStatus"] = 0
            data_status["result"] = e.args[0]
            return data_status
    else:
        data_status["responseStatus"] = 0
        data_status["result"] = "Required fields missing!"
        return data_status


@admin.route('/admin_profile_update', methods=['PUT'])
def admin_profile_update():
    uid = request.json['uid']
    displayName = request.json['displayName']
    email = request.json['email']
    data_status = {"responseStatus": 0, "result": ""}
    
    if uid and displayName and email and request.method == 'PUT':
        try:
            queryset = HewAdmin.objects.get(pk__exact=uid)
            if queryset:
                queryset.displayName = displayName
                queryset.email = email
                queryset.save()
                data_status["responseStatus"] = 1
                data_status["result"] = "Admin profile updated!"
                return data_status
        except Exception as e:
            data_status["responseStatus"] = 0
            data_status["result"] = e.args[0]
            return data_status
    else:
        data_status["responseStatus"] = 0
        data_status["result"] = "Required fields are missing!"
        return data_status


@admin.route('/admin_change_password', methods=['PATCH'])
def admin_change_password():
    uid = request.json['uid']
    password = request.json['password']
    newPassword = request.json['newPassword']
    confirmNewPassword = request.json['confirmNewPassword']
    data_status = {"responseStatus": 0, "result": ""}
    if uid and password and newPassword and confirmNewPassword and request.method == 'PATCH':
        if newPassword == confirmNewPassword:
            queryset = HewAdmin.objects.get(pk__exact=uid)
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


@admin.errorhandler(404)
def not_found(error=None):
    message = {
        'responseStatus': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp