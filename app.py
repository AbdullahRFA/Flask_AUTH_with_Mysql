import bcrypt
import mysql.connector
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from mysql.connector import Error
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sakibrfa@383'
app.config['MYSQL_DB'] = 'mydatabase'

# Secret key for CSRF protection (required by Flask-WTF)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# MySQL Connection Function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Registration Form
class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s", (field.data,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                raise ValidationError('Email Already Taken')

# Login Form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store data into the database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            connection.commit()
            cursor.close()
            connection.close()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):  # user[3] is the hashed password
                session['user_id'] = user[0]  # Assuming user[0] is the user ID
                return redirect(url_for('dashboard'))
            else:
                flash("Login failed. Please check your email and password", "danger")

    return render_template('login.html', form=form)

@app.route("/dashboard")
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                return render_template('dashboard.html', user=user)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)