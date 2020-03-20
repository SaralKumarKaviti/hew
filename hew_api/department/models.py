from mongoengine import *

class HewCustomers(Document):
    customerName = StringField(max_length=50)
    customerId = StringField(max_length=14)
    userId = ReferenceField('HewDepartmentUsers')
    customerEmail = EmailField(required=True)
    password = StringField()
    createdOn = DateTimeField()
    status = IntField()

class HewProcess(Document):
	processName = StringField(max_length=50)
	processId = StringField(max_length=20, required=True, unique=True)
	userId = ReferenceField('HewDepartmentUsers', required=True)
	createdOn = DateTimeField()
	status = IntField(default=0, required=True)

class HewSubProcess(Document):
	subProcessName = StringField(max_length=50)
	userId = ReferenceField('HewDepartmentUsers', required=True)
	subprocessId = StringField(max_length=20, required=True, unique=True)
	processId = ReferenceField('HewProcess', required=True)
	createdOn = DateTimeField()
	status = IntField(default=0, required=True)
class HewAttributes(Document):
	attributeName=StringField(max_length=50,required=True)
	values=ListField()
	userId=ReferenceField('HewDepartmentUsers',required=True)
	attributeId=StringField(max_length=20, required=True, unique=True)
	createdOn = DateTimeField()
	status = IntField(default=0, required=True)


