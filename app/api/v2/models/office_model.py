from app.api.v2 import database 

OFFICES = []

class Office():
    def __init__(self):
        self.office = OFFICES
    
    def save(self, office_name, office_type):
        """add a new office"""
        office = {
            "name": office_name,
            "office_type": office_type
        }

        query =  """INSERT INTO offices(name, office_type)
        VALUES('{}', '{}')""".format(office_name, office_type)
        database.insert_to_db(query)
        return office
    
    def fetch_all_offices(self):
        """Fetches all offices from

        the database
        """
        query = """SELECT * FROM offices"""
        return database.select_from_db(query)
    def update(self, office_id, office_name, office_type):

        query = """UPDATE offices SET name = '{}',office_type = '{}' WHERE office_id = '{}' """.format(office_name,office_type,office_id)

        database.insert_to_db(query)
    def delete(self, office_id):
        query = """DELETE FROM offices WHERE office_id = '{}' """.format(office_id)
        database.insert_to_db(query)