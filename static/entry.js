// Declares the submitForm() function.
const form = document.getElementById("entryForm");

form.addEventListener("submit", async (event) => {
    // Prevent form from submitting as it normally would
    event.preventDefault();

    // Get the form data
    const data = new FormData(event.target);    
    
    // Send the form data to the API
    try {
        let response = await fetch("/entry/submit", {
            method: "POST",
            body: data
        })
        
        // Act based on what the API told us
        switch(response.status) {
            case 200:
                alert("Entry created!");
                window.location.href = "/home";
                return true;
            case 400:
                alert("Error occurred!");
                return false
            default:
                alert("Error!")
                return false;
        }

    } catch (error) {
        console.error("Error!");
        alert("Error");
        return false;
    }
})