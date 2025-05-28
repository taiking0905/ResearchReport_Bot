from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import discord
import asyncio

DISCORD_TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])  # 数字として扱う

async def send_discord_message(message):
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        channel = client.get_channel(CHANNEL_ID)
        await channel.send(message)
        await client.close()

    await client.start(DISCORD_TOKEN)

def scrape_and_get_text():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get('https://fukaya-lab.azurewebsites.net/report.html?id=T122115')

    wait = WebDriverWait(driver, 10)
    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-bind*="current().first"]')))
    wait.until(lambda d: elem.text.strip() != '')
    text = elem.text.strip()
    driver.quit()
    return text

if __name__ == "__main__":
    text = scrape_and_get_text()
    if not text:
        asyncio.run(send_discord_message("@here まだだよ"))
    else:
        asyncio.run(send_discord_message(f"書いてあるね！\n{text}"))
