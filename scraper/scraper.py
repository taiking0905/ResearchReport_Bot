from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from slack_sdk import WebClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_and_notify():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser" 
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    
    driver.get('https://fukaya-lab.azurewebsites.net/report.html?id=T122115')

    # 最大10秒待機して要素が見つかるのを待つ
    wait = WebDriverWait(driver, 10)
    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-bind*="current().first"]')))

    # innerTextが入るのをさらに待つ
    wait.until(lambda d: elem.text.strip() != '')
    text = elem.text.strip()

    driver.quit()

    if not text:
        client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        client.chat_postMessage(channel=os.environ['SLACK_CHANNEL'], text="まだだよ")

if __name__ == "__main__":
    scrape_and_notify()
