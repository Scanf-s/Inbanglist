import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def scroll(driver):
    elem = driver.find_element(By.TAG_NAME, "body")

    no_of_pagedowns = 10
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


def get_live_details(driver, soup):
    """
    치지직 데이터 가져오기
    """
    page: str = driver.page_source
    soup = soup(page, "html.parser")

    thumbnails = []
    titles = []
    channel_names = []
    live_viewers = []
    links = []

    for thumbnail, title, channel_name, live_viewer in zip(
        soup.find_all("a", class_="video_card_thumbnail__QXYT8"),
        soup.find_all("a", class_="video_card_title__Amjk2"),
        soup.find_all("span", class_="name_text__yQG50"),
        soup.find_all("span", class_="video_card_badge__w02UD")
    ):
        img = thumbnail.find("img")
        if thumbnail.get('href'):
            link = "https://chzzk.naver.com" + thumbnail['href']
            links.append(link)
        if img and 'src' in img.attrs:
            thumbnails.append(img['src'])
        else:
            thumbnails.append("성인인증걸려있음")
        titles.append(title.text.strip("라이브 엔드로 이동"))
        channel_names.append(channel_name.text.strip().strip('\n'))
        live_viewers.append(live_viewer.text.strip())

    datas = [(thumb, link, title, channel, viewers) for thumb, link, title, channel, viewers in
                     zip(thumbnails, links, titles, channel_names, live_viewers)]

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
    url = "https://chzzk.naver.com/lives"
    driver.get(url)
    time.sleep(2)
    scroll(driver)
    return get_live_details(driver, soup)