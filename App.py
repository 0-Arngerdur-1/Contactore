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
    cur.execute("SELECT * FROM contacts")
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
        flash("¡Contacto agregado con exito! :)")
        return redirect(url_for("Index"))


@app.route("/edit/<string:id>")
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts WHERE contactID = (%s)", (id))
    mysql.connection.commit()
    data = cur.fetchall()
    print(data[0])
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
        SET name = (%s),
            phone = (%s),
            email = (%s),
            address = (%s),
            relationship = (%s),
            pending = (%s)
            WHERE contactID = (%s)
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


@app.route("/delete_contact/<string:id>")
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE contactID = (%s)", (id))
    mysql.connection.commit()
    flash("Contacto eliminado")
    return redirect(url_for("Index"))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
