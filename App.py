from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'contactore'
mysql = MySQL(app)


@app.route('/')
def Index():
    return render_template("index.html")

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        contact_name = request.form['contact_name']
        contact_phone = request.form['contact_phone']
        contact_email = request.form['contact_email']
        contact_address = request.form['contact_address']
        contact_relationship = request.form['contact_relationship']
        contact_pending = request.form['contact_pending']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (name, phone, email, address, relationship, pending) VALUES (%s, %s, %s, %s, %s, %s)', (contact_name, contact_phone, contact_email, contact_address, contact_relationship, contact_pending))
        mysql.connection.commit()
        return 'contact added!'


@app.route('/edit')
def edit_contact():
    return 'edit contact'

@app.route('/delete')
def delete_contact():
    return 'delete contact'

if __name__ == '__main__':
    app.run(port = 3000,
        debug=True)

