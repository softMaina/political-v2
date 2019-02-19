from app.api.v2 import database 

OFFICES = []

class Office():
    def __init__(self):
        self.office = OFFICES
    
    def save(self, office_name, office_type):

        office = {
            "name": office_name,
            "office_type": office_type
        }

        query =  """INSERT INTO offices(name, office_type)
        VALUES('{}', '{}')""".format(office_name, office_type)
        database.insert_to_db(query)
        return office