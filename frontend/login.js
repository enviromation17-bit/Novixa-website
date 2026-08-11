const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const username =
        document.getElementById("username").value;

    const password =
        document.getElementById("password").value;

    const message =
        document.getElementById("loginMessage");

    message.textContent = "";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/v1/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            message.textContent =
                data.detail || "Login failed.";

            return;
        }

        localStorage.setItem(
            "novixa_access_token",
            data.access_token
        );

        window.location.href = "admin/index.html";

    } catch (error) {

        console.error(error);

        message.textContent =
            "Unable to connect to the server.";
    }

});