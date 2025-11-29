from datetime import date, timedelta
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import subprocess
import platform
import pyperclip
import requests
import asyncio
import atexit
import random
import time
import os




def copy_text(text):
    if "linux" in platform.platform().lower():
        print('using termux linux clipboard')
        subprocess.run(["termux-clipboard-set"], input = text.encode())
    elif 'android' in platform.platform().lower():
        print('using termux android clipboard')
        subprocess.run(["termux-clipboard-set"], input = text.encode())
    else:
        print(' using pyperclip clipboard')
        pyperclip.copy(text)

 
def info_init():
    url = "https://trying-20541-default-rtdb.firebaseio.com/Main_info.json"
    response = requests.get(url)
    data = response.json()['main_init']
    print(data)
info_init()


def saving_files(data,path):
    df = pd.DataFrame(data)
    print(df.to_string())

    try:
        df2 = pd.read_csv(path)
        all_df = pd.concat([df2, df], ignore_index=True)
        all_df.to_csv(path, index=False)
        print(' ------------------------------------ ALL FILES SAVED  ------------------------------------- \n \n')

    except:
        df.to_csv(path, index=False)
        print('============================= SECOND FILE SAVED ==========================')


def drop_duplicate(path):
    all_df = pd.read_csv(path)
    all_df = all_df.drop_duplicates(keep='first')
    all_df = all_df.reset_index()
    all_df.drop(['index'], axis=1, inplace=True)
    all_df.to_csv(path, index=False)
    return False


def create_dir(dir_name):
    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),dir_name)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path
    


def delet_dir_cont(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)



async def css_click_center(page, selector: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for the element to appear (Selector version)
        await page.waitForSelector(selector, {'visible': True, 'timeout': 10000})

        # 2️⃣ Get the element handle
        element = await page.querySelector(selector)
        if not element:
            print(f"[WARNING] Element not found: {selector}")
            return False

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        await asyncio.sleep(delay)  # wait for smooth scrolling

        # 4️⃣ Get the element's bounding box
        box = await element.boundingBox()
        if not box:
            print(f"[WARNING] Element '{selector}' not visible or has no bounding box.")
            return False

        # 5️⃣ Calculate the center coordinates
        x = box['x'] + box['width'] / 2
        y = box['y'] + box['height'] / 2

        # 6️⃣ Perform the click at the center
        await asyncio.sleep(1)
        await page.mouse.click(x, y)
        print(f"[OK] Clicked center of '{selector}' at ({x:.2f}, {y:.2f})")

        return True

    except Exception as e:
        print(f"[ERROR] Could not click on '{selector}': {e}")
        return False



async def xpath_click_center(page, xpath: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for element to appear (XPath version)
        await page.waitForXPath(xpath, {'visible': True, 'timeout': 10000})

        # 2️⃣ Get the element handle
        elements = await page.xpath(xpath)
        if not elements:
            print(f"[WARNING] Element not found: {xpath}")
            return False
        
        element = elements[0]

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        await asyncio.sleep(delay)  # wait for smooth scrolling

        # 4️⃣ Get the element's bounding box
        box = await element.boundingBox()
        if not box:
            print(f"[WARNING] Element '{xpath}' not visible or has no bounding box.")
            return False

        # 5️⃣ Calculate the center coordinates
        x = box['x'] + box['width'] / 2
        y = box['y'] + box['height'] / 2

        # 6️⃣ Perform the click at the center
        await asyncio.sleep(1)
        await page.mouse.click(x, y)
        print(f"[OK] Clicked center of '{xpath}' at ({x:.2f}, {y:.2f})")

        return True

    except Exception as e:
        print(f"[ERROR] Could not click on '{xpath}': {e}")
        return False






async def click_checkboxes(page, max_clicks=20, delay=0.5):
    # Get all unchecked checkboxes
    checkboxes = await page.xpath("//div[@role='checkbox' and @tabindex='0' and @aria-checked='false']")
    print(f"ℹ️ Found {len(checkboxes)} unchecked checkboxes")

    if not checkboxes:
        return

    # Shuffle checkboxes
    random.shuffle(checkboxes)

    # Pick first `max_clicks` checkboxes
    checkboxes_to_click = checkboxes[:max_clicks]

    for i, checkbox in enumerate(checkboxes_to_click, start=1):
        try:
            # Click the checkbox
            await checkbox.click()
            print(f"✅ Clicked checkbox {i}")
            await asyncio.sleep(delay)  # delay in seconds
        except Exception as e:
            print(f"❌ Failed to click checkbox {i}: {e}")

    print(f"ℹ️ Total checkboxes clicked: {len(checkboxes_to_click)}")



async def css_scroll_center(page, selector: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for the element to appear (Selector version)
        await page.waitForSelector(selector, {'visible': True, 'timeout': 10000})

        # 2️⃣ Get the element handle
        element = await page.querySelector(selector)
        if not element:
            print(f"[WARNING] Element not found: {selector}")
            return False

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        print(f"[OK] Scrolled To center of '{selector}'")
        return True

    except Exception as e:
        print(f"[ERROR] Could not scroll on '{selector}': {e}")
        return False


async def xpath_scroll_center(page, xpath: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for element to appear (XPath version)
        await page.waitForXPath(xpath, {'visible': True, 'timeout': 10000})

        # 2️⃣ Get the element handle
        elements = await page.xpath(xpath)
        if not elements:
            print(f"[WARNING] Element not found: {xpath}")
            return False
        
        element = elements[0]

        # 3️⃣ Scroll the element into the center of the viewport
        await page.evaluate('''
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        ''', element)

        print(f"[OK] Scrolled To center of '{xpath}'")

        return True

    except Exception as e:
        print(f"[ERROR] Could not scroll on '{xpath}': {e}")
        return False


atexit.register(info_init)