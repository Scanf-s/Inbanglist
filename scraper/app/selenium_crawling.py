import time
from selenium_crawling import afreecatv_crawling, youtube_crawling, chzzk_crawling
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from concurrent import futures

def init_driver():
    user_info = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    service = Service(ChromeDriverManager().install())

    options = Options()
    options.add_experimental_option("detach", True)  # Keep browser open
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking', 'enable-automation'])  # Disable popup
    options.add_argument("window-size=800,1280")  # Set window size
    options.add_argument("incognito")  # Secret mode
    options.add_argument("--headless") # Run in background
    options.add_argument("--mute-audio")  # Mute audio
    options.add_argument(f"user-agent={user_info}")

    new_driver = webdriver.Chrome(options=options, service=service)
    return new_driver

def run():
    with futures.ThreadPoolExecutor() as executor:
        afreecatv_data = executor.submit(afreecatv_crawling.output, init_driver(), BeautifulSoup)
        youtube_data = executor.submit(youtube_crawling.output, init_driver(), BeautifulSoup)
        chzzk_data = executor.submit(chzzk_crawling.output, init_driver(), BeautifulSoup)

    print(len(afreecatv_data.result()))
    print(len(youtube_data.result()))
    print(len(chzzk_data.result()))

if __name__ == "__main__":
    start =  time.time()
    run()
    end = time.time()
    print(f"{end - start:.5f} sec")