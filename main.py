# Importing modules.
import bcrypt
import hashlib
import json
import os
from cs50 import SQL
from flask import Flask, render_template, request, redirect, session, send_file
from uuid import uuid4

# Creates new flask app.
app = Flask(__name__)

# Creates security key for the session.
# Uses uuid4() to change the secret_key so that cookies expire once the server is closed due to the secret_key changing.
app.secret_key = str(uuid4())

# Try's to connect to the database.
try:

    # Defines the SQL database as the string db
    db = SQL("sqlite:///database.db")

# If connection is unsuccessful the program will print an error statement to the terminal.
except Exception:

    # Displays error message if connection is not established.
    print("Couldn't connect to database!")
    # Terminates the runtime of the program.
    exit()

# Defines the folder name for the entries to be stored.
path = './diaryEntries'

# When the code starts up.
# Creates a folder for the entries if a folder doesn't already exist. 
try:

    # Makes a folder based of the path string.
    os.mkdir(path)

    # Print to the terminal that the path was created.
    print("Folder created! " + path)

# Sends a message that a folder already exists to the terminal.
except FileExistsError:

    # Prints to the terminal that the folder already exists.
    print(path + " already exists!")

# Creates a route for the register page.
@app.route('/login', methods=["get"])
def homepage():

    # Returns the html code back to the route.
    return render_template("login.html")

# Creates a route for the submitted data form the register.
@app.route('/register/submit', methods=["post"])
def submit():

    # Collects values from the html inputs and stores them 
    # within their respective variables.
    name = request.form.get("name")
    tempPassword1 = request.form.get("tempPassword1")
    tempPassword2 = request.form.get("tempPassword2")

    # Sets the parameters for the validatePassword() and checkDatabase() function.
    validatePassword(name, tempPassword1, tempPassword2)
    checkDatabase(name)
    
    # Returns the html code back to the route.
    return redirect("/login", code=301)

# Creates a route for the login
@app.route('/register', methods=["get"])
def register():

    # Returns the html code back to the login.
    return render_template("register.html")

# Create a route for the submission
@app.route("/login/submit", methods=["post"])
def loginSubmission():
    
    # Collects values from the html inputs and stores them 
    # within their respective variables.
    username = request.form.get("username")
    loginPassword = request.form.get("loginPassword")

    # Sets the parameters for the checkPassword() function.
    if checkPassword(username, loginPassword) is True:

        # Creates a session key so that the user can use the home page.
        session["user"] = username

        # Redirect the user to the home page.
        return redirect("/home", code=301)
    
    else:

        # If the password is incorrect redirects the user back to the login page.
        return redirect("/login", code=301)

# Creates a route for the home page.
@app.route("/home", methods=["get"])
def home():

    # checks if the user has a session key before allowing the user to use the page.
    if "user" in session:
        
        # If the user has a session key the page is rendered.
        return render_template("home.html")
    
    # Otherwise the user is sent back to the login page.
    else:
        return redirect("/login")
    
# Creates a route for the search input in the home page.
@app.route("/home/search", methods=["post"])
def homeSubmission():

    # Retrieves the search request from the html form.
    search = request.form.get("search")

    # Runs the searchDatabase() function and returns the response to the string.
    response = searchDatabase(search)

    # Checks to see if a response was returned.
    if response:

        # If response is returned then python opens the file and returns its contents to the front-end
        f = open("./diaryEntries/" + response + ".json", "r")

        # Returns the searched file.
        return f.read()
    
    # If a file wasn't found then it redirects the user back to the home page.
    else:

        # Redirects back to the home page.
        return redirect("/home", code=301)

# Creates a route to  render the create entry page.
@app.route("/entry", methods=["get"])
def entry():

    # Renders the html code for the create entry page.
    return render_template("entry.html")

# Creates a route for the submission of a new entry.
@app.route("/entry/submit", methods=["post"])
def entrySubmission():

    # Retrieving all the inputs from the html entry form.
    entryName = request.form.get("entryName")
    productivityCheck = request.form.get("productivityCheck")
    numberOfDays = request.form.get("numberOfDays")
    numberOfHours = request.form.get("numberOfHours")
    numberOfMinutes = request.form.get("numberOfMinutes")
    entryBodyInput = request.form.get("entryBodyInput")

    # Sets the parameters for the fileEntry() function.
    fileEntry(entryName, productivityCheck, numberOfDays, numberOfHours, numberOfMinutes, entryBodyInput)
    
    # Once the entry has been entered into the database the user is redirected to the home page.
    return redirect("/home", code=301)

# Creates a route for the css.
@app.route('/', methods=["get"])
def styleRegister():

    # Returns the css file to the route.
    return render_template("login.html")


#------------------------------------------#
#----------------Functions-----------------#
#------------------------------------------#


def checkDatabase(name):

    #!!!NEED TO WORK ON THIS!!!

    #print("Creating new table.")
    #db.execute("CREATE TABLE users (name, password, salt, entries)")
    check = db.execute("SELECT * FROM users WHERE name=(?)", name)
    
    # If the user doesn't exist in the database.
    if check == []:

        # Returns False.
        return False
    
    # If the user does exist.
    else:

        # Returns True.
        return True

# Declares the function to validate the password creation.
def validatePassword(name, tempPassword1, tempPassword2):

    # Declares an if statement that checks that tempPassword1 is the same as tempPassword2.
    if tempPassword1 == tempPassword2:

        # Defines the password variable to be the tempPassword1 that 
        # is encoded into bytes using encode().
        password = tempPassword1.encode()

        # Notifies the terminal that there is a password match
        # and that it has begun converting the password into a hash.
        print("Password Match")
        print("Converting password to hash...")

        # Defines the salt variable as a randomly generate salt using bcrypt.gensalt(),
        # also defines the hashPsw as the result of the password and the salt
        # that gets mixed together using bcrypt.hashpw().
        salt = bcrypt.gensalt()
        hashedPsw = bcrypt.hashpw(password, salt)

        # Notifies the terminal that the password has been converted 
        # into a hash and prints the result.
        print("Password converted to hash.")
        print("Result: ", hashedPsw)
        
        # Retrieves the response from the checkDatabase() function once it has checked the database for the user 
        # wanting to register to ensure the dont already exist in the database.
        response = checkDatabase(name)

        # If the person doesn't exist in the database.
        if response is False:

            # Inserts the name, hashed password and the salt that was used
            # to hash the password in the respective columns within the SQL database.
            db.execute("INSERT INTO users (name, password, salt) VALUES(?, ?, ?)", name, hashedPsw, salt)

        # If the user already exists in the database
        if response is True:
            # Notifies the terminal that the table exists for that user.
            user = db.execute("SELECT * FROM users WHERE name=(?)", name)
            print("Table already exists for " + user)

    # If the tempPassword isn't the same as tempPassword.
    else:
        # Notifies the terminal that there is a password mismatch and to try again.
        print("Password mismatch.")
        print("Please try again.")

# Declares the function that checks whether the password given to login matches with the one in the database.
def checkPassword(username, loginPassword: str):

    # Collects the relevant information about the user from the database.
    resp = db.execute("SELECT name, password, salt FROM users WHERE name=(?)", username)

    # Retrieves the salt used to hash the original password.
    tempsalt = resp[0]["salt"]

    # Hashes the password used to login with the same salt as the registered password for that user.
    loginHashedPsw = bcrypt.hashpw(loginPassword.encode(), tempsalt)

    # Returns the hashed login password is equal to the hashed registered password.
    # Returning True or False.
    return loginHashedPsw == resp[0]["password"]

# Declares a function that hashes the search request the same way the files are.
def searchDatabase(search):

    # Converts the searched request into a hashed search string.
    searchHash = hashlib.sha256(search.encode()).hexdigest()

    # Returns the hashed search string outcome.
    return searchHash

# Declares a function that creates an entry.
def fileEntry(entryName, productivityCheck, numberOfDays, numberOfHours, numberOfMinutes, entryBodyInput):

    # Converts the file name into a hash.
    fileName = hashlib.sha256(entryName.encode()).hexdigest()

    # Creating a dictionary so that it can be put into a JSON file.
    dictionary = {
        "name_of_file": entryName,
        "productive_day": productivityCheck,
        "time_to_complete_tasks": numberOfDays + "day/s " + numberOfHours + "hour/s " + numberOfMinutes + "minute/s",
        "body": entryBodyInput
    }

    # Creates a string that will write the dictionary with indents.
    json_object = json.dumps(dictionary, indent=4)

    # Finally open a file under the hashed file name and writes the contents into the file.
    with open("./diaryEntries/" + fileName + ".json", "w") as outfile:
        outfile.write(json_object)

# Runs the application.
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)