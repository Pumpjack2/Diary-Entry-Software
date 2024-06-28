// Declares the submitForm() function.
const form = document.getElementById("loginForm");

form.addEventListener("submit", async (event) => {
    // Prevent form from submitting as it normally would
    event.preventDefault();

    // Get the form data
    const formData = new FormData(form);

    // Get the username and password
    const username = formData.get("username");
    const loginPassword = formData.get("loginPassword");

    // Define a regex for allowed characters
    const regex = /^[a-zA-Z0-9!@#$%^&*()_+-=`~<>?:"{}';/.,]+$/

    // Check if the username or password is undefined
    if (username == "" || loginPassword == ""){
        alert("Missing input");
        return false;
    }

    // Ensure the username and password does not contain disallowed characters
    const loginFormVar = (username + loginPassword)
    if (!regex.test(loginFormVar)){
        alert("Invalid input");
        return false;
    }

    // Convert the form data to json ready for processing
    const formJson = Object.fromEntries(formData.entries());
    const jsonData = JSON.stringify(formJson);
    try {
        let response = await fetch("/login/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: jsonData
        })
        
        // Act based on what the API said to us
        switch(response.status) {
            case 200:
                window.location.href = "/home";
                return true;
            case 400:
                alert("Bad input!");
                return false
            case 401:
                alert("Username or password incorrect!");
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