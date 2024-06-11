import time
from random import randint, uniform
from typing import List, Tuple, Any

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
    """
    페이지 끝까지 내려주는 함수
    Contributor : im-niber(GyuJae Jo)
    """
    elem = driver.find_element(By.TAG_NAME, "body")

    no_of_pagedowns = 999
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


def press_show_all(driver):
    """
    모두보기 버튼 클릭
    """
    contents: WebElement = driver.find_element(By.ID, "contents")
    first_section: WebElement = contents.find_element(By.TAG_NAME, "ytd-rich-section-renderer")
    menu_container: WebElement = first_section.find_element(By.ID, "menu-container")
    ActionChains(driver).move_to_element(menu_container).click().perform()
    time.sleep(3)


def parse_viewer_count(viewer_count: str) -> int:
    """
    K나 M 붙은 숫자들 파싱해주는 함수 (Chat GPT 4o 사용)
    """
    viewer_count = viewer_count.replace(' watching', '').replace(',', '')
    if 'K' in viewer_count:
        return int(float(viewer_count.replace('K', '')) * 1000)
    elif 'M' in viewer_count:
        return int(float(viewer_count.replace('M', '')) * 1000000)
    else:
        return int(viewer_count)


def get_live_details(driver: WebDriver) -> Tuple[List[Any], List[str], List[str], List[str]]:
    """
    thumbnail_list : 썸네일 이미지 링크 리스트
    title_list : 방송 제목 리스트
    channel_name_list : 채널 주인장 이름 리스트
    live_viewers_list : 시청자 수 리스트
    """
    page: str = driver.page_source
    soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
    thumbnails, titles, channel_names, live_viewers = [], [], [], []

    for thumbnail, title, channel_name, viewers in zip(
            soup.find_all("ytd-thumbnail"),
            soup.find_all("yt-formatted-string", id="video-title"),
            soup.find_all("div", {"id": "text-container"}),
            soup.find_all("span", class_="inline-metadata-item style-scope ytd-video-meta-block")
    ):
        viewer_count_text = viewers.text.strip()
        if 'watching' in viewer_count_text:
            viewer_count = parse_viewer_count(viewer_count_text)
            img = thumbnail.find("img", class_="yt-core-image")
            if img and 'src' in img.attrs:
                thumbnails.append(img['src'])
            titles.append(title.text.strip())
            channel_names.append(channel_name.find('a').text.strip())
            live_viewers.append(viewer_count_text)

    return thumbnails, titles, channel_names, live_viewers


def main(driver: WebDriver):
    url: str = "https://www.youtube.com/channel/UC4R8DWoMoI7CAwX8_LjQHig"
    driver.get(url)
    time.sleep(2)

    try:
        # 모두보기 버튼 클릭
        press_show_all(driver)

        # 페이지 끝까지 내리기
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
    # 참고 블로그 :
    # https://m.blog.naver.com/ksg97031/222070026332
    # https://m.blog.naver.com/lmj4160/222462966573
    driver: WebDriver = init_driver()
    main(driver)
