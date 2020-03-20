from flask import Blueprint,request,jsonify
from hew_api.admin.models import HewCompanyPreference,HewAdmin
from hew_api.config import connect
import datetime

company_preference=Blueprint('company_preference',__name__)

@company_preference.route('/company_preference',methods=['POST'])
def create_company_preference():
    name=request.json['name']
    adminId=request.json['adminId']
    createdOn=datetime.datetime.now()
    data_status={"responseStatus":0,"result":""}

    if name and adminId and createdOn and request.method=='POST':
        try:
            queryset=HewAdmin.objects.get(pk=adminId)
            if queryset:
                company=HewCompanyPreference(
                    name=name,
                    adminId=adminId,
                    createdOn=createdOn

                )
                company_created=company.save()
                if company_created:
                    data_status["responseStatus"]=1
                    data_status["result"]="Successfully Company Preference Created"
                    return data_status
        
        except HewAdmin.DoesNotExist as e:
            data_status["responseStatus"]=0
            data_status["result"]="Admin id doesnot exist"
            return data_status
    
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields missing"


@company_preference.route('/company_preference/<cp_id>',methods=['PUT'])
def edit_company_preference(cp_id):
    name=request.json['name']
    data_status={"responseStatus":0,"result":""}

    if name and request.method=='PUT':
        try:
            queryset=HewCompanyPreference.objects(pk=cp_id).get()
            if queryset:
                queryset.name=name
                edited_company=queryset.save()

                data_status["status"]=1
                data_status["result"]="Company Preference Updated Successfully"
                return data_status

        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields are missing"
        return data_status





