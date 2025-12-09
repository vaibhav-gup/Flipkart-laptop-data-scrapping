from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

driver = webdriver.Edge()
query = "laptops"
file = 0

os.makedirs("data", exist_ok=True)

for i in range(1, 96):
    driver.get(f"https://www.flipkart.com/search?q={query}&page={i}")
    time.sleep(3)

    elems = driver.find_elements(By.CLASS_NAME, "_75nlfW")
    print("Total number of products:", len(elems))

    for elem in elems:
        d = elem.get_attribute("outerHTML")
        if d:
            with open(f"data/{query}_{file}.html", "w", encoding="utf-8") as f:
                f.write(d)
                file += 1

    time.sleep(2)

driver.close()
