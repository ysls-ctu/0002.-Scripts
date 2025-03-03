import os
import glob
import re
import datetime
import pandas as pd
import PyPDF2
from collections import defaultdict

#today = "2025.02.28" # test date
today = datetime.datetime.today().strftime("%Y.%m.%d")  

request_type = input("Press 0 for ADV, 1 for JCT >>> ")

# convert to integer 
try:
    request_type = int(request_type)
    if request_type == 0:
        request_placeholder = "ADV"
    elif request_type == 1:
        request_placeholder = "JCT"
    else:
        raise ValueError
except ValueError:
    print("Invalid input. Defaulting to JCT.")
    request_placeholder = "JCT"

excel_path = fr"C:\Users\User.DESKTOP-FC21VHI\Documents\SA\{today} - {request_placeholder}.AMZ - FULL CASE RESTOCK.xlsx"

print(f"Using Excel file: {excel_path}")

if not os.path.exists(excel_path):
    print(f"Error: Excel file not found at {excel_path}")
    exit(1)

def load_sku_mapping(excel_path):
    """Loads SKU to Model Number mapping from an Excel file."""
    df = pd.read_excel(excel_path, skiprows=8)  # Skip first 8 rows
    sku_to_model = dict(zip(df.iloc[:, 1], df.iloc[:, 2]))  # Column B -> Column C
    return sku_to_model

def extract_text_from_page(pdf_reader, page_num):
    """Extracts text from a given PDF page."""
    page = pdf_reader.pages[page_num]
    return page.extract_text()

def get_sku_from_text(text):
    """Extracts SKU using regex pattern for formats like 5D-35CL-81C1."""
    match = re.search(r'(\w{2,3}-\w{4,5}-\w{3,4})', text)
    return match.group(1) if match else None

def split_and_group_pdf(input_pdf_path, output_folder, sku_mapping):
    """Splits PDF into pairs and groups them by Model Number (using SKU mapping)."""
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer_dict = defaultdict(PyPDF2.PdfWriter)

        total_pages = len(pdf_reader.pages)

        for i in range(0, total_pages, 2):
            if i + 1 >= total_pages:
                continue  # Ensure there's a pair

            # Extract SKU from barcode page
            text = extract_text_from_page(pdf_reader, i)
            sku = get_sku_from_text(text)

            if sku:
                model_number = sku_mapping.get(sku, sku)  # Get model number, fallback to SKU
                pdf_writer = pdf_writer_dict[model_number]
                pdf_writer.add_page(pdf_reader.pages[i])  # Barcode page
                pdf_writer.add_page(pdf_reader.pages[i + 1])  # Tracker page

        # Save each SKU's grouped PDF using Model Number as filename
        for model_number, writer in pdf_writer_dict.items():
            output_pdf_path = os.path.join(output_folder, f"{model_number}.pdf")
            with open(output_pdf_path, "wb") as output_pdf:
                writer.write(output_pdf)
            print(f"Saved: {output_pdf_path}")

# Load SKU mapping
sku_mapping = load_sku_mapping(excel_path)

# Find the latest "package-FBA*.pdf" file dynamically
directory = r"C:\Users\User.DESKTOP-FC21VHI\Documents\SA"
matching_files = glob.glob(os.path.join(directory, "package-FBA*.pdf"))

if matching_files:
    file_path = max(matching_files, key=os.path.getmtime)
    print(f"Using file: {file_path}")
else:
    print("No matching file found.")
    exit(1)  # Exit if no valid PDF file is found

output_folder = os.path.join(directory, "output")
split_and_group_pdf(file_path, output_folder, sku_mapping)
