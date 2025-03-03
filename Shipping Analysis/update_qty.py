# change file directories for different computers; #C

import csv
import os
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def login_to_seller_central(driver):
    driver.get("https://sellercentral.amazon.com")
    input("Log in to Seller Central and press Enter to continue...")

def navigate_to_inventory(driver):
    driver.get("https://sellercentral.amazon.com/inventory")

def search_sku(driver, sku):
    wait = WebDriverWait(driver, 15)
    
    #  back to the Inventory page before searching
    driver.get("https://sellercentral.amazon.com/inventory")
    time.sleep(3)  # load page

    try:
        search_box = driver.execute_script(
            "return document.querySelector('kat-input[unique-id=\"katal-id-1\"]').shadowRoot.querySelector('input')"
        )
        search_box.send_keys(sku)
        search_box.send_keys(Keys.RETURN)
        print(f"Searching for ASIN: {sku} (via shadow DOM)")
    except:
        try:
            search_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "SearchBox-module__searchInput--T3Fdk")))
            search_box.send_keys(sku)
            search_box.send_keys(Keys.RETURN)
            print(f"Searching for ASIN: {sku} (via CLASS_NAME)")
        except:
            print(f"Error: Search box not found for ASIN {sku}")
            return False  # failure

    return True  


def open_product_page(driver):
    wait = WebDriverWait(driver, 15)
    time.sleep(5)
    try:
        sku_link = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'JanusSplitBox-module__panel--AbYDg')]/a")))
        product_url = sku_link.get_attribute("href")
        driver.get(product_url)
        print("Navigated to product page:", product_url)
        return True
    except Exception as e:
        print("Error navigating to product page:", str(e))
        return False

def setup_csv_file():
    save_path = r"C:\Users\User.DESKTOP-FC21VHI\Documents\SA" #C
    os.makedirs(save_path, exist_ok=True)
    current_date = datetime.datetime.now().strftime("%Y.%m.%d")
    csv_filename = os.path.join(save_path, f"{current_date} - Inbound Data.csv")

    # create the file with headers only if it doesn't exist
    if not os.path.exists(csv_filename):
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ASIN", "Shipment ID", "Shipment Name", "Destination", "Last Updated", "Created", "Qty Shipped", "Qty Received", "Shipment Status"])

    return csv_filename

def extract_inbound_data(driver, csv_filename, sku):
    wait = WebDriverWait(driver, 15)
    try:
        inbound_table = wait.until(EC.presence_of_element_located((By.XPATH, "//kat-table-body")))
        rows = inbound_table.find_elements(By.XPATH, ".//kat-table-row")
        data_found = len(rows) > 0
    except:
        data_found = False
    
    with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:  # append mode
        writer = csv.writer(file)

        if data_found:
            for row in rows:
                row_data = [sku]  # insert first column and add ASIN in the cell value
                shipment_id_element = row.find_element(By.XPATH, ".//kat-table-cell//kat-link")
                shipment_id = shipment_id_element.get_attribute("label").strip() if shipment_id_element else "N/A"
                row_data.append(shipment_id)
                cells = row.find_elements(By.XPATH, ".//kat-table-cell//label")
                row_data.extend([cell.text.strip() for cell in cells])
                writer.writerow(row_data)
        else:
            writer.writerow([sku] + ["X"] * 8)  # same for other rows but "X" in all other columns for asin that does not have inbound table

    print(f"Data for {sku} exported to {csv_filename}")

def read_asin_list(file_path): # external csv file, YYYY.MM.DD SA ASIN List.csv
    """ Reads ASINs from a CSV file (1 ASIN per row). """
    asins = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header 
            asins = [row[0] for row in reader if row]  # get asin from first column
    except Exception as e:
        print("Error reading ASIN list:", str(e))
    return asins

def main():
    driver = setup_driver()
    login_to_seller_central(driver)

    # Load ASIN list from CSV
    today_date = datetime.datetime.now().strftime("%Y.%m.%d")
    save_path = r"C:\Users\User.DESKTOP-FC21VHI\Documents\SA" #C
    input_csv = os.path.join(save_path, f"{today_date} SA ASIN List.csv")

    # Read ASINs from CSV
    with open(input_csv, mode="r", encoding="utf-8") as file:
        asin_list = [line.strip() for line in file if line.strip()]

    csv_filename = setup_csv_file()

    for asin in asin_list:
        print(f"\nProcessing ASIN: {asin}")

        success = search_sku(driver, asin)
        if not success:
            continue  # skip asin

        open_product_page(driver)
        extract_inbound_data(driver, csv_filename, asin)

    print("All ASINs processed. Data exported.")
    input("Press Enter to exit...")
    driver.quit()


if __name__ == "__main__":
    main()
