from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://app.powerbigov.us/view?r=eyJrIjoiOTQ2NDM0YjItOWI4ZC00NzczLTk5ZjctYTA1N2FjMjFkMGQ4IiwidCI6IjIwYjQ5MzNiLWJhYWQtNDMzYy05YzAyLTcwZWRjYzc1NTljNiJ9&pageName=ReportSection6d78f5d6d3ef0fea14e8"
driver.get(url)

time.sleep(30)

output_file = "power_bi_table.csv"
columns = [
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
]

# Create CSV and write the header
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()

with open(output_file, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=columns)

    while True:
        visible_rows = driver.find_elements(By.CSS_SELECTOR, '[data-testid="visual-content-desc"] [role="document"] [class="mid-viewport"] [class*="row"]')

        if visible_rows:
            for row in visible_rows:
                try:
                    row_data = {
                        "Business Entity": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="2"]').text,
                        "Location Name": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="3"]').text,
                        "Descriptive License/Permit Number": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="4"]').text,
                        "License/Permit Status": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="5"]').text,
                        "License/Permit Expiration": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="6"]').text,
                        "License/Permit Type": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="7"]').text,
                        "Location Street": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="8"]').text,
                        "Location Street 2": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="9"]').text,
                        "Location Zip Code": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="10"]').text,
                        "Location State": row.find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="11"]').text
                    }
                    writer.writerow(row_data)
                except Exception as e:
                    print(f"Error processing row: {e}")

        if visible_rows:
            last_row = visible_rows[-1]
            driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", last_row)
            time.sleep(10)

        new_visible_last_row = driver.find_elements(By.CSS_SELECTOR, '[data-testid="visual-content-desc"] [role="document"] [class="mid-viewport"] [class*="row"]')[-1]
        if last_row.get_attribute('row-index') == new_visible_last_row.get_attribute('row-index') and last_row[-1].find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="2"]').text.lower().startswith('z'):
            print(last_row.get_attribute('row-index'))
            print(new_visible_last_row.get_attribute('row-index'))
            print(last_row[-1].find_element(By.CSS_SELECTOR, '[role="gridcell"][aria-colindex="2"]').text)
            # No new rows loaded; exit the loop
            break

# Close the browser
driver.quit()

print(f"Data saved to {output_file}")