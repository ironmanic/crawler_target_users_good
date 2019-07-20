import random
from copyheaders import headers_raw_to_dict

first_num = random.randint(55, 62)
third_num = random.randint(0, 3200)
fourth_num = random.randint(0, 140)

dev_id = 'DF5D5AF8-E9B6-4040-82C7-EA7384D0A016'
# 基础的头信息
def get_header():
    # 浏览器复制的请求头，对应着小号信息，20190703-21:25
    r_h = b'''
    Cookie: buvid3=CD3256C4-1351-43A2-98CC-88E12F177A6E40768infoc; LIVE_BUVID=AUTO4715623865079860; sid=i1w7ujpe; DedeUserID=440237330; DedeUserID__ckMd5=4f6573ba8b1afb25; SESSDATA=e816c21a%2C1564978587%2Cbe6fdc71; bili_jct=ea4f385dbad9ab257970aa2d35914653; CURRENT_FNVAL=16; stardustvideo=1
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
