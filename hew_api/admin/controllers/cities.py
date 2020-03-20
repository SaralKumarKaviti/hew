from flask import Blueprint,request,jsonify
from ..models import HewCities
from hew_api.config import client
import datetime
import json

cities = Blueprint('cities',__name__)
@cities.route('/cities',methods=['GET'])
def get_cities():
    ''' This method get cities details'''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'GET':
        try:
            cities = HewCities.objects()
            if cities:
                data_status["responseStatus"]=1
                data_status["result"]="Cities list fetched successfully"
                data_status["cities"] = json.loads(cities.to_json())
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Data not available"
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["resul"]= e.args[0]
            return data_status

@cities.route('/add_cities',methods=['POST'])
def add_city():
    '''This method adds city to database'''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'POST':
        try:
            name        = request.json['name']
            countryId   = request.json['countryId']
            stateId     = request.json['stateId']
            stateCode   = request.json['stateCode']
            countryCode = request.json['countryCode']
            latitude    = request.json['latitude']
            longitude   = request.json['longitude']
            status      = request.json['status']
            
            if name and countryId and stateId and countryCode and stateCode and latitude and longitude and status in [0,1]:
                last_city = HewCities.objects.order_by('-cityId').first()
                cityId = last_city["cityId"]+1
                print(cityId)
                add_city = HewCities(
                    cityId = cityId,
                    stateId = stateId,
                    name = name,
                    countryId = countryId,
                    stateCode = stateCode,
                    countryCode = countryCode,
                    latitude = latitude,
                    longitude = longitude,
                    status = status
                )
                city = add_city.save()
                data_status["responseStatus"]=1
                data_status["result"]="City added successfully"
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except Exception as e:
            data_status["responseStatus"]= 0
            data_status["result"]= e.args
            return data_status

@cities.route('/cities/<cid>',methods=['GET'])
def get_city(cid):
    cityId = cid
    data_status = {"responseStatus":0,"result":""}
    if request.method == 'GET':
        '''This will get country details based on id'''
        try:
            city = HewCities.objects(id=cityId).get()
            if city:
                data_status["responseStatus"]=1
                data_status["result"]="success"
                data_status["country_info"] = json.loads(city.to_json())
                return data_status
        except HewCities.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="City does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@cities.route('/cities/<cid>',methods=['PUT'])
def edit_city(cid):
    cityId = cid
    data_status = {"responseStatus":0,"result":""}
    if request.method == 'PUT':
        ''' This method will update country details based on ID'''
        try:
            countryId   = request.json['countryId']
            stateId     = request.json['stateId']
            stateCode   = request.json['stateCode']
            countryCode = request.json['countryCode']
            latitude    = request.json['latitude']
            longitude   = request.json['longitude']
            status      = request.json['status']
            if countryId and stateId and countryCode and stateCode and latitude and longitude and status in [0,1]:
                city = HewCities.objects(id=cityId).get()
                if city:
                    city.update(countryId=countryId,stateId=stateId,countryCode=countryCode,stateCode=stateCode,latitude=latitude,longitude=longitude,status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="City updated successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except HewCities.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="City does not exist"
            return data_status
        except Exception as e:
            data_status["staresponseStatustus"]=0
            data_status["result"]=e.args[0]
            return data_status

@cities.route('/cities/<cid>',methods=['DELETE'])
def del_city(cid):
    cityId=cid
    data_status = {"responseStatus":0,"result":""}
    if request.method == 'DELETE':
        ''' This method will delete country'''
        try:
            city = HewCities.objects(id=cityId).get()
            if city:
                city.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Successfully deleted"
                return data_status
        except HewCities.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="City does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@cities.route('/cities_status/<cid>',methods=['PATCH'])
def update_status(cid):
    cityId = cid
    data_status = {"responseStatus":0,"result":""}
    if request.method=='PATCH':
        status = request.json['status']
        try:
            if status in [0,1]:
                city = HewCities.objects(id=cityId).get()
                if city:
                    city.update(status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Updated successfully"
                    return data_status    
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except HewCities.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="City does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status
        