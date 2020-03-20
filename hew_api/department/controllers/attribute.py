from flask import Blueprint,request,jsonify
from hew_api.department.models import HewAttributes
from hew_api.admin.models import HewDepartmentUsers
from hew_api.config import connect
import datetime,json

attribute=Blueprint('attribute',__name__)

@attribute.route('/final_attr',methods=['GET'])
def final_cp():
    queryset=HewAttributes.objects.order_by('-id').first()
    if queryset:
        attribute_id=queryset.attributeId
        num=int(attribute_id[-6:])+1
        if len(str(num))==1:
            attributeId='ATTR'+'00000'+str(num)
            # return processId
        elif len(str(num))==2:
            attributeId='ATTR'+'0000'+str(num)
            # return processId
        elif len(str(num))==3:
            attributeId='ATTR'+'000'+str(num)
            # return processId
        elif len(str(num))==4:
            attributeId='ATTR'+'00'+str(num)
            # return processId
        elif len(str(num))==5:
            attributeId='ATTR'+'0'+str(num)
            # return processId
        else:
            attributeId='ATTR'+str(num)
            return attributeId
        return attributeId
    else:
        attributeId='ATTR'+'000001'
        return attributeId

@attribute.route('/get_aid',methods=['GET'])
def generate_cp():
    data_status={"responseStatus":0,"result":""}
    queryset=HewAttributes.objects.order_by('-id').first()
    if queryset:
        attribute_id=queryset.attributeId
        num=int(attribute_id[-6:])+1
        if len(str(num))==1:
            attributeId='ATTR'+'00000'+str(num)
        elif len(str(num))==2:
            attributeId='ATTR'+'0000'+str(num)
        elif len(str(num))==3:
            attributeId='ATTR'+'000'+str(num)
        elif len(str(num))==4:
            attributeId='ATTR'+'00'+str(num)
        elif len(str(num))==5:
            attributeId='ATTR'+'0'+str(num)
        else:
            attributeId='ATTR'+str(num)
            data_status["responseStatus"] = 1
            data_status["result"] = attributeId
            return data_status

        data_status["responseStatus"] = 1
        data_status["result"] = attributeId
        return data_status
    else:
        attributeId='ATTR'+'000001'
        data_status["responseStatus"]=1
        data_status["result"]=attributeId
        return data_status


@attribute.route('/attribute',methods=['POST'])
def add_attribute():
    data_status={"responseStatus":0,"result":""}
    attributeName=request.json['attributeName']
    values=request.json['values']
    userId=request.json['userId']
    #attributeId=request.json['attributeId']
    createdOn=datetime.datetime.now()
    status=request.json['status']
    try:

        if attributeName and values and userId and createdOn and status in [0,1] and request.method=='POST':
            queryset=HewDepartmentUsers.objects.get(pk=userId)
            if queryset:
                attributeId=final_cp()
                if attributeId != None:
                    attribute=HewAttributes(
                        attributeName=attributeName,
                        values=values,
                        userId=userId,
                        attributeId=attributeId,
                        createdOn=createdOn,
                        status=status
                    )
                    attribute_created=attribute.save()
                    if attribute_created:
                        data_status["status"]=1
                        data_status["result"]="Successfully Attribute Created"
                        return data_status
                    else:
                        data_status["responseStatus"] = 0
                        data_status["result"] = "Company Preference not exist!"
                        return data_status
        else:
            data_status["responseStatus"]=0
            data_status["result"]="Required fields missing"
            return data_status
    except HewDepartmentUsers.DoesNotExist as e:
        data_status["responseStatus"] = 0
        data_status["result"] = "Department User id doesnot exist! " + type(e).__name__
        return data_status

@attribute.route('/attribute/<aid>',methods=['PUT'])
def edit_attribute(aid):
    #name=request.json['name']
    values=request.json['values']
    #userId=request.json['userId']
    #attributeId=request.json['attributeId']
    status=request.json['status']
    data_status={"responseStatus":0,"result":""}

    if values and status in [0,1] and request.method=='PUT':
        try:
            attribute=HewAttributes.objects(pk=aid).get()
            if attribute:
                #attribute.name=name
                attribute.values=values
                #attribute.userId=userId
                #attribute.attributeId=attributeId
                attribute.status=status

                updated_data=attribute.save()

                data_status["responseStatus"]=1
                data_status["result"]="Attribute Updated Successfully"
                return data_status
        except Exception as e:
            data_status["responseStatus"]=0
            data_status["result"]=e.args[0]
            return data_status
    else:
        data_status["responseStatus"]=0
        data_status["result"]="Required fields are missing"
        return data_status

@attribute.route('/attribute', methods=['GET'])
def show_attribute():
	data_status = {"responseStatus": 0, "result": ""}
	if request.method == 'GET':
		try:
			queryset = HewAttributes.objects.all()
			if queryset != None:
				data_status["responseStatus"] = 1
				data_status["result"] = json.loads((queryset.to_json()))
				return data_status

		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "No records available"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "No records available"
		return data_status

@attribute.route('/attribute/<aid>', methods=['GET'])
def show_single_attribute(aid):
	data_status = {"responseStatus": 0, "result": ""}
	if request.method == 'GET':
		try:
			queryset = HewAttributes.objects(pk=aid).get()
			if queryset != None:
				data_status["responseStatus"] = 1
				data_status["result"] = json.loads((queryset.to_json()))
				return data_status

		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "No records available"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "No records available"
		return data_status

@attribute.route('/attribute/<aid>', methods=['DELETE'])
def delete_attribute(aid):
	data_status = {"responseStatus": 0, "result": ""}
	if aid and request.method == 'DELETE':
		try:
			queryset = HewAttributes.objects.get(pk=aid)
			if queryset != None:
				queryset.delete()
				data_status["responseStatus"] = 1
				data_status["result"] = "Successfully deleted!"
				return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid Id"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status

@attribute.route('/attribute/<aid>', methods=['PATCH'])
def update_status(aid):
	data_status = {"responseStatus": 0, "result": ""}
	status = request.json['status']

	if aid and (status in [0,1]) and request.method == 'PATCH':
		try:
			queryset =HewAttributes.objects.get(pk=aid)
			if queryset != None:
				queryset.status = status
				queryset.save()
				data_status["responseStatus"] = 1
				data_status["result"] = "Successfully updated!"
				return data_status
		except Exception as e:
			data_status["responseStatus"] = 0
			data_status["result"] = "Invalid Id!"
			return data_status
	else:
		data_status["responseStatus"] = 0
		data_status["result"] = "Required fields are missing!"
		return data_status




            

