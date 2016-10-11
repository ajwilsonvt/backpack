# use https://www.python.org/dev/peps/pep-0008/ as style guide

from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
# create the app
app = Flask(__name__)

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "NotesList"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/showSignUp")
def showSignUp():
    return render_template("signup.html")

@app.route("/signUp", methods=["POST", "GET"])
def signUp():
    try:
        # read the values input by the user
        _name = request.form["inputName"]
        _email = request.form["inputEmail"]
        _password = request.form["inputPassword"]

        # validate inputs
        if _name and _email and _password:
            # input is good, call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()

            # create hashed password with salting module
            _hashed_password = generate_password_hash(_password)

            # call the stored procedure sp_createUser
            cursor.callproc("sp_createUser",(_name,_email,_hashed_password))

            # verify that the procedure was executed successfully
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({"message":"user created"})
            else:
                return json.dumps({"error":str(data[0])})
        else:
            return json.dumps({"html":"<span>enter required fields</span>"})
    except Exception as e:
        return json.dumps({"error":str(e)})
    #finally:
        #cursor.close()
        #conn.close()

app.debug = True
if __name__ == "__main__":
    app.run()
