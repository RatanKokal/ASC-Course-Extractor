import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client

# Function to send WhatsApp notification
def send_whatsapp_notification(changed_table):
    # Twilio credentials (replace with your details)
    account_sid = ''  # Replace with your Twilio Account SID
    auth_token = ''    # Replace with your Twilio Auth Token
    client = Client(account_sid, auth_token)

    # WhatsApp numbers (replace with your phone numbers)
    from_whatsapp_number = 'whatsapp:+14155238886'  # Twilio's WhatsApp sandbox number
    to_whatsapp_number = ''  # Recipient's WhatsApp number

    # Create the message content
    message_body = f"The table has changed:\n\n{changed_table.to_string()}"

    # Send WhatsApp message
    message = client.messages.create(
        body=message_body,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )

    print(f"WhatsApp notification sent. SID: {message.sid}")

# Initialize WebDriver
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# Navigate to the page
driver.get('https://asc.iitb.ac.in/acadmenu/index.jsp')

input("Press Enter after completing CAPTCHA...")

# Locate the frame and click on the link
driver.switch_to.frame('leftname')
element = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr/td[2]/div/div/div/div/div[1]/table/tbody/tr/td[1]')
element.click()
element = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr/td[2]/div/div/div/div/div[1]/div/div[11]/table/tbody/tr/td[3]/a')
element.click()
element = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr/td[2]/div/div/div/div/div[1]/div/div[11]/div/div[1]/table/tbody/tr/td[4]/a[2]')
element.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Select the current semester
driver.switch_to.default_content()
driver.switch_to.frame('right2')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(2)

# Locate the table and extract data
table = driver.find_element(By.XPATH, '/html/body/center/table[4]')
rows = table.find_elements(By.XPATH, './/tr')

# Extract table data into a list
table_data = []
for row in rows:
    cells = row.find_elements(By.TAG_NAME, 'td')
    table_data.append([cell.text for cell in cells])

# Convert the data into a DataFrame
current_df = pd.DataFrame(table_data)

# Initialize previous_df to compare with the first data scrape
previous_df = current_df.copy()

# Continuous monitoring
while True:
    time.sleep(30)  # Check every 30 seconds
    driver.refresh()

    # Locate the frame and click on the link
    driver.switch_to.frame('leftname')
    element = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr/td[2]/div/div/div/div/div[1]/table/tbody/tr/td[1]')
    element.click()
    element = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr/td[2]/div/div/div/div/div[1]/div/div[11]/table/tbody/tr/td[3]/a')
    element.click()
    element = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr/td[2]/div/div/div/div/div[1]/div/div[11]/div/div[1]/table/tbody/tr/td[4]/a[2]')
    element.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Select the current semester
    driver.switch_to.default_content()
    driver.switch_to.frame('right2')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(2)

    # Re-locate and extract table data
    table = driver.find_element(By.XPATH, '/html/body/center/table[4]')
    rows = table.find_elements(By.XPATH, './/tr')

    table_data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        table_data.append([cell.text for cell in cells])

    # Convert to DataFrame
    current_df = pd.DataFrame(table_data)

    # Compare current table with previous table
    if not current_df.equals(previous_df):
        print("Table has changed!")
        send_whatsapp_notification(current_df)  # Send notification
        previous_df = current_df.copy()  # Update previous data

# Close the browser session
driver.quit()
