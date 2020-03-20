from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from hew_api.admin.controllers.admin import admin
from hew_api.admin.controllers.countries import countries
from hew_api.admin.controllers.states import states
from hew_api.admin.controllers.cities import cities
from hew_api.admin.controllers.substrate import substrate
from hew_api.admin.controllers.measurements import measurements
from hew_api.admin.controllers.uom import uom
from hew_api.admin.controllers.risk_factor import risk_factor
from hew_api.admin.controllers.other_fields import other_fields
from hew_api.admin.controllers.user import user
from hew_api.admin.controllers.role import role
from hew_api.admin.controllers.role_type import role_type
from hew_api.admin.controllers.company_preference import company_preference
from hew_api.admin.controllers.department import department
from hew_api.admin.controllers.designation import designation





app.register_blueprint(admin,url_prefix='/api/admin')
app.register_blueprint(countries,url_prefix='/api/admin')
app.register_blueprint(states,url_prefix='/api/admin')
app.register_blueprint(cities,url_prefix='/api/admin')
app.register_blueprint(substrate,url_prefix='/api/admin')
app.register_blueprint(measurements,url_prefix='/api/admin')
app.register_blueprint(uom,url_prefix='/api/admin')
app.register_blueprint(risk_factor,url_prefix='/api/admin')
app.register_blueprint(other_fields,url_prefix='/api/admin')
app.register_blueprint(user,url_prefix='/api/admin')
app.register_blueprint(role,url_prefix='/api/admin')
app.register_blueprint(role_type,url_prefix='/api/admin')
app.register_blueprint(company_preference,url_prefix='/api/admin')
app.register_blueprint(department,url_prefix='/api/admin')
app.register_blueprint(designation,url_prefix='/api/admin')


from hew_api.department.controllers.attribute import attribute
from hew_api.department.controllers.customers import customers

app.register_blueprint(attribute,url_prefix='/api/department')
app.register_blueprint(customers,url_prefix='/api/department')
