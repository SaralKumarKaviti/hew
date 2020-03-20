from flask import Blueprint,request,jsonify
from ..models import HewSubstrate
from hew_api.config import client
import datetime
import json

substrate = Blueprint('substrate',__name__)
@substrate.route('/add_substrate',methods=['POST'])
def add_substrate():
    '''This will create a Hew Substrate'''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'POST':
        name    = request.json['name']
        adminId = request.json['adminId']
        status  = request.json['status']
        try:
            if name and adminId and status in [0,1]:
                substrate = HewSubstrate(
                    name      =   name,
                    adminId   =   adminId,
                    createdOn = datetime.datetime.now(),
                    status    = status
                )
                substrate_created = substrate.save()
                data_status["responseStatus"]=1
                data_status["result"]="Substrate created Successfully"
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@substrate.route('/substrate',methods=['GET'])
def get_substrates():
    ''''This will give a list of substrates'''
    if request.method == 'GET':
        data_status={"responseStatus":0,"result":""}
        try:
            substrates = HewSubstrate.objects()
            if substrates:
                data_status["responseStatus"]=1
                data_status["result"]="Substrates list fetched successfully"
                data_status["substrates"] = json.loads(substrates.to_json())
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Data not available"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@substrate.route('/substrate/<sid>',methods=['PUT'])
def edit_substrate(sid):
    '''This edit Hew Substrate'''
    if request.method == 'PUT':
        substrateId = sid
        data_status={"responseStatus":0,"result":""}
        try:
            name = request.json['name']
            status = request.json['status']
            if name and status in [0,1]:
                substrate = HewSubstrate.objects(id=substrateId).get()
                if substrate:
                    substrate.update(name = name, status = status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Substrate Updated Successfully"
                    return data_status
                else:
                    data_status["responseStatus"]=0
                    data_status["result"]="Substrate does not exist"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except HewSubstrate.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]= "Substrate does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@substrate.route('/substrate/<sid>',methods=['GET'])
def get_substrate(sid):
    '''This Method get Hew Substrate based on Id'''
    if request.method == 'GET':
        substrateId = sid
        data_status={"responseStatus":0,"result":""}
        try:
            substrate = HewSubstrate.objects(id=substrateId).get()
            if substrate:
                data_status["responseStatus"]=1
                data_status["result"]="success"
                data_status["substrate_info"] = json.loads(substrate.to_json())
                return data_status
        except HewSubstrate.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Substrate does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@substrate.route('/substrate/<sid>',methods=['DELETE'])
def del_substrate(sid):
    '''This Method delete HEW Substrate based on Id'''
    if request.method == 'DELETE':
        substrateId = sid
        data_status={"responseStatus":0,"result":""}
        try:
            substrate = HewSubstrate.objects(id=substrateId).get()
            if substrate:
                substrate.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Successfully deleted"
                return data_status
        except HewSubstrate.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Substrate does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status


@substrate.route('/substrate_status/<sid>',methods=['PATCH'])
def update_substrate_status(sid):
    ''' This updates status '''
    if request.method == 'PATCH':
        substrateId = sid
        data_status={"status":0,"result":""}
        status = request.json['status']
        try:
            if status in [0,1]:
                substrate = HewSubstrate.objects(id=substrateId).get()
                if substrate:
                    substrate.update(status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Status updated successfully"
                    return data_status
                else:
                    data_status["responseStatus"]=0
                    data_status["result"]="Substrate does not found"
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except HewSubstrate.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Substrate does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status  






