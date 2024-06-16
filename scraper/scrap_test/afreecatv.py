import time
from random import randint, uniform
from typing import List, Tuple, Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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


def scroll(driver: WebDriver):
    """
    아프리카TV 라이브 페이지를 실제 사람이 사용하는 것처럼 스크롤하는 함수
    """
    last_height: int = driver.execute_script("return document.documentElement.scrollHeight")

    for i in range(5):
        # 랜덤한 높이로 스크롤
        scroll_height: int = uniform(200, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_height});")

        # 랜덤한 대기 시간
        time.sleep(uniform(1.0, 3.0))

        # 새로운 높이 확인
        new_height: int = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            # 높이가 변하지 않았다면 마지막 시도로 스크롤
            driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight);")
            time.sleep(uniform(1.0, 3.0))
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
        last_height = new_height

        # 특정 요소가 나타날 때까지 기다리기
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "yt-core-image"))
            )
        except Exception as e:
            print(f"Error during waiting for new content: {e}")
            break


def get_live_details(driver: WebDriver):
    """
    아프리카TV 데이터 가져오기
    """
    page: str = driver.page_source
    soup: BeautifulSoup = BeautifulSoup(page, "html.parser")

    thumbnails: List = []
    titles: List = []
    channel_names: List = []
    live_viewers: List = []

    for thumbnail, title, channel_name, live_viewer in zip(
        soup.find_all("div", class_="thumbs-box"),
        soup.find_all("a", class_="title"),
        soup.find_all("a", class_="nick"),
        soup.find_all("span", class_="views"),
    ):

        img = thumbnail.find("img")
        if img and 'src' in img.attrs:
            thumbnails.append("https:" + img['src'])
        titles.append(title.text)
        channel_names.append(channel_name.text)

        em = live_viewer.find("em")
        if em:
            live_viewers.append(live_viewer.text)

    return thumbnails, titles, channel_names, live_viewers


def main(driver: WebDriver):
    url: str = "https://www.afreecatv.com/?hash=all"
    driver.get(url)
    time.sleep(2)

    try:
        # 페이지 조금만 내려주기 (아프리카TV에서 이미 인기순으로 정렬해서 제공하므로 적당히만 내려주면 된다.)
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
