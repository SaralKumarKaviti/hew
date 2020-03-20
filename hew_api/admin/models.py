from mongoengine import *

class HewAdmin(Document):
    displayName = StringField(max_length=100)
    userName = StringField(max_length=50,unique=True)
    email = StringField(max_length=50,unique=True, required=True)
    password = StringField(max_length=150)
    permissionId = IntField()
    createdOn = DateTimeField()
    status = IntField(default=0, required=True)
    lastLogin = DateTimeField()
    lastLogout = DateTimeField()
    verification = StringField(max_length=50)
    image = StringField()

class HewRoles(Document):
    roleName = StringField(max_length=50,unique=True)
    adminId=ReferenceField('HewAdmin', required=True)
    rolePermissions = ListField()
    createdOn = DateTimeField()
    status = IntField(default=0, required=True)

class HewDepartmentUsers(Document):
    displayName = StringField(max_length=100)
    userName = StringField(max_length=50,unique=True)
    email = StringField(max_length=50, unique=True)
    phoneNumber = StringField()
    password = StringField(max_length=150)
    roleId = ReferenceField('HewRoles', required=True)
    createdOn = DateTimeField()
    status = IntField(default=0, required=True)
    lastLogin = DateTimeField()
    lastLogout = DateTimeField()
    verification = StringField(max_length=50)

class HewRoleTypes(Document):
    roletype=StringField(max_length=50)
    adminId=ReferenceField('HewAdmin', required=True)

class HewDesignation(Document):
    name = StringField(max_length=50, unique=True)
    adminId = ReferenceField('HewAdmin', required=True)
    createdOn = DateTimeField()
    status = IntField(default=0, required=True)

class HewDepartment(Document):
    name=StringField(max_length=50)
    adminId = ReferenceField('HewAdmin', required=True)
    createdOn = DateTimeField()
    status = IntField(default=0, required=True)

class HewCompanyPreference(Document):
    name=StringField(max_length=50,unique=True)
    adminId=ReferenceField('HewAdmin', required=True)
    createdOn=DateTimeField()

# Change this status to int
class HewCountries(Document):
    countryId = IntField()
    countryName = StringField(max_length=50)
    iso3 = StringField(max_length=10)
    iso2 = StringField(max_length=10)
    phoneCode = StringField(max_length=10)
    capital = StringField(max_length=10)
    currency = StringField(max_length=10)
    status = IntField(required=True)

class HewStates(Document):
    stateId = IntField()
    name = StringField(max_length=50)
    countryId = IntField()
    countryCode = StringField(max_length=10)
    stateCode = StringField(max_length=10)
    status = IntField()

class HewCities(Document):
    cityId = IntField()
    name = StringField(max_length=50)
    latitude = StringField(max_length=11)
    longitude = StringField(max_length=11)
    stateId = IntField()
    countryId = IntField()
    countryCode = StringField(max_length=10)
    stateCode = StringField(max_length=10)
    status = IntField()  

class HewSubstrate(Document):
    name = StringField(max_length=50)
    adminId = ReferenceField('HewAdmin')
    createdOn = DateTimeField()
    status = IntField(required=True)

class HewMeasurement(Document):
    name = StringField(max_length=50)
    adminId = ReferenceField('HewAdmin')
    createdOn = DateTimeField()
    status = IntField(required=True)

class HewUom(Document):
    name = StringField(max_length=50)
    adminId = ReferenceField('HewAdmin')
    createdOn = DateTimeField()
    status = IntField(required=True)

class HewRiskFactor(Document):
    name = StringField(max_length=50)
    adminId = ReferenceField('HewAdmin')
    createdOn = DateTimeField()
    status = IntField(required=True)

class HewOtherFields(Document):
    name = StringField(max_length=50)
    adminId = ReferenceField('HewAdmin')
    createdOn = DateTimeField()
    status = IntField(required=True)
