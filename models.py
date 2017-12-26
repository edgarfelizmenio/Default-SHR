from database import Base, db_session

Encounter = Base.classes.Encounter
EncounterProvider = Base.classes.EncounterProvider
EncounterRole = Base.classes.EncounterRole
EncounterType = Base.classes.EncounterType
Observation = Base.classes.Observation

def create_encounter(data):
    return None

def get_encounter_ids(patient_id = None):
    if patient_id is not None:
        result = db_session.query(Encounter).filter(
            Encounter.patient_id == patient_id).all()
    else:
        result = db_session.query(Encounter).all()
    return [e.encounter_id for e in result]

def get_encounter(encounter_id):
    result = db_session.query(Encounter, EncounterType).join(
        EncounterType
    ).filter(Encounter.encounter_id == encounter_id).first()
    if result is None:
        return None
    encounter, encounter_type = result
    encounterObject = {
        'encounter_id': encounter.encounter_id,
        'patient_id': encounter.patient_id,
        'location_id': encounter.location_id,
        'encounter_datetime': str(encounter.encounter_datetime),
        'encounter_type_name': encounter_type.name,
        'encounter_type_description': encounter_type.description
    }
    # mamaya na yung encounter providers
    providers = []
    provider_result = db_session.query(EncounterProvider, EncounterRole).join(
        EncounterRole).filter(
            EncounterProvider.encounter_id == encounterObject['encounter_id']).all()
    for encounter_provider, encounter_role in provider_result:
        providers.append({
            'provider_id': encounter_provider.provider_id,
            'role': encounter_role.name,
            'role_description': encounter_role.description
        })
    encounterObject['providers'] = providers

    # mamaya na yung observations
    observations = []
    observation_result = db_session.query(Observation).filter(
        Observation.encounter_id == encounterObject['encounter_id']).all()
    for observation in observation_result:
        observationObject = {
            'obs_id': observation.obs_id,
            'person_id': observation.person_id,
            'concept_id': observation.concept_id,
            'obs_datetime': str(observation.obs_datetime),
            'location_id': observation.location_id,
            'comments': observation.comments,
            'value_boolean': observation.value_boolean,
            'value_coded': observation.value_coded,
            'value_coded_name_id': observation.value_coded_name_id,
            'value_datetime': str(observation.value_datetime) if observation.value_datetime else None,
            'value_numeric': float(observation.value_numeric) if observation.value_numeric else None
        }
        if observation.value_boolean:
            observationObject['value'] = observation.value_boolean
        if observation.value_coded:
            observationObject['value'] = observation.value_coded
        if observation.value_coded_name_id:
            observationObject['value'] = observation.value_coded_name_id
        if observation.value_datetime:
            observationObject['value'] = str(observation.value_datetime)
        if observation.value_numeric:
            observationObject['value'] = float(observation.value_numeric)
        observations.append(observationObject)
    encounterObject['observations'] = observations
    return encounterObject

def add_encounter(data):
    encounter = Encounter(
        encounter_type = data['encounter_type'],
        patient_id = data['patient_id'],
        location_id = data['location_id'],
        encounter_datetime = data['encounter_datetime'],
        creator = 0,
        date_created = None
    )
    db_session.add(encounter)
    # iterate over encounter providers
    for provider in data.get('providers', []):
        encounter_provider = EncounterProvider(
            encounter=encounter,
            provider_id = provider['provider_id'],
            encounter_role_id = provider['encounter_role_id'],
            creator = 0,
            date_created = None
        )
        db_session.add(encounter_provider)
    for obs in data.get('observations', []):
        observation = Observation(
            person_id = obs['person_id'],
            concept_id = obs['concept_id'],
            encounter = encounter,
            obs_datetime = obs['obs_datetime'],
            location_id = location_id,
            comments = obs['comments'],
            creator = 0,
            date_created = None
        )
        if 'value_boolean' in obs:
            observation.value_boolean = obs['value_boolean']
        if 'value_coded' in obs:
            observation.value_coded = obs['value_coded']
        if 'value_coded_name_id' in obs:
            observation.value_coded_name_id = obs['value_coded_name_id']
        if 'value_datetime' in obs:
            observation.value_datetime = obs['value_datetime']
        if 'value_numeric' in obs:
            observation.value_numeric = obs['value_numeric']
        db_session.add(observation)
    return encounter.encounter_id

    # iterate over observations
    db_session.commit()