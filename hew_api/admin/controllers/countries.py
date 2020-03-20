from flask import Blueprint,request,jsonify
from ..models import HewCountries
from hew_api.config import client
import datetime
import json

countries = Blueprint('countries',__name__)
@countries.route('/country',methods=['GET'])
def get_countries():
    ''' This will give list of countries'''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'GET':
        try:
            countries = HewCountries.objects()
            if countries:
                data_status["responseStatus"]=1
                data_status["result"]="Countries list fetched successfully"
                data_status["countries"] = json.loads(countries.to_json())
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Data not available"
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["resul"]= e.args[0]
            return data_status

@countries.route('/add_country',methods=['POST'])
def add_countries():
    ''' This will add countries'''
    data_status={"responseStatus":0,"result":""}
    if request.method == 'POST':
        try:
            countryName = request.json['countryName']
            iso3        = request.json['iso3']
            iso2        = request.json['iso2']
            phoneCode   = request.json['phoneCode']
            capital     = request.json['capital']
            currency    = request.json['currency']
            status      = request.json['status']

            if countryName and iso2 and iso3 and phoneCode and capital and currency and status in [0,1]:
                last_country = HewCountries.objects.order_by('-countryId').first()
                countryId = last_country["countryId"]+1
                print(countryId)
                add_country = HewCountries(
                    countryId = countryId,
                    countryName = countryName,
                    iso2 = iso2,
                    iso3 = iso3,
                    phoneCode = phoneCode,
                    capital = capital,
                    currency = currency,
                    status = status
                )
                country = add_country.save()
                data_status["responseStatus"]=1
                data_status["result"]="Country added successfully"
                return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except Exception as e:
            data_status["responseStatus"]= 0
            data_status["result"]= e.args
            return data_status



@countries.route('/country/<cid>',methods=['GET'])
def get_country(cid):
    countryId = cid
    data_status = {"responseStatus":0,"result":""}
    if request.method == 'GET':
        '''This will get country details based on id'''
        try:
            country = HewCountries.objects(id=countryId).get()
            if country:
                data_status["responseStatus"]=1
                data_status["result"]="success"
                data_status["country_info"] = json.loads(country.to_json())
                return data_status
        except HewCountries.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Country does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

    
@countries.route('/country/<cid>',methods=['PUT'])
def edit_country(cid):
    countryId = cid
    data_status = {"responseStatus":0,"result":""}
    if request.method == 'PUT':
        ''' This method will update country details based on ID'''
        try:
            iso3        = request.json['iso3']
            iso2        = request.json['iso2']
            phoneCode   = request.json['phoneCode']
            capital     = request.json['capital']
            currency    = request.json['currency']
            status      = request.json['status']
            if iso3 and iso2 and phoneCode and capital and currency and status in [0,1]:
                country = HewCountries.objects(id=countryId).get()
                if country:
                    country.update(iso3=iso3,iso2=iso2,phoneCode=phoneCode,capital=capital,currency=currency,status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Country updated successfully"
                    return data_status
            else:
                data_status["responseStatus"]=0
                data_status["result"]="required fields missing"
                return data_status
        except HewCountries.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Country does not exist"
            return data_status
        except Exception as e:
            data_status["staresponseStatustus"]=0
            data_status["result"]=e.args[0]
            return data_status
            
@countries.route('/country/<cid>',methods=['DELETE'])
def delete_country(cid):
    countryId = cid
    data_status = {"responseStatus":0,"result":""}
    if request.method == 'DELETE':
        ''' This method will delete country'''
        try:
            country = HewCountries.objects(id=countryId).get()
            if country:
                country.delete()
                data_status["responseStatus"]=1
                data_status["result"]="Successfully deleted"
                return data_status
        except HewCountries.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Country does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status

@countries.route('/country_status/<cid>',methods=['PATCH'])
def update_country_status(cid):
    countryId = cid
    data_status = {"responseStatus":0,"result":""}
    if request.method=='PATCH':
        status = request.json['status']
        try:
            if status in [0,1]:
                country = HewCountries.objects(id=countryId).get()
                if country:
                    country.update(status=status)
                    data_status["responseStatus"]=1
                    data_status["result"]="Updated successfully"
                    return data_status    
            else:
                data_status["responseStatus"]=0
                data_status["result"]="Required fields missing"
                return data_status
        except HewCountries.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Country does not exist"
            return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status
        





