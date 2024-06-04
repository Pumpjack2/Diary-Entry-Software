// Defines the const's by making equal to the html elements in the home html file.
const fileNameResultElement = document.getElementById("name_of_file");
const productivityCheckResultElement = document.getElementById("productive_day");
const timeToCompleteTasksResultElement = document.getElementById("time_to_complete_tasks")
const bodyResultElement = document.getElementById("body");

// Declares the submitForm() function.
function submitForm() {

    // Defines the form const as the form within the register html file.
    const form = document.getElementById("form");

    // Defines the variables as the inputs of there respective names from the register form in the register html file.
    var name = document.forms["Form"]["name"].value;
    var password1 = document.forms["Form"]["tempPassword1"].value;
    var password2 = document.forms["Form"]["tempPassword2"].value;

    // Checks whether the first password matches with the second password entered. 
    // If the passwords do not match.
    if (password1 !== password2){
        // Prints error to the terminal.
        console.log("Error!")
        // Prints an error message to the register page.
        alert("Password mis-match!");
        // Returns false.
        return false;
    }

    // Says that the data is submitting.
    console.log("Submitting data.");
    // Submits the form to the server.
    form.submit();
    // Returns true.
    return true;
}

// Declares the submitSearch() function.
async function submitSearch(event) {

    // Prevents the default function of event from happening.
    event.preventDefault() 
    // Submits the search to the server.
    data = new FormData(event.target);

    // Awaits a response from the server.
    const response = await fetch("/home/search", {
        method: "post",
        body: data,
    })

    // Grabs the result from the server and stores it in the results const.
    const result = await response.json();

    // Brings the data back to the home html file to be used.
    fileNameResultElement.innerHTML = result.name_of_file;
    productivityCheckResultElement.innerHTML = result.productive_day
    timeToCompleteTasksResultElement.innerHTML = result.time_to_complete_tasks
    bodyResultElement.innerHTML = result.body;

    // Sets the searchedFrom as x for easier use.
    var x = document.getElementById("searchedForm");

    // Changes the display of the searchedForm.
    if(x.style.display == "none") {
        // If searchedForm is none it then changes it to block.
        x.style.display = "block";
    } 

    else {

        x.style.display = "block";
    }
}

// Declares the submitEntry() function.
async function submitEntry(event) {

    
    event.preventDefault();

    console.log("working1");

    data = new FormData(event.target);

    const response = await fetch("/entry/submit", {
        method: "post",
        body: data,
    })

    // Clears the form after this function returns true and tells the user it was successful.
    if (response.status == 200) {
        window.location.href = "/home";
        return true;
    }

    alert("Failed to submit");
    return false;
}