// Declares the submitForm() function.
const form = document.getElementById("form");

form.addEventListener("submit", async (event) => {
    // Prevent form from submitting as it normally would
    event.preventDefault();

    // Get the form data
    const formData = new FormData(form);

    // Defines the variables as the inputs of there respective names from the register form in the register html file.
    let password1 = formData.get("tempPassword1");
    let password2 = formData.get("tempPassword2");

    // Checks whether the first password matches with the second password entered. 
    if (password1 !== password2){
        // Prints an error message to the register page.
        alert("Password mismatch!");
        return false;
    }

    // Convert the form data to json, ready for processing
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
        
        // Action based on what API said to us
        switch(response.status) {
            case 200:
                alert("You have successfully been registered!");
                return true;
            case 400:
                alert("You already have an account or cannot sign up at this time!");
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