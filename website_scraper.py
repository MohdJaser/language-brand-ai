# ============================================
# website_scraper.py — COMPLETE UPGRADED VERSION
# Works with ALL websites including:
# Amazon, Flipkart, BBC, Wikipedia, Swiggy,
# Instagram, any JavaScript heavy website!
# ============================================

import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ============================================
# STEP 1 — DETECT WEBSITE TYPE
# WHAT: Looks at the URL and decides what
#       kind of website it is
# WHY:  Amazon needs different extraction
#       than BBC or Wikipedia
# ============================================
def detect_website_type(url):
    url_lower = url.lower()

    if any(x in url_lower for x in [
        "amazon", "flipkart", "myntra",
        "meesho", "snapdeal", "ebay", "shopify"
    ]):
        return "ecommerce"

    elif any(x in url_lower for x in [
        "bbc", "cnn", "ndtv", "thehindu",
        "timesofindia", "reuters", "bloomberg"
    ]):
        return "news"

    elif any(x in url_lower for x in [
        "zomato", "swiggy", "ubereats", "doordash"
    ]):
        return "food"

    else:
        return "general"


# ============================================
# STEP 2 — SETUP CHROME BROWSER
# WHAT: Creates an invisible Chrome browser
# WHY:  JavaScript websites need a real
#       browser to load their content
# HOW:  Chrome runs silently in background
#       (headless mode — no window appears)
# ============================================
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    import platform
    if platform.system() == "Linux":
        # Streamlit Cloud (Linux server)
        options.binary_location = "/usr/bin/chromium"
        service = Service("/usr/bin/chromedriver")
    else:
        # Your Windows laptop
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    return driver

# ============================================
# STEP 3 — SMART SCROLL
# WHAT: Scrolls the page like a real user
# WHY:  Amazon, Flipkart load products only
#       when you scroll down the page
#       Without scrolling = empty results
# ============================================
def smart_scroll(driver, scrolls=4):
    last_height = driver.execute_script(
        "return document.body.scrollHeight"
    )

    for _ in range(scrolls):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(2)
        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )
        # Stop if no new content loaded
        if new_height == last_height:
            break
        last_height = new_height

    # Scroll back to top
    driver.execute_script("window.scrollTo(0, 0);")


# ============================================
# STEP 4 — EXTRACT CONTENT FROM ECOMMERCE
# WHAT: Pulls product titles, prices,
#       features, descriptions, reviews
# WHY:  E-commerce sites have specific HTML
#       structure — we target those elements
# ============================================
def extract_ecommerce(soup):
    special = {}

    # ── Product Title ──
    headings = []
    for sel in [
        "span#productTitle",
        ".B_NuCI",
        "h1.x-item-title",
        "[data-testid='title']",
        "h1", "h2"
    ]:
        for el in soup.select(sel)[:5]:
            t = el.get_text(strip=True)
            if t and len(t) > 5:
                headings.append(t)
        if headings:
            break

    # ── Price ──
    prices = []
    for sel in [
        "span.a-price-whole",
        "span#priceblock_ourprice",
        "span#priceblock_dealprice",
        ".CEmiEU", "._30jeq3",
        "[data-testid='price']",
        ".price"
    ]:
        for el in soup.select(sel)[:3]:
            t = el.get_text(strip=True)
            if t:
                prices.append(t)
        if prices:
            break

    if prices:
        special["prices"] = prices[:3]

    # ── Product Features ──
    features = []
    for sel in [
        "#feature-bullets li",
        ".features li",
        "ul.a-unordered-list li",
        ".product-features li"
    ]:
        for el in soup.select(sel)[:8]:
            t = el.get_text(strip=True)
            if t and len(t) > 10:
                features.append(t)
        if features:
            break

    if features:
        special["features"] = features[:8]

    # ── Product Description ──
    paragraphs = []
    for sel in [
        "#productDescription p",
        "#product-description",
        ".product-description",
        "div[data-testid='description']"
    ]:
        el = soup.select_one(sel)
        if el:
            t = el.get_text(strip=True)[:500]
            if t:
                paragraphs.append(t)
            break

    # ── Customer Reviews ──
    reviews = []
    for sel in [
        "span[data-hook='review-body']",
        ".review-text",
        ".review-body"
    ]:
        for el in soup.select(sel)[:3]:
            t = el.get_text(strip=True)[:200]
            if t:
                reviews.append(t)
        if reviews:
            break

    if reviews:
        special["reviews"] = reviews[:3]

    return headings, paragraphs, special


# ============================================
# STEP 5 — EXTRACT CONTENT FROM NEWS/GENERAL
# WHAT: Pulls headlines, articles, paragraphs
# WHY:  News sites have article-based layout
# ============================================
def extract_general(soup):
    headings = []
    paragraphs = []

    for tag in soup.find_all(["h1", "h2", "h3"]):
        t = tag.get_text(strip=True)
        if t and len(t) > 5:
            headings.append(t)

    for p in soup.find_all("p"):
        t = p.get_text(strip=True)
        if t and len(t) > 40:
            paragraphs.append(t)

    return headings[:10], paragraphs[:6], {}


# ============================================
# STEP 6 — MAIN SCRAPING FUNCTION
# WHAT: The main function that does everything
# HOW:  1. Opens Chrome browser
#        2. Goes to the website
#        3. Waits for JavaScript to load
#        4. Scrolls to get all content
#        5. Extracts all useful content
#        6. Closes browser
#        7. Returns clean content dictionary
# ============================================
def scrape_website(url):

    # Fix URL format
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    driver = None

    try:
        # ── Open Browser ──
        driver = get_driver()

        # ── Go to Website ──
        driver.get(url)

        # ── Wait for Page to Load ──
        # WHY: JavaScript takes time to run
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        # Extra wait for heavy JavaScript sites
        time.sleep(5)

        # ── Scroll for Dynamic Content ──
        smart_scroll(driver, scrolls=3)

        # ── Get Full Page HTML ──
        html = driver.page_source

        # ── Parse HTML ──
        soup = BeautifulSoup(html, "html.parser")

        # ── Remove Junk Tags ──
        for tag in soup([
            "script", "style", "meta",
            "noscript", "iframe", "svg", "head"
        ]):
            tag.decompose()

        # ── Detect Website Type ──
        website_type = detect_website_type(url)

        # ── Extract Content Based on Type ──
        if website_type == "ecommerce":
            headings, paragraphs, special = \
                extract_ecommerce(soup)
        else:
            headings, paragraphs, special = \
                extract_general(soup)

        # ── Extract Common Elements ──

        # Page title
        title = ""
        if driver.title:
            title = driver.title
        elif soup.title:
            title = soup.title.get_text(strip=True)

        # Navigation items
        nav_items = []
        nav = soup.find("nav")
        if nav:
            for item in nav.find_all(["a", "li"]):
                t = item.get_text(strip=True)
                if t and 2 < len(t) < 35:
                    nav_items.append(t)

        # Buttons and CTAs
        buttons = []
        for btn in soup.find_all(["button", "a"]):
            t = btn.get_text(strip=True)
            if t and 2 < len(t) < 40:
                buttons.append(t)

        # Footer
        footer_text = ""
        footer = soup.find("footer")
        if footer:
            footer_text = footer.get_text(
                strip=True
            )[:300]

        # ── Clean Duplicates ──
        def clean(lst, limit):
            return list(dict.fromkeys(
                [x for x in lst if x]
            ))[:limit]

        content = {
            "url":          url,
            "website_type": website_type,
            "title":        title,
            "headings":     clean(headings, 10),
            "paragraphs":   clean(paragraphs, 6),
            "buttons":      clean(buttons, 12),
            "nav_items":    clean(nav_items, 10),
            "footer":       footer_text,
            "special":      special
        }

        return content, None

    except Exception as e:
        return None, f"❌ Scraping failed: {str(e)}"

    finally:
        # Always close browser to free RAM
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


# ============================================
# TESTING BLOCK
# Run this file directly to test the scraper
# ============================================
if __name__ == "__main__":

    test_urls = [
        "https://books.toscrape.com",
        "https://www.amazon.in",
        "https://www.bbc.com",
    ]

    for url in test_urls:
        print("\n" + "=" * 55)
        print(f"Testing: {url}")
        print("=" * 55)

        content, error = scrape_website(url)

        if error:
            print(f"Error: {error}")
        else:
            print(f"Type    : {content.get('website_type', 'N/A')}")
            print(f"Title   : {content.get('title', 'Not found')[:80]}")
            print(f"Headings: {content.get('headings', [])[:2]}")
            print(f"Buttons : {content.get('buttons', [])[:3]}")

            # Show ecommerce extras
            special = content.get("special", {})
            if special.get("prices"):
                print(f"Prices  : {special['prices']}")
            if special.get("features"):
                print(f"Features: {special['features'][:2]}")
