from bs4 import BeautifulSoup
import requests
import csv
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()


class MPfinder:
    def __init__(self, csv_file, output_file, error_file):
        self.csv_file = csv_file
        self.output_file = output_file
        self.error_file = error_file
        self.proxies = {}
        self.session = requests.Session() 
        proxy = os.environ.get("proxy",None)                                                           ## Use any proxy as per your convenience 
        self.proxies["http"] = proxy
        self.proxies["https"] = proxy
        self.session.proxies = self.proxies
        self.session.headers.update({
            "Origin": "https://www.ubereats.com",
            "X-Csrf-Token": "x",
            "Content-Type": "application/json",
        })

        # Initialize output CSV files
        self.init_csv(self.output_file, ["product_url", "product_id", "product_name", "merchant_url", "size"])
        self.init_csv(self.error_file, ["search_term", "merchant_name", "latitude", "longitude", "store_uuid", "merchant_url"])

    def init_csv(self, file_path, headers):
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

    def append_to_csv(self, file_path, data):
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writerow(data)

    def extract_merchant_data(self):
        with open(self.csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield (
                    row["search_term"],
                    row["merchant_name"],
                    row["latitude"],
                    row["longitude"],
                    row["store_uuid"],
                    row["merchant_url"],
                )

    def process_row(self, search_term, merchant_name, latitude, longitude, store_uuid, merchant_url):
        try:
            body_1 = {
                "diningMode": "DELIVERY",
                "sectionUUIDs": None,
                "storeUUIDs": [store_uuid],
                "userQuery": search_term,
                "isGrocery": True,
                "targetLocation": {
                    "address": "",
                    "streetAddress": "",
                    "city": "",
                    "country": "US",
                    "postalCode": "",
                    "region": "",
                    "latitude": float(latitude),
                    "longitude": float(longitude),
                    "geo": {"city": "", "country": "us", "region": ""},
                    "locationType": "GROCERY_STORE",
                },
                "entrypointContext": "IN_STORE_SEARCH",
            }

            request_url_1 = "https://www.ubereats.com/_p/api/getInStoreSearchV1"
            response = self.session.post(
                request_url_1,
                json=body_1,
                timeout=30,
                verify=False,
            )
            json_data1 = response.json()

            # Handle response and verify merchant page if needed
            if response.status_code == 200 and json_data1["status"] == "success":
                catalog_sections = json_data1["data"].get("catalogSectionsMap", {})
                if catalog_sections:
                    values = list(catalog_sections.values())[0][0]
                    product_data = values["payload"]["standardItemsPayload"]["catalogItems"]
                    for item in product_data:
                        section_uuid1 = item.get("sectionUuid")
                        subsection_uuid2 = item.get("subsectionUuid")
                        product_uuid3 = item.get("uuid")
                        product_name = item.get("title")
                        size = product_name.split('(')[1].split(')')[0] if product_name and '(' in product_name and ')' in product_name else None

                        product_url = f"{merchant_url}/{section_uuid1}/{subsection_uuid2}/{product_uuid3}"
                        product_record = {
                            "product_url": product_url,
                            "product_id": product_uuid3,
                            "product_name": product_name,
                            "merchant_url": merchant_url,
                            "size": size
                        }
                        # Append each product to the output CSV
                        self.append_to_csv(self.output_file, product_record)
                else:
                    self.verify_merchant_page(merchant_url, search_term, merchant_name, latitude, longitude, store_uuid)
            else:
                self.verify_merchant_page(merchant_url, search_term, merchant_name, latitude, longitude, store_uuid)

        except Exception as e:
            print(f"Error processing {merchant_name}: {e}")
            self.append_to_csv(self.error_file, {
                "search_term": search_term,
                "merchant_name": merchant_name,
                "latitude": latitude,
                "longitude": longitude,
                "store_uuid": store_uuid,
                "merchant_url": merchant_url
            })

    def verify_merchant_page(self, merchant_url, search_term, merchant_name, latitude, longitude, store_uuid):
        try:
            verify_merchant_req = self.session.get(merchant_url, verify=False)
            if verify_merchant_req.ok:
                soup = BeautifulSoup(verify_merchant_req.text, "html.parser")
                full_content = soup.select_one(
                    '[data-testid="store-loaded"] [data-testid="store-desktop-loaded-coi"]'
                )
                if not full_content:
                    print(f"Store is not opened: {merchant_url}")
                    # Log error in the error CSV
                    self.append_to_csv(self.error_file, {
                        "search_term": search_term,
                        "merchant_name": merchant_name,
                        "latitude": latitude,
                        "longitude": longitude,
                        "store_uuid": store_uuid,
                        "merchant_url": merchant_url
                    })
            else:
                raise Exception(f"Failed to load merchant URL: {merchant_url}")
        except Exception as e:
            print(f"Error while verifying merchant page: {e}")
            self.append_to_csv(self.error_file, {
                "search_term": search_term,
                "merchant_name": merchant_name,
                "latitude": latitude,
                "longitude": longitude,
                "store_uuid": store_uuid,
                "merchant_url": merchant_url
            })

    def process_data(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self.process_row, *data): data
                for data in self.extract_merchant_data()
            }
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in thread: {e}")


if __name__ == "__main__":
    # Provide the input CSV file
    input_file = "testing_input(in).csv"
    output_file = "Uber_eats_MP_Finder_output.csv"
    error_file = "Uber_eats_MP_Finder_error.csv"

    finder = MPfinder(input_file, output_file, error_file)
    finder.process_data()
