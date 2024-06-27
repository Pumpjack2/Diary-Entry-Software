# Importing modules.
import bcrypt
import hashlib
import json
import os
from cs50 import SQL
from flask import Flask, render_template, request, redirect, session, send_file
from uuid import uuid4


PORT = 3004


# Defines the folder name for the entries to be stored.
PATH = "./diaryEntries" 
# ^^^^^^^^^^^^^^^^^^
# 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
# Capitalized variable name signifies a "constant." It's not really constant, but marks it should't change
# Constants tend to be placed at the top of the program for easy-changing
# ^^^^^^^^^^^^^^^^^^
# Pls remove this comment
# 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
# 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀


# Creates new flask app.
app = Flask(__name__)

# Creates security key for the session.
# Uses uuid4() to change the secret_key so that cookies expire once the server is closed due to the secret_key changing.
app.secret_key = str(uuid4())

# Try to connect to the database. If connection is unsuccessful the program will print an error statement to the terminal.
try:
    db = SQL("sqlite:///database.db")
except Exception:
    print("Couldn't connect to database!")
    exit(1)

# Creates a folder for the entries if a folder doesn't already exist. 
try:
    os.mkdir(PATH)
    print("Folder created! " + PATH)

# If the folder exists, show a warning, but proceed
except FileExistsError:
    print(PATH + " already exists!")



#------------------------------------------#
#------------------Routes------------------#
#------------------------------------------#

# GET route for the index page; redirect to home.
@app.route('/', methods=["get"])
def index():
    return redirect("/home", code=301)

# GET route for the login page.
@app.route('/login', methods=["get"])
def login():
    return render_template("login.html")

# POST route for the login submission
@app.route("/login/submit", methods=["post"])
def loginSubmission():

    # Retrieve the submitted form json body
    json = request.json

    # Collects values from the request and stores them within their respective variables.
    username = json["username"]
    loginPassword = json["loginPassword"]

    # Existence check
    if not (username and loginPassword):
        return "Bad Request", 400
    
    # Validating that the username and password is alphanumeric
    loginGroup = username + loginPassword
    if loginGroup.isalnum() is False:
        return "Bad Request", 400

    # Ensures the password is correct, then return a 200 OK, otherwise send a 301 REDIRECT back to login
    if check_password(username, loginPassword) is True:
        # Creates a session key so that the user can use the home page.
        session["user"] = username
        return "OK!", 200 # 200 OK
    
    else:
        return "Unauthorized", 401 # 401 UNAUTHORIZED



# GET route for the register page
@app.route('/register', methods=["get"])
def register():
    return render_template("register.html")

# POST route for the submitted data from registration
@app.route('/register/submit', methods=["post"])
def registerSubmission():

    # Retrieve the submitted form json body
    json = request.json

    # Collects values from the request and stores them within their respective variables.
    username = json["name"]
    password = json["tempPassword1"]
    confirm_password = json["tempPassword2"]

    # Existence check
    if not (username and password and confirm_password):
        return "Bad Request", 400
    
    # Validating that the username and password is alphanumeric
    registerGroup = username + password + confirm_password
    if registerGroup.isalnum() is False:
        return "Bad Request", 400

    # Checks if we failed to create a user, either due to password mismatch or already existing user
    if create_user(username, password, confirm_password) is False:
        return "Bad Request", 400

    # If we reached this point, checks have passed. We know the user has been created; 200 OK
    return "OK!", 200



# GET route for the home page.
@app.route("/home", methods=["get"])
def home():
    
    # Ensures the user has a valid session token before rendering home otherwise redirect user back to login
    if "user" in session:
        return render_template("home.html")
    else:
        return redirect("/login", code=302)
    
# POST route for the search input in the home page.
@app.route("/home/search", methods=["post"])
def homeSubmission():

    # Retrieve the submitted form json body
    json = request.json

    # Retrieves the search value from the html form.
    search = json["search"]

    # Existence check. Return 400 BAD REQUEST
    if not (search):
        return "Bad Request", 400

    # Validate search term is alphanumeric. Return 400 BAD REQUEST
    if search.isalnum() is False:
        return "Bad Request", 400

    # Hash the search term into SHA256
    response = hash_file_name(search)

    # # If we didn't find the entry, return a 404 NOT FOUND
    # if not response:
    #     return "Not found", 404

    # Try to read the content of the entry and return its data, otherwise return 404 NOT FOUND
    try:
        f = open("./diaryEntries/" + response + ".json", "r")
        return f.read(), 200
    except FileNotFoundError:
        return "Not found", 404




# GET route to render the create entry page.
@app.route("/entry", methods=["get"])
def entry():
    return render_template("entry.html")

# POST route for the submission of a new entry.
@app.route("/entry/submit", methods=["post"])
def entrySubmission():

    # Retrieving all the inputs from the html entry form.
    entry_name = request.form.get("entryName")
    productivity_check = request.form.get("productivityCheck")
    number_of_days = request.form.get("numberOfDays")
    number_of_hours = request.form.get("numberOfHours")
    number_of_minutes = request.form.get("numberOfMinutes")
    entry_body_input = request.form.get("entryBodyInput")

    # Existence check for the required fields, if any are False (don't exist), this block will run
    if not (entry_name and productivity_check and number_of_days and number_of_hours and number_of_minutes and entry_body_input and True):
        return "Bad Request", 400
    
    # Validate all entries are alphanumeric
    entryGroup = entry_name + productivity_check + number_of_days + number_of_hours + number_of_minutes + entry_body_input
    if entryGroup.isalnum() is False:
        return "Bad Request", 400



    # Sets the parameters for the fileEntry() function.
    file_entry(entry_name, productivity_check, number_of_days, number_of_hours, number_of_minutes, entry_body_input)

    # ^^^^^^^^^^^^^^^^^^
    # 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
    # You never checked if this is successful or not. Even if its not successful, it'll return a 200 OK
    # This is fine, but just be aware of it. Only reason if it'd fail if environment ran out of disk space
    # or you ran this python app on like MacOS or Linux
    # ^^^^^^^^^^^^^^^^^^
    # Pls remove this comment
    # 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
    # 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀



    # Once the entry has been entered into the database the user is redirected to the home page.
    return "OK!", 200
    #return redirect("/home", code=301)


#------------------------------------------#
#----------------Functions-----------------#
#------------------------------------------#


# Lambda function to check if the user already exists in the database, True if exist
check_database: bool = lambda name: True if db.execute("SELECT * FROM users WHERE name=(?)", name) else False

# Lambda function that hashes the search request
hash_file_name = lambda search: hashlib.sha256(search.encode()).hexdigest()



# Declares the function to validate the password creation.
def create_user(name: str, password: str, confirm_password: str) -> bool:

    # Guard clause to prevent password mismatch
    if password != confirm_password:
        print("Password mismatch!")
        return False
    
    # Guard clause to ensure the user doesn't already exist in the database
    if check_database(name) is True:
        print("User already registered!")
        return False
    
    print("Hashing password...")

    # Hash the password with use of a randomly generated salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    print(f"Hashing completed. \n Result: {hashed_password}")
    
    # By this point, we know the passwords match, they don't have an account already, and the password is securely hashed 
    
    # Finally commit the new user into the database
    db.execute("INSERT INTO users (name, password, salt) VALUES(?, ?, ?)", name, hashed_password, salt)
    return True



# Declares the function that checks whether the password given to login matches with the one in the database.
def check_password(username: str, loginPassword: str) -> bool:

    # Check if the user exists before checking their password matches
    if check_database(username) is False: return False

    # Collects the relevant information about the user from the database.
    user = db.execute("SELECT name, password, salt FROM users WHERE name=(?)", username)

    # Retrieves the salt used to hash the original password.
    salt = user[0]["salt"]

    # Hashes the password used to login with the same salt as the registered password for that user.
    login_hashed_password = bcrypt.hashpw(loginPassword.encode(), salt)

    # Returns boolean of the hashed login password compared to the database stored hash
    return login_hashed_password == user[0]["password"]



# Declares a function that creates an entry.
def file_entry(entryName, productivityCheck, numberOfDays, numberOfHours, numberOfMinutes, entryBodyInput):

    # Converts the file name into a hash
    fileName = hash_file_name(entryName)

    # Prepare dictionary ready for JSON file.
    dictionary = {
        "name_of_file": entryName,
        "productive_day": productivityCheck,
        "time_to_complete_tasks": numberOfDays + "day/s " + numberOfHours + "hour/s " + numberOfMinutes + "minute/s",
        "body": entryBodyInput
    }

    # Creates a JSON string ready for writing.
    json_object = json.dumps(dictionary, indent=4)

    # Finally open a file under the hashed file name and writes the contents into the file.
    with open("./diaryEntries/" + fileName + ".json", "w") as outfile:
        outfile.write(json_object)

    return True



# Runs the application
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=PORT)