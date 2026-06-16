import mysql.connector
import re
from flask import session
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask import request
import os


app = Flask (__name__)

app.secret_key = 'rahasia123' 

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_testapi"
)

@app.route('/')
def index():
    return render_template(
        "index.html"
    )

@app.route('/register', methods=['GET','POST'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('input_fullname')
        email = request.form.get('input_email')
        password = request.form.get('input_password')

        if not username or not email or not password:
            flash('semua field harus diisi')
            return redirect(url_for('register_page'))

        conn = db
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s OR password=%s", (username, email))  

        if cursor.fetchone():
            cursor.close()
            conn.close()
            flash('username atau email sudah di gunakan')
            return redirect(url_for('register_page'))
    
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        flash('akun berhasil dibuat, silakan login')
        return redirect(url_for('login_page'))
    
    # Kalau method GET, tampilkan form
    return render_template('AccountPage/Createaccount.html')

# Route untuk menampilkan halaman login
@app.route('/login_page')
def login_page():
    return render_template('AccountPage/Loginpage.html')

print(os.getcwd())

if __name__ == "__main__":
    app.run(debug=True)