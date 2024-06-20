import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def scroll(driver):
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
    contents = driver.find_element(By.ID, "contents")
    first_section = contents.find_element(By.TAG_NAME, "ytd-rich-section-renderer")
    menu_container = first_section.find_element(By.ID, "menu-container")
    ActionChains(driver).move_to_element(menu_container).click().perform()
    time.sleep(2)


def get_live_details(driver, soup):
    """
    Crawling 함수
    + 필터링 기능
    """
    page = driver.page_source
    soup = soup(page, "html.parser")

    thumbnail_list = [img['src'] for yt_image in soup.find_all("yt-image") for img in yt_image.find_all("img") if
                      'src' in img.attrs]
    link_list = [link.get('href') for link in soup.find_all("a", class_="yt-simple-endpoint inline-block style-scope ytd-thumbnail") if link.get('href')]
    title_list = [title.text for title in soup.find_all("yt-formatted-string", id="video-title")]
    channel_name_list = [channel_name.text for text_container in soup.find_all("div", {"id": "text-container"}) for
                         channel_name in text_container.find_all('a')]
    live_viewers_list = [viewers.text for viewers in
                         soup.find_all("span", class_="inline-metadata-item style-scope ytd-video-meta-block")]

    # 만약 방금 종료된 방송이 있다면, 제외시켜야 하므로 정규식을 사용해서 필터링합니다.
    datas = [(thumb, link, title, channel, viewers) for thumb, link, title, channel, viewers in
                     zip(thumbnail_list, link_list, title_list, channel_name_list, live_viewers_list) if
                     not re.search(r'Streamed \d+', viewers)]

    # dictionary list로 바꿔서 제공해줍니다.
    live_data_list = [
        {
            'thumbnail': data[0],
            'link': data[1],
            'title': data[2],
            'channel_name': data[3],
            'viewers': data[4],
        } for data in datas
    ]

    return live_data_list

def output(driver, soup):
    url = "https://www.youtube.com/channel/UC4R8DWoMoI7CAwX8_LjQHig"
    driver.get(url)
    time.sleep(2)
    press_show_all(driver)
    scroll(driver)
    return get_live_details(driver, soup)
