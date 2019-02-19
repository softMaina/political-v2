from app.api.v2 import database 

PARTIES = []

class Party(object):
    def __init__(self):
        
        self.party = PARTIES
    
    def save(self, party_name, party_hqaddress, party_logoUrl):
        """ save a political party """
        party = {
            "name": party_name,
            "hqaddress":party_hqaddress,
            "logoUrl": party_logoUrl
        }

        query =  """INSERT INTO parties(name, hqaddress,logoUrl)
        VALUES('{}', '{}','{}')""".format(party_name,party_hqaddress, party_logoUrl)
        database.insert_to_db(query)

        return party
    def delete(self, party_id):
        query = """DELETE FROM parties WHERE party_id = '{}' """.format(party_id)
        database.insert_to_db(query)
    def fetch_all_parties(self):
        """Fetches all parties from

        the database
        """
        query = """SELECT * FROM parties"""
        return database.select_from_db(query)

    def update(self, party_id, party_logoUrl, party_hqaddress, party_name):

        query = """UPDATE parties SET name = '{}',hqaddress = '{}', logourl = '{}' WHERE party_id = '{}' """.format(party_name,party_hqaddress, party_logoUrl,party_id)

        database.insert_to_db(query)