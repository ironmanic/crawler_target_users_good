import requests
import re
import random
from crawler_target_users_good import header_my as hm
from crawler_target_users_good import utils
import time
import json
from tenacity import *
import sys

# session会话
session = requests.Session()
session.keep_alive = False
headers = hm.get_header()
# 取出csrf
cookie = headers[b'Cookie']
# print(cookie)
bili_jct = re.search('bili_jct=(\w+)', str(cookie))
csrf = bili_jct.group(1)
# print(csrf)


# 点赞， 视频av号， 评论编号，0/1(取消/点赞)， 登陆信息
url_like = 'https://api.bilibili.com/x/v2/reply/action'

@retry(stop=stop_after_attempt(5), wait=wait_fixed(utils.RETRY_WAIT_TIME))
def action_like(oid, rpid, action):
    headers[b'Referer'] = b'https://www.bilibili.com/video/av' + bytes(oid, 'utf8')
    data_like = 'oid={}&type=1&rpid={}&action={}&jsonp=jsonp&csrf={}'.format(oid, rpid, action, csrf)
    res = session.post(url_like, data=data_like, headers=headers, proxies=random.choice(hm.proxies), timeout=5)
    res_json = json.loads(res.text)
    print('\t\t\tacton_like: ', res.status_code, '\t', res_json['message'])

    if res_json['code']==12004:
        time.sleep(180)



# 关注，关注者id， 1/2（关注/取消）, 登陆信息
url_follow = 'https://api.bilibili.com/x/relation/modify'
@retry(stop=stop_after_attempt(5), wait=wait_fixed(utils.RETRY_WAIT_TIME))
def action_follow(fid, act):
    follow_data = 'fid={}&act={}&re_src=15&csrf={}'.format(fid, act, csrf)
    res_follow = session.post(url_follow, data=follow_data, headers=headers, proxies=random.choice(hm.proxies), timeout=5)
    res_follow_json = json.loads(res_follow.text)
    print('\t\t\taction_follow: ', res_follow.status_code, '\t', res_follow_json['message'])
    # 到达关注上限，停止行为
    if res_follow_json['code']==22009:
        print('停止爬虫，到达关注上限！！！')
        sys.exit(0)


# 发私信, dev_id在header中定义
url_sendmsg = 'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg'
msg_content = '{"content":"你好，"}'
time.time()
form_data_msg = {
        'msg[sender_uid]': xxx,
        'msg[receiver_id]': 10036266,
        'msg[receiver_type]': 1,
        'msg[msg_type]': 1,
        'msg[content]': msg_content,
        'msg[timestamp]': int(time.time()),
        'msg[dev_id]': hm.dev_id,
        'csrf_token': csrf
    }
@retry(stop=stop_after_attempt(5), wait=wait_fixed(utils.RETRY_WAIT_TIME))
def action_sendmsg():
    res_send_msg = session.post(url_sendmsg, data=form_data_msg, headers=headers, proxies=random.choice(hm.proxies))
    res_send_json = json.loads(res_send_msg.text)
    print('\t\t\taction_sendmsg: ', res_send_msg.status_code, '\t', res_send_json['data']['msg_key'])
    time.sleep(100)


# 从av号解析cid oid==av
@retry(stop=(stop_after_attempt(1)))
def action_1(av):
    url_1 = 'https://api.bilibili.com/x/player/pagelist?aid={}'.format(av)
    res_cid = session.get(url_1, headers=headers, proxies=random.choice(hm.proxies), timeout=5)
    # print('action_1: ', res_cid.status_code)


# 首页排行榜
@retry(stop=(stop_after_attempt(1)))
def action_2(day):
    url_2 = 'https://api.bilibili.com/x/web-interface/ranking?rid=0&day={}&type=1&arc_type=0&jsonp=jsonp'.format(day)
    res_rank = session.get(url_2, headers=headers, proxies=random.choice(hm.proxies), timeout=10)
    # print('action_2: ', res_rank.status_code)


# up主投稿视频信息
@retry(stop=(stop_after_attempt(1)))
def action_3(mid):
    url_3 = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={}&pagesize=10&tid=0&page=1&keyword=&order=pubdate'.format(mid)
    res_videos = session.get(url_3, headers=headers, proxies=random.choice(hm.proxies), timeout=10)
    # print('action_3: ', res_videos.status_code)




# 入口
if __name__=='__main__':
    oid = '32142910'
    act = '1'

    rpid = '1723670427'
    # action_like(oid, rpid, act)
    # action_1(oid)
    # action_2(3)
    # action_3('927587') # 木鱼
    action_sendmsg()
    try:
        pass
    except RetryError as e:
        print(e)
