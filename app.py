#use https://www.python.org/dev/peps/pep-0008/ as style guide

from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL #flask.ext.mysql is deprecated
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

#set secret key for session object to store user-specific info
app.secret_key = "/HVkkQuhZn8y7gmI"

#MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = ""
app.config["MYSQL_DATABASE_DB"] = "NotesList"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)

@app.route("/")
def main():
    #session variable user is set in validateLogin()
    if session.get("user"):
        return render_template("userhome.html")
    else:
        return render_template("index.html")

@app.route("/showSignUp")
def showSignUp():
    return render_template("signup.html")

@app.route("/showSignIn")
def showSignIn():
    #session variable user is set in validateLogin()
    if session.get("user"):
        return render_template("userhome.html")
    else:
        return render_template("signin.html")

@app.route("/userHome")
def userHome():
    #session variable user is set in validateLogin()
    if session.get("user"):
        return render_template("userhome.html")
    else:
        return render_template("error.html", error = "unauthorized access")

@app.route("/showAddNote")
def showAddNote():
    #session variable user is set in validateLogin()
    if session.get("user"):
        return render_template("addnote.html")
    else:
        return render_template("error.html", error = "unauthorized access")

@app.route("/logout")
def logout():
    #make the user variable null
    session.pop("user", None)
    return redirect("/")

#anything returned from this function is passed to jquery in signup.js and printed to console
@app.route("/getNotes", methods=["GET"])
def getNotes():
    try:
        #initialize
        message = "error: unhandled error"

        #connect to MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        #session variable user is set in validateLogin()
        if session.get("user"):
            #read user inputs
            _user = session.get("user")

            #call stored procedure sp_getNote
            cursor.callproc("sp_getUserNotes", (_user,))

            notes = cursor.fetchall()

            #create a list of dictionaries
            notes_dict = []
            #iterate through the list of tuples one tuple at a time
            for note in notes:
                #create a dictionary for each individual tuple
                note_dict = {
                    "id": note[0],
                    "date": note[2],
                    "title": note[3],
                    "post": note[4]
                }
                #append the dictionary to the larger list
                notes_dict.append(note_dict)

            #store the list of dictionaries
            message = json.dumps(notes_dict)
        else:
            #not logged in
            message = "error: unauthorized access"
    except Exception as e:
        message = "error: " + str(e)
    finally:
        return message

        #close connection to database
        cursor.close()
        conn.close()

#this function currently allows notes with empty title and post
@app.route("/addNote", methods=["POST"])
def addNote():
    try:
        #connect to MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        #session variable user is set in validateLogin()
        if session.get("user"):
            #read user inputs
            _user = session.get("user")
            _title = request.form["inputTitle"]
            _post = request.form["inputPost"]

            #call stored procedure sp_addNote
            cursor.callproc("sp_addNote", (_user, _title, _post))

            #verify that the procedure was executed successfully
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return redirect("/userHome")
            else:
                #some error occurred
                return render_template("error.html", error = "an error occurred")
        else:
            #not logged in
            return render_template("error.html", error = "unauthorized access")
    except Exception as e:
        return render_template("error.html", error = str(e))
    finally:
        #close connection to database
        cursor.close()
        conn.close()

@app.route("/validateLogin", methods=["POST"])
def validateLogin():
    try:
        #connect to MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        #read user inputs
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        #validate inputs
        if _email and _password:
            #input is good

            #call the stored procedure sp_validateLogin
            cursor.callproc("sp_validateLogin", (_email,))

            #validate user
            data = cursor.fetchall()
            if len(data) > 0:
                #check if returned hashed password matches user entered password
                if check_password_hash(str(data[0][3]), _password):
                    #set the session variable user
                    session["user"] = data[0][0]
                    return redirect("/userHome")
                else:
                    #incorrect password
                    return render_template("error.html", error = "incorrect email address or password")
            else:
                #user not found in database
                return render_template("error.html", error = "incorrect email address or password")
        else:
            #did not enter both email and password
            return json.dumps({"html":"enter required fields"})
    except Exception as e:
        return render_template("error.html", error = str(e))
    finally:
        #close connection to database
        cursor.close()
        conn.close()

#anything returned from this function is passed to jquery in signup.js and printed to console
@app.route("/signUp", methods=["POST"])
def signUp():
    try:
        #initialize
        message = "unhandled error"

        #connect to MySQL
        conn = mysql.connect()
        cursor = conn.cursor()

        #read the values input by the user
        _name = request.form["inputName"]
        _email = request.form["inputEmail"]
        _password = request.form["inputPassword"]

        #validate inputs
        if _name and _email and _password:
            #input is good

            #create hashed password with salting module
            _hashed_password = generate_password_hash(_password)

            #call the stored procedure sp_createUser
            cursor.callproc("sp_createUser", (_name, _email, _hashed_password))

            #verify that the procedure was executed successfully
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                message = "user created"
            else:
                #some error occurred
                message = str(data[0][0])
        else:
            #did not enter values in all fields
            message = "enter required fields"
    except Exception as e:
        #e will be an error message returned as a tuple from MySQL
        message = str(e[1])
    finally:
        return message

        #close connection to database
        cursor.close()
        conn.close()

app.debug = True
if __name__ == "__main__":
    app.run() #app.run(port=7000) would change port from default 5000
