# Persistent database (google cloud, update to have public read/write permissions. use "gcloud init" in terminal to authenticate)
# CRUD to database (use st.data_editor with onChange call)
# 4 Questions implemented

import streamlit as st

st.set_page_config(page_title="CSE 587 Project")
st.sidebar.success("Select a Question to View")

st.header("CSE 587 Project - Rent Predictor", divider=True)

st.subheader("Team #4 (Saagnik Sarbadhikari, Marcus Hartman, Bharath Reddy)")

#TODO: needs link
st.link_button("Acesss Report", "https://docs.google.com/document/d/1W4us3Q4Ymc-IyGFI4kM7BXtndfYfwWfLcG3xxy4O2Yo/edit?usp=sharing")

st.text("Database interaction is embedded within each question to provide easier and more focused control for the user. The algorithms presented are based off our Phase 2 answers, and incorporated into a question that can be accessed using the sidebar on the left.")
