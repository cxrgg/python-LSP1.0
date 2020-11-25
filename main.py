# -*- coding = utf-8 -*-

import os
import random
import re
import string
import urllib.error
import urllib.request
import time

from bs4 import BeautifulSoup

bastChildPath = "https://qql6k.com:5561/"


def getBeautifulSoup(url):
    head = {
        "user-agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome / "
                      "87.0.4280.66 Safari / 537.36 "
    }

    request = urllib.request.Request(url, headers=head)
    html_doc = ""
    try:
        response = urllib.request.urlopen(request, timeout=2)
        html_doc = response.read().decode("GBK")
    except urllib.error as e:
        print("出错了：" + e)
    return BeautifulSoup(html_doc, 'html.parser')


def main(num):
    baseUrl = f"https://qql6k.com:5561/luyilu/list_5_{num}.html"
    soup = getBeautifulSoup(baseUrl)
    for item in soup.find_all("a", attrs={"target": "_blank", "title": re.compile(r".*\[")}):
        childPathFirst = bastChildPath + item.get("href")
        strArray = childPathFirst.split(".")
        file_path = "./" + re.sub(r'[^\u4e00-\u9fa5]', '', item.get("title"))
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path)
                for item1 in range(1, 50):
                    if item1 > 1:
                        childPath = strArray[0] + "." + strArray[1] + "_" + "%d" % item1 + "." + strArray[2]
                    else:
                        childPath = strArray[0] + "." + strArray[1] + "." + strArray[2]

                    child_soup = getBeautifulSoup(childPath)
                    article = child_soup.select("article.article-content>p>img")
                    if article is None:
                        return
                    for img in article:
                        img_url = img.get("src")
                        # 获得图片后缀
                        file_suffix = os.path.splitext(img_url)[1]
                        # 拼接图片名（包含路径）
                        filename = "{}{}{}{}".format(file_path, os.sep,
                                                     ''.join(random.sample(string.ascii_letters + string.digits, 8)),
                                                     file_suffix)
                        print(filename)
                        # 下载图片，并保存到文件夹中
                        urllib.request.urlretrieve(img_url, filename=filename)
                    else:
                        continue

        except Exception as e:
            print("Exception:" + str(e))


if __name__ == "__main__":
    for myIndex in range(1, 1000):
        t1 = time.time()
        main(myIndex)
