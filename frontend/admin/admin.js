let allContacts = [];
async function loadContacts() {


    const table = document.getElementById("leadTable");

    table.innerHTML = "";

    try {

        const response = await fetch("http://127.0.0.1:8000/api/v1/contacts");

        allContacts = await response.json();

        renderTable(allContacts);

        document.getElementById("totalLeads").textContent = allContacts.length;

        const ai = allContacts.filter(
            c => c.project.toLowerCase().includes("ai")
        ).length;

        const automation = allContacts.filter(
            c => c.project.toLowerCase().includes("automation")
        ).length;

        document.getElementById("aiProjects").textContent = ai;

        document.getElementById("automationProjects").textContent = automation;

    }

    catch(error){

        console.error(error);

    }

}

loadContacts();
function renderTable(contacts){

    const table = document.getElementById("leadTable");

    table.innerHTML = "";

    contacts.forEach(contact=>{

        table.innerHTML += `

        <tr>

            <td>${contact.name}</td>

            <td>${contact.company}</td>

            <td>${contact.email}</td>

            <td>${contact.project}</td>

        </tr>

        `;

    });

}
document.getElementById("searchInput").addEventListener("input", function(){

    const keyword = this.value.toLowerCase();

    const filtered = allContacts.filter(contact =>

        contact.name.toLowerCase().includes(keyword) ||

        contact.company.toLowerCase().includes(keyword) ||

        contact.email.toLowerCase().includes(keyword)

    );

    renderTable(filtered);

});