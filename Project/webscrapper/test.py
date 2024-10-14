from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import random
import csv

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
                # Extracting LinkedIn profile URL
                links.append(href.split('&')[0].replace('/url?q=', ''))
        
        # Break if no more links are found on the current page
        if not soup.find_all('a'):
            break
    return list(set(links))  # Remove duplicates

def scrape_profile_data(links):
    """Scrapes LinkedIn profile data given a list of profile links."""
    profile_data = []
    for link in links:
        driver.get(link)
        time.sleep(random.uniform(2, 5))  # Random delay
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extracting profile data
        name = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
        headline = soup.find('div', {'class': 'text-body-medium'}).text.strip() if soup.find('div', {'class': 'text-body-medium'}) else 'N/A'

        # Extracting work experience
        work_experiences = []
        work_section = soup.find_all('section', {'id': 'experience-section'})
        for work in work_section:
            positions = work.find_all('li', {'class': 'result-card'})
            for position in positions:
                job_title = position.find('h3').text.strip() if position.find('h3') else 'N/A'
                company = position.find('p', {'class': 'pv-entity__secondary-title'}).text.strip() if position.find('p', {'class': 'pv-entity__secondary-title'}) else 'N/A'
                duration = position.find('span', {'class': 'pv-entity__date-range'}).text.strip() if position.find('span', {'class': 'pv-entity__date-range'}) else 'N/A'
                work_experiences.append(f"{job_title} at {company} ({duration})")

        # Extracting education
        education_list = []
        education_section = soup.find_all('section', {'id': 'education-section'})
        for education in education_section:
            schools = education.find_all('li', {'class': 'result-card'})
            for school in schools:
                school_name = school.find('h3').text.strip() if school.find('h3') else 'N/A'
                degree = school.find('span', {'class': 'pv-entity__degree-name'}).text.strip() if school.find('span', {'class': 'pv-entity__degree-name'}) else 'N/A'
                field_of_study = school.find('span', {'class': 'pv-entity__fos'}).text.strip() if school.find('span', {'class': 'pv-entity__fos'}) else 'N/A'
                education_list.append(f"{degree} in {field_of_study} from {school_name}")

        # Extracting projects
        projects_list = []
        projects_section = soup.find_all('section', {'id': 'projects-section'})
        for project in projects_section:
            project_items = project.find_all('li', {'class': 'result-card'})
            for item in project_items:
                project_title = item.find('h3').text.strip() if item.find('h3') else 'N/A'
                project_description = item.find('p', {'class': 'pv-entity__description'}).text.strip() if item.find('p', {'class': 'pv-entity__description'}) else 'N/A'
                projects_list.append(f"{project_title}: {project_description}")

        # Add scraped data to the list
        profile_data.append({
            'Name': name,
            'Headline': headline,
            'Profile URL': link,
            'Work Experience': '; '.join(work_experiences) if work_experiences else 'N/A',
            'Education': '; '.join(education_list) if education_list else 'N/A',
            'Projects': '; '.join(projects_list) if projects_list else 'N/A'
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
    pagesNumber = 20
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