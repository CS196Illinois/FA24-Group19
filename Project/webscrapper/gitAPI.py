'''
from time import sleep 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 

options = webdriver.ChromeOptions() 
options.add_argument("headless") 

exe_path = 'C:/Users/pillai7/Downloads/chromedriver-win64/chromedriver.exe'
service = Service(exe_path) 
driver = webdriver.Chrome(service=service, options=options) 

driver.get("https://www.linkedin.com/login") 
sleep(6) 

linkedin_username = "chaitempura@gmail.com"
linkedin_password = "qwerty@123"

driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[\1]/input").send_keys(linkedin_username) 
driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[\2]/input").send_keys(linkedin_password) 
sleep(3) 
driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[\3]/button").click() 

profiles = ['https://www.linkedin.com/in/vinayak-rai-a9b231193/', 'https://www.linkedin.com/in/dishajindgar/', 'https://www.linkedin.com/in/ishita-rai-28jgj/'] 

for i in profiles: 
	driver.get(i) 
	sleep(5) 
	title = driver.find_element(By.XPATH, "//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']").text 
	print(title) 
	description = driver.find_element(By.XPATH, "//div[@class='text-body-medium break-words']").text 
	print(description) 
	sleep(4) 
driver.close() 
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options
options = webdriver.ChromeOptions()
# options.add_argument("headless")  # Uncomment for headless mode
options.add_argument('--disable-web-security')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

exe_path = 'C:/Users/pillai7/Downloads/chromedriver-win64/chromedriver.exe'
service = Service(exe_path)
driver = webdriver.Chrome(service=service, options=options)

driver.implicitly_wait(10)  # Set an implicit wait

try:
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
    print("Logged in successfully.")

    # Proceed with profile scraping
    profiles = [
        'https://www.linkedin.com/in/vinayak-rai-a9b231193/',
        'https://www.linkedin.com/in/dishajindgar/',
        'https://www.linkedin.com/in/ishita-rai-28jgj/'
    ]

    for profile in profiles:
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

finally:
    driver.quit()  # Ensure the browser closes even if an error occurs

