from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import re  
import pandas as pd 

def instantiate_driver(url):
    options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')
    # options.add_argument('--user-data-dir=C:/temp/chrome')

    options.add_argument('--user-data-dir=C:/Users/USER/AppData/Local/Google/Chrome/User Data/Default')


    driver = webdriver.Chrome(options=options)

    driver.get(url)
    # print(driver.title)  # Should print "Google"

    sleep(2)


    zoom_percentage=50

    driver.execute_script(f"document.body.style.zoom='{zoom_percentage}%'")
    return driver



def scroll_page(driver):
    # Get the initial page height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load
        sleep(2)  # Adjust time if necessary for content to load

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def click_button(driver):
    sleep(10)
    initial_XPATH = '//*[@id="__next"]/div[1]/main/div[4]/button'
    max_click_SHOW_MORE = 13
    count = 0 
    while count <= max_click_SHOW_MORE:
        try:
            print("count",count)
            scroll_page(driver)

            # driver.execute_script("arguments[0].scrollIntoView(true);", parent_div)
            # driver.execute_script("arguments[0].scrollIntoView(true);", element)
            sleep(3)
            WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()
            count = count+1 
            # sleep(2)
        except Exception as E:
            print(E)
            break


def get_branch_name_and_address(driver):
    sleep(2)
    try:
        element=driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/main/div[2]/div/div[1]/h1')
        sleep(1)
        branch_name=element.text
        # /html/body/div[1]/div[1]/main/div[2]/div/div[2]/p
        element=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/main/div[2]/div/div[2]/p')
        sleep(1)
        address=element.text
    except Exception as e:
        print(e)
    finally:
        return branch_name,address



def goto_branch_page(kfc_london_list,location):
    data = []

    try:
        for index, branch in enumerate(kfc_london_list):
            try:
                # Clean up the branch name for the URL
                branch = branch.lower().strip()
                branch = re.sub(r'\s+', ' ', branch)  # Replace multiple spaces with a single space
                branch = re.sub(r'\s*-\s*', '-', branch)  # Handle spaces around hyphens
                branch = branch.replace(' ', '-')  # Replace remaining spaces with hyphens
                
                # Form the URL
                url = f'https://www.kfc.co.uk/kfc-near-me/{branch}'
                print("__________________________________url:", url)
                
                # Wait for a bit before making the request
                # sleep(1)
                
                # Instantiate the driver and load the URL
                driver = instantiate_driver(url)
                
                # Extract the branch name and address
                branch_name, address = get_branch_name_and_address(driver)
                if branch_name and address:
                    print(f"Result {index + 1}: Branch Name: {branch_name}, Address: {address}")
                    data.append({"Branch Name": branch_name, "Address": address})
                else:
                    print(f"Result {index + 1}: Branch name or address not found")
                
            except Exception as e:
                print(f"Error processing result {index + 1}: {e}")
            
            finally:
                # Make sure to close the driver after each iteration
                driver.quit()
                
    except TimeoutException:
        print("The page took too long to load or the search results were not found.")
    
    finally:
        # Create a DataFrame from the data list
        df = pd.DataFrame(data)
        
        # Write the DataFrame to an Excel file
        path=f"kfc_{location}_branches_and_addresses.xlsx"
        df.to_excel(path, index=False)
        print("Data has been saved")


def get_kfc_london_list(driver, num_elements=150, initial_sleep=10):
    """
    Extracts text from elements on a page using XPath and appends them to a list.

    Args:
        driver (webdriver): The Selenium WebDriver instance.
        num_elements (int): The number of elements to iterate through and extract.
        initial_sleep (int): Initial sleep time before starting to extract elements.

    Returns:
        list: A list of extracted text from elements.
    """
    sleep(initial_sleep)  # Initial sleep before starting the process
    kfc_london_list = []
    count = 0

    try:
        for i in range(1, num_elements + 1):
            print(i)
            if count > 0:
                # Construct the XPath for the element
                xpath = f'/html/body/div[1]/div[1]/main/div[4]/div/div[{i}]'
                print(xpath)
                
                # Find the element using the constructed XPath
                element = driver.find_element(By.XPATH, xpath)
                
                # Extract the text from the element and append to the list
                print(element.text)
                kfc_london_list.append(element.text)
            
            count += 1
            
    except Exception as e:
        print(f"Error occurred while extracting elements: {e}")
    
    return kfc_london_list


if __name__ == "__main__":
    url='https://www.kfc.co.uk/kfc-near-me/london'
    # locations = [
    #     "south-east", "wales", "north-west", "west-midlands",
    #     "eastern", "yorkshire-and-humber", "south-west", "scotland",
    #     "east-midlands", "north-east", "republic-ireland", "northern-ireland"
    # ]

    locations = [
        "yorkshire-and-humber", "south-west", "scotland",
        "east-midlands", "north-east", "republic-ireland", "northern-ireland"
    ]
    
    for i in locations:
        url = f'https://www.kfc.co.uk/kfc-near-me/{i}'
        print(url)
        driver=instantiate_driver(url)
        scroll_page(driver)
        click_button(driver)
        print("out of click loop ----------------------------------------")
        # driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + Keys.HOME)

        driver.execute_script("window.scrollTo(0, document.body.scrollTop);")


        kfc_london_list=get_kfc_london_list(driver)
        print(kfc_london_list)
        driver.quit()
        # initiate the data frame
        goto_branch_page(kfc_london_list,i)



        
            
