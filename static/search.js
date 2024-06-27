// Get the elements from the DOM
const fileNameResultElement            = document.getElementById("name_of_file");
const productivityCheckResultElement   = document.getElementById("productive_day");
const timeToCompleteTasksResultElement = document.getElementById("time_to_complete_tasks")
const bodyResultElement                = document.getElementById("body");


// Runs when the search is made
async function submitSearch(event) {
    // Prevent form from submitting as it normally would
    event.preventDefault() 

    // Get the form data, extract the search term, make new json object
    const formData = new FormData(event.target);
    const formJson = Object.fromEntries(formData.entries());
    const jsonData = JSON.stringify(formJson);
    let search = formData.get("search");

    // Existence check for the search term
    if (search == "") {
        alert("Missing input!");
        return false;
    }

    // Regex for the allowable characters
    const regex = /^[a-zA-Z0-9!@#$%^&*()_+-=`~<>?:"{}';/.,]+$/
    if (!regex.test(search)) {
        alert("Bad search term!");
        return false;
    }

    // Send the search to the server
    const response = await fetch("/home/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: jsonData,
    })

    // Switch on the API response
    switch(response.status) {
        case 200:
            // Okay, proceed
            break;
        case 404:
            alert("Cannot find that diary entry!");
            return false
        default:
            alert("Error!")
            return false;
    }

    // Grabs the result from the server and stores it in the results const
    const result = await response.json();

    // Brings the data back to the home html file to be used.
    fileNameResultElement.innerHTML             = result.name_of_file;
    productivityCheckResultElement.innerHTML    = result.productive_day
    timeToCompleteTasksResultElement.innerHTML  = result.time_to_complete_tasks
    bodyResultElement.innerHTML                 = result.body;

    // Get the searchedForm element from the DOM
    const searchedForm = document.getElementById("searchedForm");

    // Make searchedForm visible
    searchedForm.style.display = "block";
}