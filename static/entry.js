// Declares the submitForm() function.
const form = document.getElementById("entryForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = new FormData(event.target);    
    
    try {
        let response = await fetch("/entry/submit", {
            method: "post",
            body: data
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