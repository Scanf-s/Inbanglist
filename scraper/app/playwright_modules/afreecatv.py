from random import uniform

async def scroll(page):
    last_height = await page.evaluate("document.documentElement.scrollHeight")
    more_cnt = 6

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

async def afreecatv_crawling(page, soup):
    await page.goto("https://www.afreecatv.com/?hash=all")
    await scroll(page)

    links = []
    thumbnails = []
    titles = []
    channel_names = []
    live_viewers = []

    html = await page.content()
    soup = soup(html, "html.parser")
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

    print("Afreeca")
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