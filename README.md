# 🍽️ AfriPlates - African Recipe Recommender

**For Africa, By Africa** - *Flavour | Culture | Home*

AfriPlates is an AI-powered recipe recommendation platform that celebrates African cuisine by providing personalized recipe suggestions based on available ingredients, with integrated payment processing for premium content.

## 🌟 Features

### Core Functionality
- 🤖 **AI-Powered Recipe Generation** - Get personalized African recipes using OpenAI/Gemini
- 🌍 **Country-Specific Recipes** - Choose from 6 African countries (Kenya, Nigeria, Ghana, South Africa, Tanzania, Uganda)
- 👤 **User Authentication** - Secure signup/login system with session management
- 📊 **Dashboard Analytics** - Track popular recipes, trending ingredients, and recipe statistics
- 💳 **Payment Integration** - Purchase premium recipes using Intasend (M-Pesa, Card, Bank)

### Advanced Features
- 🔐 **Session Management** - Secure user sessions with Flask sessions
- 🗄️ **Database Storage** - TiDB Cloud MySQL for scalable data storage
- 📱 **Responsive Design** - Mobile-friendly interface
- 🔄 **Real-time Updates** - Dynamic content loading and payment status tracking

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **Flask-Bcrypt** - Password hashing
- **OpenAI API** - Recipe generation
- **Intasend API** - Payment processing
- **TiDB Cloud** - MySQL database hosting

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript** - Interactive functionality
- **Flask Templates** - Server-side rendering

### Database
- **MySQL** - Primary database (TiDB Cloud)
- **SSL Encryption** - Secure database connections

## 📋 Prerequisites

- Python 3.8+
- Git
- OpenAI API Key (or Gemini API Key)
- TiDB Cloud Account
- Intasend Account (for payments)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Flavian6972/AfriPlates.git
cd AfriPlates
```

### 2. Create Virtual Environment
```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Or use the provided activation script
.\activate.ps1
```

### 3. Install Dependencies
```powershell
pip install flask flask-sqlalchemy flask-bcrypt flask-cors openai python-dotenv mysql-connector-python pymysql intasend-python
```

### 4. Environment Configuration
Create a `.env` file in the project root:

```env
# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
# GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@host:port/database

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production

# Intasend Payment Configuration
INTASEND_PUBLISHABLE_KEY=your_intasend_publishable_key
INTASEND_SECRET_KEY=your_intasend_secret_key
INTASEND_TEST_MODE=True

# Application Settings
DEBUG=True
```

### 5. Database Setup
Ensure your TiDB Cloud certificate is in the `backend` folder:
```
backend/isrgrootx1.pem
```

### 6. Run the Application
```powershell
# Activate virtual environment
.\activate.ps1

# Run the Flask app
python backend\app.py
```

The application will be available at: `http://127.0.0.1:5000`

## 📁 Project Structure

```
AfriPlates/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   └── isrgrootx1.pem     # TiDB SSL certificate
├── frontend/
│   ├── homePage.html       # Main dashboard
│   ├── login_page.html     # Authentication page
│   ├── auth.js            # Authentication logic
│   ├── interactive.js     # Main functionality
│   └── styling/
│       ├── styles.css      # Main styles
│       └── login_style.css # Authentication styles
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── activate.ps1          # Virtual environment activation
└── README.md             # This file
```

## 🎯 Usage Guide

### User Authentication
1. **Sign Up**: Create a new account with username and password
2. **Login**: Access your account with credentials
3. **Session Management**: Stay logged in across browser sessions
4. **Logout**: Securely end your session

### Recipe Generation
1. **Choose Country**: Select from 6 African countries
2. **Enter Ingredients**: List available ingredients (comma-separated)
3. **Get Recipes**: AI generates personalized African recipes
4. **Save to Database**: All generated recipes are stored for future reference

### Dashboard Features
1. **Popular Recipes**: AI-generated trending African recipes
2. **Recipe Statistics**: Track weekly and total recipe generation
3. **Trending Ingredients**: Discover popular African cooking ingredients
4. **Premium Content**: Purchase exclusive recipes with payments

### Payment System
1. **Select Premium Recipe**: Choose from AI-generated premium content
2. **Payment Method**: M-Pesa, Card, or Bank transfer
3. **Secure Processing**: Intasend handles all payment transactions
4. **Instant Access**: Unlock recipe content upon successful payment

## 🔧 API Endpoints

### Authentication
- `POST /signup` - Create new user account
- `POST /login` - User authentication
- `POST /logout` - End user session
- `GET /login` - Login page

### Recipe Management
- `GET /` - Main dashboard
- `POST /recommend` - Generate recipe recommendations
- `GET /popular-recipes` - Get popular African recipes
- `GET /trending-ingredients` - Get trending ingredients
- `GET /recipe-stats` - Get recipe generation statistics

### Payment Processing
- `POST /buy-recipe` - Purchase premium recipe
- `GET /payment-status/<id>` - Check payment status

## 🗄️ Database Schema

### User Table
- `id` - Primary key
- `username` - Unique username
- `email` - User email
- `password` - Hashed password

### Recipe Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `ingredients` - Input ingredients
- `recipes` - Generated recipes
- `created_at` - Timestamp

### PopularRecipe Table
- `id` - Primary key
- `title` - Recipe title
- `content` - Recipe content
- `is_premium` - Premium status
- `price` - Recipe price
- `created_at` - Timestamp

### Payment Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `recipe_id` - Foreign key to recipes
- `amount` - Payment amount
- `status` - Payment status
- `transaction_id` - Payment reference
- `created_at` - Timestamp

## 🔐 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **Session Management**: Flask sessions with secure keys
- **SQL Injection Protection**: SQLAlchemy ORM
- **SSL Database Connection**: Encrypted data transmission
- **Environment Variables**: Secure API key management

## 💳 Payment Integration

### Supported Payment Methods
- **M-Pesa**: Mobile money payments (Kenya)
- **Card Payments**: Visa/Mastercard
- **Bank Transfers**: Direct bank payments
- **Mobile Money**: Other African mobile payment systems

### Payment Flow
1. User selects premium content
2. Choose payment method
3. Intasend processes payment
4. Real-time status updates
5. Content unlocked upon success

## 🌍 Deployment

### Local Development
```powershell
.\activate.ps1
python backend\app.py
```

### Production Deployment
1. **Environment Setup**: Configure production environment variables
2. **Database**: Set up production TiDB Cloud instance
3. **SSL Certificates**: Ensure valid SSL certificates
4. **Payment Setup**: Configure live Intasend credentials
5. **WSGI Server**: Use Gunicorn or similar for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Database Connection Errors**
- Verify TiDB Cloud credentials
- Check SSL certificate path
- Ensure network connectivity

**API Key Issues**
- Verify OpenAI/Gemini API keys
- Check API quota and billing
- Ensure correct environment variables

**Payment Failures**
- Verify Intasend credentials
- Check test/live mode settings
- Ensure sufficient account balance

**Installation Problems**
- Use Python 3.8+ 
- Activate virtual environment
- Install all required dependencies

### Getting Help
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

## 📞 Contact

- **Project**: [AfriPlates](https://github.com/Flavian6972/AfriPlates)
- **Author**: Flavian6972
- **Email**: [Contact through GitHub]

##**Team AfriPlates**

Flavian Onyango
Paul Tibi
Fabian Kitonyi
