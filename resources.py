from flask import request
from flask_restful import Resource

import models

class ClinicalRecords(Resource):

    def get(self, patient_id):
        """
            Return a list of clinical records based on patient Id
        """
        encounters = models.get_encounter_ids(patient_id)
        return encounters, 200

    def post(self, patient_id):
        """
            Create new encounter for a patient
        """
        pass


class AddClinicalRecord(Resource):

    def post(self):
        data = request.form
        encounter_id = models.create_encounter(data)
        if encounter_id is None:
            return {'status': 400, 'message': 'Insufficient Data'}
        return patient_id, 201

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