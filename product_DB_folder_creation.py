import os
import csv
import string

# Path to the CSV file
csv_file_path = r"C:\Users\User.DESKTOP-FC21VHI\Documents\SA\01. Folder Creation per Item in Inflow\000SourceFiles\2024.12.06 Inventory Summary.csv"
# change this to appropriate folder path in your dekstop


# Folder to create the directories in
base_directory = r"C:\Users\User.DESKTOP-FC21VHI\Documents\SA\01. Folder Creation per Item in Inflow"
# change this to appropriate folder path in your dekstop
os.makedirs(base_directory, exist_ok=True)

# Function to sanitize folder names
def sanitize_folder_name(name):
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}" 
    sanitized = ''.join(c for c in name if c in valid_chars)      
    sanitized = sanitized.replace("/", "").replace("\\", "")      
    return sanitized.upper()  # Capitalize folder name

# Function to process the description
def process_description(description):
    if "|" in description:
        
        parts = description.split('|')
        if len(parts) > 2:
            description = ' '.join(parts[:2])  
        else:
            description = parts[0] 
    return description.strip().upper() 

# Open the CSV and process
with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:  
    reader = csv.DictReader(csvfile)
    
    reader.fieldnames = [header.strip('"') for header in reader.fieldnames]
    print("CSV Headers (Processed):", reader.fieldnames)  # Debugging 

    # Get all rows as a list and sort them by product name
    rows = list(reader)
    rows.sort(key=lambda row: row['ProductName'].upper())  # 
    
    process_flag = False

    for row in rows:
        product_name = row['ProductName']
        
        if product_name == "KS1101-GRN-OWL":
            process_flag = True  # Start processing after this product
        
        if process_flag:
            if product_name == "KS9922-YEL-XL":
                process_flag = False  # Stop processing after this product
            
            # Sanitize and format product name
            product_name_sanitized = sanitize_folder_name(product_name)  
            product_desc_full = row['Description']
            
            # Process the description
            product_desc = process_description(product_desc_full)
            
            # Combine product name and description for folder name
            folder_name = f"{product_name_sanitized} - {product_desc}"
            folder_path = os.path.join(base_directory, folder_name)
            
            # Create the folder
            try:
                os.makedirs(folder_path, exist_ok=True)
            except OSError as e:
                print(f"Error creating folder '{folder_name}': {e}")

print(f"Folders created in '{base_directory}'.")

# expected no. of folders = 1708
# total no. of rows (raw file) = 1859
