const form = document.getElementById("contact-form");

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const data = {

        name: document.getElementById("name").value,

        company: document.getElementById("company").value,

        email: document.getElementById("email").value,

        project: document.getElementById("project").value,

        message: document.getElementById("message").value

    };

    try {

        const response = await fetch("http://127.0.0.1:8000/api/v1/contact", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(data)

        });

        const result = await response.json();

        alert(result.message);

        form.reset();

    }

    catch (error) {

        alert("Server connection failed.");

        console.log(error);

    }

});