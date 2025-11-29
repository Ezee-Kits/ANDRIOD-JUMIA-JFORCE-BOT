import time
import asyncio
import pyperclip

from func import css_click_center,xpath_click_center,copy_text
      


async def Facebook_Bot(page,df):
    await page.bringToFront()
    await xpath_click_center(page, '//span[contains(text(), "What\'s on your mind")]')

    file_input = await page.waitForSelector('input[type="file"]', {'visible': False})
    await asyncio.sleep(1.5)
    img = [eval(x) for x in df['PRODUCT_PIC_URLS']][0]
    await file_input.uploadFile(*img)
    await asyncio.sleep(2)


    fb_box = await page.waitForXPath('//div[@role="textbox" and @contenteditable="true"]')
    await fb_box.click()
    await asyncio.sleep(1)
    await fb_box.click()
    await asyncio.sleep(1)


    key_features = '\n'.join([f"- {x}" for x in eval(df['KEY_FEATURES'][0])])
    specifications = '\n'.join([f"- {x}" for x in eval(df['SPECIFICATION'][0])])
    text_content = f"""
    💥 {df['NAME'][0].split(',')[0]} 💥

    PRICE : {df['NAIRA_PRICE'][0]}

    
    ➡️  KEY FEATURES
    {key_features}

    
    ⚙️  SPECIFICATION
    {specifications}

    
    📦 CONDITION : BRAND NEW
    👉 Pay After Delivery Is Available

    
    Chat Up Now!!

    📞 CALL OR WHATSAPP @ 09027794130
    """


    copy_text(text_content)
    
    await asyncio.sleep(1)
    await fb_box.click()
    await page.keyboard.down('Control')
    await page.keyboard.press('V')
    await page.keyboard.up('Control')
    await asyncio.sleep(2)

    try:
        next_btn = await page.waitForXPath('//div[@role="button" and @aria-label="Next"]')
        await next_btn.click()
    except:
        post_btn = await page.waitForXPath('//div[@aria-label="Post" and @role="button"]')
        await post_btn.click()

    await asyncio.sleep(2)
    await xpath_click_center(page, '//div[@aria-label="Post" and @role="button"]')
    await asyncio.sleep(3)



 