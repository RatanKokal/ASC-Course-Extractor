from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.implicitly_wait(10)

driver.get('https://asc.iitb.ac.in/acadmenu/index.jsp')

input()

# Locate the frame and click on the link
driver.switch_to.frame('leftname')
element = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr/td[2]/div/div/div/div/div[1]/table/tbody/tr/td[1]')
element.click()
element = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr/td[2]/div/div/div/div/div[1]/div/div[6]/table/tbody/tr/td[2]')
element.click()
element = driver.find_element(By.XPATH, '/html/body/div[1]/table/tbody/tr/td[2]/div/div/div/div/div[1]/div/div[6]/div/div[1]/table/tbody/tr/td[4]/a[2]')
element.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Select the current semester
driver.switch_to.default_content()
driver.switch_to.frame('right2')
dropdown = Select(driver.find_element(By.NAME, 'year'))
dropdown.select_by_value('2024')
dropdown = Select(driver.find_element(By.NAME, 'semester'))
dropdown.select_by_value('1')
element = driver.find_element(By.NAME, 'submit')
element.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(2)

table = driver.find_element(By.XPATH, '/html/body/table')
rows = table.find_elements(By.XPATH , './/tr')
length = len(rows)

for ind in range(3, length):
    driver.switch_to.default_content()
    driver.switch_to.frame('right2')
    table = driver.find_element(By.XPATH, '/html/body/table')
    rows = table.find_elements(By.XPATH , './/tr')
    row = rows[ind]
    try:
        col = row.find_elements(By.XPATH,'.//td')[0]
        link = row.find_elements(By.XPATH,'.//a')
        name = link[0].text
        link[0].click()
        time.sleep(3)
        driver.switch_to.default_content()
        driver.switch_to.frame('right2')
        with open(name+'.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        driver.back()
    except:
        pass
    time.sleep(2)

# Close the browser session
driver.quit()