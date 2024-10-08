from random import uniform
from datetime import datetime
from convert_int import convert_to_int

async def scroll(page):
    last_height = await page.evaluate("document.documentElement.scrollHeight")
    more_cnt = 2

    for _ in range(10):
        scroll_height = uniform(200, 800)
        await page.evaluate(f"window.scrollBy(0, {scroll_height});")

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
    channel_links = []
    channel_profile_images = []

    html = await page.content()
    soup = soup(html, "html.parser")
    for thumbnail, title, channel_name, live_viewer, channel_link in zip(
        soup.find_all("div", class_="thumbs-box"),
        soup.find_all("a", class_="title"),
        soup.find_all("a", class_="nick"),
        soup.find_all("span", class_="views"),
        soup.find_all("a", class_="thumb")
    ):
        link_elm = thumbnail.find("a")
        if link_elm.get('href'):
            links.append(link_elm['href'])

        img = thumbnail.find("img")
        if img and 'src' in img.attrs:
            thumbnails.append("https:" + img['src'])
        else:
            thumbnails.append("secret thmbnaik")

        titles.append(title.text)
        channel_names.append(channel_name.text)

        em = live_viewer.find("em")
        if em:
            live_viewers.append(live_viewer.text)

        if channel_link.get('href'):
            channel_links.append(channel_link.get('href'))

        profile_img = channel_link.find("img")
        if profile_img.get("src"):
            channel_profile_images.append(profile_img['src'])

    print(
        "Afreeca "
        f"Links: {len(links)}, "
        f"Thumbnails: {len(thumbnails)}, "
        f"Titles: {len(titles)}, "
        f"Channel Names: {len(channel_names)}, "
        f"Live Viewers: {len(live_viewers)}, "
        f"Channel Links: {len(channel_links)}, "
        f"Channel Profile Images: {len(channel_profile_images)}"
    )

    datas = zip(thumbnails, links, titles, channel_names, live_viewers, channel_links, channel_profile_images)

    live_data_list = []
    for thumbnail, streaming_link, title, channel_name, concurrent_viewers, channel_link, channel_profile_image in datas:
        live_data_list.append({
            'channel_name': channel_name,
            'thumbnail': thumbnail,
            'concurrent_viewers': convert_to_int(concurrent_viewers),
            'title': title,
            'platform': "afreecatv",
            'streaming_link': streaming_link,
            'channel_link': channel_link,
            'channel_description': "",
            'channel_followers': 0,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'channel_profile_image': channel_profile_image
        })

    return live_data_list