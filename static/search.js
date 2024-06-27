// Defines the const's by making equal to the html elements in the home html file.
const fileNameResultElement = document.getElementById("name_of_file");
const productivityCheckResultElement = document.getElementById("productive_day");
const timeToCompleteTasksResultElement = document.getElementById("time_to_complete_tasks")
const bodyResultElement = document.getElementById("body");


// Declares the submitSearch() function.
async function submitSearch(event) {

    // Prevents the default function of event from happening.
    event.preventDefault() 
    // Submits the search to the server.
    data = new FormData(event.target);

    const formData = new FormData(event.target);

    let search = formData.get("search");

    let regex = /^[a-zA-Z0-9!@#$%^&*()_+-=`~<>?:"{}';/.,]+$/

    if (search == ""){
        
        console.log("Error!")
        
        alert("Missing input");
        
        return false;
    }

    if (regex.test(search)){
        
        console.log("Error!")
        
        alert("Invalid input");
        
        return false;
    }

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

    // Otherwise just keep the display of the searchedForm as block. 
    else {
        x.style.display = "block";
    }
}