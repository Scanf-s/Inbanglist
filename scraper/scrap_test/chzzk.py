import time
from random import randint, uniform
from typing import List, Tuple, Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def init_driver() -> WebDriver:
    """
    웹 드라이버 초기화
    """
    user_info = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    service = Service(ChromeDriverManager().install())

    options: Options = Options()
    options.add_experimental_option("detach", True)  # Keep browser open
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking', 'enable-automation'])  # Disable popup
    options.add_argument("window-size=800,1280")  # Set window size
    options.add_argument("incognito")  # Secret mode
    # options.add_argument("--headless") # Run in background
    options.add_argument("--mute-audio")  # Mute audio
    options.add_argument(f"user-agent={user_info}")

    new_driver: WebDriver = webdriver.Chrome(options=options, service=service)
    return new_driver


def scroll(driver):
    elem = driver.find_element(By.TAG_NAME, "body")

    no_of_pagedowns = 7
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    last_chk_cnt = 0
    while no_of_pagedowns:

        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if last_height == new_height:
            last_chk_cnt += 1

        else:
            last_chk_cnt = 0

        if last_chk_cnt > 5:
            break

        last_height = new_height
        no_of_pagedowns -= 1


def get_live_details(driver: WebDriver):
    """
    치지직 데이터 가져오기
    """
    page: str = driver.page_source
    soup: BeautifulSoup = BeautifulSoup(page, "html.parser")

    thumbnails: List = []
    titles: List = []
    channel_names: List = []
    live_viewers: List = []

    for thumbnail, title, channel_name, live_viewer in zip(
        soup.find_all("a", class_="video_card_thumbnail__QXYT8"),
        soup.find_all("a", class_="video_card_title__Amjk2"),
        soup.find_all("span", class_="name_text__yQG50"),
        soup.find_all("span", class_="video_card_badge__w02UD")
    ):
        img = thumbnail.find("img")
        if img and 'src' in img.attrs:
            thumbnails.append(img['src'])
        else:
            thumbnails.append("성인인증걸려있음")
        titles.append(title.text.strip("라이브 엔드로 이동"))
        channel_names.append(channel_name.text.strip().strip('\n'))
        live_viewers.append(live_viewer.text.strip())

    return thumbnails, titles, channel_names, live_viewers


def main(driver: WebDriver):
    url: str = "https://chzzk.naver.com/lives"
    driver.get(url)
    time.sleep(2)

    try:
        # 페이지 조금만 내려주기 (치지직은 이미 인기순으로 정렬되어 있어서 적당히만 내려주면 된다.)
        scroll(driver)

        thumbnail_list, title_list, channel_name_list, live_viewers_list = get_live_details(driver)
        for i, el in enumerate(thumbnail_list):
            print(f"{i}th: {el}")

        for i, el in enumerate(title_list):
            print(f"{i}th: {el}")

        for i, el in enumerate(channel_name_list):
            print(f"{i}th: {el}")

        for i, el in enumerate(live_viewers_list):
            print(f"{i}th: {el}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    driver: WebDriver = init_driver()
    main(driver)
