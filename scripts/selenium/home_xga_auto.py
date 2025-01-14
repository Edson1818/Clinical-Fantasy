import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

# Specify the path to ChromeDriver
service = Service("C:/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Navigate to the EPL page
driver.get("https://understat.com/league/EPL")
print("Loading page...")
time.sleep(5)  # Wait for the page to load

# Click the 'home' tab
print("Clicking the 'home' tab...")
away_tab_xpath = "/html/body/div[1]/div[3]/div[3]/div/div[1]/div[2]/label[3]"
away_tab = driver.find_element(By.XPATH, away_tab_xpath)
away_tab.click()
print("'home' tab clicked.")
time.sleep(5)  # Wait for the table to load

# Locate the table rows
table_xpath = "//*[@id='league-chemp']/table/tbody/tr"
rows = driver.find_elements(By.XPATH, table_xpath)

print("Extracting data from the table...")
data = []

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells:
        team = cells[1].text.strip()  # Team name
        matches = cells[2].text.strip()  # Matches played (M)
        
      # Clean xG and xGA values using re.sub to remove green/red values
        xg_full_text = cells[9].text.strip()
        xg_cleaned = re.sub(r"[+-]\d+\.\d+", "", xg_full_text).strip()

        xga_full_text = cells[10].text.strip()
        xga_cleaned = re.sub(r"[+-]\d+\.\d+", "", xga_full_text).strip()

        data.append([team, matches, xg_cleaned, xga_cleaned])
        print(f"Row extracted: {team}, {matches}, {xg_cleaned}, {xga_cleaned}")

# Save the data into a DataFrame and export it to CSV
columns = ["Team", "M", "xG", "xGA"]
df = pd.DataFrame(data, columns=columns)
df.to_csv("away_table_data_cleaned.csv", index=False)
print("Data saved to 'away_table_data_cleaned.csv'.")

# Close the browser
driver.quit()