import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        requests_log = []
        def on_request(request):
            if "api.kmong.com" in request.url or "kmong.com/api" in request.url:
                requests_log.append((request.method, request.url))

        page.on("request", on_request)

        await page.goto("https://kmong.com/gig/795325", wait_until="networkidle")
        print("Page title:", await page.title())
        print("\nLogged requests for gig detail:")
        for method, url in requests_log:
            print(f"{method} {url}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
