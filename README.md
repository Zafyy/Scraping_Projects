# **Merchant Product Finder**

## **Overview**  
The **Merchant Product Finder** is a Python-based project designed to extract product details for merchants from an input CSV file. The tool processes merchant data via API requests and web scraping (using `BeautifulSoup`), saving the results into an output CSV file. Merchants for whom the data extraction fails are logged into a separate CSV file.  

This project utilizes multi-threading for faster and efficient processing.

---
## **Process Overview for UberEats Merchant Finder**
`UberEates_MP_Finder_input(in).csv` is the raw data of all the merchants available on UberEats. First, we will run the script `MP_finder_input_maker.py` to create a new CSV file, `final_input.csv`, as per the needs of the next script.  

The `final_input.csv` will then be used as the input file for `MP_Finder.py` (MP: Marketplace Page). After running this script, two CSV files will be created:  

1. **Data CSV**: Captures all the extracted product data.  
2. **Failed Merchants CSV**: Logs details of merchants where extraction failed, so the process can be retried if needed.  

## **Features**  
* Reads merchant details from an input CSV file.  
* Processes multiple merchants simultaneously using multi-threading.  
* Handles API requests and fallback scraping using `BeautifulSoup`.  
* Writes successful results into an output CSV file in real-time.  
* Logs failed merchant data into a separate CSV file for debugging.  
* Supports session management with custom headers and proxy settings.  

---

## **Project Structure**  
```plaintext
merchant_product_finder/
├── input.csv             # Input file with merchant details
├── output.csv            # Output file with extracted product details
├── failed_merchants.csv  # File for failed merchant details
├── MPfinder.py           # Main Python script
└── README.md             # Project documentation (this file)

## **Technologies Used**
* Python
* Requests
* BeautifulSoup (bs4)
* Threading (concurrent.futures.ThreadPoolExecutor)
* CSV

## **Usage**
**Prepare Input File**

* Create an input.csv file with the following columns:
* search_term
* merchant_name
* latitude
* longitude
* store_uuid
* merchant_url


**Run the Script**

*Execute the script:
python MPfinder.py

**Output Files**

* output.csv: Contains the extracted product details.
* failed_merchants.csv: Logs merchants where data extraction failed.

