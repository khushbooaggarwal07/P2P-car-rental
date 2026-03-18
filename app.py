import streamlit as st
import google.generativeai as genai

st.title("Peer-to-Peer Car Rental AI")
st.write("Tell the AI about your trip, and it will recommend the best car for you to rent.")

api_key = st.text_input("Enter Gemini API Key", type="password")

trip_details = st.text_area("Where are you going and what do you need the car for?")

# List of cars hardcoded as a string
available_cars = """
1. 2018 Subaru Outback: Has All-Wheel Drive, a roof rack, good for snow or mountains. $65/day.
2. 2021 Tesla Model 3: Electric vehicle, fast acceleration, good for city driving or tech fans. $90/day.
3. 2015 Honda Odyssey: Minivan that seats 8 people, good for big families and road trips. $70/day.
4. 2019 Ford Mustang: Convertible sports car, good for nice weather and weekends. $120/day.
5. 2012 Toyota Prius: Hybrid, saves money on gas, good for long cheap drives. $35/day.
6. 2020 Ford F-150: Big pickup truck, good for moving furniture or moving dirt. $85/day.
"""

if st.button("Find Best Car"):
    if trip_details == "":
        st.write("Please enter your trip details.")
    elif api_key == "":
        st.write("Please enter your API Key.")
    else:
        st.write("The AI is picking your car...")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = "You work for a car rental company. Here are the cars we have available to rent: " + available_cars + " The customer said this about their trip: '" + trip_details + "'. Write a short message telling them which car they should rent and why it is the perfect fit."
        
        try:
            response = model.generate_content(prompt)
            st.write("Here is your recommendation:")
            st.write("---")
            st.write(response.text)
        except Exception as e:
            st.write("An error occurred.")
            st.write(e)
