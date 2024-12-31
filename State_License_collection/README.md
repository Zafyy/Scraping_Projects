# Power BI Table Scraper

This repository contains two solutions—one in **Python** and **JavaScript**—to scrape data from a Power BI table embedded in a web page. The table dynamically loads visible rows, making only the currently visible elements available in the HTML DOM. These scripts implement logic to sequentially scroll through the table and extract all rows efficiently.

---

## Features

- Extracts rows from dynamically loading Power BI tables.
- Handles the challenge of limited DOM availability by scrolling through the table.
- Saves data into a CSV file for easy analysis.
- **Python Script**: Uses Selenium for automated browser control.
- **JavaScript Script**: Can be directly executed in the browser's console.

---

## Table of Contents

- [Requirements](#requirements)
- [Python Script](#python-script)
- [JavaScript Script](#javascript-script)
- [How It Works](#how-it-works)
- [Output](#output)
- [Contributing](#contributing)

---

## Requirements

### Python Script
- **Python 3.7 or higher**
- **Google Chrome browser**
- **ChromeDriver**
- Required Python packages:
  - `selenium`
  - `webdriver_manager`

Install the dependencies using:
```bash
pip install selenium webdriver_manager
```

---

### How to Run
Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

Execute the Python script:
```bash
python power_bi_scraper.py
```

The script will:

- **Launch a Chrome browser.**
- **Navigate to the Power BI table URL.**
- **Start scraping visible rows.**
The extracted data will be saved in a file named power_bi_table.csv in the same directory.

---

## JavaScript Script
### How to Use
- **Open the target Power BI table in a Chrome browser.**
- **Open the browser developer tools:**
    - ***Press Ctrl+Shift+I (Windows/Linux) or Cmd+Option+I (Mac).***
- **Go to the "Console" tab.**
- **Copy the JavaScript code and paste it into the console.**
- **Press Enter to execute the script.**
The script will download a CSV file named power_bi_table.csv with the extracted data.

---

## How It Works
### Dynamic Loading Issue
The Power BI table only renders elements for visible rows in the viewport. As you scroll, rows above and below the current viewport are dynamically loaded and unloaded.

### Solution Logic
- **Both scripts identify the last visible row in the current viewport.**
- **The last visible row is scrolled to the top of the table, triggering the loading of new rows.**
- **The process repeats until all rows are fetched.**

### Python Implementation
Utilizes **Selenium WebDriver** to automate browser interactions, scroll through the table, and extract visible rows.

### JavaScript Implementation
Executes directly in the browser's console to scroll through the table and extract data row by row.

---

## Output
### The data is saved in a CSV file with the following columns:

**Column Name**
- **Business Entity**
- **Location Name**
- **Descriptive License/Permit Number**
- **License/Permit Status**
- **License/Permit Expiration**
- **License/Permit Type**
- **Location Street**
- **Location Street 2**
- **Location Zip Code**
- **Location State**

---

