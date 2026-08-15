/* ============================================================
   NOVIXA — CONTACT FORM
   Client-side validation + submission to the existing FastAPI
   contact API. No mock backend is introduced here; this simply
   posts the form payload to the configured endpoint.

   To point at a different backend, set the endpoint below or
   define window.NOVIXA_CONTACT_ENDPOINT before this script runs.
   ============================================================ */

(function () {
    "use strict";

    const form = document.getElementById("contact-form");
    if (!form) return;

    const statusEl = document.getElementById("form-status");
    const submitBtn = document.getElementById("contact-submit");

    /* Endpoint matches the existing FastAPI route (see backend/app/routes/v1/contact.py). */
    const ENDPOINT =
        window.NOVIXA_CONTACT_ENDPOINT || "http://127.0.0.1:8000/api/v1/contacts";

    const setStatus = (message, type) => {
        if (!statusEl) return;
        statusEl.textContent = message;
        statusEl.classList.remove("is-success", "is-error");
        if (type) statusEl.classList.add("is-" + type);
    };

    const markInvalid = (field, invalid) => {
        if (field) field.setAttribute("aria-invalid", String(invalid));
    };

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const fields = {
            name: document.getElementById("name"),
            company: document.getElementById("company"),
            email: document.getElementById("email"),
            project: document.getElementById("project"),
            message: document.getElementById("message"),
        };

        /* ---- Basic client-side validation (mirrors backend schema) ---- */
        let firstInvalid = null;
        const checks = {
            name: fields.name.value.trim().length >= 2,
            company: fields.company.value.trim().length >= 2,
            email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(fields.email.value.trim()),
            project: fields.project.value.trim().length >= 3,
            message: fields.message.value.trim().length >= 10,
        };

        Object.keys(checks).forEach((key) => {
            const ok = checks[key];
            markInvalid(fields[key], !ok);
            if (!ok && !firstInvalid) firstInvalid = fields[key];
        });

        if (firstInvalid) {
            setStatus("Please complete the highlighted fields correctly.", "error");
            firstInvalid.focus();
            return;
        }

        const payload = {
            name: fields.name.value.trim(),
            company: fields.company.value.trim(),
            email: fields.email.value.trim(),
            project: fields.project.value.trim(),
            message: fields.message.value.trim(),
        };

        /* ---- Submit ---- */
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.dataset.label = submitBtn.textContent;
            submitBtn.textContent = "Sending…";
        }
        setStatus("Sending your message…", null);

        try {
            const response = await fetch(ENDPOINT, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            const result = await response.json().catch(() => ({}));

            if (!response.ok) {
                throw new Error(result.detail || "Request failed");
            }

            setStatus(
                result.message ||
                    "Thank you — we have received your request and will respond within 24 hours.",
                "success"
            );
            form.reset();
            Object.values(fields).forEach((f) => markInvalid(f, false));
        } catch (error) {
            setStatus(
                "We couldn't send your message right now. Please try again, or email hello@novixa.com.",
                "error"
            );
            console.log("[v0] Contact form submission failed:", error.message);
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = submitBtn.dataset.label || "Send Message";
            }
        }
    });

    /* Clear invalid state as the user corrects a field. */
    form.querySelectorAll("input, select, textarea").forEach((el) => {
        el.addEventListener("input", () => markInvalid(el, false));
    });
})();
