import random
from copyheaders import headers_raw_to_dict

first_num = random.randint(55, 62)
third_num = random.randint(0, 3200)
fourth_num = random.randint(0, 140)

dev_id = 'xxx'
# 基础的头信息
def get_header():
    # 浏览器复制的请求头，对应着小号信息，20190703-21:25
    r_h = b'''
    Cookie: buvid3=xxx
    '''
    headers = headers_raw_to_dict(r_h)
    headers[b'Content-Type'] = b'application/x-www-form-urlencoded; charset=UTF-8'
    headers[b'Connection'] = b'keep-alive'
    headers[b'User-Agent'] = bytes(FakeChromeUA.get_ua(), 'utf8')

    return headers


# 代理
proxies = [
    {
        'https': 'https://203.42.227.113:8080',
    },
    {
        'https': 'https://125.65.79.60:3311',
    },
    {
        'https': 'https://202.99.172.145:8081',
    },
    {
        'http': 'http://120.27.210.60:8080',
    },
]


# 自动生成chrome ua
class FakeChromeUA:
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]

    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36']
                        )
