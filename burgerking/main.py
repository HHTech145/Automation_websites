

import re  
import pandas as pd 
import requests
from bs4 import BeautifulSoup


def get_branches_data(url):
    branches_list=[]
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

def get_branch_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Parse the HTML content
    # soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <ul> elements with the class "Directory-listTeasers"
    ul_elements = soup.find_all('ul', class_='Directory-listTeasers')

    # Extract href links from all <a> tags within <li> elements
    hrefs = []
    for ul in ul_elements:
        for li in ul.find_all('li', class_='Directory-listTeaser'):
            a_tag = li.find('a', class_='Teaser-cardLink')
            if a_tag and a_tag.has_attr('href'):
                hrefs.append(a_tag['href'])

    # Print the extracted href links
    for href in hrefs:
        print(href)
    return hrefs    


if __name__ == "__main__":

    url="https://locations.burgerking.co.uk/"
    branches_list=get_branches_data(url)
    print(branches_list)
    for branch in branches_list:
        url=f'https://locations.burgerking.co.uk//{branch}'
        print(url)
        get_branch_list(url)
        # data_dict=get_branches_address(url,i,branch,data_dict)
        break