import streamlit as st
import vote_generate as vote
import database as db

st.title("Get Result")

database = db.database()

def get_results_from_database():
    counted_votes = []
    locations = database.get_locations()
    for person in vote.get_fields():
        location_votes = []
        person_dict = {
            "person": person.name,
            "votes": len(database.get_vote_by_person(person.field))
            }
        for location in locations:
            person_dict.update({
                location[0]: len(database.get_vote_by_person_and_location(person.field, location))
            })
        counted_votes.append(person_dict)
    return counted_votes

st.dataframe(get_results_from_database())
st.dataframe(database.get_votes())
