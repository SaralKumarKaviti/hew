from flask import Blueprint,request,jsonify
from ..models import HewStates
from hew_api.config import client
import datetime
import json

states = Blueprint('states',__name__)

@states.route('/state',methods=['GET'])
def get_states():
    ''' This method gives existing states'''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'GET':
        try:
            states = HewStates.objects()
            data_status["responseStatus"]=1
            data_status["result"]="Countries list fetched successfully"
            data_status["states"] = json.loads(states.to_json())
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@states.route('/add_state',methods=['POST'])
def add_state():
    '''This method add a state'''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'POST':
        try:
            name        = request.json['name']
            countryId   = request.json['countryId']
            stateCode   = request.json['stateCode']
            countryCode = request.json['countryCode']
            status      = request.json['status']

            if name and countryId and countryCode and stateCode and status in [0,1]:
                last_country = HewStates.objects.order_by('-stateId').first()
                stateId = last_country["stateId"]+1
                print(stateId)
                add_state = HewStates(
                    stateId = stateId,
                    name = name,
                    countryId = countryId,
                    stateCode = stateCode,
                    countryCode = countryCode,
                    status = status
                )
                state = add_state.save()
                data_status["responseStatus"]=1
                data_status["result"]="State added successfully"
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except Exception as e:
            data_status["responseStatus"]= 0
            data_status["result"]= e.args
            return data_status

@states.route('/state/<sid>',methods=['GET'])
def get_one_state(sid):
    stateId = sid
    data_status = {"responseStatus":0,"result":""}
    if request.method == 'GET':
        '''This will get country details based on id'''
        try:
            state = HewStates.objects(id=stateId).get()
            if state:
                data_status["responseStatus"]=1
                data_status["result"]="success"
                data_status["state_info"] = json.loads(state.to_json())
                return data_status
        except HewStates.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="State does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@states.route('/state/<sid>',methods=['PUT'])
def edit_state(sid):
    stateId = sid
    data_status = {"responseStatus":0,"result":""}
    if request.method == 'PUT':
        ''' This method will update state details based on ID'''
        try:
            countryId   = request.json['countryId']
            stateCode   = request.json['stateCode']
            countryCode = request.json['countryCode']
            status      = request.json['status']
            if countryId and stateCode and countryCode and status in [0,1]:
                state = HewStates.objects(id=stateId).get()
                if state:
                    state.update(countryId=countryId,stateCode=stateCode,countryCode=countryCode,status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="State updated successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except HewStates.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="State does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@states.route('/state/<sid>',methods=['DELETE'])
def del_state(sid):
    stateId=sid
    data_status = {"responseStatus":0,"result":""}
    if request.method == 'DELETE':
        ''' This method will delete country'''
        try:
            state = HewStates.objects(id=stateId).get()
            if state:
                state.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Successfully deleted"
                return data_status
        except HewStates.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Country does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@states.route('/state_status/<sid>',methods=['PATCH'])
def update_status(sid):
    stateId = sid
    data_status = {"responseStatus":0,"result":""}
    if request.method=='PATCH':
        status = request.json['status']
        try:
            if status in [0,1]:
                state = HewStates.objects(id=stateId).get()
                if state:
                    state.update(status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Updated successfully"
                    return data_status    
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except HewStates.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Country does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

    