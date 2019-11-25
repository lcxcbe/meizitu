import concurrent
import concurrent.futures
import os
import requests
from lxml import etree

PICTURES_PATH = os.path.join(os.getcwd(), 'pictures/')

# 设置headers
headers = {
    'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)'
                  'Chrome/65.0.3325.181Safari/537.36',
    'Referer': "http://www.meizitu.com"
}

try:
    os.mkdir(PICTURES_PATH)
except:
    pass

def getpicurls(i):
    html_ = str(i) + ".html"
    page_url = 'https://www.meizitu.com/a/' + html_
    html = requests.get(page_url).content
    selector = etree.HTML(html)

    pic_urls = selector.xpath('//div[@class="postContent"]/p//@src')

    pic_path = PICTURES_PATH + str(i)
    try:
        os.mkdir(pic_path)
    except Exception as e:
        print("{}已存在".format(i))
    savepic(pic_urls, html_, pic_path)


def download_all_images(html_first, html_last):
    # 获取每一个详情妹纸

    with concurrent.futures.ThreadPoolExecutor(20) as exector:
        for i in range(html_first,html_last):
            exector.submit(getpicurls, i)

def savepic(pic_urls, html_, pic_path):
    img_name = 0
    for pic_url in pic_urls:
        img_name += 1
        img_data = requests.get(pic_url, headers=headers)
        save_path = pic_path + '/a' + str(img_name) + '.jpg'
        if os.path.isfile(save_path):
            print("{}第{}张已存在".format(html_, img_name))
            pass
        else:
            with open(save_path, 'wb') as f:
                f.write(img_data.content)
                print("正在保存{}第{}张".format(html_, img_name))
                f.close()

download_all_images(1,400)