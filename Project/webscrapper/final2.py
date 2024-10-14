from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import csv
import datetime

# Configure Chrome WebDriver
chrome_driver_path = 'C:/Users/pillai7/Downloads/chromedriver-win64/chromedriver.exe'
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Runs Chrome in headless mode.
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
    
    time.sleep(100)  # Wait for login processing
    print("Logged in successfully.")

    for profile in links:
        driver.get(profile)
        print(f"Opened profile: {profile}")
        time.sleep(random.uniform(5, 10))  # Delay between profile accesses

        try:
            # Wait for name to be present
            name = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]"))
            ).text
            
            # Wait for current position to be present
            current_position = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-body-medium')]"))
            ).text
            
            # Wait for past experience section
            past_experience = []
            experience_elements = driver.find_elements(By.XPATH, "//section[contains(@class, 'experience-section')]//li")
            for experience in experience_elements:
                title = experience.find_element(By.XPATH, ".//h3").text
                company = experience.find_element(By.XPATH, ".//p[contains(@class, 'pv-entity__secondary-title')]").text
                past_experience.append(f"{title} at {company}")
            
            # Wait for education section
            education = []
            education_elements = driver.find_elements(By.XPATH, "//section[contains(@class, 'education-section')]//li")
            for edu in education_elements:
                school = edu.find_element(By.XPATH, ".//h3").text
                degree = edu.find_element(By.XPATH, ".//p[contains(@class, 'pv-entity__summary-info')]").text
                education.append(f"{degree} from {school}")

            # Wait for projects section (if available)
            projects = []
            project_elements = driver.find_elements(By.XPATH, "//section[contains(@class, 'project-section')]//li")
            for project in project_elements:
                project_title = project.find_element(By.XPATH, ".//h3").text
                projects.append(project_title)

            # Add scraped data to the list
            profile_data.append({
                'Name': name,
                'Current Position': current_position,
                'Past Experience': "; ".join(past_experience),
                'Education': "; ".join(education),
                'Projects': "; ".join(projects),
                'Profile URL': profile,
            })

            # Print out the scraped data
            print(f"Profile Data for {name}:")
            print(f"  Current Position: {current_position}")
            print(f"  Past Experience: {', '.join(past_experience)}")
            print(f"  Education: {', '.join(education)}")
            print(f"  Projects: {', '.join(projects)}")

        except Exception as e:
            print(f"Could not retrieve profile data for {profile}: {e}")

    return profile_data

def save_to_csv(data, filename=None):
    """Saves scraped data to a CSV file."""
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'linkedin_profiles_{timestamp}.csv'
    
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Main execution
try:
    temp = "Google SWE".split(" ")
    job_description = "+".join(temp)
    pagesNumber = 1
    profile_links = search_google_for_linkedin_profiles(job_description, pagesNumber)
    print(f"Found {len(profile_links)} LinkedIn profiles.")
    
    if profile_links:
        scraped_data = scrape_profile_data(profile_links)
        save_to_csv(scraped_data)
        print(f"Data saved to 'linkedin_profiles.csv'. Total profiles scraped: {len(scraped_data)}")
    else:
        print("No profiles found.")
finally:
    driver.quit()