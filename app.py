from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# ✅ Replace this with your actual Groq API key
openai.api_key = ""
openai.base_url = "https://api.groq.com/openai/v1/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json['question']

    try:
        response = openai.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are an expert airline assistant. Help users with flights, luggage, bookings, and travel advice."},
                {"role": "user", "content": user_question}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    






import requests

# Add this helper function
def get_flight_status(flight_code):
    api_key = "bf4e666f279a848fe38b8e9e200a5417"  # Replace with your API key
    url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&flight_iata={flight_code}"

    res = requests.get(url)
    data = res.json()

    if "data" in data and len(data["data"]) > 0:
        flight = data["data"][0]
        status = flight["flight_status"]
        departure = flight["departure"]["airport"]
        arrival = flight["arrival"]["airport"]
        airline = flight["airline"]["name"]
        scheduled = flight["departure"]["scheduled"]
        return f"{airline} flight {flight_code} is currently **{status.upper()}**.\nDeparture: {departure}\nArrival: {arrival}\nScheduled Time: {scheduled}"
    else:
        return "Sorry, I couldn't find details for that flight."




if __name__ == '__main__':
    app.run(debug=True)
