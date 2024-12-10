import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

MAPION_KYOTO_STREETS_URL = "https://www.mapion.co.jp/phonebook/M08015/26100/"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(30)
driver.set_page_load_timeout(30)

current_url = MAPION_KYOTO_STREETS_URL
street_names = set()
while True:
    driver.get(current_url)
    print(current_url)

    current_street_names = driver.find_elements(
        By.XPATH, '//table[@class="list-table"]/tbody/tr/th//a'
    )
    current_street_names = list(
        map(lambda a_tag: a_tag.get_attribute("title"), current_street_names)
    )
    street_names.update(current_street_names)

    next_page_link = driver.find_elements(By.XPATH, '//a[@class="pagination-link"]')[-1]
    if next_page_link.text != "後へ":
        break
    next_page_link = next_page_link.get_attribute("href")
    current_url = next_page_link

    time.sleep(10)

driver.quit()

df_streets = pd.DataFrame(street_names, columns=["street"])
df_streets.to_csv("data/streets.csv", index=False)
