# Car Rental AI

This is my project for the emerging tools and technologies subject.

I decided to use a **Vector Database** for my project. I am using ChromaDB, which runs 100% locally on my computer and requires absolutely NO api keys or internet connection.

## What it does
Normal car rental websites make you use bad keyword filters to find a car. It's annoying. I made it so you can just type a sentence about your trip.

The Vector Database mathematically converts your trip details into coordinates, and matches it with the best car in the fleet based on the actual *meaning* of your words, not just basic keyword matching.

## How to run it
1. Open terminal and install the packages: `pip install -r requirements.txt`
2. Run the app: `streamlit run app.py`
3. Just type your trip details in! No passwords or API keys are required. (Note: the very first time you run a search, it might take 10-20 seconds to download the tiny local AI model if it isn't cached yet, but after that it is instant!)
