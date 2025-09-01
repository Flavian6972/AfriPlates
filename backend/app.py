from openai.types.chat.chat_completion import ChatCompletion
from config import Config
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI

# Initialize flask app
app = Flask(__name__)

# Code automatically hot-reloads when changes are made
app.run(debug=True)

# ---- CONFIG ----
app.config["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Enable CORS
CORS(app)


# ---- ROUTES ----
@app.route("/")
def home():
    return render_template("homePage.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    # Validate that the request contains JSON data
    if not request.json:
        return jsonify({"error": "Invalid input"}), 400

    data = request.json
    ingredients = data.get("ingredients")

    # Validate ingredients field exists and is not empty
    if not ingredients:
        return jsonify({"error": "Ingredients field is required"}, 400)

    # The Completion API is deprecated. Use ChatCompletion API instead.
    # response: openai.OpenAIObject = openai.Completion.create(
    #     engine="text-davinci-003", prompt=prompt, max_tokens=150
    # )

    # recipes: str = response.choices[0].text.strip()

    # Call OpenAI API
    prompt: str = (
        f"Suggest 3 simple recipes using these ingredients: {ingredients}. Keep it short and clear."
    )
    try:
        response: ChatCompletion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=150,  # use instead of max_tokens which is deprecated
        )

        # Handle potential None content
        message_content = response.choices[0].message.content
        if message_content is None:
            return jsonify({"error": "No response generated"}), 500

        recipes: str = message_content.strip()

        return jsonify({"recipes": recipes})

    except Exception as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
