from re import search
from datetime import datetime
from convert_int import convert_to_int

async def press_show_all(page):
    contents = await page.query_selector("#contents")
    first_section = await contents.query_selector("ytd-rich-section-renderer")
    menu_container = await first_section.query_selector("#menu-container")
    await menu_container.click()

async def scroll(page):
    no_of_pagedowns = 22
    last_height = await page.evaluate("document.documentElement.scrollHeight")
    
    last_chk_cnt = 0
    while no_of_pagedowns > 0:
        await page.keyboard.press("PageDown")

        new_height = await page.evaluate("document.documentElement.scrollHeight")

        if last_height == new_height:
            last_chk_cnt += 1
        else:
            last_chk_cnt = 0

        no_of_pagedowns -= 1

async def youtube_crawling(page, soup):
    await page.goto("https://www.youtube.com/channel/UC4R8DWoMoI7CAwX8_LjQHig")
    await press_show_all(page)
    await scroll(page)
    
    html = await page.content()
    soup = soup(html, "html.parser")

    thumbnail_list = [img['src'] for yt_image in soup.find_all("yt-image") for img in yt_image.find_all("img") if
                      'src' in img.attrs]
    link_list = [link.get('href') for link in soup.find_all("a", class_="yt-simple-endpoint inline-block style-scope ytd-thumbnail") if link.get('href')]
    title_list = [title.text for title in soup.find_all("yt-formatted-string", id="video-title")]
    channel_name_list = [channel_name.text for text_container in soup.find_all("div", {"id": "text-container"}) for
                         channel_name in text_container.find_all('a')]
    live_viewers_list = [viewers.text for viewers in
                         soup.find_all("span", class_="inline-metadata-item style-scope ytd-video-meta-block") if
                         not search(r'조회수', viewers.text)]
    
    channel_links = [link.get('href') for link in soup.find_all("a", id="avatar-link") if link.get('href')]
    channel_profile_images = [img['src'] for img in soup.find_all("img", class_="style-scope yt-img-shadow") if img.get('src')]

    print("Links:", len(link_list))
    print("Thumbnails:", len(thumbnail_list))
    print("Titles:", len(title_list))
    print("Channel Names:", len(channel_name_list))
    print("Live Viewers:", len(live_viewers_list))
    print("channel_link:", len(channel_links))
    print("channel_profile_images:", len(channel_profile_images))

    datas = [(thumb, link, channel_link, title, channel, viewers, channel_profile_image) for thumb, link, channel_link, title, channel, viewers, channel_profile_image in
                     zip(thumbnail_list, link_list, channel_links, title_list, channel_name_list, live_viewers_list, channel_profile_images) if
                     not search(r'Streamed \d+|스트리밍|분', viewers)]
    print(len(datas))
    
    live_data_list = []
    for thumbnail, streaming_link, channel_link, title, channel_name, concurrent_viewers, channel_profile_image in datas:
        live_data_list.append({
            'channel_name': channel_name,
            'thumbnail': thumbnail,
            'concurrent_viewers': convert_to_int(concurrent_viewers),
            'title': title,
            'platform': "youtube",
            'streaming_link': "https://www.youtube.com" + streaming_link,
            'channel_link': "https://www.youtube.com" + channel_link,
            'channel_description': "",
            'channel_followers': 0,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'channel_profile_image': channel_profile_image
        })

    return live_data_list