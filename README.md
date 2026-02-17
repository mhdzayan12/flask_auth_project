🔐 Flask Authentication System

A secure user authentication system built using Flask.
This project demonstrates registration, login, hashed password storage, session management, email verification, and SQLite database integration following modern security best practices.

📌 Project Description

The Flask Authentication System is a beginner-friendly yet secure web application that allows users to create accounts and log in safely.

It implements password hashing, flash messaging, strong password validation, unique user constraints, rate limiting, and secure session handling to ensure user data is protected.

The project structure is clean and organized, making it ideal for learning secure authentication workflows using Flask.

🚀 Features
🔑 Authentication

User Registration

Secure Login System

Logout Functionality

Session Management

🛡️ Security Features

Hashed Password Storage

Strong Password Policy Enforcement

Unique Username Validation

Unique Email Validation

Email Verification System

Rate Limiting (Brute Force Protection)

Flash Messages for Secure Feedback

SQLite Database Integration

Clean UI Design

🛠️ Technologies Used

Python

Flask

Flask-Limiter

HTML5

CSS3

SQLite

Werkzeug Security

SMTP (Email Verification)

Git

📂 Project Structure
flask-authentication-system/
│
├── app.py
├── requirements.txt
│
├── static/
│   └── style.css
│
├── templates/
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   └── verify_email.html
│
└── database.db

⚙️ Installation & Usage
1️⃣ Clone the Repository
git clone https://github.com/your-username/flask-authentication-system.git
cd flask-authentication-system

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
python app.py


Then open your browser and go to:

http://127.0.0.1:5000/

🛡️ Security Implementation
1️⃣ Strong Password Policy

Passwords must:

Be at least 8 characters long

Contain uppercase letters (A–Z)

Contain lowercase letters (a–z)

Include numbers (0–9)

Include special characters (!, @, #, $, %, /, >, <, etc.)

Example of a valid password:

Zayan@2026!

2️⃣ Hashed Password Storage

Passwords are never stored in plain text.

They are securely hashed using:

generate_password_hash()

check_password_hash()

This ensures that even if the database is exposed, user passwords remain protected.

3️⃣ Unique User Validation

Usernames must be unique

Emails must be unique

Duplicate registrations are prevented at the database level

4️⃣ Email Verification

Users must verify their email before accessing the dashboard

Secure token-based verification system

Prevents fake or invalid account creation

5️⃣ Rate Limiting

Limits repeated login attempts

Protects against brute-force attacks

Implemented using Flask-Limiter

📸 Screenshots
<img width="1177" height="818" alt="Register Page" src="https://github.com/user-attachments/assets/38b298f5-909f-4451-995f-c16bf16775fe" /> <br> <img width="849" height="740" alt="Login Page" src="https://github.com/user-attachments/assets/91d74e21-5b36-4c7b-a15d-117d0a2d0bcf" /> <br><img width="1184" height="687" alt="Screenshot 2026-02-17 120019" src="https://github.com/user-attachments/assets/32a3f36e-c854-4752-9363-014da2ec29a8" />

👨‍💻 Author

Muhammed Zayan.T
