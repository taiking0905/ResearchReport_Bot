from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from slack_sdk import WebClient



def scrape_and_notify():
    options.binary_location = "/usr/bin/chromium-browser" 
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get('https://fukaya-lab.azurewebsites.net/report.html?id=T122115')

    elem = driver.find_element_by_css_selector('div[data-bind*="current().first"]')
    text = elem.text if elem else ''

    driver.quit()

    if not text:
        client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        client.chat_postMessage(channel=os.environ['SLACK_CHANNEL'], text="まだだよ")

if __name__ == "__main__":
    scrape_and_notify()
