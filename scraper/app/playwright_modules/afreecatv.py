from random import uniform

async def scroll(page):
    last_height = await page.evaluate("document.documentElement.scrollHeight")
    more_cnt = 2

    for _ in range(10):
        # 랜덤한 높이로 스크롤
        scroll_height = uniform(200, 800)
        await page.evaluate(f"window.scrollBy(0, {scroll_height});")

        # 새로운 높이 확인
        new_height = await page.evaluate("document.documentElement.scrollHeight")

        if new_height == last_height:
            more_cnt -= 1
            await page.evaluate("window.scrollBy(0, document.documentElement.scrollHeight);")
            
            try:
                btn_more = await page.query_selector(".btn-more")
                await btn_more.click()
                new_height = await page.evaluate("document.documentElement.scrollHeight")
            except Exception as e:
                print(f"Could not find the 'btn-more' button: {e}")
                break

            if more_cnt == 0:
                break

        last_height = new_height

async def afreecatv_crawling(page):
    await page.goto("https://www.afreecatv.com/?hash=all")
    await scroll(page)

    links = []
    thumbnails = []
    titles = []
    channel_names = []
    live_viewers = []

    thumbnails_boxes = await page.query_selector_all("div.thumbs-box")
    title_elements = await page.query_selector_all("a.title")
    nick_elements = await page.query_selector_all("a.nick")
    view_elements = await page.query_selector_all("span.views")
    
    for thumbnail, title, channel_name, live_viewer in zip(thumbnails_boxes, title_elements, nick_elements, view_elements):
        link_elm = await thumbnail.query_selector("a")
        if link_elm and await link_elm.get_attribute('href'):
            links.append(await link_elm.get_attribute('href'))

        img = await thumbnail.query_selector("img")
        if img and await img.get_attribute('src'):
            thumbnails.append("https:" + await img.get_attribute('src'))
        
        titles.append(await title.text_content())
        channel_names.append(await channel_name.text_content())

        em = await live_viewer.query_selector("em")
        if em:
            live_viewers.append(await live_viewer.text_content())

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