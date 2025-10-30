import time
import random
import asyncio
import pyperclip
from func import css_click_center,xpath_click_center,click_checkboxes







async def Facebook_MarketPlace_Bot(page,df):
    await page.bringToFront()
    await xpath_click_center(page, '//span[contains(text(), "Sell Something")]')
    await asyncio.sleep(2)
    await xpath_click_center(page, '//span[contains(text(), "Item for sale")]')
    await asyncio.sleep(2)

    img = [eval(x) for x in df['PRODUCT_PIC_URLS']][0]
    # Step 1: Find all image-type file inputs
    file_inputs = await page.querySelectorAll('input[type="file"][accept*="image"]')
    if not file_inputs:
        print("❌ No image file inputs found!")
    else:
        print(f"ℹ️ Found {len(file_inputs)} image file inputs. Filtering...")

        # Step 2: Choose the input with multiple upload enabled
        target_input = None
        for i, input_elem in enumerate(file_inputs):
            accept_attr = await page.evaluate('(el) => el.getAttribute("accept")', input_elem)
            multiple_attr = await page.evaluate('(el) => el.hasAttribute("multiple")', input_elem)
            if "image" in accept_attr and multiple_attr:
                target_input = input_elem
                print(f"✅ Picked file input #{i} (multiple upload enabled)")
                break

        # Step 3: Fallback if no multiple input found
        if not target_input:
            target_input = file_inputs[-1]
            print("ℹ️ No multiple-input found. Using last available input.")

        # Step 4: Make it visible
        await page.evaluate('el => el.style.display = "block"', target_input)

        # Step 5: Upload the file
        await target_input.uploadFile(*img)
        print("✅ File uploaded to input successfully")

        # Step 6: Dispatch React’s change event
        await page.evaluate('''el => {
            const event = new Event('change', { bubbles: true });
            el.dispatchEvent(event);
        }''', target_input)
        print("✅ Change event dispatched successfully")


        # Step 7: Disable the input after upload to stop re-triggers
        await page.evaluate('''el => {
            el.disabled = true;
            el.style.display = "none";
        }''', target_input)
        print("🧩 Input disabled to prevent multiple uploads")

        await asyncio.sleep(2)


    await asyncio.sleep(2)

    title_input = await page.waitForXPath('//span[text()="Title"]/following-sibling::input')
    await asyncio.sleep(2)
    title_input.click()
    await title_input.type(f"{df['NAME'][0].split(',')[0]}")

    price_input = await page.waitForXPath('//span[contains(text(),"Price")]/following-sibling::input')
    await asyncio.sleep(2)
    price_input.click()
    await price_input.type(f"{df['PRODUCT_PRICE'][0]}")

    await asyncio.sleep(2)
    await xpath_click_center(page,'//label[.//span[text()="Condition"]]')
    await asyncio.sleep(2)
    new_option_handle = await page.evaluateHandle('''
    () => {
        const el = Array.from(document.querySelectorAll('div[role="option"]'))
            .find(e => e.innerText && e.innerText.trim() === "New");
        if (el) {
            // Scroll it smoothly to the center
            el.scrollIntoView({ behavior: "smooth", block: "center" });
        }
        return el || null;
    }
    ''')

    if new_option_handle:
        box = await new_option_handle.boundingBox()
        if box:
            x = box['x'] + box['width'] / 2
            y = box['y'] + box['height'] / 2
            await page.mouse.click(x, y)
            print("✅ 'New' option clicked successfully!")
        else:
            print("❌ Element found but not visible.")
    else:
        print("❌ 'New' option not found on this page.")

    await asyncio.sleep(2)
    more_details = await page.waitForXPath('//div[@role="button" and .//span[text()="More details"]]')
    expanded = await page.evaluate('(element) => element.getAttribute("aria-expanded")', more_details)
    if expanded == "false":
        await more_details.click()
        print("✅ Clicked to open the 'More details' section.")
    else:
        print("ℹ️ 'More details' section already open.")

    await xpath_click_center(page,'//label[.//span[text()="Description"]]//textarea')
    await asyncio.sleep(1)
    await xpath_click_center(page,'//label[.//span[text()="Description"]]//textarea')

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
    pyperclip.copy(text_content)
    await asyncio.sleep(1)
    await xpath_click_center(page,'//label[.//span[text()="Description"]]//textarea')
    await page.keyboard.down('Control')
    await page.keyboard.press('V')
    await page.keyboard.up('Control')
    await asyncio.sleep(3)

    await css_click_center(page, 'div[role="button"][aria-label="Next"]')
    await asyncio.sleep(2)

    marketplace_btn = await page.evaluateHandle('''() => {
        const btn = Array.from(document.querySelectorAll('div[role="button"]'))
            .find(el => el.innerText && el.innerText.trim().includes("Marketplace"));
        return btn || null;
    }''')
    if marketplace_btn:
        # Scroll it smoothly to the center of the viewport
        await page.evaluate('el => el.scrollIntoView({ behavior: "smooth", block: "center" })', marketplace_btn)
        await marketplace_btn.click()
        print("✅ 'Marketplace' button clicked successfully!")
    else:
        print("❌ 'Marketplace' button not found on this page.")

    await asyncio.sleep(2)
    await click_checkboxes(page, max_clicks=20, delay=0.5)

    await css_click_center(page, 'div[role="button"][aria-label="Post"]')


    await asyncio.sleep(10)
