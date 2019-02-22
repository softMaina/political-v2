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


    def fetch_all_votes(self,office_id):
        """Fetches all votes cast

        the database
        """
        query = """ SELECT * FROM votes """
        # query = """SELECT offices.name AS office, users.firstname AS firstname, users.lastname AS lastname,
        #         COUNT (votes.candidate) AS votes FROM votes JOIN offices ON offices.office_id = votes.office
        #         JOIN  users ON users.user_id = votes.candidate GROUP BY users.firstname, users.lastname, offices.name
        #       """

        candidates_query = """SELECT * FROM candidates JOIN users ON candidates.candidate=users.user_id WHERE office= '{}'""".format(office_id)

        candidates = database.select_from_db(candidates_query)

        size = len(candidates)

        votes = []

        if size > 0:
            for candidate in candidates:
                vote_query = """SELECT candidate , COUNT(*) as votes FROM votes WHERE candidate = '{}' GROUP by candidate""".format(candidate["candidate_id"])
                candidate_votes = database.select_from_db(vote_query)
                votes.append({"candidate":candidate["firstname"], "votes":candidate_votes})

        return votes
