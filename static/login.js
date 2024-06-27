// Declares the submitForm() function.
const form = document.getElementById("loginForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    let username = formData.get("username");
    let loginPassword = formData.get("loginPassword");

    let regex = /^[a-zA-Z0-9!@#$%^&*()_+-=`~<>?:"{}';/.,]+$/

    if (username == "" || loginPassword == ""){
        
        console.log("Error!")
        
        alert("Missing input");
        
        return false;
    }

    let loginFormVar = (username + loginPassword)

    if (!regex.test(loginFormVar)){
        
        console.log("Error!")
        
        alert("Invalid input");
        
        return false;
    }
    
    console.log("Submitting data.");

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
        
        switch(response.status) {
            case 200:
                alert("Ok!");
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