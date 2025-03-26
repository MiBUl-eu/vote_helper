import streamlit as st

st.title("Settings")

if "location_widget" not in st.session_state:
    if "location" in st.session_state:
        st.session_state.location_widget = st.session_state.location

if "vote_id_widget" not in st.session_state:
    if "vote_id" in st.session_state:
        st.session_state.vote_id_widget = st.session_state.vote_id

location = st.text_input("Location", key="location_widget", value=st.session_state.location_widget)
vote_id = st.number_input("Vote ID", key="vote_id_widget", value=int(st.session_state.vote_id_widget), step=1000, format="%d")

if st.button("Save"):
    st.session_state.location = location
    st.session_state.vote_id = vote_id
    st.write("Settings saved.")