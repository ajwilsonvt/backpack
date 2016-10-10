# use https://www.python.org/dev/peps/pep-0008/ as style guide

from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__) # , template_folder="templates")

@app.route("/")
def main():
    # return "hello world" would display hello world as text
    return render_template("index.html")

@app.route("/showSignUp")
def showSignUp():
    return render_template("signup.html")

@app.route("/signUp", methods=["POST"])
def signUp():
    # read the values input by the user
    _name = request.form["inputName"]
    _email = request.form["inputEmail"]
    _password = request.form["inputPassword"]

    # validate inputs
    if _name and _email and _password:
        return json.dumps({"html":"<span>fields are good</span>"})
    else:
        return json.dumps({"html":"<span>enter required fields</span>"})

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
# app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "NotesList"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)
# to start and stop MySQL server navigate to folder and type
# mysql.server start or mysql.server stop

conn = mysql.connect()
cursor = conn.cursor()

_hashed_password = generate_password_hash(_password)

cursor.callproc("sp_createUser", (_name, _email, _hashed_password))
data = cursor.fetchall()

def commitChanges():
    if len(data) is 0:
        conn.commit()
        return json.dumps({"message":"user created"})
    else:
        return json.dumps({"error":str(data[0])})

app.debug = True
if __name__ == "__main__":
    app.run()
