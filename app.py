import mysql.connector
from flask import session
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask (__name__)

app.secret_key = 'rahasia123' 

def get_db_connection():
    return mysql.connector.connect(
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
            conn = get_db_connection()
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

@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email dan password harus diisi')
            return redirect(url_for('login_page'))

        try:
            conn = get_db_connection()
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
                return redirect(url_for('Home_page'))
            else:
                flash('Email atau password salah')
                return redirect(url_for('login_page'))

        except Exception as e:
            print(f"Error saat login: {e}")
            flash('Terjadi kesalahan pada server, coba lagi nanti')
            return redirect(url_for('login_page'))

    return render_template('AccountPage/Loginpage.html')

@app.route('/Home_page')
def Home_page():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'Homepage.html',
        books=books
    )


@app.route('/logout')
def logout():
    session.clear()  # hapus semua session
    flash('Berhasil logout')
    return redirect(url_for('login_page'))





############################ dAFTAR API ############################ 

@app.route('/api/users', methods=['GET'])
def api_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, username, email FROM users"
        )

        users = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "data": users
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
@app.route('/api/register', methods=['POST'])
def api_register():

    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({
            "status": "error",
            "message": "Semua field harus diisi"
        }), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s OR email=%s",
            (username, email)
        )

        if cursor.fetchone():
            cursor.close()
            conn.close()

            return jsonify({
                "status": "error",
                "message": "Username atau email sudah digunakan"
            }), 409

        hashed_password = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
            (username, email, hashed_password)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "User berhasil dibuat"
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

@app.route('/api/login', methods=['POST'])
def api_login():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({
                "status": "error",
                "message": "Email tidak ditemukan"
            }), 404

        if not check_password_hash(
            user['password'],
            password
        ):
            return jsonify({
                "status": "error",
                "message": "Password salah"
            }), 401

        return jsonify({
            "status": "success",
            "user_id": user['id'],
            "username": user['username']
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

if __name__ == "__main__":
    app.run(debug=True)