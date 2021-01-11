from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
# MySQL connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "contactore"
mysql = MySQL(app)

# Session
app.secret_key = "mysecretkey"

# Routes
@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY name ASC")
    mysql.connection.commit()
    data = cur.fetchall()
    return render_template("index.html", contacts=data)


@app.route("/add_contact", methods=["POST"])
def add_contact():
    if request.method == "POST":
        contact_name = request.form["contact_name"]
        contact_phone = request.form["contact_phone"]
        contact_email = request.form["contact_email"]
        contact_address = request.form["contact_address"]
        contact_relationship = request.form["contact_relationship"]
        contact_pending = request.form["contact_pending"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO contacts (name, phone, email, address, relationship, pending) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                contact_name,
                contact_phone,
                contact_email,
                contact_address,
                contact_relationship,
                contact_pending,
            ),
        )
        mysql.connection.commit()
        flash("¡Contacto agregado con éxito! :)")
        return redirect(url_for("Index"))


@app.route("/edit/<id>")
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE contactID = {0}".format(id))
    data = cur.fetchall()
    return render_template("edit_contact.html", contact=data[0])


@app.route("/update_contact/<id>", methods=["POST"])
def update_contact(id):
    if request.method == "POST":
        contact_name = request.form["contact_name"]
        contact_phone = request.form["contact_phone"]
        contact_email = request.form["contact_email"]
        contact_address = request.form["contact_address"]
        contact_relationship = request.form["contact_relationship"]
        contact_pending = request.form["contact_pending"]

        cur = mysql.connection.cursor()
        cur.execute(
            """
        UPDATE contacts
        SET name = %s,
            phone = %s,
            email = %s,
            address = %s,
            relationship = %s,
            pending = %s
            WHERE contactID = %s
            """,
            (
                contact_name,
                contact_phone,
                contact_email,
                contact_address,
                contact_relationship,
                contact_pending,
                id,
            ),
        )
        mysql.connection.commit()
        flash("Contacto actualizado :D")
        return redirect(url_for("Index"))


@app.route("/delete_contact/<id>")
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE contactID = {0}".format(id))
    mysql.connection.commit()
    flash("Contacto eliminado")
    return redirect(url_for("Index"))


@app.route("/search_contact", methods=["POST"])
def search_contact():
    if request.method == "POST":
        contact_search = request.form["contact_search"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM contacts WHERE name LIKE '%{0}%'".format(contact_search)
        )
        mysql.connection.commit()
        data = cur.fetchall()
        print(data)
        return render_template("search_contact.html", contacts=data)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
