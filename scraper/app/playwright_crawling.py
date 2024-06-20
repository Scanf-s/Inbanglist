import time
import asyncio
from playwright.async_api import async_playwright

from playwright_modules.afreecatv import afreecatv_crawling
from playwright_modules.chzzk import chzzk_crawling
from playwright_modules.youtube import youtube_crawling

afreecatv_datas = []
youtube_datas = []
chzzk_datas = []
browsers = []

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, slow_mo=500)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )

        tasks = []
        tasks.append(asyncio.create_task(afreecatv_crawling(await context.new_page())))
        tasks.append(asyncio.create_task(youtube_crawling(await context.new_page())))
        tasks.append(asyncio.create_task(chzzk_crawling(await context.new_page())))

        await asyncio.gather(*tasks)

        await browser.close()

if __name__ == "__main__":
    start =  time.time()
    asyncio.run(main())
    end = time.time()
    print(f"{end - start:.5f} sec")
