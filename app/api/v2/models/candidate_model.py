from app.api.v2 import database 

CANDIDATES = []
class Candidate():
    def __init__(self):
        self.candidate = CANDIDATES

    def save(self, office, party, candidate):
       

        query =  """INSERT INTO candidates(office, party, candidate)
        VALUES('{}','{}','{}')""".format(office, party, candidate)
        database.insert_to_db(query)
    
    def update(self, candidate_id, office, party, candidate):

        query = """UPDATE candidates SET office = '{}',party = '{}', candidate = '{}' WHERE candidate_id = '{}' """.format(office,party,candidate,candidate_id)
        database.insert_to_db(query)


    def fetch_all_candidates(self):
        """Fetches all candidates from

        the database
        """
        query = """SELECT * FROM candidates"""
        return database.select_from_db(query)

    def delete(self, candidate_id):
        query = """DELETE FROM candidates WHERE candidate_id = '{}' """.format(candidate_id)
        database.insert_to_db(query)

      
    @staticmethod
    def check_candidature(candidate):
        #candidate should not be registered to more than one office and with more than one party
        query = """SELECT * FROM candidates WHERE candidate = '{}'""".format(candidate)

        number_of_rows = database.select_from_db(query)
        
        return number_of_rows
    @staticmethod
    def check_office(office):
        query = """SELECT * FROM offices WHERE office_id = '{}' """.format(office)

        number_of_rows = database.select_from_db(query)

        return number_of_rows
    
    @staticmethod
    def check_party(office):
        query = """ SELECT * FROM parties WHERE party_id = '{}' """.format(office)

        number_of_rows = database.select_from_db(query)

        return number_of_rows