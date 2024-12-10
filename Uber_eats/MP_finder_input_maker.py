import csv
import json

# Define input and output file paths
input_file = "UberEates_MP_Finder_input(in).csv"  # Replace with your input file name
output_file = "Final_input.csv"  # Replace with your desired output file name

# Read the input CSV and write the output CSV
with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    # Define the field names for the output CSV
    fieldnames = ["search_term", "store_uuid", "latitude", "longitude", "merchant_name", "merchant_url"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    # Process each row in the input CSV
    for row in reader:
        # Parse the additional_data column as JSON
        additional_data = json.loads(row["additional_data"])
        latitude = additional_data["latitude"]
        longitude = additional_data["longitude"]
        store_uuid = additional_data["store_id"]
        merchant_name = row["merchant_name"]
        merchant_url =row["url"]
        
        # Iterate over search terms in the array
        search_terms = json.loads(row["search_terms"])
        for term in search_terms:
            # Write a new row for each search term
            writer.writerow({
                "search_term": term,
                "store_uuid": store_uuid,
                "latitude": latitude,
                "longitude": longitude,
                "merchant_name": merchant_name,
                "merchant_url": merchant_url
            })

print(f"Processed data has been written to {output_file}")
