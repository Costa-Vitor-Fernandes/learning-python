import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

def get_platform(url):
    try:
        # Send a GET request to the provided URL
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for specific HTML elements or patterns indicative of different e-commerce platforms

        # Shopify
        if soup.find("script", attrs={"src": re.compile("shopify.*.js")}) or \
                re.search(r"\bshopify\b", response.text, re.IGNORECASE):
            return "Shopify"
        
        # WooCommerce (WordPress)
        elif re.search(r"\bwoocommerce\b", response.text, re.IGNORECASE):
            return "WooCommerce (WordPress)"
        
        # Magento
        elif soup.find("link", attrs={"rel": "stylesheet", "href": re.compile(".*magento.*\.css")}) or \
                soup.find("link", attrs={"rel": "stylesheet", "href": re.compile(".*\.magento2.*\.css")}) or \
                re.search(r"\bmagento\b", response.text, re.IGNORECASE):
            return "Magento"

        # BigCommerce
        elif soup.find("script", attrs={"src": re.compile("bigcommerce.*.js")}) or \
                re.search(r"\bbigcommerce\b", response.text, re.IGNORECASE):
            return "BigCommerce"
        
        # Tray
        elif re.search(r"\btray\b", response.text, re.IGNORECASE):
            return "Tray"
        
        # Nuvemshop
        elif re.search(r"\bnuvemshop\b", response.text, re.IGNORECASE):
            return "Nuvemshop"
        
        # Loja Integrada
        elif re.search(r"\blojaintegrada\b", response.text, re.IGNORECASE):
            return "Loja Integrada"
        
        # Squarespace
        elif re.search(r"\bsquarespace\b", response.text, re.IGNORECASE):
            return "Squarespace"

        # WordPress (without WooCommerce)
        elif re.search(r"\bwordpress\b", response.text, re.IGNORECASE):
            # Check for common WordPress files or directories
            if response.status_code == 200:
                if re.search(r"\bwp-content\b", response.text, re.IGNORECASE) or \
                        re.search(r"\bwp-admin\b", response.text, re.IGNORECASE) or \
                        re.search(r"\bwp-includes\b", response.text, re.IGNORECASE):
                    return "WordPress (without WooCommerce)"
        
        else:
            return "Unknown"

    except requests.exceptions.RequestException:
        return "Invalid URL"

def get_cnpj(url):
    try:
        # Send a GET request to the provided URL
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for patterns matching the CNPJ format
        cnpj_pattern = r"CNPJ: *\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}"
        matches = re.findall(cnpj_pattern, response.text)

        if matches:
            # Extract the CNPJ number from the matched pattern
            cnpj = re.search(r"\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}", matches[0])
            return cnpj.group()
        else:
            return "No CNPJ found"
    
    except requests.exceptions.RequestException:
        return "Invalid URL"

# Get the path of the current directory
current_directory = os.getcwd()

# Read the input URLs from the spreadsheet in the current directory (Assuming they are in a column named 'URL')
file_path = os.path.join(current_directory, 'input_urls.xlsx')
df = pd.read_excel(file_path)

# Create new columns named 'Platform' and 'CNPJ' to store the identified platform and CNPJ
df['Platform'] = ''
df['CNPJ'] = ''

# Iterate through each URL and identify the platform and CNPJ
for index, row in df.iterrows():
    url = row['URL']
    platform = get_platform(url)
    cnpj = get_cnpj(url)
    df.at[index, 'Platform'] = platform
    df.at[index, 'CNPJ'] = cnpj

# Export the results to a new spreadsheet in the current directory
output_path = os.path.join(current_directory, 'output_info.xlsx')
df.to_excel(output_path, index=False)