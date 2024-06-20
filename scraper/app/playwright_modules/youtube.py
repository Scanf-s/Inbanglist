from re import search

async def press_show_all(page):
    contents = await page.query_selector("#contents")
    first_section = await contents.query_selector("ytd-rich-section-renderer")
    menu_container = await first_section.query_selector("#menu-container")
    await menu_container.click()

async def scroll(page):
    no_of_pagedowns = 999
    last_height = await page.evaluate("document.documentElement.scrollHeight")
    
    last_chk_cnt = 0
    while no_of_pagedowns > 0:
        await page.keyboard.press("PageDown")

        new_height = await page.evaluate("document.documentElement.scrollHeight")

        if last_height == new_height:
            last_chk_cnt += 1
        else:
            last_chk_cnt = 0

        if last_chk_cnt > 5:
            break

        last_height = new_height
        no_of_pagedowns -= 1

async def youtube_crawling(page):
    await page.goto("https://www.youtube.com/channel/UC4R8DWoMoI7CAwX8_LjQHig")
    await press_show_all(page)
    await scroll(page)

    yt_images = await page.query_selector_all("yt-image img")
    thumbnail_list = [await img.get_attribute('src') for img in yt_images if await img.get_attribute('src')]

    links = await page.query_selector_all("a.yt-simple-endpoint.inline-block.style-scope.ytd-thumbnail")
    link_list = [await link.get_attribute('href') for link in links if await link.get_attribute('href')]

    titles = await page.query_selector_all("yt-formatted-string#video-title")
    title_list = [await title.text_content() for title in titles]

    text_containers = await page.query_selector_all("div#text-container a")
    channel_name_list = [await channel_name.text_content() for channel_name in text_containers]

    viewers = await page.query_selector_all("span.inline-metadata-item.style-scope.ytd-video-meta-block")
    live_viewers_list = [await viewer.text_content() for viewer in viewers]

    print("Links:", len(link_list))
    print("Thumbnails:", len(thumbnail_list))
    print("Titles:", len(title_list))
    print("Channel Names:", len(channel_name_list))
    print("Live Viewers:", len(live_viewers_list))

    datas = [(thumb, link, title, channel, viewers) for thumb, link, title, channel, viewers in
                     zip(thumbnail_list, link_list, title_list, channel_name_list, live_viewers_list) if
                     not search(r'Streamed \d+', viewers)]

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