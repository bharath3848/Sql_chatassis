import streamlit as st
import requests

# URL of your Flask API (Assuming the Flask app is running locally on port 5000)
flask_api_url = "http://localhost:5000/ask"

# Title of the Streamlit app
st.title("Company Info Query Assistant")

# Input field for the query
query = st.text_input("Ask your query here:")

# When user submits a query
if query:
    # Send the query to the Flask API
    response = requests.get(flask_api_url, params={"query": query})

    # Check if the response is valid
    if response.status_code == 200:
        data = response.json()
        st.write(data['answer'])  # Display the answer from the Flask API
    else:
        st.write("Sorry, there was an error with the request.")
