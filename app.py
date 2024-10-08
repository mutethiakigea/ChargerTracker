from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
from flask import send_file
import qrcode
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'P@ssw0rd@321'
app.config['MYSQL_DB'] = 'ev_charger_db'

# Initialize MySQL
mysql = MySQL(app)

# Sign Up Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account:
            flash('Account already exists!')
        else:
            cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            flash('You have successfully registered!')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        
        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('charger_form'))
        else:
            flash('Incorrect email or password!')
    
    return render_template('login.html')

# EV Charger Form Route
@app.route('/charger', methods=['GET', 'POST'])
def charger_form():
    if 'loggedin' in session:
        if request.method == 'POST':
            charger_id = request.form['charger_id']
            charger_model = request.form['charger_model']
            user_id = session['id']
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO chargers (user_id, charger_id, charger_model) VALUES (%s, %s, %s)', (user_id, charger_id, charger_model))
            mysql.connection.commit()
           
        
        return render_template('charger.html')
    
    return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('You have successfully logged out.')
    return redirect(url_for('login'))

# Main Route
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/chargers')
def chargers():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM chargers WHERE user_id = %s', (session['id'],))
        chargers = cursor.fetchall()
        cursor.close()

        return render_template('chargers.html', chargers=chargers)

    return redirect(url_for('login'))

@app.route('/qr_code/<charger_id>')
def qr_code(charger_id):
    # Generate QR code for the charger ID
    charger_url = f'http://example.com/charger/{charger_id}'  # Replace with your desired URL
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(charger_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    
    # Save the QR code image to a bytes buffer
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
