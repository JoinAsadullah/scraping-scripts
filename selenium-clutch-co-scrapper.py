from bs4 import BeautifulSoup
from selenium import webdriver
import time
from urllib.parse import urlparse
import csv


# Initialize the Chrome web driver
profile_directory = 'C:/Users/masdu/AppData/Local/Google/Chrome/User Data'


# Initialize the Chrome web driver
options = webdriver.ChromeOptions()
options.add_argument(f'--user-data-dir={profile_directory}')
options.add_argument('--profile-directory=Profile 1')
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)

# Base URL and initial page
base_url = 'https://clutch.co/agencies/digital-marketing'
page_number = 0

# Create a list to store the data from all pages
all_data = []

try:
    # Loop through 500 pages
    while page_number < 30:
        # Construct the URL for the current page
        if page_number == 0:
            url = base_url
        else:
            url = f'{base_url}?page={page_number}'
        
        # Open the URL using the Selenium driver
        driver.get(url)
        
        # Give the page some time to load (you can adjust the wait time)
        time.sleep(3)
        
        # Get the page source after it has loaded
        page_source = driver.page_source
        
        # Parse the HTML content
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find the parent ul element with class "directory-list"
        directory_ul = soup.find('ul', class_='directory-list')

        # Find all direct child li elements of the ul
        cards = directory_ul.find_all('li', recursive=False, class_=['provider-row', 'sponsor'])
        
        # Extract data from each card
        for card in cards:
            # Find the company name and website link (if available)
            company_name = card.find('a', class_='company_title')
            website_link = card.find('a', class_='website-link__item')
            if website_link == None:
                continue
            
            # Initialize variables to store the extracted data
            company_name_text = None
            website_link_href = None
            
            # Check if the company name and website link exist
            if company_name:
                company_name_text = company_name.get_text().strip()
            else:
                company_name_text = ""
            if website_link:
                website_link_href = website_link['href']
                parsed_url = urlparse(website_link_href)
                # Extract the hostname
                hostname = parsed_url.hostname
            else:
                hostname = ""
            
            # Create a dictionary with the extracted data
            data_dict = {
                'Company Name': company_name_text, 'Website Link' : 'https://'+hostname
            }
            
            # Append the data to the list
            all_data.append(data_dict)
        time.sleep(3)
        # Print progress
        print(f'Page {page_number} scraped.')
        
        # Increment the page number
        page_number += 1
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the Selenium driver when you're done
    driver.quit()

# Save all_data to a CSV file
csv_filename = 'digital_marketing_agencies.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Company Name', 'Website Link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for data in all_data:
        writer.writerow(data)


print(f'Data saved to {csv_filename}')

# Now you have all the data from 500 pages in the `all_data` list
# Each entry in the list is a dictionary containing the company name and website link
# You can further process or save this data as needed
