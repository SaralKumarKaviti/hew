from flask import Blueprint,request,jsonify
from hew_api.admin.models import HewDepartmentUsers, HewRoles, HewCompanyPreference
from hew_api.department.models import HewProcess, HewSubProcess
from hew_api.config import client
import datetime
import json


sub_processes = Blueprint('sub_processes', __name__)

@sub_processes.route('/sub_processes', methods=['GET'])
def add_subproces():
	return "Saral"