from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from wtforms.validators import Regexp
from flask_limiter import Limiter
from flask import session
from flask_limiter.util import get_remote_address
from flask_login import current_user
import os

app = Flask(__name__)

# RATE LIMITER
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


# CONFIG


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

# MAIL CONFIG
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mmhdzayant@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = 'mmhdzayant@gmail.com'


# EXTENSIONS


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# DATABASE MODEL


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    failed_attempts = db.Column(db.Integer, default=0)
    is_locked = db.Column(db.Boolean, default=False)



# REGISTER FORM


class RegisterForm(FlaskForm):

    username = StringField(
        validators=[
            InputRequired(),
            Length(min=4, max=20),
            Regexp(
                r'^[A-Za-z][A-Za-z0-9_]*$',
                message="Username must start with a letter and contain only letters, numbers, and underscore."
            )
        ],
        render_kw={"placeholder": "Username"}
    )

    email = StringField(
        validators=[InputRequired(), Email()],
        render_kw={"placeholder": "Email"}
    )

    password = PasswordField(
    validators=[
        InputRequired(),
        Length(min=8, max=20),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#]).+$',
            message="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
        )
    ],
    render_kw={"placeholder": "Password"}
)



    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already exists.")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered.")



# LOGIN FORM

class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired()],
        render_kw={
            "placeholder": "Username",
            "autocomplete": "off"
        }
    )

    password = PasswordField(
        validators=[InputRequired()],
        render_kw={
            "placeholder": "Password",
            "autocomplete": "new-password"
        }
    )

    submit = SubmitField('Login')




# ROUTES


@app.route('/')
def home():
     if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
     return render_template('home.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))


# REGISTER

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        # Generate verification token
        token = serializer.dumps(new_user.email, salt='email-confirm')
        link = url_for('verify_email', token=token, _external=True)

        msg = Message(
            'Verify Your Email',
            recipients=[new_user.email]
        )

        msg.body = f'Click this link to verify your account:\n{link}'

        mail.send(msg)

        flash("Registration successful! Check your email to verify.")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



# EMAIL VERIFICATION


@app.route('/verify/<token>')
def verify_email(token):
    try:
        email = serializer.loads(
            token,
            salt='email-confirm',
            max_age=3600  # 1 hour expiry
        )
    except:
        flash("Verification link is invalid or expired.")
        return redirect(url_for('login'))

    user = User.query.filter_by(email=email).first()

    if user:
        user.is_verified = True
        db.session.commit()
        flash("Email verified successfully! You can now login.")

    return redirect(url_for('login'))



# LOGIN


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user:

            
            if user.is_locked:
                flash("Account locked due to too many failed attempts.")
                return redirect(url_for('login'))

            
            if bcrypt.check_password_hash(user.password, form.password.data):

                
                user.failed_attempts = 0
                db.session.commit()

                if not user.is_verified:
                    flash("Please verify your email first.")
                    return redirect(url_for('login'))

                login_user(user)
                return redirect(url_for('dashboard'))

            else:
                
                user.failed_attempts += 1

                if user.failed_attempts >= 5:
                    user.is_locked = True
                    flash("Account locked due to too many failed attempts.")

                else:
                    flash("Invalid username or password.")

                db.session.commit()

        else:
            flash("Invalid username or password.")

    return render_template('login.html', form=form)



@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response



# MAIN


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

