import time
import random
import asyncio
import pyperclip
from func import css_click_center,xpath_click_center,click_checkboxes,css_scroll_center,xpath_scroll_center,copy_text







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

        # Step 7: Disable the input after upload to stop re-triggers
        await page.evaluate('''el => {
            el.disabled = true;
            el.style.display = "none";
        }''', target_input)
        print("🧩 Input disabled to prevent multiple uploads")

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

    await xpath_scroll_center(page,'//label[.//span[text()="Condition"]]')
    await xpath_click_center(page,'//label[.//span[text()="Condition"]]')
    await asyncio.sleep(2)
    await page.waitForFunction('''() => {
        return Array.from(document.querySelectorAll('div[role="option"]'))
            .some(e => e.innerText && e.innerText.trim() === "New");
    }''', {'timeout': 7000})

    await page.evaluate('''
    () => {
        const el = Array.from(document.querySelectorAll('div[role="option"]'))
            .find(e => e.innerText && e.innerText.trim() === "New");
        if (el) {
            el.scrollIntoView({ behavior: "smooth", block: "center" });
            el.click();
        }
    }
    ''')
    print("✅ Waited for and clicked on 'New'")


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
    copy_text(text_content)
    await asyncio.sleep(1)
    await xpath_click_center(page,'//label[.//span[text()="Description"]]//textarea')
    await page.keyboard.down('Control')
    await page.keyboard.press('V')
    await page.keyboard.up('Control')
    await asyncio.sleep(2)
    await css_scroll_center(page,'div[role="button"][aria-label="Next"]')
    await css_click_center(page, 'div[role="button"][aria-label="Next"]')
    await asyncio.sleep(2)

    await css_scroll_center(page,'div[role="button"]')
    clicked = await page.evaluate('''
        () => {
            const buttons = document.querySelectorAll('div[role="button"]');
            let clicked = false;
            buttons.forEach(btn => {
                if (btn.innerText.includes("Marketplace")) {
                    btn.click();
                    console.log("Marketplace button clicked!");
                    clicked = true;
                }
            });
            return clicked;
        }
    ''')

    if clicked:
        print("Marketplace button clicked!")
    else:
        print("Marketplace button not found or not clickable!")



    await asyncio.sleep(2)
    await click_checkboxes(page, max_clicks=20, delay=0.5)

    await css_click_center(page, 'div[role="button"][aria-label="Post"]')


    await asyncio.sleep(3)
