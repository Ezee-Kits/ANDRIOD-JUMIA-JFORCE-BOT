# JUMIA JFORCE BOT — Full Mobile & Desktop Social Posting / Marketplace Uploader

**Short description:**  
JUMIA JFORCE BOT is a complete automation toolkit that scrapes Jumia product pages, builds product datasets (images, specs, prices), and automatically posts those products across social platforms (Facebook, Twitter/X, Instagram, Facebook Marketplace, etc.). Designed to run on **Android (Termux)** or desktop (Windows/Linux) using **Pyppeteer / Chromium**. Full setup and walkthrough on my YouTube channel — **Ezee Kits**.

---

## 🚀 What this project does (big-picture)
This repository automates the entire pipeline from **finding Jumia product URLs** → **extracting product information and images** → **building product CSVs** → **posting product ads** across multiple social channels — fully unattended once configured.

It’s organized into **3 main folders** (as you designed) plus a set of Python scripts that orchestrate crawling, data saving, and posting.

---

## 📁 Main repository layout

Jumia-JForce-Bot/
├── ALL-URLS/ # scraped urls CSVs (ALL URL.csv)
├── PRODUCT/ # product folders / csvs / product images
├── PY-FILES/ # core .py scripts (main, posting bot, platform-specific bots)
│ ├── main.py # crawler & product extractor (Jumia)
│ ├── posting_bot.py # orchestrator (launches browser tabs & platform bots)
│ ├── Facebook.py # Facebook posting logic
│ ├── Twitter.py # Twitter (X) posting logic
│ ├── Instagram.py # Instagram posting logic
│ ├── FB_MarketPlace.py # Facebook Marketplace posting logic
│ ├── jumiaBot_Phone.py # Termux / Android entry (mobile config)
│ └── func.py # utilities (csv save, click helpers, screenshot, XPath helpers)
├── CSV FILES/ # runtime logs + saved daily data
└── README.md # this file



---

## 🔎 Components explained (detailed)

### 1) `ALL-URLS/`
- Stores `ALL URL.csv` — every Jumia product page URL your crawler captured.
- Purpose: keep a queue of candidate product pages to parse into product items.

### 2) `PRODUCT/`
- Each product saved here includes:
  - Product CSV with fields like `NAME`, `BRAND`, `PRODUCT_PRICE`, `NAIRA_PRICE`, `KEY_FEATURES`, `SPECIFICATION`, `BAG_INFO`, `SELLER_INFO`, `PRODUCT_PIC_URLS`
  - Images folder (`pic_0.jpg`, `pic_1.jpg`, ...).
- These product items are consumed by posting scripts.

### 3) `PY FILES` (core scripts)
- `main.py` — crawler and product extractor:
  - Scrapes Jumia home → category → product links.
  - Downloads product images and saves product CSVs into `PRODUCT/`.
- `posting_bot.py` — orchestrator for desktop:
  - Launches Chrome/Chromium, opens multiple tabs, and runs posting flows (Facebook, Instagram, X, Marketplace).
- `jumiaBot_Phone.py` — Termux / Android entrypoint:
  - Same logic adapted to Termux Chromium paths and mobile-friendly options.
- `Facebook.py`, `Twitter.py`, `Instagram.py`, `FB_MarketPlace.py` — each contains the platform-specific posting flows:
  - Prepare message text (features, specs, contact).
  - Upload images, paste content, click publish, handle UI variations.
- `func.py` — utilities:
  - CSV save and dedupe functions
  - Directory helpers
  - Async helpers for clicking and scrolling using selectors/XPath
  - Screenshot and upload helpers

---

## ⚙️ Features (what makes it powerful)
- Full pipeline automation: discovery → product extraction → posting.
- Multi-tab concurrent posting (desktop) to speed up workflow.
- Termux-ready: runs on Android with Chromium installed.
- Uses real Chrome profile (`userDataDir`) for persistent sessions (keeps logins/cookies).
- Smart text builder: product name, price, features, specs formatted for social posts.
- Upload proof / screenshot automation where required.
- CSV logging & deduplication per day for traceability.

---

## 🛠️ Requirements & Dependencies

**Core:**
- Python 3.9+  
- Chromium / Google Chrome (desktop) or Chromium package in Termux (Android)

**Primary Python packages:**
```text
pyppeteer
pandas
beautifulsoup4
lxml
pyperclip
asyncio


Install via pip:

pip install pyppeteer pandas beautifulsoup4 lxml pyperclip


On Termux (Android) you also need:

pkg update && pkg upgrade -y
pkg install python git chromium -y


NOTE: On desktop, supply the correct executablePath to Chrome (example used in scripts). On Termux, the path is /data/data/com.termux/files/usr/lib/chromium/chrome.

🧭 Quick start — Desktop (Windows / Linux)

Clone repo:

git clone https://github.com/<your-username>/Jumia-JForce-Bot.git
cd Jumia-JForce-Bot


Install dependencies:

pip install -r requirements.txt
# OR individually:
pip install pyppeteer pandas beautifulsoup4 lxml pyperclip


Create or clone a Chrome profile (optional but recommended for persistent login):

Open Chrome → chrome://version → copy the Profile Path.

In posting_bot.py set userDataDir to a copy for automation (e.g. C:\Users\YOU\SE_ChromeProfile).

Run the orchestrator:

python posting_bot.py


It will open browser tabs, fetch a random product from PRODUCT/, and post across configured platforms.

🧭 Quick start — Android (Termux)

Install Termux, then install Python & Chromium:

pkg update && pkg upgrade -y
pkg install python git chromium -y
pip install pyppeteer pandas beautifulsoup4 lxml pyperclip


Clone repo:

git clone https://github.com/<your-username>/Jumia-JForce-Bot.git
cd Jumia-JForce-Bot


Run Termux entry:

python jumiaBot_Phone.py


Scripts use Chromium path and userDataDir configured for Termux.

You will be prompted to set up accounts the first run; after that sessions persist.

🧾 Usage examples (what you’ll see)

Crawling / extracting URLs

$ python main.py
LENGHT OF ALL LINKS =  120
CURRENTLY TARGETING URL : https://www.jumia.com.ng/category?page=12#catalog-listing
Saved 120 product URLs to All Urls/ALL URL.csv


Extracting product info

Product name: Samsung Galaxy A14 6GB
Price: ₦ 120,000
Images saved: PRODUCT/product123/pic_0.jpg, pic_1.jpg
Saved product CSV -> PRODUCT/product123.csv


Posting

Opening Facebook tab...
Uploading images...
Composed message:
💥 Samsung Galaxy A14 💥
PRICE : ₦120,000
➡️ KEY FEATURES
- 6GB RAM
- 128GB Storage
POSTED ✅

✅ Best practices & tips

Use a cloned Chrome profile for automation (keeps cookies & prevents captchas). Create a dedicated profile for this bot.

Throttle actions (sleep between 1–5s) — prevents rapid-fire behavior that could trigger platform defenses.

Test in private / small groups before posting at scale (avoid spamming public groups).

Keep product images small (optimize) to avoid upload timeouts on mobile.

Back up your product CSVs regularly — they are the single source of truth.

Review platform TOS — automation can violate terms; use responsibly for permitted tasks only.



⚠️ Troubleshooting & common issues

Pyppeteer download errors: run python -m pyppeteer.install or install matching Chromium package.

Selectors changed / UI updated: platform UIs change often. If a click fails, inspect the web page and update selector/XPath in the matching bot file.

Timeouts on Termux: ensure Chromium is installed and Termux has appropriate storage permissions.

File upload fails: check input[type="file"] existence; some UIs use different upload widgets. Screenshot fallback is implemented in some flows.

Login issues: use a userDataDir with a logged-in profile or login manually the first run and keep the session.


⚙️ Extending & customizing

Add platform modules for Telegram, Pinterest, or others by following the pattern in Facebook.py.

Improve message templates in Facebook.py to support localization or multiple templates.

Add scheduling logic to post at optimal times.

Integrate a small GUI (Tkinter/CLI options) to select which platforms to post to on each run.

🧾 Author & support

Ezee Kits
Automation engineer & developer. I explained installation, Termux setup, and full walkthrough on my YouTube channel — go watch the full tutorial for visual step-by-step guidance:

👉 YouTube: https://www.youtube.com/@Ezee_Kits

📧 Email: ezeekits@gmail.com

NOTE: Do not include my real name in public repo files; use Ezee Kits as author.

📜 License

MIT License — free to use, modify, and redistribute. Please keep credit to Ezee Kits in the README or project header.



Jumia JForce Bot — Scrape Jumia products and auto-post to Facebook, X, Instagram & Marketplace. Termux-ready mobile automation with a full step-by-step YouTube tutorial by Ezee Kits.
