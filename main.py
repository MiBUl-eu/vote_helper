import streamlit as st 
import vote_generate as vote
import time
import database as db

database = db.database()

if "location" not in st.session_state:
    st.session_state.location = ""
if "vote_id" not in st.session_state:
    st.session_state.vote_id = 0

st.write("Vote_id: {}".format(st.session_state.vote_id))   
st.write("Location: {}".format(st.session_state.location))
#fields = []
# if "saved" not in st.session_state:
#     st.session_state.saved = True

# if st.session_state.saved:
#     st.write("Vote submitted.")
#     st.session_state.saved = False
#     time.sleep(1)
#     st.rerun()
# else:
for person in vote.get_fields():
    st.number_input(person.name, 0, 1, 0, key=person.field + str(st.session_state.vote_id))

st.write("It was voted for {} persons".format(sum([st.session_state[person.field + str(st.session_state.vote_id)] for person in vote.get_fields()])))


if st.button("Submit"):
    v = vote.vote(id=1)
    for i, person in enumerate(vote.get_fields()):
        setattr(v, person.field, st.session_state[person.field + str(st.session_state.vote_id)])
    v.location = st.session_state.location
    v.vote_id = st.session_state.vote_id
    if database.insert_vote(v):
        st.write("Vote submitted.")
        st.session_state.vote_id += 1
        # st.session_state.saved = True
        st.rerun()
    else:
        st.write("Error submitting vote.")