from flask import Blueprint,request,jsonify
from hew_api.department.models import HewCustomers
from hew_api.config import client
import datetime
import json
from werkzeug import generate_password_hash, check_password_hash

customers = Blueprint('customer',__name__)


def final_cp():
    queryset=HewCustomers.objects.order_by('-id').first()
    if queryset:
        customerId=queryset.customerId
        num=int(customerId[-6:])+1
        if len(str(num))==1:
            customerId='CUST'+'00000'+str(num)
        elif len(str(num))==2:
            customerId='CUST'+'0000'+str(num)
        elif len(str(num))==3:
            customerId='CUST'+'000'+str(num)
        elif len(str(num))==4:
            customerId='CUST'+'00'+str(num)
        elif len(str(num))==5:
            customerId='CUST'+'0'+str(num)
        else:
            customerId='CUST'+str(num)
            return customerId

        return customerId
    else:
        customerId='CUST'+'000001'
        return customerId

@customers.route('/get_customer_id',methods=['GET'])
def generate_cp():
    data_status={"responseStatus":0,"result":""}
    queryset=HewCustomers.objects.order_by('-id').first()
    if queryset:
        customerId=queryset.customerId
        num=int(customerId[-6:])+1
        if len(str(num))==1:
            customerId='CUST'+'00000'+str(num)
        elif len(str(num))==2:
            customerId='CUST'+'0000'+str(num)
        elif len(str(num))==3:
            customerId='CUST'+'000'+str(num)
        elif len(str(num))==4:
            customerId='CUST'+'00'+str(num)
        elif len(str(num))==5:
            customerId='CUST'+'0'+str(num)
        else:
            customerId='CUST'+str(num)
            data_status["responseStatus"] = 1
            data_status["result"] = customerId
            return data_status

        data_status["responseStatus"] = 1
        data_status["result"] = customerId
        return data_status
    else:
        customerId='CUST'+'000001'
        data_status["responseStatus"]=1
        data_status["result"]=customerId
        return data_status

@customers.route('/customer',methods=['POST'])
def add_customer():
    data_status = {"responseStatus":0,"result":""}
    customerName    = request.json['customerName']
    userId          = request.json['userId']
    customerEmail   = request.json['customerEmail']
    password        = request.json['password']
    createdOn       = datetime.datetime.now()
    status          = request.json['status']

    if customerEmail and customerName and userId and password and createdOn and status in[0,1]:
        try:
            queryset = HewCustomers.objects.get(email__iexact=customerEmail)
            if queryset:
                data_status["responseStatus"] = 0
                data_status["result"] = "Email id already registered!"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]

        customer = HewCustomers(
            customerName  = customerName,
            customerEmail = customerEmail,
            userId = userId,
            password = generate_password_hash(password),
            createdOn = createdOn,
            status = status
        )
        customer.save()
        data_status["responseStatus"]=1
        data_status["result"]="Customer created Successfully"
        return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields missing"
        return data_status