import re
import requests
import json
from crawler_target_users_good import bili_action
from crawler_target_users_good import utils
import time
import random
from tenacity import *

# 初始化变量
# stop_date = '2018-07-10 00:00:00'
# stop_date = '2000-03-15 00:00:00'
stop_date = utils.STOP_DATE
keywords_comment_bad = './keywords/keywords_comment_bad'

# 类， 提供出事变量
class Count(object):
    count_to_pause = 1


def reply_url(pn_r, oid):
    # oid就是av号
    return 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={}&type=1&oid={}&sort=0'.format(pn_r, oid)
url_dm = ''
url_send_msg = ''

# 时间戳转换日期格式
def timeStamp_to_date(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def hit_comment(content):
    with open(keywords_comment_bad, encoding='utf-8') as f_keys:
        f_keywords = f_keys.read()
        keyword_list = f_keywords.splitlines()

    for key in keyword_list:
        if re.search(key, content) is not None:
            return False
    return True


# 随机调用
def act_random(video_id, rpid, mid):
    # time.sleep(random.randint(1, 3))
    time.sleep(1)
    # 10次 就暂停
    if Count.count_to_pause%10 == 0:
        time.sleep(utils.RETRY_WAIT_TIME)
    try:
        i = random.randint(1, 10)
        bili_action.action_like(video_id, rpid, '1')
        bili_action.action_follow(mid, '1')
        if i==8:
            bili_action.action_2('3')
        if i==9:
            bili_action.action_1(video_id)
        if i==10:
            bili_action.action_3(mid)
        Count.count_to_pause = Count.count_to_pause+1
    except RetryError as e:
        print(e)

# 过滤精确的目标
def get_target_user(comment):
    comment = comment.lower()
    re_xiang = '想|打算|入'
    re_list = ['i[57]', '[入买弄搞]', '1[3456789][年款的寸吋]|十[三四五六七八九][年款的寸吋]', '(mac)|(苹果)|mba|mbp']
    count = 0
    str_hit = ['入手', '想入', '想买', '推荐', '买什么', '怎么选', '买那款', '买哪款', ]
    for hit in str_hit:
        result = re.search(hit, comment)
        if result is not None:
            print('\t\t\t'+comment)
            return True
    # 统计命中关键字次数
    for re_str in re_list:
        # print(re_str)
        result = re.search(re_str, comment)
        if result is not None: count = count + 1
    # 命中想字， 在命中一个list中的一个就触发
    if re.search(re_xiang, comment) is not None:
        if count > 0:
            print('\t\t\t'+comment)
            return True
    # 否则 至少要命中3个
    else:
        if count > 2:
            print('\t\t\t'+comment)
            return True


# 解析评论 二级评论 保存到文件
def parse_reply(video_id, replies, f_comm):
    if replies is not None:
        for reply in replies:
            # 评论
            comment_msg = reply['content']['message']
            # rpid 点赞
            rpid = reply['rpid_str'];
            # 时间戳 转日期
            date_comm = timeStamp_to_date(reply['ctime'])
            # mid用户id
            mid = str(reply['member']['mid'])
            uname = reply['member']['uname']

            # 在截止日期之前 且 是目标用户
            if date_comm > stop_date and hit_comment(comment_msg) is True:
                comment_msg = re.sub('\n', '___', comment_msg)

                # 过滤精确目标
                got_user = get_target_user(comment_msg)
                if got_user:
                    # 评论信息保存到本地
                    f_comm.write(mid + '\t' + comment_msg + '\t' + date_comm + '\t' + uname + '\t' + rpid+'\n')
                    # 入口 随机选择
                    act_random(video_id, rpid, mid)



            # 二级回复 递归
            if reply['rcount'] > 0:
                reply_sec = reply['replies']
                # f_comm.write('\t\t')
                parse_reply(video_id, reply_sec, f_comm)

            # 截止日期 停掉爬虫
            if date_comm < stop_date:
                return False
    return True


@retry(stop=stop_after_attempt(3), wait=wait_fixed(utils.RETRY_WAIT_TIME))
def get_reply(video_id):
    comment_detail_path = 'write_to_local/comments_hit_{}.txt'.format(video_id)
    f_comm = open(comment_detail_path, 'w+', encoding='utf-8')
    page_r = 1
    while True:

        print('\t\t当前正在爬第{}页'.format(page_r))
        res_reply = requests.get(reply_url(page_r, video_id))
        res_reply_json = json.loads(res_reply.text)
        # pprint.pprint(res_reply_json)
        reply_ori = res_reply_json['data']['replies']
        # 总评论数量
        count_reply = res_reply_json['data']['page']['count']
        pages = count_reply/20
        # 评论详情
        flag = parse_reply(video_id, reply_ori, f_comm)

        # 分页数量
        if flag is False or page_r >= pages:
        # if flag is False or page_r >= 13:
            break
        page_r = page_r + 1
        time.sleep(1)
    # 关掉文件，写入硬盘
    f_comm.close()




if __name__ == '__main__':
    # 初始化参数
    video_id = '45261119'
    video_id = '32142910'
    video_id = '55270114' # 纳言 mac
    video_id = '9212564' #testv 值不值得买
    video_id = '31141936'# 测试用

    # get_reply(video_id)
    print(get_target_user('请问一个问题，目前在慢慢学习PS和视频剪辑，手头的电脑很卡，试试用苹果电脑 13寸 16g 512，不知道上i7会不会有点浪费？个人原因不是很上15寸……'))