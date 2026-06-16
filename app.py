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

@app.route('/book/<int:id>')
def detail_book(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
 
    # Ambil data buku
    cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cursor.fetchone()
 
    # Cek apakah buku ini sudah difavoritkan oleh user yang login
    is_favorited = False
    if session.get('user_id'):
        cursor.execute(
            "SELECT id FROM favorites WHERE user_id = %s AND book_id = %s",
            (session['user_id'], id)
        )
        is_favorited = cursor.fetchone() is not None
 
    cursor.close()
    conn.close()
 
    return render_template('BookDetail.html',
                           book=book,
                           is_favorited=is_favorited)  # kirim status ke HTML

@app.route('/profile')
def profile_page():
    if not session.get('user_id'):
        return redirect(url_for('login_page'))
    return render_template('ProfilPage.html')
                           

@app.route('/logout')
def logout():
    session.clear()  # hapus semua session
    flash('Berhasil logout')
    return redirect(url_for('login_page'))




############################ PROFILE & FAVORITES API ############################

#api untuk mengambil data akun dari id
@app.route('/api/profile', methods=['GET'])
def api_profile():

    user_id = session.get('user_id')

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Belum login"
        }), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, username, email FROM users WHERE id=%s",
        (user_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "data": user
    })


@app.route('/api/favorites', methods=['GET'])
def api_get_favorites():

    user_id = session.get('user_id')

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Belum login"
        }), 401

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                books.id,
                books.title,
                books.author,
                books.cover_image
            FROM favorites
            JOIN books ON favorites.book_id = books.id
            WHERE favorites.user_id = %s
        """, (user_id,))

        favorites = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "data": favorites
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    

#berfungsi untuk delete buku dari favorit
@app.route('/api/favorites/<int:book_id>', methods=['DELETE'])
def api_remove_favorite(book_id):
    """Hapus buku dari favorit"""
    user_id = session.get('user_id')
 
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Belum login"
        }), 401
 
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
 
        cursor.execute(
            "DELETE FROM favorites WHERE user_id = %s AND book_id = %s",
            (user_id, book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
 
        return jsonify({
            "status": "success",
            "message": "Buku dihapus dari favorit"
        })
 
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# berfungsi untuk menambahkan buku ke favorit
@app.route('/api/favorites/<int:book_id>', methods=['POST'])
def api_add_favorite(book_id):
    """Tambah buku ke favorit"""
    user_id = session.get('user_id')
 
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Belum login"
        }), 401
 
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
 
        # Cek apakah sudah ada
        cursor.execute(
            "SELECT id FROM favorites WHERE user_id = %s AND book_id = %s",
            (user_id, book_id)
        )
 
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Buku sudah ada di favorit"
            }), 409
 
        # Simpan ke database
        cursor.execute(
            "INSERT INTO favorites (user_id, book_id) VALUES (%s, %s)",
            (user_id, book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
 
        return jsonify({
            "status": "success",
            "message": "Buku berhasil ditambahkan ke favorit"
        }), 201
 
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



if __name__ == "__main__":
    app.run(debug=True)