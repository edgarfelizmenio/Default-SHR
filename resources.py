from flask import request
from flask_restful import Resource

import models

class AllEncounters(Resource):

    def get(self):
        """
            Convenience method for generating test data
        """
        print('lol nigga')
        all_encounters = models.get_all_encounters()
        return all_encounters, 200

class ClinicalRecords(Resource):

    def get(self, patient_id):
        """
            Return a list of clinical records based on patient Id
        """
        encounters = models.get_encounter_ids(patient_id)
        return encounters, 200

    def post(self, patient_id):
        data = request.get_json()
        encounter_id = models.add_encounter(patient_id, data)
        if encounter_id is None:
            return {'status': 400, 'message': 'Insufficient Data'}
        return encounter_id, 201

class AddClinicalRecord(Resource):

    def post(self):
        data = request.get_json()
        encounter_id = models.create_encounter(data)
        if encounter_id is None:
            return {'status': 400, 'message': 'Insufficient Data'}
        return encounter_id, 201

class ClinicalRecord(Resource):

    def get(self, encounter_id):
        """
            Return a clinical record based on encounter
        """
        encounterObject = models.get_encounter(encounter_id)
        print(encounterObject)
        if encounterObject is None:
            return {'status': 404, 'message': 'Encounter with id={} not found.'.format(encounter_id)}
        return encounterObject, 200

class Encounters(Resource):
    def get(self):
        encounters = models.get_encounter_ids()
        return encounters, 200
    
    def delete(self):
        models.delete_all()
        return 200
