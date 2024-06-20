async def scroll(page):
    no_of_pagedowns = 30
    while no_of_pagedowns > 0:
        await page.keyboard.press("PageDown")
        no_of_pagedowns -= 1

async def chzzk_crawling(page, soup):
    await page.goto("https://chzzk.naver.com/lives")
    await scroll(page)

    links = []
    thumbnails = []
    titles = []
    channel_names = []
    live_viewers = []

    html = await page.content()
    soup = soup(html, "html.parser")
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
    
    print("chzzk")
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