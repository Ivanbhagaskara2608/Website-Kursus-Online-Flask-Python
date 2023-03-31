from flask import Flask, flash, render_template, session, request, redirect, url_for
from flask_mysqldb import MySQL
app = Flask(__name__)

app.secret_key = '!@#$%'
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'prak9'
mysql = MySQL(app)

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users where email = %s and password = %s", (email, passwd))
        result = cur.fetchone()
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect(url_for('index_logout'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # hapus data session
    if "is_logged_in" in session:
        session.pop('is_logged_in', None)
        session.pop('username', None)
        # Redirect to login page
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        address = request.form['address']
        noTelp = request.form['noTelp']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username,password,email,alamat,no_telp) VALUES(%s,%s,%s,%s,%s)", (username,passwd,email,address,noTelp))
        mysql.connection.commit()
        return redirect(url_for('login'))

@app.route("/")
def index():
    flash('Anda harus login terlebih dahulu!')
    return render_template('index-login.html')

@app.route("/index")
def index_logout():
    if 'is_logged_in' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
    

@app.route("/meetings")
def meetings():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM webinar")
    data = cur.fetchall()
    cur.close()
    return render_template('meetings.html', data = data)

@app.route("/meeting-details/<string:id>")
def detail(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM webinar WHERE id = {id}")
    data = cur.fetchall()
    cur.close()
    return render_template('meeting-details.html', data = data)

@app.route('/insert', methods=['POST', 'GET'])
def customerinsert():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        notelp = request.form['notelp']
        kelas = request.form['kelas']
        alamat = request.form['alamat']
    
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO daftarkelas (nama,email,notelp,kelas,alamat) VALUES (%s,%s,%s,%s,%s)", (nama,email,notelp,kelas,alamat))
        mysql.connection.commit()
        flash('Anda berhasil daftar!')
        return redirect(url_for('index_logout'))

if __name__ == "__main__":
    app.run(debug=True)