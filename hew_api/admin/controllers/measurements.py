from flask import Blueprint,request,jsonify
from ..models import HewMeasurement
from hew_api.config import client
import datetime
import json

measurements = Blueprint('measurement',__name__)
@measurements.route('/add_measurement',methods=['POST'])
def add_measurement():
    '''This will create a Hew Measurement '''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'POST':
        name    = request.json['name']
        adminId = request.json['adminId']
        status  = request.json['status']
        try:
            if name and adminId and status in [0,1]:
                measure = HewMeasurement(
                    name      =   name,
                    adminId   =   adminId,
                    createdOn = datetime.datetime.now(),
                    status    = status
                )
                measurement_created = measure.save()
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

@measurements.route('/measurement',methods=['GET'])
def get_all_measurements():
    ''''This will give a list of measurements'''
    if request.method == 'GET':
        data_status={"responseStatus":0,"result":""}
        try:
            measurements = HewMeasurement.objects()
            if measurements:
                data_status["responseStatus"]=1
                data_status["result"]="Measurements list fetched successfully"
                data_status["measurements"] = json.loads(measurements.to_json())
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Data not available"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@measurements.route('/measurement/<mid>',methods=['PUT'])
def edit_measurement(mid):
    '''This edit Hew Measurement'''
    if request.method == 'PUT':
        measurementId = mid
        data_status={"responseStatus":0,"result":""}
        try:
            name = request.json['name']
            status = request.json['status']
            if name and status in [0,1]:
                measurement = HewMeasurement.objects(id=measurementId).get()
                if measurement:
                    measurement.update(name = name, status = status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Measurement Updated Successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except HewMeasurement.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]= "Measurement does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]= e.args[0]
            return data_status

@measurements.route('/measurement/<mid>',methods=['GET'])
def get_measurement(mid):
    '''This Method get Hew Measurement based on Id'''
    if request.method == 'GET':
        measurementId = mid
        data_status={"responseStatus":0,"result":""}
        try:
            measurement = HewMeasurement.objects(id=measurementId).get()
            if measurement:
                data_status["responseStatus"]=1
                data_status["result"]="success"
                data_status["measurement_info"] = json.loads(measurement.to_json())
                return data_status
        except HewMeasurement.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Measurement does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@measurements.route('/measurement/<mid>',methods=['DELETE'])
def del_measurement(mid):
    '''This Method delete Hew Measurement based on Id'''
    if request.method == 'DELETE':
        measurementId = mid
        data_status={"responseStatus":0,"result":""}
        try:
            measurement = HewMeasurement.objects(id=measurementId).get()
            if measurement:
                measurement.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Successfully deleted"
                return data_status
        except HewMeasurement.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Measurement does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@measurements.route('/measurement_status/<mid>',methods=['PATCH'])
def update_measurement_status(mid):
    ''' This updates status '''
    if request.method == 'PATCH':
        measurementId = mid
        data_status={"responseStatus":0,"result":""}
        status = request.json['status']
        try:
            if status in [0,1]:
                measurement = HewMeasurement.objects(id=measurementId).get()
                if measurement:
                    measurement.update(status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Status updated successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except HewMeasurement.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Measurement does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status