"""
create tables for the application
"""

import sys
import os
import psycopg2
import psycopg2.extras
from instance.config import config

def init_db(db_url=None):
    # initialize db connection
    try:
        if os.getenv('FLASK_ENV') == 'testing':
            conn, cursor = query_database()
            queries = drop_table_if_exists()+create_tables()
        else:
            conn, cursor = query_database()
            queries = create_tables()
        
        i=0
        while i != len(queries):
            query = queries[i]
            cursor.execute(query)
            conn.commit()
            i += 1
        conn.close()
    except Exception as error:
        print("DB Error: {} \n".format(error))


def create_tables():
    """Queries for setting up the database tables"""

    users_table_query = """
    CREATE TABLE IF NOT EXISTS users  (
        user_id SERIAL PRIMARY KEY,
        firstname VARCHAR (30) NOT NULL,
        lastname VARCHAR (30) NOT NULL,
        othername VARCHAR (30) NOT NULL,
        email VARCHAR (30) NOT NULL UNIQUE,
        phoneNumber VARCHAR (11) NOT NULL UNIQUE,
        passportUrl VARCHAR (40) NOT NULL,
        password VARCHAR (128) NOT NULL,
        isAdmin  BOOLEAN DEFAULT FALSE
    )"""

    party_table_query = """
    CREATE TABLE IF NOT EXISTS parties (
        party_id SERIAL PRIMARY KEY,
        name VARCHAR (24) NOT NULL UNIQUE,
        hqaddress VARCHAR (50) NOT NULL,
        logoUrl VARCHAR (60) NOT NULL
    )"""

    office_table_query = """
    CREATE TABLE IF NOT EXISTS offices (
        office_id SERIAL PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        office_type VARCHAR (50) NOT NULL
    )"""

    petition_table_query = """
    CREATE TABLE IF NOT EXISTS petitions (
        petition_id SERIAL PRIMARY KEY,
        createdOn TIMESTAMP DEFAULT NOW(),
        createdBy INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
        office INTEGER NOT NULL REFERENCES offices(office_id) ON DELETE CASCADE,
        body VARCHAR(200) NOT NULL
    )"""

    candidate_table_query = """
    CREATE TABLE IF NOT EXISTS candidates (
        candidate_id SERIAL PRIMARY KEY,
        office INTEGER NOT NULL REFERENCES offices(office_id) ON DELETE CASCADE,
        party INTEGER NOT NULL REFERENCES parties(party_id) ON DELETE CASCADE,
        candidate INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE
    )
    """


    vote_table_query = """
    CREATE TABLE IF NOT EXISTS votes (
        vote_id SERIAL PRIMARY KEY,
        createdOn TIMESTAMP DEFAULT NOW(),
        createdBy INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
        office INTEGER NOT NULL REFERENCES offices(office_id) ON DELETE CASCADE,
        candidate INTEGER NOT NULL REFERENCES candidates(candidate_id) ON DELETE CASCADE
    )"""

 
    return [users_table_query, party_table_query, office_table_query,
            petition_table_query, candidate_table_query, vote_table_query]



def drop_table_if_exists():
    """Drop tables before recreating them"""

    drop_parties_table = """
    DROP TABLE IF EXISTS parties CASCADE"""

    drop_offices_table = """
    DROP TABLE IF EXISTS offices CASCADE"""

    drop_users_table = """
    DROP TABLE IF EXISTS users CASCADE"""

    drop_petitions_table = """
    DROP TABLE IF EXISTS petitions CASCADE"""

    drop_candidates_table = """
    DROP TABLE IF EXISTS candidates CASCADE"""

    drop_votes_table = """
    DROP TABLE IF EXISTS votes CASCADE"""

    return [drop_parties_table, drop_offices_table,
    drop_users_table, drop_petitions_table, drop_candidates_table, drop_votes_table]

def query_database(query=None,db_url=None):
    conn = None

    if db_url is None:
        db_url = config[os.getenv("FLASK_ENV")].DB_URL
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if query:
            cursor.execute(query)
            conn.commit()
    except(Exception,
           psycopg2.DatabaseError,
           psycopg2.ProgrammingError) as error:
        print(error)
        return None

    return conn, cursor


def insert_to_db(query):
    try:
        conn = query_database(query)[0]
        conn.close()
    except psycopg2.Error as error:
        print("Insertion error: {}".format(error))
        sys.exit(1)


def select_from_db(query):
    fetched_content = None
    conn, cursor = query_database(query)
    if conn:
        fetched_content= cursor.fetchall()
        conn.close()

    return fetched_content


if __name__ == '__main__':
    init_db()
    query_database()