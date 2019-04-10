# coding:utf-8
import requests
import re
import pymongo


######
# 爬虫v0.1 利用urlib 和 字符串内建函数
######
def getHtml(url):
    # 获取网页内容
    html = requests.get(url)
    return html.content


def content(html):
    # 内容分割的标签
    str = '<article class="article-content">'
    content = html.partition(str)[2]
    str1 = '<div class="article-social">'
    content = content.partition(str1)[0]
    return content  # 得到网页的内容


def title(content, beg=0):
    # 匹配title
    # 思路是利用str.index()和序列的切片
    # beg 检测范围的开始
    try:
        title_list = []
        while True:
            num1 = content.index('】', beg) + 3
            num2 = content.index('</p>', num1)
            title_list.append(content[num1:num2])
            beg = num2

    except ValueError:
        return title_list


def get_img(content, beg=0):
    # 匹配图片的url
    # 思路是利用str.index()和序列的切片
    _cententLen = len(content)
    try:
        img_list = []
        while True:
            src1 = content.index('https://ww', beg)
            if (re.search('src=', content[beg:_cententLen]) == None):
                src2 = content.index('[/img]', src1)
            else:
                src2 = content.index('/></p>', src1)
            img_list.append(content[src1:src2])
            beg = src2

    except ValueError:
        return img_list


def insert_data(titles, imgs, collection):
    # 写入数据库
    for i in range(0, len(titles)):
        _title = titles[i]
        _img = imgs[i]
        _data = {'title': _title, 'img': _img}  # 将数据存入到字典变量data中
        collection.insert(_data)  # 将data中的输入插入到mongodb数据库


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["pythonTest"]
mycol = mydb["imgCol"]
content = content(getHtml("http://bohaishibei.com/post/10475/"))
titles = title(content)
imgs = get_img(content)
insert_data(titles, imgs, mycol)
# 实现了爬的单个页面的title和img的url插入数据库
