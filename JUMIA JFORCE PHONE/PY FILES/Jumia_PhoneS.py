
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth





executable_path = '/data/data/com.termux/files/usr/lib/chromium/chrome' # set to string path if required

async def main():
    args = [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--disable-renderer-backgrounding",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-blink-features=AutomationControlled",
        "--disable-extensions",
        "--disable-popup-blocking",
        "--disable-infobars",
        "--enable-features=UseOzonePlatform",
        "--ozone-platform=x11",
        "--password-store=basic",
        "--use-mock-keychain",
        "--ignore-certificate-errors",
        "--allow-running-insecure-content",
        "--no-first-run",
        "--no-default-browser-check",
        "--start-maximized",
        "--window-size=1280,800",
        "--enable-features=NetworkService,NetworkServiceInProcess",
    ]

    browser = await launch(
        headless=False,              # run headful for best stealth; set True if you must run headless (less reliable)
        args=args,
        executablePath=executable_path,
        userDataDir = "/data/data/com.termux/files/home/JForceBrowserData",
        ignoreDefaultArgs=["--enable-automation"],  # remove automation flag
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        defaultViewport={"width": 1280, "height": 800},
    )

    page = await browser.newPage()

    # Set a real-like user agent (rotate this in production)
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    await page.setUserAgent(ua)

    # Set languages and timezone to realistic values
    await page.setExtraHTTPHeaders({"Accept-Language": "en-US,en;q=0.9"})
    await page.evaluateOnNewDocument(
        """() => {
            // Pass the webdriver check
            Object.defineProperty(navigator, 'webdriver', { get: () => false, configurable: true });

            // Mock plugins and mimeTypes
            Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5], configurable: true });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'], configurable: true });

            // Fake chrome runtime
            window.chrome = { runtime: {} };

            // hardwareConcurrency (cores)
            try {
                Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
            } catch (e) {}

            // Provide a consistent webdriver-less userAgent platform
            Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
        }"""
    )

    # Apply pyppeteer_stealth tweaks (best-effort)
    await stealth(page)

    # Optional: set viewport & device scale
    await page.setViewport({"width": 1280, "height": 800, "deviceScaleFactor": 1})

    # Navigate to TikTok
    try:
        response = await page.goto(
            "https://www.tiktok.com/",
            {"waitUntil": "networkidle2", "timeout": 0}
        )
        print("Navigation response status:", response.status if response else "no response")
    except Exception as e:
        print("Goto error:", e)
    
    input('PRESS ENTER :::::::::::::::')

    # Wait a bit to let dynamic content load (adjust as needed)
    await asyncio.sleep(6)

    # Optionally: dismiss cookie consent dialog (example tries common selectors)
    try:
        # Example - adjust selectors to the site state/locale
        accept_buttons = [
            'button:has-text("Accept")',
            'button:has-text("I Accept")',
            'button[aria-label="accept"]',
            'button[title="Accept"]',
            'button:has-text("Agree")',
        ]
        for sel in accept_buttons:
            try:
                el = await page.querySelector(sel)
                if el:
                    await el.click()
                    print("Clicked cookie/consent button:", sel)
                    break
            except Exception:
                pass
    except Exception as e:
        print("Consent click error:", e)

    # Example: take screenshot to verify page loaded
    await page.screenshot({"path": "tiktok_home.png", "fullPage": False})
    print("Saved screenshot tiktok_home.png")

    # Keep browser open for manual inspection; close when done
    # await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
