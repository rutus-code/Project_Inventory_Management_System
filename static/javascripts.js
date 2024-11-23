/**
 * Created By : Rutu Shah
 * Created Date : 18th November 2024
 * Hello professor, this is my javascript file trying to make only one so I can demonstrate the code re-usability feature
 */

function redirectToAddProducts() {
    window.location.href = '/pythonlogin/AddProduct'; // Update the URL if needed
}

    // Function to filter table rows based on search input for both products, category to demonstrate the code re-usability
 function searchTable() {
    const input = document.getElementById("searchInput");
    const filter = input.value.toLowerCase();
    const table = document.getElementById("searchTable");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) { // Start from 1 to skip the header
        let cells = rows[i].getElementsByTagName("td");
        let rowContainsFilter = false;

        for (let j = 0; j < cells.length; j++) {
            if (cells[j].innerText.toLowerCase().includes(filter)) {
                rowContainsFilter = true;
                break;
            }
        }

        rows[i].style.display = rowContainsFilter ? "" : "none";
    }
}

function redirectToAddCategories() {
    window.location.href = '/pythonlogin/AddCategory'; // Update the URL if needed
}

function redirectToAddInventory() {
    window.location.href = '/pythonlogin/addInventory'; // Update the URL if needed
}