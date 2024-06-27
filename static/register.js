// Declares the submitForm() function.
const form = document.getElementById("form");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    // Defines the form const as the form within the register html file.

    const formData = new FormData(form);

    // Defines the variables as the inputs of there respective names from the register form in the register html file.
    //var name = formData.get("username");
    let password1 = formData.get("tempPassword1");
    let password2 = formData.get("tempPassword2");


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

    const formJson = Object.fromEntries(formData.entries());
    const jsonData = JSON.stringify(formJson);
    try {
        let response = await fetch("/register/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: jsonData
        })
        
        switch(response.status) {
            case 200:
                alert("Ok!");
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