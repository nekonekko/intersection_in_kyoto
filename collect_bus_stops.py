import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

NAVITIME_KYOTO_BUS_TOP_URL = "https://www.navitime.co.jp/bus/route/busroutelist?cCode=00001064&cName=%E4%BA%AC%E9%83%BD%E5%B8%82%E4%BA%A4%E9%80%9A%E5%B1%80"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)


driver = webdriver.Chrome(options=options)
driver.implicitly_wait(30)
driver.set_page_load_timeout(30)

current_url = NAVITIME_KYOTO_BUS_TOP_URL
bus_links = []
while True:
    driver.get(current_url)

    current_bus_links = driver.find_elements(By.XPATH, '//li[@class="link"]/a')
    current_bus_links = list(
        map(lambda link: link.get_attribute("href"), current_bus_links)
    )
    bus_links.extend(current_bus_links)

    next_page_link = driver.find_element(By.XPATH, '//img[@alt="次へ"]').find_element(
        By.XPATH, ".."
    )
    next_page_link = next_page_link.get_attribute("href")
    if next_page_link is None:
        break
    current_url = next_page_link

bus_stops = set()
for bus_link in bus_links:
    driver.get(bus_link)
    print(driver.title)
    current_stop_links = driver.find_elements(By.XPATH, '//dt[@class="node_name"]/a')
    for stop_link in current_stop_links:
        bus_stops.add(stop_link.text)
    time.sleep(10)

driver.quit()

df_bus_stops = pd.DataFrame(bus_stops, columns=["bus_stop"])
df_bus_stops.to_csv("data/bus_stops.csv", index=False)
