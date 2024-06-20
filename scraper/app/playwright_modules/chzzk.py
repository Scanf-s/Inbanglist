async def scroll(page):
    no_of_pagedowns = 10
    while no_of_pagedowns > 0:
        await page.keyboard.press("PageDown")
        no_of_pagedowns -= 1

async def chzzk_crawling(page):
    await page.goto("https://chzzk.naver.com/lives")
    await scroll(page)

    links = []
    thumbnails = []
    titles = []
    channel_names = []
    live_viewers = []
    
    thumbnails_elements = await page.query_selector_all('a.video_card_thumbnail__QXYT8 img')
    title_elements = await page.query_selector_all('a.video_card_title__Amjk2')
    channel_name_elements = await page.query_selector_all('span.name_text__yQG50')
    live_viewer_elements = await page.query_selector_all('span.video_card_badge__w02UD')

    for thumbnail_element, title_element, channel_name_element, live_viewer_element in zip(thumbnails_elements, title_elements, channel_name_elements, live_viewer_elements):
        thumbnail_src = await thumbnail_element.evaluate('(element) => element.src')
        thumbnails.append(thumbnail_src if thumbnail_src else '성인인증걸려있음')

        link_href = await thumbnail_element.evaluate('(element) => element.parentElement.href')
        link = "https://chzzk.naver.com" + link_href if link_href else ''
        links.append(link)

        title_text = await title_element.text_content()
        titles.append(title_text.strip("라이브 엔드로 이동"))

        channel_name_text = await channel_name_element.text_content()
        channel_names.append(channel_name_text.strip())

        live_viewer_text = await live_viewer_element.text_content()
        live_viewers.append(live_viewer_text.strip())

    print("Links:", len(links))
    print("Thumbnails:", len(thumbnails))
    print("Titles:", len(titles))
    print("Channel Names:", len(channel_names))
    print("Live Viewers:", len(live_viewers))

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