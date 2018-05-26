import mysql.connector

delete_observation = """
    DELETE FROM Observation
"""

delete_encounter_provider = """
    DELETE FROM EncounterProvider
"""

delete_encounter = """
    DELETE FROM Encounter
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
    cursor.execute(delete_observation)
    connection.commit()
    cursor.execute(delete_encounter_provider)
    connection.commit()
    cursor.execute(delete_encounter)
    connection.commit()

except Error as e:
    print(e)

finally:
    connection.close()
    print('Connection closed.')
