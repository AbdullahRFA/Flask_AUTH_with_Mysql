# setup vitual environment

    python3 -m venv .venv

# active source

    source .venv/bin/active

# install flask

    pip install flask

# install flask-wtf

    pip install flask-wtf

# 1. Install pkg-config:

    brew install pkg-config

# 2. Install MySQL Development Libraries:

    brew install mysql-client

# Flask MySQL Web Application

This is a simple web application built with Flask and MySQL that allows users to register, log in, and view their dashboard. It demonstrates the basic use of Flask, MySQL integration, and user authentication using Flask-WTF forms.

# Table of Contents

1. Requirements
2. Installation
3. Environment Setup
4. Application Overview
5. Usage
6. Contributing
7. License

# Requirements

Before you begin, ensure you have met the following requirements:

1.  Python 3.x

2.  Flask
3.  Flask-WTF
4.  Flask-MySQL
5.  bcrypt
6.  MySQL Server

# Installation

To install and set up the project, follow these steps: 1. Clone the repository:

git clone https://github.com/AbdullahRFA/Flask_AUTH_with_Mysql.git

# 2. Set up a virtual environment (optional but recommended):

    python -m venv venv

# 3. Activate the virtual environment:

• For Windows:

        .\venv\Scripts\activate

• For Mac/Linux:

    source venv/bin/activate

# 4.Install dependencies:

        pip install -r requirements.txt

This will install all necessary Python libraries including Flask, Flask-WTF, MySQL Connector, and bcrypt.

Environment Setup

# MySQL Configuration

# 1. Set up MySQL Database:

Ensure you have MySQL installed and running. Then, create a new database called mydatabase.

CREATE DATABASE mydatabase;

# 2. Create a users table:

Create a table to store user data (name, email, password):

    CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
    );

# 3. Database Configuration:

In the app.py file, set the MySQL connection parameters such as MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DB according to your local setup.

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'your_password_here'
    app.config['MYSQL_DB'] = 'mydatabase'

# Application Overview

## The Flask MySQL application consists of the following:

**Home Page**: A simple home page that introduces the application

**Registration Page**: Users can register by providing their name, email, and password.

**Login Page**: Registered users can log in with their credentials.

**Dashboard Page**: Displays user information after successful login.

**Logout**: Allows users to log out and clear their session.

# Routes:

    • /: Home Page
    • /register: Registration Page
    • /login: Login Page
    • /dashboard: Dashboard Page (requires login)
    • /logout: Log out the user

# Forms:

Registration Form: Contains fields for name, email, and password.

Login Form: Contains fields for email and password.

# Security:

Passwords are hashed using bcrypt before being stored in the database to ensure secure authentication.
Flask-WTF is used to handle form validation and CSRF protection.

# Usage 1. Run the Application:

After completing the setup, you can run the Flask application with:

    python app.py

# Access the Application:

Once the application is running, you can access it in your web browser at http://127.0.0.1:5000/.

# Features:

    • Registration: You can create a new user account.
    • Login: Registered users can log in and view their dashboard.
    • Dashboard: Displays user information.
    • Logout: After logging in, you can log out and the session will end.

# Contributing

Contributions are welcome! If you want to contribute to the project, follow these steps:

1. Fork the repository.

2. Create a new branch (git checkout -b feature-branch).

3. Make your changes.

4. Commit your changes (git commit -m 'Add new feature').

5. Push to the branch (git push origin feature-branch).

6. Open a pull request.

# License

This project is licensed under the MIT License - see the LICENSE file for details.

# Additional Notes

• Ensure that your MySQL server is running before starting the application.

• The application uses Flask sessions for storing user login status.

• You can customize the CSS in the app.html and dashboard.html
templates to make the app look more professional as per your preference.

This README file should help guide users through the installation and usage of your project and provide clear instructions for setting up the environment, installing dependencies, and contributing to the project.
