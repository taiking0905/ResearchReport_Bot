import os
import asyncio
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = os.environ['SCRAPE_URL']
DISCORD_TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])

# --- Discordにメッセージを送る関数 ---
async def send_discord_message(message):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel = client.get_channel(CHANNEL_ID)
        await channel.send(message)
        await client.close()

    await client.start(DISCORD_TOKEN)

# --- スクレイピングしてテキストを取得 ---
def scrape_and_get_text():
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL)

        wait = WebDriverWait(driver, 10)
        elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-bind*="current().first"]')))
        
        # innerTextを直接使って空チェック
        wait.until(lambda d: elem.text.strip() != '')
        text = elem.text.strip()
        return text
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None
    finally:
        driver.quit()


# --- 実行部分 ---
if __name__ == "__main__":
    text = scrape_and_get_text()

    if text is None or text == "":
        asyncio.run(send_discord_message("@here まだだよ"))
    else:
        asyncio.run(send_discord_message(f"書いてあるね！\n{text}"))
