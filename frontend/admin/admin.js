const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const token = localStorage.getItem("novixa_access_token");

// ========================================
// AUTHENTICATION
// ========================================

if (!token) {
    window.location.href = "../login.html";
}


// ========================================
// STATE
// ========================================

let allContacts = [];


// ========================================
// DOM ELEMENTS
// ========================================

const tableBody = document.getElementById("leadTable");
const searchInput = document.getElementById("searchInput");
const statusFilter = document.getElementById("statusFilter");


// ========================================
// AUTHENTICATED REQUEST HELPER
// ========================================

async function apiRequest(url, options = {}) {

    const response = await fetch(url, {
        ...options,

        headers: {
            "Authorization": `Bearer ${token}`,
            "Accept": "application/json",
            ...(options.body
                ? { "Content-Type": "application/json" }
                : {}),
            ...(options.headers || {})
        }
    });

    // Token expired / invalid
    if (response.status === 401) {

        localStorage.removeItem("novixa_access_token");

        window.location.href = "../login.html";

        throw new Error("Authentication expired.");
    }

    return response;
}


// ========================================
// LOAD CONTACTS
// ========================================

async function loadContacts() {

    tableBody.innerHTML = `
        <tr>
            <td colspan="7">
                Loading client leads...
            </td>
        </tr>
    `;

    try {

        const response = await apiRequest(
            `${API_BASE_URL}/contacts`
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (!Array.isArray(data)) {
            throw new Error("Invalid contacts response.");
        }

        allContacts = data;

        updateStats();
        applyFilters();

    } catch (error) {

        console.error(
            "[Novixa Admin] Failed to load contacts:",
            error
        );

        tableBody.innerHTML = `
            <tr>
                <td colspan="7">
                    Unable to load leads.
                    Please check that the Novixa API is running.
                </td>
            </tr>
        `;
    }
}


// ========================================
// UPDATE DASHBOARD STATISTICS
// ========================================

function updateStats() {

    const totalLeads = allContacts.length;

    const aiProjects = allContacts.filter(contact =>
        (contact.project || "")
            .toLowerCase()
            .includes("ai")
    ).length;

    const automationProjects = allContacts.filter(contact =>
        (contact.project || "")
            .toLowerCase()
            .includes("automation")
    ).length;

    document.getElementById("totalLeads").textContent =
        totalLeads;

    document.getElementById("aiProjects").textContent =
        aiProjects;

    document.getElementById("automationProjects").textContent =
        automationProjects;
    const newLeads =
     allContacts.filter(contact =>
          (contact.status || "")
              .toLowerCase() === "new"
        ).length;

    document.getElementById("newLeads")
        .textContent = newLeads;
}


// ========================================
// FILTER CONTACTS
// ========================================

function applyFilters() {

    const keyword =
        searchInput.value
            .toLowerCase()
            .trim();

    const selectedStatus =
        statusFilter.value
            .toLowerCase();

    const filteredContacts =
        allContacts.filter(contact => {

            const name =
                (contact.name || "").toLowerCase();

            const company =
                (contact.company || "").toLowerCase();

            const email =
                (contact.email || "").toLowerCase();

            const status =
                (contact.status || "").toLowerCase();

            const matchesSearch =
                name.includes(keyword) ||
                company.includes(keyword) ||
                email.includes(keyword);

            const matchesStatus =
                !selectedStatus ||
                status === selectedStatus;

            return matchesSearch && matchesStatus;
        });

    renderTable(filteredContacts);
}


// ========================================
// RENDER TABLE
// ========================================

function renderTable(contacts) {

    tableBody.innerHTML = "";

    if (contacts.length === 0) {

        tableBody.innerHTML = `
            <tr>
                <td colspan="7">
                    No client leads found.
                </td>
            </tr>
        `;

        return;
    }

    contacts.forEach(contact => {

        const row = document.createElement("tr");

        const status =
            (contact.status || "new").toLowerCase();

        row.innerHTML = `

            <td>
                ${escapeHTML(contact.name)}
            </td>

            <td>
                ${escapeHTML(contact.company)}
            </td>

            <td>
                ${escapeHTML(contact.email)}
            </td>

            <td>
                ${escapeHTML(contact.project)}
            </td>

            <td>

                <select
                    class="status-select status-${escapeHTML(status)}"
                    data-id="${contact.id}"
                    aria-label="Change lead status"
                >

                    <option value="new"
                        ${status === "new" ? "selected" : ""}>
                        New
                    </option>

                    <option value="contacted"
                        ${status === "contacted" ? "selected" : ""}>
                        Contacted
                    </option>

                    <option value="qualified"
                        ${status === "qualified" ? "selected" : ""}>
                        Qualified
                    </option>

                    <option value="closed"
                        ${status === "closed" ? "selected" : ""}>
                        Closed
                    </option>

                </select>

            </td>

            <td>
                ${formatDate(contact.created_at)}
            </td>

            <td>

                <button
                    class="delete-button"
                    data-id="${contact.id}"
                    type="button"
                >
                    Delete
                </button>

            </td>

        `;

        tableBody.appendChild(row);
    });

    attachRowActions();
}


// ========================================
// ROW ACTIONS
// ========================================

function attachRowActions() {

    const statusButtons =
        document.querySelectorAll(".status-select");

    statusButtons.forEach(select => {

        select.addEventListener(
            "change",
            async function () {

                const contactId =
                    this.dataset.id;

                const newStatus =
                    this.value;

                await updateContactStatus(
                    contactId,
                    newStatus,
                    this
                );
            }
        );
    });


    const deleteButtons =
        document.querySelectorAll(".delete-button");

    deleteButtons.forEach(button => {

        button.addEventListener(
            "click",
            async function () {

                const contactId =
                    this.dataset.id;

                await deleteContact(
                    contactId,
                    this
                );
            }
        );
    });
}


// ========================================
// UPDATE CONTACT STATUS
// ========================================

async function updateContactStatus(
    contactId,
    newStatus,
    selectElement
) {

    const oldStatus =
        selectElement.dataset.previousStatus ||
        "";

    selectElement.disabled = true;

    try {

        const response = await apiRequest(
            `${API_BASE_URL}/contacts/${contactId}/status`,
            {
                method: "PATCH",

                body: JSON.stringify({
                    status: newStatus
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to update status."
            );
        }

        // Update local state
        const contact =
            allContacts.find(
                item => item.id === Number(contactId)
            );

        if (contact) {
            contact.status = newStatus;
        }

        selectElement.dataset.previousStatus =
            newStatus;

        selectElement.className =
            `status-select status-${newStatus}`;

        console.log(
            `[Novixa Admin] Contact ${contactId} status changed to ${newStatus}`
        );

    } catch (error) {

        console.error(
            "[Novixa Admin] Status update failed:",
            error
        );

        alert(
            `Unable to update status.\n\n${error.message}`
        );

        // Restore previous value if available
        if (oldStatus) {
            selectElement.value = oldStatus;
        }

    } finally {

        selectElement.disabled = false;
    }
}


// ========================================
// DELETE CONTACT
// ========================================

async function deleteContact(
    contactId,
    buttonElement
) {

    const contact =
        allContacts.find(
            item => item.id === Number(contactId)
        );

    if (!contact) {
        return;
    }

    const confirmed =
        window.confirm(
            `Delete the lead from ${contact.name || "this client"}?\n\n` +
            `This will permanently remove the lead from the database.`
        );

    if (!confirmed) {
        return;
    }

    buttonElement.disabled = true;
    buttonElement.textContent = "Deleting...";

    try {

        const response = await apiRequest(
            `${API_BASE_URL}/contacts/${contactId}`,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to delete contact."
            );
        }

        // Remove from local state
        allContacts =
            allContacts.filter(
                item => item.id !== Number(contactId)
            );

        updateStats();
        applyFilters();

        console.log(
            `[Novixa Admin] Contact ${contactId} deleted.`
        );

    } catch (error) {

        console.error(
            "[Novixa Admin] Delete failed:",
            error
        );

        alert(
            `Unable to delete lead.\n\n${error.message}`
        );

        buttonElement.disabled = false;
        buttonElement.textContent = "Delete";
    }
}


// ========================================
// FORMAT DATE
// ========================================

function formatDate(dateValue) {

    if (!dateValue) {
        return "—";
    }

    const date = new Date(dateValue);

    if (Number.isNaN(date.getTime())) {
        return "—";
    }

    return date.toLocaleString(
        undefined,
        {
            dateStyle: "medium",
            timeStyle: "short"
        }
    );
}


// ========================================
// BASIC HTML ESCAPING
// ========================================

function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ========================================
// SEARCH
// ========================================

searchInput.addEventListener(
    "input",
    applyFilters
);


// ========================================
// STATUS FILTER
// ========================================

statusFilter.addEventListener(
    "change",
    applyFilters
);


// ========================================
// LOGOUT
// ========================================

const logoutButton =
    document.getElementById("logoutButton");

if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        function () {

            localStorage.removeItem(
                "novixa_access_token"
            );

            window.location.href =
                "../login.html";
        }
    );
}


// ========================================
// INITIAL LOAD
// ========================================

loadContacts();