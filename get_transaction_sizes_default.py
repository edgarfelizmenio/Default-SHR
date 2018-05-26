import mysql.connector

querystring = """
	SELECT (encounter.size + obs.size + encounter_provider.size) as transaction_size FROM
	(SELECT encounter_id, (
	LENGTH(encounter_id) +
	LENGTH(encounter_type) +
	LENGTH(patient_id) +
	LENGTH(location_id) +
	LENGTH(encounter_datetime) +
	LENGTH(creator) +
	LENGTH(date_created)
	) AS size FROM Encounter) as encounter JOIN
	(SELECT encounter_id, SUM(
		LENGTH(obs_id) +
		LENGTH(person_id) +
		LENGTH(concept_id) +
		LENGTH(encounter_id) +
		LENGTH(obs_datetime) +
		LENGTH(location_id) +
		IFNULL(LENGTH(value_boolean), 0) +
		IFNULL(LENGTH(value_coded), 0) +
		IFNULL(LENGTH(value_coded_name_id), 0) +
		IFNULL(LENGTH(value_datetime), 0) +
		IFNULL(LENGTH(value_numeric), 0) +
		IFNULL(LENGTH(comments), 0) +
		LENGTH(creator) +
		LENGTH(date_created)
		) AS size FROM Observation
		GROUP BY encounter_id) as obs ON encounter.encounter_id = obs.encounter_id JOIN
	(SELECT encounter_id, SUM(
		LENGTH(encounter_provider_id) +
		LENGTH(encounter_id) + 
		LENGTH(provider_id) +
		LENGTH(encounter_role_id) +
		LENGTH(creator) +
		LENGTH(date_created)				
		) AS size FROM EncounterProvider
		GROUP BY encounter_id) as encounter_provider ON encounter.encounter_id = encounter_provider.encounter_id;
"""



try:
	connection = mysql.connector.connect(host='localhost',
		port=3307,
		database='raw_shr',
		user='root',
		password='password')
	if connection.is_connected():
		print('Connected to MySQL database')

	cursor = connection.cursor()
	cursor.execute(querystring)
	rows = cursor.fetchall()

	transaction_sizes = [int(txn[0]) for txn in rows]

	with open('transaction_sizes_default.txt', "w") as txn_sizes_file:
		txn_sizes_file.writelines(["{}\n".format(txn_size) for txn_size in transaction_sizes])

except Error as e:
	print(e)

finally:
	connection.close()
	print('Connection closed.')
