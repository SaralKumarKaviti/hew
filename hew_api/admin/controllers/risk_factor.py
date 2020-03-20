from flask import Blueprint,request,jsonify
from hew_api.admin.models import HewRiskFactor
from hew_api.config import client
import datetime
import json

risk_factor = Blueprint('risk_factor',__name__)
@risk_factor.route('/add_risk_factor',methods=['POST'])
def add_risk_factor():
    '''This will create a Hew Risk Factor '''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'POST':
        name    = request.json['name']
        adminId = request.json['adminId']
        status  = request.json['status']
        try:
            if name and adminId and status in [0,1]:
                risk = HewRiskFactor(
                    name      =   name,
                    adminId   =   adminId,
                    createdOn = datetime.datetime.now(),
                    status    = status
                )
                risk_created = risk.save()
                data_status["responseStatus"]=1
                data_status["result"]="Measurement created Successfully"
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@risk_factor.route('/risk_factor',methods=['GET'])
def get_all_risk_factors():
    ''''This will give a list of risk factors'''
    if request.method == 'GET':
        data_status={"responseStatus":0,"result":""}
        try:
            risks = HewRiskFactor.objects()
            if risks:
                data_status["responseStatus"]=1
                data_status["result"]="Measurements list fetched successfully"
                data_status["measurements"] = json.loads(risks.to_json())
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Data not available"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@risk_factor.route('/risk_factor/<rid>',methods=['PUT'])
def edit_risk_factor(rid):
    '''This edit Hew Risk Factor'''
    if request.method == 'PUT':
        riskId = rid
        data_status={"responseStatus":0,"result":""}
        try:
            name = request.json['name']
            status = request.json['status']
            if name and status in [0,1]:
                risk = HewRiskFactor.objects(id=riskId).get()
                if risk:
                    risk.update(name = name, status = status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Risk Factor Updated Successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except HewRiskFactor.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]= "Risk Factor does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@risk_factor.route('/risk_factor/<rid>',methods=['GET'])
def get_risk_factor(rid):
    '''This Method get Hew Risk Factor based on Id'''
    if request.method == 'GET':
        riskId = rid
        data_status={"responseStatus":0,"result":""}
        try:
            risk = HewRiskFactor.objects(id=riskId).get()
            if risk:
                data_status["responseStatus"]=1
                data_status["result"]="success"
                data_status["measurement_info"] = json.loads(risk.to_json())
                return data_status
        except HewRiskFactor.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Risk Factor does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@risk_factor.route('/risk_factor/<rid>',methods=['DELETE'])
def del_risk_factor(rid):
    '''This Method delete Hew Risk Factor based on Id'''
    if request.method == 'DELETE':
        riskId = rid
        data_status={"responseStatus":0,"result":""}
        try:
            risk = HewRiskFactor.objects(id=riskId).get()
            if risk:
                risk.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Successfully deleted"
                return data_status
        except HewRiskFactor.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Risk Factor does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@risk_factor.route('/risk_factor_status/<rid>',methods=['PATCH'])
def update_risk_factor_status(rid):
    ''' This updates status '''
    if request.method == 'PATCH':
        riskId = rid
        data_status={"responseStatus":0,"result":""}
        status = request.json['status']
        try:
            if status in [0,1]:
                risk = HewRiskFactor.objects(id=riskId).get()
                if risk:
                    risk.update(status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Status updated successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except HewRiskFactor.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Risk Factor does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status