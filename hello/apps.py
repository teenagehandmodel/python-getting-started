# app.py
from flask import Flask, request, jsonify, render_template
import openai, os, json
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Config (replace with your keys in .env)
openai.api_key = os.getenv("OPENAI_KEY")

@app.route('/')
def home():
    return render_template('index.html')  # You'll create this next

@app.route('/get-estimate', methods=['POST'])
def get_estimate():
    data = request.json
    category = data.get('category')
    issue = data.get('issue')

    prompt = f"""Act as a {category} repair expert. For this issue: '{issue}', provide:
    - Cost range (parts + labor)
    - Time to fix
    - Urgency (1-10)
    Output as JSON with keys: cost, time, urgency."""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify(json.loads(response.choices[0].message.content))

if __name__ == '__main__':
    app.run(debug=True)