from datetime import datetime
from convert_int import convert_to_int

async def scroll(page):
    no_of_pagedowns = 20
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
    channel_links = []

    channel_profile_images = []

    html = await page.content()
    soup = soup(html, "html.parser")
    for thumbnail, title, channel_name, live_viewer, channel_link, channel_profile_image in zip(
        soup.find_all("a", class_="video_card_thumbnail__QXYT8"),
        soup.find_all("a", class_="video_card_title__Amjk2"),
        soup.find_all("span", class_="name_text__yQG50"),
        soup.find_all("span", class_="video_card_badge__w02UD"),
        soup.find_all("a", class_="video_card_channel__AjQ+P"),
        soup.find_all("a", class_="video_card_image__yHXqv")
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

        if channel_link.get('href'):
            channel_link = "https://chzzk.naver.com" + channel_link.get('href')
            channel_links.append(channel_link)
            
        profile_image = channel_profile_image.find("img")
        if 'src' in profile_image.attrs:
            channel_profile_images.append(profile_image['src'])

    
    print("chzzk")
    print("Links:", len(links))
    print("Thumbnails:", len(thumbnails))
    print("Titles:", len(titles))
    print("Channel Names:", len(channel_names))
    print("Live Viewers:", len(live_viewers))
    print("Channel Links:", len(channel_links))
    print("channel_profile_images:", len(channel_profile_images))

    datas = zip(thumbnails, links, titles, channel_names, live_viewers, channel_links, channel_profile_images)

    live_data_list = []
    for thumbnail, streaming_link, title, channel_name, concurrent_viewers, channel_link, channel_profile_image in datas:
        live_data_list.append({
            'channel_name': channel_name,
            'thumbnail': thumbnail,
            'concurrent_viewers': convert_to_int(concurrent_viewers),
            'title': title,
            'platform': "chzzk",
            'streaming_link': streaming_link,
            'channel_link': channel_link,
            'channel_description': "",
            'channel_followers': 0,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'channel_profile_image': channel_profile_image

        })

    return live_data_list