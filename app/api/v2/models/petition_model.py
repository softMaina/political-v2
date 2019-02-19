from app.api.v2 import database 

PETITIONS = []

class Petition():
    def __init__(self):
        self.petition = PETITIONS
    
    def save(self, createdOn, createdBy, office, body):
        query =  """INSERT INTO petitions(createdOn, createdBy, office, body)
        VALUES('{}', '{}','{}','{}')""".format(createdOn,createdBy,office,body)
        database.insert_to_db(query)
    
    def update(self, petition_id, createdOn, createdBy, office, body):

        query = """UPDATE offices SET createdOn = '{}',createdBy = '{}', office = '{}', body = '{}' WHERE petition_id = '{}' """.format(createdOn,createdBy,office,body, petition_id)

        database.insert_to_db(query)


    def fetch_all_petitions(self):
        """Fetches all offices from

        the database
        """
        query = """SELECT * FROM petitions"""
        return database.select_from_db(query)

    def delete(self, petition_id):
        query = """DELETE FROM offices WHERE petition_id = '{}' """.format(petition_id)
        database.insert_to_db(query)