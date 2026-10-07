import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        requests_log = []
        def on_request(request):
            if "api" in request.url or "gql" in request.url or "category" in request.url:
                requests_log.append((request.method, request.url))

        page.on("request", on_request)

        await page.goto("https://kmong.com/category/668", wait_until="networkidle")
        print("Page title:", await page.title())
        print("\nLogged requests:")
        for method, url in requests_log[:30]:
            print(f"{method} {url}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
