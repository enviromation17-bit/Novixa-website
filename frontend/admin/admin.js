const token =
    localStorage.getItem("novixa_access_token");

if (!token) {
    window.location.href = "../login.html";
}

let allContacts = [];

async function loadContacts() {

    const table = document.getElementById("leadTable");

    table.innerHTML = "";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/v1/contacts",
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        } 
);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        allContacts = await response.json();

        updateStats();
        filterContacts();

    } catch (error) {

    console.error("Failed to load contacts:", error);

    table.innerHTML = `
        <tr>
            <td colspan="6">
                Unable to load leads.
                Please check your connection and try again.
            </td>
        </tr>
        `;

    }

} 



function updateStats() {

    document.getElementById("totalLeads").textContent =
        allContacts.length;

    const ai = allContacts.filter(contact =>
        (contact.project || "")
            .toLowerCase()
            .includes("ai")
    ).length;

    const automation = allContacts.filter(contact =>
        (contact.project || "")
            .toLowerCase()
            .includes("automation")
    ).length;

    document.getElementById("aiProjects").textContent = ai;

    document.getElementById("automationProjects").textContent =
        automation;
}


function applyFilters() {

    const keyword =
        document.getElementById("searchInput").value
        .toLowerCase()
        .trim();

    const selectedStatus =
        document.getElementById("statusFilter").value
        .toLowerCase();

    const filtered = allContacts.filter(contact => {

        const name = (contact.name || "").toLowerCase();
        const company = (contact.company || "").toLowerCase();
        const email = (contact.email || "").toLowerCase();
        const status = (contact.status || "").toLowerCase();

        const matchesSearch =
            name.includes(keyword) ||
            company.includes(keyword) ||
            email.includes(keyword);

        const matchesStatus =
            !selectedStatus ||
            status === selectedStatus;

        return matchesSearch && matchesStatus;

    });

    renderTable(filtered);
}

document
    .getElementById("searchInput")
    .addEventListener("input", applyFilters);

document
    .getElementById("statusFilter")
    .addEventListener("change", applyFilters);