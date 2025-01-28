
import re  
import pandas as pd 
import requests
from bs4 import BeautifulSoup


def get_branches_data(url,branches_list):
    # Step 1: Fetch the webpage
    # url = 'https://restaurants.subway.com/united-kingdom/en'  # Replace with the actual URL
    response = requests.get(url)

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Step 3: Find the <ul> element with the class "Directory-listLinks"
    ul_element = soup.find('ul', class_='Directory-listLinks')

    # Step 4: Extract all <li> items and their respective links, text, and data-count
    li_items = ul_element.find_all('li')

    for li in li_items:
        link = li.find('a')
        text = link.get_text(strip=True).lower()
        branches_list.append(text)
    
    return branches_list
        # href = link['href']

        # data_count = link.get('data-count', 'N/A').strip('()')   # Default to 'N/A' if attribute not found
        # print(f'Text: {text}, Href: {href}, Data-count: {data_count}')

def get_map_url(url):
    print("_________________in map ___________________________")
    
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize href to handle cases where the link is not found
    href = None

    # Find the <link> tag with the itemprop 'hasMap' inside a <div> with class 'location-map-wrapper'
    link_tag = soup.select_one('div.location-map-wrapper link[itemprop="hasMap"]')

    # Extract the href attribute if the <link> tag is found
    if link_tag and link_tag.has_attr('href'):
        href = link_tag['href']
        print(f"Map URL: {href}")
    else:
        print("Map URL not found")
    
    return href

def edit_text(address):
    address = address.lower().strip()
    address = re.sub(r'\s+', ' ', address)  # Replace multiple spaces with a single space
    address = re.sub(r'\s*-\s*', '-', address)  # Handle spaces around hyphens
    address = address.replace(' ', '-')  # Replace remaining spaces with hyphens
    return address


def get_branches_address(url, state, branch, data_dict):
    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Handle both types of <ul> elements
    ul_elements = soup.find_all('ul', class_=['Directory-listTeasers', 'Directory-row', 'Directory-listTeasers--single'])

    for ul_element in ul_elements:
        # Check for multiple <li> elements
        li_elements = ul_element.find_all('li', class_='Directory-listTeaser')
        
        # If no <li> elements found with that class, check if it's the single <li> class
        if not li_elements:
            li_elements = ul_element.find_all('li', class_='Directory-listTeaser--single')
        
        for li in li_elements:
            # Extract data from the <li> element
            a_tag = li.find('a', class_='Teaser-title')
            address = li.find('address', class_='c-address')
            
            if a_tag and address:
                name = a_tag.text.strip()
                
                # Extract address lines
                address_lines = [span.text.strip() for span in address.find_all('span')]

                # Extract postal code
                postal_code_span = address.find('span', class_='c-address-postal-code')
                postal_code_text = postal_code_span.get_text(strip=True) if postal_code_span else 'Postal code not found'

                # Extract additional address information
                address_row_div = li.find('div', class_='c-AddressRow')
                address_text_2 = address_row_div.find('span', class_='c-address-street-1').get_text(strip=True) if address_row_div else 'Address not found'
                
                # Format address URL
                address_text_2 = edit_text(address_text_2)  # Ensure this function is defined
                url = f"https://restaurants.subway.com/united-kingdom/{state}/{branch}/{address_text_2}"
                
                # Get map URL
                map_url = get_map_url(url)  # Ensure this function is defined

                # Join address lines into a single string
                full_address = ', '.join(address_lines)

                # Print results
                print(f"Name: {name}")
                print(f"Address: {full_address}")
                print(f"Map URL: {map_url}")
                print(f"Postal Code: {postal_code_text}")

                # Append to data_dict
                data_dict.append({
                    "Branch Name": name,
                    "Address": full_address,
                    "Map URL": map_url,
                    "Postal Code": postal_code_text
                })
        
        print('---')  # Separator for readability   
    return data_dict


if __name__ == "__main__":

    locations = [
        "en","ni","sc","wa"

    ]
    
    for i in locations:
        url = f'https://restaurants.subway.com/united-kingdom/{i}'
        print(url)
        data_dict=[]
        branches_list=[]
        branches_list=get_branches_data(url,branches_list)
        print(branches_list)
        for branch in branches_list:
            url=f'https://restaurants.subway.com/united-kingdom/{i}/{branch}'
            print(url)
            data_dict=get_branches_address(url,i,branch,data_dict)
            # break
            # break
        print("______________________")
        print(data_dict)

        df = pd.DataFrame(data_dict)
        
        # # Write the DataFrame to an Excel file
        path=f"subway_{i}_branches_and_addresses.xlsx"
        df.to_excel(path, index=False)
        print(path,"Data has been saved")

        
