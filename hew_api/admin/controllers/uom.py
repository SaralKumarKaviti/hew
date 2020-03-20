from flask import Blueprint,request,jsonify
from ..models import HewUom
from hew_api.config import client
import datetime
import json

uom = Blueprint('uom',__name__)
@uom.route('/add_uom',methods=['POST'])
def add_uom():
    '''This will create a Hew UOM '''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'POST':
        name    = request.json['name']
        adminId = request.json['adminId']
        status  = request.json['status']
        try:
            if name and adminId and status in[0,1]:
                uom_new = HewUom(
                    name      =   name,
                    adminId   =   adminId,
                    createdOn = datetime.datetime.now(),
                    status    = status
                )
                uom_created = uom_new.save()
                data_status["responseStatus"]=1
                data_status["result"]="UOM created Successfully"
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@uom.route('/uom',methods=['GET'])
def get_all_uom():
    ''''This will give a list of uom'''
    if request.method == 'GET':
        data_status={"responseStatus":0,"result":""}
        try:
            uoms = HewUom.objects()
            if uoms:
                data_status["responseStatus"]=1
                data_status["result"]="UOMs list fetched successfully"
                data_status["uoms"] = json.loads(uoms.to_json())
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Data not available"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@uom.route('/uom/<uid>',methods=['PUT'])
def edit_uom(uid):
    '''This edit Hew UOM based on ID'''
    if request.method == 'PUT':
        uomId = uid
        data_status={"responseStatus":0,"result":""}
        try:
            name = request.json['name']
            status = request.json['status']
            if name and status in [0,1]:
                uom = HewUom.objects(id=uomId).get()
                if uom:
                    uom.update(name = name, status = status)
                    data_status["responseStatus"]=1
                    data_status["result"]="UOM Updated Successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except HewUom.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]= "UOM does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@uom.route('/uom/<uid>',methods=['GET'])
def get_uom(uid):
    '''This Method get Hew UOM based on Id'''
    if request.method == 'GET':
        uomId = uid
        data_status={"responseStatus":0,"result":""}
        try:
            uom = HewUom.objects(id=uomId).get()
            if uom:
                data_status["responseStatus"]=1
                data_status["result"]="success"
                data_status["uom_info"] = json.loads(uom.to_json())
                return data_status
        except HewUom.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="UOM does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@uom.route('/uom/<uid>',methods=['DELETE'])
def del_uom(uid):
    '''This Method delete Hew UOM based on Id'''
    if request.method == 'DELETE':
        uomId = uid
        data_status={"responseStatus":0,"result":""}
        try:
            uom = HewUom.objects(id=uomId).get()
            if uom:
                uom.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Successfully deleted"
                return data_status
        except HewUom.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="UOM does not exist"
            return data_status
        except Exception as e:
            data_status["status"]=0
            data_status["result"]=e.args[0]
            return data_status

@uom.route('/uom_status/<uid>',methods=['PATCH'])
def update_uom_status(uid):
    '''This updates status'''
    if request.method == 'PATCH':
        uomId = uid
        data_status={"responseStatus":0,"result":""}
        status = request.json['status']
        try:
            if status in [0,1]:
                uom = HewUom.objects(id=uomId).get()
                if uom:
                    uom.update(status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Status updated successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except HewUom.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="UOM does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status