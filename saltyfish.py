import requests
import os
import json
import re


keyword = "surface book"
minPrice = "5000"
maxPrice = "11000"


# 获取Json数据
def getJSon(page="1"):
    # arguments
    page = str(page)

    filename = os.path.join(".", "temp", page + ".json")
    if os.path.exists(filename):
        content = ""
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content

    payload = {
        "type": "1",
        "st_trust": "1",
        "start": minPrice,
        "end": maxPrice,
        "q": keyword,
        "ist": "1",
        "wp": page
    }

    rep = requests.get(
        url="https://s.2.taobao.com/list/waterfall/waterfall.htm?", params=payload)
    print(rep.url)

    rep.encoding = rep.apparent_encoding

    res = rep.text

    with open(filename, "w", encoding="utf-8") as f:
        content = f.write(res)

    return res


def clearJsonOuter(text):
    return re.findall(r"\s*\((.*)\)\s*", text.replace('\\', '\\\\').replace('\ufffd', ''), flags=re.S)[0]


# 获得商品数据
def getGoodData():
    finish = False
    page = 1

    resolveList = []
    while not finish:
        data = json.loads(clearJsonOuter(getJSon(page)))
        numFound = data['numFound']
        currPage = data['currPage']
        totalPage = data['totalPage']
        resolveList += data['idle']
        if currPage == totalPage:
            finish = True
        else:
            page += 1

    resList = []
    for item in resolveList:
        resList.append(item['item'])
    return resList

# 处理商品数据


def analydata(dataList):
    resList = []
    for item in dataList:
        resList.append({
            'id': re.findall(r'//2\.taobao\.com/item\.htm\?id=([0-9]+)&amp;from=list&amp;similarUrl=', item["itemUrl"])[0],
            'price': item['price'],
            'title': item['title'],
            'describe': item['describe'],
            'url': item["itemUrl"],
            'img': item['imageUrl'],
        })
    return resList



if __name__ == '__main__':
    if not os.path.exists('temp'):
        os.mkdir('temp')

    data = getGoodData()
    data = analydata(data)

    with open("data.csv", "w", encoding="gb2312") as f:
        for row in data:
            for col in row:
                f.write(row[col].replace(",", " ") + ",")
            f.write("\n")

    print("data saves in data.csv")
    print("You can use Excel to find what you want")