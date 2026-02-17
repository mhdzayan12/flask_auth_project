🔐 Flask Authentication System


A secure user authentication system built using Flask.
This project demonstrates registration, login, password hashing, session management, and SQLite database integration following basic security best practices.


📌 Project Description


The Flask Authentication System is a beginner-friendly yet secure web application that allows users to create accounts and log in safely.

It implements password hashing, flash messaging, and session handling to ensure user data is protected. The project structure is organized and easy to understand, making it ideal for learning Flask authentication workflows.


🚀 Features


User Registration

Secure Login System

Password Hashing

Flash Messages

Session Management

SQLite Database Integration

Clean UI Design

🛠️ Technologies Used

Python

Flask

HTML5

CSS3

SQLite

Werkzeug Security


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
│   └── dashboard.html
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

Contain uppercase letters (A-Z)

Contain lowercase letters (a-z)

Include numbers (0-9)

Include special characters (!, @, #, $, %, /, >, <, etc.)

Example of valid password:

Zayan@2026!

2️⃣ Unique User Validation

Usernames must be unique

Emails must be unique

Duplicate registrations are prevented

3️⃣ Email Verification

Users must verify their email before login

Verification token system implemented

Prevents fake or invalid account creation

4️⃣ Password Security

Passwords are hashed using generate_password_hash()

Passwords are never stored in plain text

Verification uses check_password_hash()

5️⃣ Rate Limiting

Limits repeated login attempts

Protects against brute-force attacks

Can be implemented using Flask-Limiter



Screen shorts:



<img width="1177" height="818" alt="Screenshot 2026-02-17 115921" src="https://github.com/user-attachments/assets/38b298f5-909f-4451-995f-c16bf16775fe" />

<img width="849" height="740" alt="Screenshot 2026-02-17 115947" src="https://github.com/user-attachments/assets/91d74e21-5b36-4c7b-a15d-117d0a2d0bcf" /

<img width="849" height="740" alt="Screenshot 2026-02-17 115947" src="https://github.com/user-attachments/assets/d3db433c-05de-4bfe-a63e-f04b42d6a000" />




👨‍💻 Author :
Muhammed Zayan.T
