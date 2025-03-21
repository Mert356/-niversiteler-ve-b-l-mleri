import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from universities_list import universities


def scrape_yokatlas(universities):
    
    driver = webdriver.Chrome()
    driver.get("https://yokatlas.yok.gov.tr/")
    wait = WebDriverWait(driver, 10)

    all_data = {}

    for uni in universities:
        try:
            print(f"{uni} için arama yapılıyor...")

            search_box = wait.until(EC.element_to_be_clickable((By.ID, "search")))
            search_box.click()
            search_box.clear()
            search_box.send_keys(uni)

            time.sleep(1)
            search_box.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            search_box.send_keys(Keys.ENTER)

            time.sleep(3)

            departments = driver.find_elements(By.XPATH, "//div[@style='overflow: hidden; text-overflow: ellipsis; white-space: nowrap;width:80%']")
            department_list = [dept.text.strip() for dept in departments if dept.text.strip()]

            if department_list:
                all_data[uni] = department_list
            else:
                print(f"{uni} için bölüm bulunamadı.")

        except Exception as e:
            print(f"Hata: {uni} işlenemedi. ({e})")

    driver.quit()

    with open("universiteler.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print("Tüm veriler 'universiteler.json' dosyasına kaydedildi.")

scrape_yokatlas(universities)
