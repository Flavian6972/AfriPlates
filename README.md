🌍 AfriPlates

AfriPlates is a recipe recommendation web app tailored for Africans. Users can input available ingredients, and the app suggests authentic African recipes using those ingredients.

Built for the Vibe Coding Hackathon 🎉


---

🚀 Features

🔑 Login & Signup (with basic auth system)

🍲 Recipe Recommendations powered by AI (OpenAI API)

🌍 African Food Focus – recipes inspired by different African countries

📄 About Page showcasing African dishes and the team

💻 Simple & Clean UI (HTML, CSS, JS + Flask backend)



---

🛠️ Tech Stack

Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

AI API: OpenAI GPT

Extras: Flask-CORS for frontend-backend communication



---

📂 Project Structure

AfriPlates/
│── static/             # CSS, JS, images  
│   ├── styles.css  
│   ├── interactive.js  
│── templates/          # HTML pages  
│   ├── index.html  
│   ├── login.html  
│   ├── about.html  
│── app.py              # Flask backend  
│── auth.js             # Login/Signup handling  
│── README.md           # Project documentation


---

⚡ Setup & Installation

1. Clone the repo

git clone https://github.com/your-username/afriplates.git
cd afriplates

2. Create a virtual environment

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3. Install dependencies

pip install flask flask-cors openai

4. Add your OpenAI API Key

In app.py:

openai.api_key = "YOUR_OPENAI_API_KEY"

5. Run the app

python app.py

Visit: http://127.0.0.1:5000


---

🎯 Future Improvements

✅ Add M-Pesa / Stripe payments for premium recipes

✅ Better personalized recommendations

✅ More African cuisines & cultures included



---

👨‍👩‍👧‍👦 Team AfriPlates

Flavian Onyango
Paul Tibi
Fabian Kitonyi


Paul Tibi

Fabian
