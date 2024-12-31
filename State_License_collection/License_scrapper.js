(async function() {
    const columns = [
        "Business Entity",
        "Location Name",
        "Descriptive License/Permit Number",
        "License/Permit Status",
        "License/Permit Expiration",
        "License/Permit Type",
        "Location Street",
        "Location Street 2",
        "Location Zip Code",
        "Location State"
    ];

    // Function to download the CSV file
    function downloadCSV(data, filename) {
        const blob = new Blob([data], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.setAttribute("href", url);
        link.setAttribute("download", filename);
        link.style.visibility = "hidden";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // Convert data array to CSV string
    function convertToCSV(dataArray, headers) {
        const rows = [headers.join(",")];
        dataArray.forEach(row => {
            const values = headers.map(header => `"${row[header] || ""}"`);
            rows.push(values.join(","));
        });
        return rows.join("\n");
    }

    const data = [];
    let lastRowIndex = null;

    while (true) {
        const visibleRows = document.querySelectorAll('[data-testid="visual-content-desc"] [role="document"] [class="mid-viewport"] [class*="row"]');
        if (visibleRows.length === 0) break;

        for (const row of visibleRows) {
            try {
                const rowData = {
                    "Business Entity": row.querySelector('[role="gridcell"][aria-colindex="2"]')?.innerText || "",
                    "Location Name": row.querySelector('[role="gridcell"][aria-colindex="3"]')?.innerText || "",
                    "Descriptive License/Permit Number": row.querySelector('[role="gridcell"][aria-colindex="4"]')?.innerText || "",
                    "License/Permit Status": row.querySelector('[role="gridcell"][aria-colindex="5"]')?.innerText || "",
                    "License/Permit Expiration": row.querySelector('[role="gridcell"][aria-colindex="6"]')?.innerText || "",
                    "License/Permit Type": row.querySelector('[role="gridcell"][aria-colindex="7"]')?.innerText || "",
                    "Location Street": row.querySelector('[role="gridcell"][aria-colindex="8"]')?.innerText || "",
                    "Location Street 2": row.querySelector('[role="gridcell"][aria-colindex="9"]')?.innerText || "",
                    "Location Zip Code": row.querySelector('[role="gridcell"][aria-colindex="10"]')?.innerText || "",
                    "Location State": row.querySelector('[role="gridcell"][aria-colindex="11"]')?.innerText || ""
                };
                data.push(rowData);
            } catch (error) {
                console.error("Error processing row:", error);
            }
        }

        const lastRow = visibleRows[visibleRows.length - 1];
        lastRow.scrollIntoView({ block: "start" });
        await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for new rows to load

        const newVisibleRows = document.querySelectorAll('[data-testid="visual-content-desc"] [role="document"] [class="mid-viewport"] [class*="row"]');
        const newLastRow = newVisibleRows[newVisibleRows.length - 1];
        const newRowIndex = newLastRow.getAttribute("row-index");
        const lastRowText = lastRow.querySelector('[role="gridcell"][aria-colindex="2"]')?.innerText.toLowerCase() || "";

        if (lastRowIndex === newRowIndex && lastRowText.startsWith("z")) {
            console.log("Last row reached or text starts with 'z':", lastRowText);
            break;
        }
        lastRowIndex = newRowIndex;
    }

    // Convert data to CSV and download
    const csvContent = convertToCSV(data, columns);
    downloadCSV(csvContent, "power_bi_table.csv");
})();
