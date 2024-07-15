import time
from random import uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def scroll(driver):
    """
    아프리카TV 라이브 페이지를 실제 사람이 사용하는 것처럼 스크롤하는 함수
    """
    last_height: int = driver.execute_script("return document.documentElement.scrollHeight")
    more_cnt = 2

    for i in range(10):
        # 랜덤한 높이로 스크롤
        scroll_height: int = uniform(200, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_height});")

        # 랜덤한 대기 시간
        time.sleep(0.5)

        # 새로운 높이 확인
        new_height: int = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            more_cnt -= 1
            driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight);")
            btn_more = driver.find_element(By.CLASS_NAME, "btn-more")
            ActionChains(driver).move_to_element(btn_more).click().perform()
            time.sleep(0.5)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")

            if more_cnt == 0:
                break

        last_height = new_height

def get_live_details(driver, soup):
    """
    아프리카TV 데이터 가져오기
    """
    page: str = driver.page_source
    soup = soup(page, "html.parser")

    thumbnails = []
    titles = []
    channel_names = []
    live_viewers = []
    links = []

    for thumbnail, title, channel_name, live_viewer in zip(
        soup.find_all("div", class_="thumbs-box"),
        soup.find_all("a", class_="title"),
        soup.find_all("a", class_="nick"),
        soup.find_all("span", class_="views"),
    ):
        link_elm = thumbnail.find("a")
        if link_elm.get('href'):
            links.append(link_elm['href'])

        img = thumbnail.find("img")
        if img and 'src' in img.attrs:
            thumbnails.append("https:" + img['src'])
        titles.append(title.text)
        channel_names.append(channel_name.text)

        em = live_viewer.find("em")
        if em:
            live_viewers.append(live_viewer.text)

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
    url = "https://www.afreecatv.com/?hash=all"
    driver.get(url)
    time.sleep(2)
    scroll(driver)
    return get_live_details(driver, soup)
