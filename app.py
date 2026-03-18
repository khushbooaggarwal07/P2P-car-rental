import streamlit as st
import chromadb

st.title("Peer-to-Peer Car Rental AI")
st.write("This app uses a Vector Database to mathematically search for your perfect car. No API keys needed!")

trip_details = st.text_area("Where are you going and what do you need the car for?")

cars = [
    {"id": "1", "name": "2018 Subaru Outback", "desc": "Has All-Wheel Drive, a roof rack, good for snow or mountains. $65/day."},
    {"id": "2", "name": "2021 Tesla Model 3", "desc": "Electric vehicle, fast acceleration, good for city driving or tech fans. $90/day."},
    {"id": "3", "name": "2015 Honda Odyssey", "desc": "Minivan that seats 8 people, good for big families and road trips. $70/day."},
    {"id": "4", "name": "2019 Ford Mustang", "desc": "Convertible sports car, good for nice weather and weekends. $120/day."},
    {"id": "5", "name": "2012 Toyota Prius", "desc": "Hybrid, saves money on gas, good for long cheap drives. $35/day."},
    {"id": "6", "name": "2020 Ford F-150", "desc": "Big pickup truck, good for moving furniture or moving dirt. $85/day."}
]

# Set up the local Vector Database
# This will save a tiny database file to your folder
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="rental_cars")

# Only add the cars to the database if it is empty
if collection.count() == 0:
    for car in cars:
        collection.add(
            documents=[car["desc"]],
            metadatas=[{"name": car["name"]}],
            ids=[car["id"]]
        )

if st.button("Find Best Car"):
    if trip_details == "":
        st.write("Please enter your trip details.")
    else:
        st.write("Searching database...")
        
        # Search the database locally! Zero APIs needed.
        # It turns your typed sentence into coordinates and finds the closest car based on meaning.
        results = collection.query(
            query_texts=[trip_details],
            n_results=1
        )
        
        best_car_name = results["metadatas"][0][0]["name"]
        best_car_desc = results["documents"][0][0]
        
        st.write("---")
        st.write("### The AI recommends this car:")
        st.write("**" + best_car_name + "**")
        st.write(best_car_desc)
