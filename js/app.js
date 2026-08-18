/* ============================================================
   NOVIXA — CONTACT FORM
   Frontend ↔ FastAPI integration
   Endpoint: POST /api/v1/contacts
   ============================================================ */

(function () {
    "use strict";

    const form = document.getElementById("contact-form");

    /* Contact form may not exist on every page. */
    if (!form) return;

    const statusEl = document.getElementById("form-status");
    const submitBtn = document.getElementById("contact-submit");

    /*
       Development API endpoint.

       Change this to your production API URL when Novixa
       is deployed.
    */
    const ENDPOINT =
        window.NOVIXA_CONTACT_ENDPOINT ||
        "http://127.0.0.1:8000/api/v1/contacts";


    /* ========================================================
       STATUS MESSAGE
    ======================================================== */

    function setStatus(message, type = null) {

        if (!statusEl) return;

        statusEl.textContent = message;

        statusEl.classList.remove(
            "is-success",
            "is-error"
        );

        if (type) {
            statusEl.classList.add("is-" + type);
        }
    }


    /* ========================================================
       FIELD VALIDATION
    ======================================================== */

    function markInvalid(field, invalid) {

        if (!field) return;

        field.setAttribute(
            "aria-invalid",
            String(invalid)
        );
    }


    function validateFields(fields) {

        const checks = {

            name:
                fields.name.value.trim().length >= 2,

            company:
                fields.company.value.trim().length >= 2,

            email:
                /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
                    fields.email.value.trim()
                ),

            project:
                fields.project.value.trim().length >= 3,

            message:
                fields.message.value.trim().length >= 10
        };


        let firstInvalid = null;


        Object.keys(checks).forEach((key) => {

            const valid = checks[key];

            markInvalid(
                fields[key],
                !valid
            );

            if (!valid && !firstInvalid) {
                firstInvalid = fields[key];
            }

        });


        return firstInvalid;
    }


    /* ========================================================
       SUBMIT FORM
    ======================================================== */

    form.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const fields = {

                name:
                    document.getElementById("name"),

                company:
                    document.getElementById("company"),

                email:
                    document.getElementById("email"),

                project:
                    document.getElementById("project"),

                message:
                    document.getElementById("message")
            };


            /* -----------------------------------------------
               Make sure all expected fields exist.
            ------------------------------------------------ */

            const missingField = Object.values(fields)
                .some((field) => !field);


            if (missingField) {

                console.error(
                    "Novixa contact form: required field missing."
                );

                setStatus(
                    "The contact form is not configured correctly.",
                    "error"
                );

                return;
            }


            /* -----------------------------------------------
               Client-side validation
            ------------------------------------------------ */

            const firstInvalid =
                validateFields(fields);


            if (firstInvalid) {

                setStatus(
                    "Please complete the highlighted fields correctly.",
                    "error"
                );

                firstInvalid.focus();

                return;
            }


            /* -----------------------------------------------
               Build payload matching FastAPI ContactRequest
            ------------------------------------------------ */

            const payload = {

                name:
                    fields.name.value.trim(),

                company:
                    fields.company.value.trim(),

                email:
                    fields.email.value.trim(),

                project:
                    fields.project.value.trim(),

                message:
                    fields.message.value.trim()
            };


            /* -----------------------------------------------
               Loading state
            ------------------------------------------------ */

            if (submitBtn) {

                submitBtn.disabled = true;

                submitBtn.dataset.originalLabel =
                    submitBtn.textContent;

                submitBtn.textContent =
                    "Sending…";
            }


            setStatus(
                "Sending your message…"
            );


            try {

                /* -------------------------------------------
                   Send request to FastAPI
                ------------------------------------------- */

                const response = await fetch(
                    ENDPOINT,
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(payload)
                    }
                );


                /* -------------------------------------------
                   Try to read JSON response
                ------------------------------------------- */

                const result =
                    await response.json()
                        .catch(() => ({}));


                /* -------------------------------------------
                   Handle HTTP errors
                ------------------------------------------- */

                if (!response.ok) {

                    let errorMessage =
                        "Unable to send your message.";

                    /*
                       FastAPI validation errors normally
                       return a "detail" field.
                    */

                    if (response.status === 422) {

                        errorMessage =
                            "Please check the information you entered.";

                    } else if (response.status === 429) {

                        errorMessage =
                            "Too many requests. Please wait a moment and try again.";

                    } else if (result.detail) {

                        errorMessage =
                            typeof result.detail === "string"
                                ? result.detail
                                : errorMessage;
                    }

                    throw new Error(errorMessage);
                }


                /* -------------------------------------------
                   Successful response
                ------------------------------------------- */

                setStatus(
                    result.message ||
                    "Thank you. We have received your project request and will get back to you soon.",
                    "success"
                );


                /* Reset form after successful submission. */

                form.reset();


                /* Clear validation states. */

                Object.values(fields).forEach(
                    (field) => markInvalid(field, false)
                );


            } catch (error) {

                console.error(
                    "[Novixa] Contact submission failed:",
                    error
                );


                /*
                   Distinguish connection failure from
                   an API-generated error.
                */

                if (
                    error instanceof TypeError
                ) {

                    setStatus(
                        "We couldn't connect to the Novixa server. Please try again shortly.",
                        "error"
                    );

                } else {

                    setStatus(
                        error.message ||
                        "We couldn't send your message right now. Please try again.",
                        "error"
                    );
                }


            } finally {

                /* -------------------------------------------
                   Restore submit button
                ------------------------------------------- */

                if (submitBtn) {

                    submitBtn.disabled = false;

                    submitBtn.textContent =
                        submitBtn.dataset.originalLabel ||
                        "Send Message";
                }
            }

        }
    );


    /* ========================================================
       CLEAR INVALID STATE WHILE USER CORRECTS INPUT
    ======================================================== */

    form.querySelectorAll(
        "input, select, textarea"
    ).forEach((field) => {

        field.addEventListener(
            "input",
            () => markInvalid(field, false)
        );

        field.addEventListener(
            "change",
            () => markInvalid(field, false)
        );

    });


})();