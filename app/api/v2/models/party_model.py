from app.api.v2 import database 

PARTIES = []

class Party(object):
    def __init__(self):
        
        self.party = PARTIES
    
    def save(self, party_name, party_hqaddress, party_logoUrl):
        party = {
            "name": party_name,
            "hqaddress":party_hqaddress,
            "logoUrl": party_logoUrl
        }

        query =  """INSERT INTO parties(name, hqaddress,logoUrl)
        VALUES('{}', '{}','{}')""".format(party_name,party_hqaddress, party_logoUrl)
        database.insert_to_db(query)

        return party
    