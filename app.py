from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)
# ---- CONFIG ----
openai.api_key = "YOUR_OPENAI_API_KEY"   # <-- Replace with your key

# ---- ROUTES ----
@app.route('/')
def home():
    return render_template("homePage.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    ingredients = data.get("ingredients")

    # Call OpenAI API
    prompt = f"Suggest 3 simple recipes using these ingredients: {ingredients}. Keep it short and clear."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    recipes = response.choices[0].text.strip()

    return jsonify({"recipes": recipes})


if __name__ == "_main_":
    app.run(debug=True)