from openai.types.chat.chat_completion import ChatCompletion
from config import Config
from flask import Flask, request, jsonify, render_template, session
from flask_bcrypt import Bcrypt  # type:ignore
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from typing import Optional, cast
import os

# Import Intasend - problematic
# from intasend import APIService

# Initialize flask app
app = Flask(__name__)

# ---- CONFIG ----
app.config["OPENAI_API_KEY"] = Config.OPENAI_API_KEY
client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Initialize Intasend
# intasend = APIService(
#     token=Config.INTASEND_SECRET_KEY,
#     publishable_key=Config.INTASEND_PUBLISHABLE_KEY,
#     test=Config.INTASEND_TEST_MODE,
# )

# TiDB Cloud MySQL connection
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = Config.SECRET_KEY or "fallback-secret-key-for-development"
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


# class Payment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     recipe_id = db.Column(
#         db.Integer, db.ForeignKey("popular_recipe.id"), nullable=False
#     )
#     amount = db.Column(db.Float, nullable=False)
#     payment_status = db.Column(db.String(50), default="pending")
#     payment_method = db.Column(db.String(50))
#     transaction_id = db.Column(db.String(200))
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


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

    user: Optional[User] = cast(
        Optional[User], User.query.filter_by(username=username).first()
    )
    if not user:
        return jsonify({"error": "User not found", "action": "signup"}), 404
    if bcrypt.check_password_hash(user.password, password):  # type: ignore
        session["user_id"] = user.id
        session["username"] = user.username
        return jsonify({"message": "Login successful", "username": user.username}), 200
    return jsonify({"error": "Invalid password"}), 401


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


@app.route("/check_session")
def check_session():
    if "user_id" in session:
        return jsonify({"logged_in": True, "username": session.get("username")}), 200
    return jsonify({"logged_in": False}), 200


@app.route("/")
def home():
    is_logged_in = "user_id" in session
    username = session.get("username", "") if is_logged_in else ""
    return render_template(
        "index.html", is_logged_in=is_logged_in, username=username
    )


@app.route("/login")
def login_page():
    return render_template("login_page.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    # Check if user is logged in
    if "user_id" not in session:
        return jsonify({"error": "Please log in to get recipe recommendations"}), 401

    if not request.json:
        return jsonify({"error": "Invalid input"}), 400

    data = request.json
    ingredients = data.get("ingredients")
    if not ingredients:
        return jsonify({"error": "Ingredients field is required"}), 400

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