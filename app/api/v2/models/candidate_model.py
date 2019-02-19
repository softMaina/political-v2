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