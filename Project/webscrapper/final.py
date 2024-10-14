from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import csv

# Configure Chrome WebDriver
chrome_driver_path = 'C:/Users/pillai7/Downloads/chromedriver-win64/chromedriver.exe'
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Runs Chrome in headless mode.
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
driver = webdriver.Chrome(service=service, options=options)

def search_google_for_linkedin_profiles(query, max_pages):
    """Searches Google for LinkedIn profiles based on a query across multiple pages."""
    links = []
    for page in range(max_pages):
        start = page * 10
        search_url = f"https://www.google.com/search?q={query}+linkedin&start={start}"
        driver.get(search_url)
        time.sleep(random.uniform(2, 5))  # Random delay

        # Extract search results
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for item in soup.find_all('a'):
            href = item.get('href')
            if href and 'linkedin.com/in/' in href:
                # Extracting LinkedIn profile URL
                links.append(href.split('&')[0].replace('/url?q=', ''))
        
        # Break if no more links are found on the current page
        if not soup.find_all('a'):
            break
    return list(set(links))  # Remove duplicates

def scrape_profile_data(links):
    """Scrapes LinkedIn profile data given a list of profile links."""
    profile_data = []
    
    # Open LinkedIn login page
    driver.get("https://www.linkedin.com/login")
    print("Navigated to LinkedIn login page.")
    
    # Wait for username field
    username_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    username_field.send_keys("chaitempura@gmail.com")
    
    # Wait for password field
    password_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_field.send_keys("qwerty@123")
    
    # Wait for login button
    login_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()
    print("Clicked login button.")
    
    # Check if login is successful
    time.sleep(10)
    print("Logged in successfully.")

    for profile in links:
        driver.get(profile)
        print(f"Opened profile: {profile}")
        
        try:
            # Wait for title to be present
            title = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]"))
            ).text
            print("Profile Title:", title)
            
            # Wait for description to be present
            description = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-body-medium')]"))
            ).text
            print("Profile Description:", description)

        except Exception as e:
            print(f"Could not retrieve profile data for {profile}: {e}")


        # Add scraped data to the list
        profile_data.append({
            'Name': title,
            'Headline': description,
            'Profile URL': profile,
        })
    return profile_data

def save_to_csv(data, filename='linkedin_profiles.csv'):
    """Saves scraped data to a CSV file."""
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Main execution
try:
    temp = "Google SWE".split(" ")
    job_description = "+".join(temp)
    pagesNumber = 15
    profile_links = search_google_for_linkedin_profiles(job_description , pagesNumber)
    print(f"Found {len(profile_links)} LinkedIn profiles.")
    
    if profile_links:
        scraped_data = scrape_profile_data(profile_links)
        save_to_csv(scraped_data)
        print(f"Data saved to 'linkedin_profiles.csv'. Total profiles scraped: {len(scraped_data)}")
    else:
        print("No profiles found.")
finally:
    driver.quit()