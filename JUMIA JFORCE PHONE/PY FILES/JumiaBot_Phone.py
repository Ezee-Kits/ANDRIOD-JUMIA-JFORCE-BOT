import os
import time
import asyncio
import warnings
import pandas as pd
from pyppeteer import launch
from Twitter import Twitter_Bot
from Facebook import Facebook_Bot
from Instagram import Instagram_Bot
from FB_MarketPlace import Facebook_MarketPlace_Bot
from Main import main_func_random,Getting_urls
from func import create_dir

warnings.filterwarnings("ignore", category=RuntimeWarning, module="pyppeteer")



product_dir = create_dir('PRODUCT')
  



async def main():
    browser = await launch({
        'executablePath': '/data/data/com.termux/files/usr/lib/chromium/chrome',
        'args':[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-software-rasterizer",
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-popup-blocking",
            "--disable-infobars",
            "--password-store=basic",
            "--use-mock-keychain",
            "--ignore-certificate-errors",
            "--allow-running-insecure-content",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=1920,1080",
            "--start-maximized",
            "--force-device-scale-factor=1",
            "--high-dpi-support=1",
        ],
        'headless': False,
        'userDataDir': '/data/data/com.termux/files/home/JForceBrowserData'
    })



    tab1 = await browser.newPage()
    tab2 = await browser.newPage()
    tab3 = await browser.newPage()
    tab4 = await browser.newPage()

    # 3. Give each tab a name for reference
    tabs = {
        "Facebook": tab1,
        "Twitter": tab2,
        "Instagram": tab3,
        "Facebook_MarketPlace": tab4
    }


    for all_runings in range(1,100):
        if all_runings % 5 == 0:
            Getting_urls()

        for retrying in range(5):
            try:
                main_func_random()
                product_csv_path = [os.path.join(product_dir, file_name) for file_name in os.listdir(product_dir) if file_name.endswith('csv')][0]
                product_df = pd.read_csv(product_csv_path)
                if product_csv_path:
                    print('THE PRODUCT CSV PATH IS VALID >>>>>>>',product_csv_path)
                    break
            except:
                print('\n ERROR OCCURED IN THE RUNNING OF THE CSV PRODUCT FILE AND RETRYING {retrying}\n')



        try:
            try:
                await tabs["Facebook"].close()
            except Exception as e:
                print("⚠️ Could not close old Facebook tab:", e)
            tabs["Facebook"] = await browser.newPage()
            await tabs["Facebook"].goto("https://web.facebook.com/", {"timeout": 0,"waitUntil": "networkidle2"})
            await Facebook_Bot(page=tabs["Facebook"], df=product_df)
        except:
            print('\n ERROR HAPPENDED ON Facebook \n')
        
        try:

            try:
                await tabs["Facebook_MarketPlace"].close()
            except Exception as e:
                print("⚠️ Could not close old Facebook_MarketPlace tab:", e)
            tabs["Facebook_MarketPlace"] = await browser.newPage()
            await tabs["Facebook_MarketPlace"].goto("https://web.facebook.com/groups/361814259953483", {"timeout": 0,"waitUntil": "networkidle2"})
            await Facebook_MarketPlace_Bot(page=tabs["Facebook_MarketPlace"], df=product_df)
        
        except:
            print('\n ERROR HAPPENDED ON Facebook_MarketPlace \n')

        try:
            try:
                await tabs["Instagram"].close()
            except Exception as e:
                print("⚠️ Could not close old Instagram tab:", e)
            tabs["Instagram"] = await browser.newPage()
            await tabs["Instagram"].goto("https://www.instagram.com/", {"timeout": 0,"waitUntil": "networkidle2"})
            await Instagram_Bot(page=tabs["Instagram"], df=product_df)
        except:
            print('\n ERROR HAPPENDED ON Instagram \n')


        try:
            try:
                await tabs["Twitter"].close()
            except Exception as e:
                print("⚠️ Could not close old Twitter tab:", e)
            tabs["Twitter"] = await browser.newPage()
            await tabs["Twitter"].goto("https://x.com/home", {"timeout": 0,"waitUntil": "networkidle2"})
            await Twitter_Bot(page=tabs["Twitter"], df=product_df)
        except:
            print('\n ERROR HAPPENDED ON Twitter \n')
            
        await asyncio.sleep(7)  # Wait for 7 seconds before the next iteration

    await browser.close()

asyncio.run(main())


