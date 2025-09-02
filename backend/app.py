from openai.types.chat.chat_completion import ChatCompletion
from config import Config
from flask import Flask, request, jsonify, render_template, session
from flask_bcrypt import Bcrypt  # type:ignore
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from typing import Optional, cast
import os

# Initialize flask app
app = Flask(__name__)

# ---- CONFIG ----
app.config["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
client = OpenAI(api_key=Config.OPENAI_API_KEY)

# TiDB Cloud MySQL connection
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "ssl": {"ca": os.path.join(os.path.dirname(__file__), "isrgrootx1.pem")}
    }
}

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Enable CORS
CORS(app)

# ---- MODELS ----
class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password: str = db.Column(db.String(255), nullable=False)

    def __init__(self, username: str, password: str, email: str = ""):
        self.username = username
        self.password = password
        self.email = email


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    recipes = db.Column(db.Text, nullable=False)

    def __init__(self, ingredients: str, recipes: str, user_id: Optional[int] = None):
        self.ingredients = ingredients
        self.recipes = recipes
        self.user_id = user_id

# ---- ROUTES ----
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if not data:
        return jsonify({"error": "No json data outputted"}), 400

    username: str = data.get("username")
    password: str = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")  # type: ignore
    user = User(username=username, password=pw_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "No json data provided"}), 400

    username = data.get("username")
    password: str = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user: Optional[User] = cast(Optional[User], User.query.filter_by(username=username).first())
    if not user:
        return jsonify({"error": "User not found"}), 404
    if user and bcrypt.check_password_hash(user.password, password):  # type: ignore
        session["user_id"] = user.id
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/")
def home():
    return render_template("homePage.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    if not request.json:
        return jsonify({"error": "Invalid input"}), 400

    data = request.json
    ingredients = data.get("ingredients")
    if not ingredients:
        return jsonify({"error": "Ingredients field is required"}, 400)

    prompt: str = (
        f"Suggest 3 simple recipes using these ingredients: {ingredients}. Keep it short and clear."
    )
    try:
        response: ChatCompletion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=150,
        )

        message_content = response.choices[0].message.content
        if message_content is None:
            return jsonify({"error": "No response generated"}), 500

        recipes: str = message_content.strip()

        # Save to TiDB Cloud
        recipe_record = Recipe(
            ingredients=ingredients,
            recipes=recipes,
            user_id=session.get("user_id"),
        )
        db.session.add(recipe_record)
        db.session.commit()

        return jsonify({"recipes": recipes})

    except Exception as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates User & Recipe tables if not exist
    app.run(debug=True)
