from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re
import json


# Configure Gemini API
GOOGLE_API_KEY = "Your API key"  # Replace with your Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Predefined data for travel assistance
flights_data = [
    {"origin": "India", "destination": "USA", "flight_name": "Air India Express", "date": "2024-12-15", "departure": "10:00 AM", "price": 500},
    {"origin": "India", "destination": "UK", "flight_name": "British Airways", "date": "2024-12-20", "departure": "1:30 PM", "price": 400},
    {"origin": "India", "destination": "Canada", "flight_name": "Air Canada", "date": "2024-12-25", "departure": "6:00 PM", "price": 600},
    {"origin": "India", "destination": "Australia", "flight_name": "Qantas Airways", "date": "2024-12-18", "departure": "9:00 AM", "price": 700},
    {"origin": "USA", "destination": "Germany", "flight_name": "Lufthansa", "date": "2024-12-15", "departure": "11:30 AM", "price": 550},
]

hotels_data = {
    "USA": [{"name": "Best Western", "price_per_night": 120}],
    "UK": [{"name": "London Hilton", "price_per_night": 150}],
    "Canada": [{"name": "Toronto Marriott", "price_per_night": 100}],
    "Australia": [{"name": "Sydney Grand", "price_per_night": 180}],
    "Germany": [{"name": "Berlin Palace", "price_per_night": 130}],
}

weather_data = {
    "India": {"description": "Hot", "temperature": 30},
    "USA": {"description": "Cold", "temperature": 5},
    "UK": {"description": "Mild", "temperature": 15},
    "Canada": {"description": "Snowy", "temperature": -5},
    "Australia": {"description": "Sunny", "temperature": 25},
    "Germany": {"description": "Chilly", "temperature": 10},
}

def prompt(user_input):
    # Call Gemini API with the user input
    response = model.generate_content(user_input)
    print(response.text)  # Optional: Print the response for debugging
    return response.text



# Helper function to fetch travel details
def get_travel_details(origin, destination):
    flight = next((f for f in flights_data if f["origin"].lower() == origin.lower() and f["destination"].lower() == destination.lower()), None)
    hotel = hotels_data.get(destination, [{}])[0]
    weather = weather_data.get(destination, {})

    if flight and hotel and weather:
        return (
            f"Flight: {flight['flight_name']} departs at {flight['departure']} for ${flight['price']}. "
            f"Hotel: {hotel['name']}, Price per night: ${hotel['price_per_night']}. "
            f"Weather: {weather['description']}, {weather['temperature']}°C."
        )
    return "Sorry, I couldn't find complete travel details for your request."

# Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    user_input = request.form.get('user_input').strip().lower()

    # Check if the input matches any predefined responses
    response = "Sorry, I couldn't find a response to your request."

    with open('chatbot_data.json', 'r') as file:
        data = json.load(file)
        for item in data['responses']:
            if item['user_input'].lower() in user_input:
                response = item['bot_response']
                break

    # If no predefined response, get response from Gemini model
    if response == "Sorry, I couldn't find a response to your request.":
        response = prompt(user_input)

    return jsonify({'response': response})



if __name__ == '__main__':
   
    app.run(debug=True)

