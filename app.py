import mysql.connector
import re
from flask import session
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask import request
import os

from werkzeug.security import generate_password_hash


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

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form.get('input_fullname')
        email = request.form.get('input_email')
        password = request.form.get('input_password')

        # --- Validasi input (kondisi 400) ---
        if not username or not email or not password:
            flash('Semua field harus diisi')
            return redirect(url_for('register_page'))

        # --- Try-except mulai di sini ---
        try:
            conn = db
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))

            if cursor.fetchone():
                cursor.close()
                conn.close()
                flash('Username atau email sudah digunakan')
                return redirect(url_for('register_page'))

            hashed_password = generate_password_hash(password)

            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )

            conn.commit()
            cursor.close()
            conn.close()

            flash('Akun berhasil dibuat, silakan login')
            return redirect(url_for('login_page'))

        except Exception as e:
            print(f"Error saat register: {e}")  # log untuk debugging
            flash('Terjadi kesalahan pada server, coba lagi nanti')
            return redirect(url_for('register_page'))
        # --- Try-except selesai ---

    return render_template('AccountPage/Createaccount.html')




from werkzeug.security import check_password_hash

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email dan password harus diisi')
            return redirect(url_for('login_page'))

        try:
            conn = db
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if not user:
                flash('Email atau password salah')
                return redirect(url_for('login_page'))

            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']

                flash('Login berhasil')
                return redirect(url_for('test_page'))
            else:
                flash('Email atau password salah')
                return redirect(url_for('login_page'))

        except Exception as e:
            print(f"Error saat login: {e}")
            flash('Terjadi kesalahan pada server, coba lagi nanti')
            return redirect(url_for('login_page'))

    return render_template('AccountPage/Loginpage.html')

@app.route('/test_page', methods=['GET', 'POST'])
def test_page():
    return render_template('TestPage.html')

print(os.getcwd())

if __name__ == "__main__":
    app.run(debug=True)