import bcrypt
import mysql.connector
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from mysql.connector import Error
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

# Initialize the Flask application
app = Flask(__name__)

# MySQL Configuration
# Replace these values with your MySQL database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sakibrfa@383'
app.config['MYSQL_DB'] = 'mydatabase'

# Secret key for CSRF protection (required by Flask-WTF)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Function to establish and return a MySQL database connection
def get_db_connection():
    try:
        # Attempt to connect to the MySQL database
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return connection
    except Error as e:
        # Print any connection errors for debugging
        print(f"Error: {e}")
        return None

# Registration Form using Flask-WTF
class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    # Custom validator to check if the email already exists in the database
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

# Login Form using Flask-WTF
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Route for the homepage
@app.route("/")
def index():
    return render_template('index.html')

# Route for user registration
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # Check if form submission is valid
        # Retrieve form data
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Hash the password using bcrypt for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store user data in the database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password)
            )
            connection.commit()  # Commit the transaction
            cursor.close()
            connection.close()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Route for user login
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Check if form submission is valid
        # Retrieve form data
        email = form.email.data
        password = form.password.data

        # Verify user credentials
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()  # Fetch user data
            cursor.close()
            connection.close()

            # Check if user exists and the password matches
            if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):  # user[3] is the hashed password
                session['user_id'] = user[0]  # Assuming user[0] is the user ID
                return redirect(url_for('dashboard'))
            else:
                flash("Login failed. Please check your email and password", "danger")

    return render_template('login.html', form=form)

# Route for the user dashboard
@app.route("/dashboard")
def dashboard():
    if 'user_id' in session:  # Check if user is logged in
        user_id = session['user_id']

        # Retrieve user data from the database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                return render_template('dashboard.html', user=user)

    # Redirect to login if user is not authenticated
    return redirect(url_for('login'))

# Route for user logout
@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('user_id', None)
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)