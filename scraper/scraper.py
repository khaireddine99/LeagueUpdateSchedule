from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time, json

# Setup Edge in headless mode
edge_options = Options()


# Path to Edge WebDriver
driver = webdriver.Edge(options=edge_options)

# url to scrape 
url = 'https://support-leagueoflegends.riotgames.com/hc/en-us/articles/360018987893-Patch-Schedule-League-of-Legends'

driver.get(url)

time.sleep(10)

tds = driver.find_elements(By.XPATH, "//td")

dates = []
patches = []

for i, item in enumerate(tds):
    if i % 2 == 0:
        dates.append(item.text)

    else:
        patches.append(item.text)

print(f'our dates are {dates}')
print(f'our patches are {patches}')

# Combine into list of dicts
combined = [{"value": d, "date": v} for d, v in zip(dates, patches)]

# Save as JSON file
with open("output.json", "w") as f:
    json.dump(combined, f, indent=4)

# Close browser
driver.quit()