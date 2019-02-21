from app.api.v2 import database 

VOTES=[]

class Vote():
    def __init__(self):
        self.vote = VOTES
    
    def save(self, createdOn, createdBy, office, candidate):
        query =  """INSERT INTO votes(createdOn, createdBy, office, candidate)
        VALUES('{}','{}','{}','{}')""".format(createdOn, createdBy, office, candidate)
        database.insert_to_db(query)
    
    def update(self, vote_id, createdOn, createdBy, candidate):

        query = """UPDATE votes SET createdOn = '{}',createdBy = '{}', candidate = '{}' WHERE vote_id = '{}' """.format(createdOn,createdBy,candidate,vote_id)
        database.insert_to_db(query)


    def fetch_all_votes(self):
        """Fetches all votes cast

        the database
        """
        query = """ SELECT * FROM votes """
        # query = """SELECT offices.name AS office, users.firstname AS firstname, users.lastname AS lastname,
        #         COUNT (votes.candidate) AS votes FROM votes JOIN offices ON offices.office_id = votes.office
        #         JOIN  users ON users.user_id = votes.candidate GROUP BY users.firstname, users.lastname, offices.name
        #       """
        return database.select_from_db(query)
