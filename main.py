# Import the library Selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Make browser open in background
options = webdriver.ChromeOptions()
options.add_argument('headless')

# Create the webdriver object
browser = webdriver.Chrome(ChromeDriverManager().install())


# Obtain the Google Map URL
url = ["https://www.google.com/maps/place/\
Papa+John's+Pizza/@40.7936551,-74.0124687,17z/data=!3m1!4b1!\
4m5!3m4!1s0x89c2580eaa74451b:0x15d743e4f841e5ed!8m2!3d40.\
7936551!4d-74.0124687", "https://www.google.com/maps/place/\
Lucky+Dhaba/@30.653792,76.8165233,17z/data=!3m1!4b1!4m5!3m4!\
1s0x390feb3e3de1a031:0x862036ab85567f75!8m2!3d30.653792!4d76.818712"]

# Initialize variables and declare it 0
i = 0

# Create a loop for obtaining data from URLs
for i in range(len(url)):

	# Open the Google Map URL
	browser.get(url[i])

	# click "zaakceptuj wszystko"
	button_path = '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button'
	wait = WebDriverWait(browser, 1)
	button = wait.until(EC.visibility_of_element_located((By.XPATH, button_path)))
	button.click()
	wait = WebDriverWait(browser, 1)

	# Obtain the title of that place
	title = browser.find_element(By.CLASS_NAME,
		"x3AX1-LfntMc-header-title-title")
	print(i+1, "-", title.text)

	# Obtain the address of that place
	address = browser.find_elements(By.CLASS_NAME,"CsEnBe")[0]
	print("Address: ", address.text)
	print("\n")
