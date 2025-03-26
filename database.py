import mariadb
import os
import streamlit as st 
import vote_generate as vote

class database:
    def __init__(self):
        self.cursor = None
        self.conn = None
        self.connect()

    def connect(self):
        try:
            conn = mariadb.connect(
                user=os.environ['DATABASE_USER'],
                password=os.environ['DATABASE_PASSWORD'],
                host=os.environ['DATABASE_HOST'],
                port=int(os.environ['DATABASE_PORT']),
                database=os.environ['DATABASE_NAME'])
            create_string = "CREATE TABLE IF NOT EXISTS vote (id INT PRIMARY KEY AUTO_INCREMENT, vote_id INT, location VARCHAR(255), "
            for person in vote.get_fields():
                create_string += "{} INT, ".format(person.field)
            create_string = create_string[:-2] + ")"
            conn.cursor().execute(create_string)
            self.conn = conn
            self.cursor =  conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return None

    def get_votes(self):
        if not self.cursor:
            print("Connecting")
            self.connect()
        try:
            self.cursor.execute("SELECT * FROM vote")
            votes_sql = self.cursor.fetchall()
            votes_pretty = []
            for vote_sql in votes_sql:
                vote_pretty = {
                    "vote_id": vote_sql[1],
                    "location": vote_sql[2]
                }
                for i, person in enumerate(vote.get_fields()):
                    vote_pretty.update({
                        person.name: vote_sql[i+3]
                    })
                votes_pretty.append(vote_pretty)
        except mariadb.Error as e:
            print(f"Error: {e}")
        return votes_pretty

    def get_vote(self, id):
        if not self.cursor:
            self.connect()
        try:
            self.cursor.execute("SELECT * FROM vote WHERE id=?", (id,))
            vote_sql = self.cursor.fetchone()
            vote_pretty = {
                "vote_id": vote_sql[1],
                "location": vote_sql[2]
            }
            for i, person in enumerate(vote.get_fields()):
                vote_pretty.update({
                    person.name: vote_sql[i+3]
                })
        except mariadb.Error as e:
            print(f"Error: {e}")
        return vote_pretty

    def get_vote_by_person(self, person):
        if not self.cursor:
            self.connect()
        try:
            self.cursor.execute("SELECT * FROM vote WHERE {}=1".format(person))
            votes = self.cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error: {e}")
        return votes

    def get_vote_by_person_and_location(self, person, location):
        if type(location) == tuple:
            location = location[0]
        if not self.cursor:
            self.connect()
        try:
            self.cursor.execute("SELECT * FROM vote WHERE {}=1 AND location=?".format(person), (location,))
            votes = self.cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error: {e}")
        return votes

    def get_vote_by_location(self, location):
        if not self.cursor:
            self.connect()
        try:
            self.cursor.execute("SELECT * FROM vote WHERE location=?", (location,))
            votes = self.cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error: {e}")
        return votes

    def get_insert_string(self):
        name_string = ""
        value_string = ""
        for person in vote.get_fields():
            name_string += person.field + ", "
            value_string += "?, "
        return "INSERT INTO vote (vote_id, location, {}) VALUES (?, ?, {})".format(name_string[:-2], value_string[:-2])

    def insert_vote(self, vote_to_save):
        if not self.cursor:
            connect
        try:
            list_to_save = [vote_to_save.vote_id, vote_to_save.location]
            list_to_save.extend([getattr(vote_to_save, person.field) for person in vote.get_fields()])
            self.cursor.execute(self.get_insert_string(), list_to_save)
            self.conn.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
        return True

    def count_votes(self):
        if not self.cursor:
            self.connect()
        try:
            self.cursor.execute("SELECT COUNT(*) FROM vote")
            count = self.cursor.fetchone()
        except mariadb.Error as e:
            print(f"Error: {e}")
        return count

    def count_votes_by_person(self, person):
        if not self.cursor:
            self.connect()
        try:
            self.cursor.execute("SELECT COUNT(*) FROM vote WHERE {}=1".format(person))
            count = self.cursor.fetchone()
        except mariadb.Error as e:
            print(f"Error: {e}")
        return count

    def count_votes_by_location(self, location):
        if not self.cursor:
            self.connect()
        try:
            self.cursor.execute("SELECT COUNT(*) FROM vote WHERE location=?", (location,))
            count = self.cursor.fetchone()
        except mariadb.Error as e:
            print(f"Error: {e}")
        return count

    def count_votes_by_person_and_location(self, person, location):
        if type(location) == tuple:
            location = location[0]
        if not self.cursor:
            self.connect()
        try:
            self.cursor.execute("SELECT COUNT(*) FROM vote WHERE {}=1 AND location=?".format(person), (location,))
            count = self.cursor.fetchone()
        except mariadb.Error as e:
            print(f"Error: {e}")
        return count

    def get_locations(self):
        if not self.cursor:
            self.connect()
        try:
            self.cursor.execute("SELECT DISTINCT location FROM vote")
            locations = self.cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error: {e}")
        return locations