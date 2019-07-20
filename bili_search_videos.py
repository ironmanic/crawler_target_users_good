import requests
import re
import json
from crawler_target_users_good import bili_reply
from crawler_target_users_good import utils
from tenacity import *


def open_list_file(file_path):
    with open(file_path, encoding='utf-8') as f_file:
        f_keywords = f_file.read()
        keyword_list = f_keywords.splitlines()
        return keyword_list


# 去掉标题中的标签
def remove_label(text):
    list_splits = re.split("(<.*?>)", text)
    strSum = ''
    for split in list_splits:
        if split.strip() != '':
            # 找到带有标签的行
            hit_key = re.search("(<.*>)", split)
            if hit_key is not None:
                # 保留的字
                word = re.search('>(.*)<', split)
                if word is not None:
                    strSum = strSum + word.group(1)
            # 这里是正常文字，直接相加
            else:
                strSum = strSum + split

    return strSum

@retry(stop=stop_after_attempt(3), wait=wait_fixed(utils.RETRY_WAIT_TIME))
def req_get(url):
    res = requests.get(url)
    res_json = json.loads(res.text)
    return res_json


# 搜索视频，过滤已经爬过的
def search_video():
    keywords_path = 'keywords/keyword_search'
    keyword_list = open_list_file(keywords_path)

    # i = 1
    for kw in keyword_list:
        # print('正在搜索第 {}个关键字...'.format(i))
        # 从当前页来时0+1页
        curPage = utils.SEARCH_START_PAGE
        pages = 50
        while curPage < pages:
            curPage = curPage+1
            print('搜索的第 {}页...'.format(curPage))
            # 搜索 先行者 第一页https://api.bilibili.com/x/web-interface/search/type?search_type=video&highlight=1&keyword=macbook%20pro&page=2&jsonp=jsonp
            url_search =  'https://api.bilibili.com/x/web-interface/search/type?search_type=video&highlight=1&keyword={}&page={}&jsonp=jsonp'.format(kw, curPage)
            try:
                res_json = req_get(url_search)
                numPages = res_json['data']['numPages']
                video_list = res_json['data']['result']

                j = 1
                for video in video_list:

                    video_id_int = video['aid']
                    video_id = str(video_id_int)
                    title = video['title']
                    description = video['description']
                    title = remove_label(title)
                    print('\t正在爬取第 {}个视频...'.format(j), title)

                    j = j + 1
                    # 文件
                    liked_lsit_path = 'keywords/liked_video_list'
                    # r+ 读写不创建文件(只有这个读出来的不是空)    w+ 读写和创建会清空之前的内容重新创建文件      a+ 附加方式打开，相当于读出来的为空
                    with open(liked_lsit_path, encoding='utf-8', mode='r+') as f_file:
                        f_keywords = f_file.read()
                        liked_list = f_keywords.splitlines()

                        if video_id not in liked_list:
                            # 入口， 开始爬取这个视频
                            bili_reply.get_reply(video_id)
                            # 把已经爬完的视频av，加到名单中
                            f_file.write(video_id + '\n')
            except RetryError as e:
                print(e)


# 入口
search_video()
print('再见！')
