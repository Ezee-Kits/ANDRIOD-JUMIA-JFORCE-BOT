import time
import asyncio
import pyperclip
from func import css_click_center,xpath_click_center



async def Twitter_Bot(page,df):
    await page.bringToFront()
    await css_click_center(page,'[data-testid="SideNav_NewTweet_Button"]')
    tweet_box = await page.waitForSelector('div[data-testid="tweetTextarea_0"]')
    await tweet_box.click()
    await asyncio.sleep(1)
    await tweet_box.click()
    # await asyncio.sleep(1)
    # await page.keyboard.down('Control')
    # await page.keyboard.press('A')
    # await page.keyboard.up('Control')
    # await page.keyboard.press('Backspace')
    # await tweet_box.click()
    # await asyncio.sleep(1)
    # await tweet_box.click()
    await asyncio.sleep(1)

    text_content = f'''
    💥 {df['NAME'][0].split(',')[0]} 💥

    PRICE : {df['NAIRA_PRICE'][0]}

    CONDITION : BRAND NEW
    👉 Pay After Delivery Is Avaliable 

    📞CALL OR WHATSAPP @ 09027794130
    '''
    pyperclip.copy(text_content)
    await asyncio.sleep(1)
    await tweet_box.click()
    await page.keyboard.down('Control')
    await page.keyboard.press('V')
    await page.keyboard.up('Control')
    await asyncio.sleep(2)

    # Upload image or video
    file_input = await page.waitForSelector('input[data-testid="fileInput"]')
    await asyncio.sleep(1.5)

    img = [eval(x) for x in df['PRODUCT_PIC_URLS']][0]
    await file_input.uploadFile(*img[:4])
    await asyncio.sleep(2)
    await xpath_click_center(page,'//button[contains(@data-testid, "tweetButton")]//span[text()="Post"]')
    await asyncio.sleep(10)