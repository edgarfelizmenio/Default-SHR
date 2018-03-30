from flask import Flask
from flask_restful import Api
import config

app=Flask(__name__)
api = Api(app)

import database

@app.teardown_appcontext
def shutdown_session(Exception = None):
    database.db_session.remove()

import resources

api.add_resource(resources.ClinicalRecords, '/encounters/patient/<int:patient_id>')
api.add_resource(resources.ClinicalRecord, '/encounters/<int:encounter_id>')
api.add_resource(resources.Encounters, '/encounters')
api.add_resource(resources.AddClinicalRecord, '/encounters')
api.add_resource(resources.AllEncounters, '/all')

if __name__ == '__main__':
    app.run(port=4000)