import time
import shlex
import hashlib
import json
import os
import random
import requests
import ssl
from urllib import parse
from requests.exceptions import ChunkedEncodingError, ConnectionError, ConnectTimeout

# 忽略证书校验
requests.packages.urllib3.disable_warnings()
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

user_agent = ['Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1 ; x64; en-US; rv:1.9.1b2pre) Gecko/20081026 Firefox/3.1b2pre',
                      'Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60',
                      'Opera/8.01 (J2ME/MIDP; Opera Mini/2.0.4062; en; U; ssr)',
                      'Mozilla/5.0 (Windows; U; Windows NT 5.1; ; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14',
                      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
                      'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                      'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)',
                      'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16',
                      'Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5',
                      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
                      "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                      "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
                      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                      "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
                      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
                      "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
                      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
                      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
                      "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
                      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
                      "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
                      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
                      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
                      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
                      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
                      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
                      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
                      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
                      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
                      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
                      "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
                      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
                      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
                      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                      "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
                      ]


class Html(object):
    def __init__(self, text, status_code, content, headers, cookies, encoding):
        self.text = text
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self.cookies = cookies
        self.encoding = encoding

class Requests(object):
    def __init__(self, isProxy=False, baseUrl=True):
        if isProxy is False or isProxy == "否":
            self.isProxy = False
        elif isProxy == "云":
            self.isProxy = "云"
        else:
            self.isProxy = True
        if baseUrl is True or baseUrl == "是":
            self.baseUrl = True
        else:
            self.baseUrl = False
        self.proxyList = self.getProxyList()
        self.session = requests.Session()

    def getProxyList(self):
        if self.isProxy == "云":
            if not os.path.isfile('pocs/proxy/yunproxy'):
                return []
            with open('pocs/proxy/yunproxy', 'rb') as f:
                proxyList = f.readlines()
            if len(proxyList) > 0:
                return ["云"] + proxyList
            else:
                return []
        elif self.isProxy is False:
            return []
        else:
            if not os.path.isfile('pocs/proxy/proxy'):
                return ['127.0.0.1:8080']
            with open('pocs/proxy/proxy', 'rb') as f:
                proxyList = f.readlines()
            if len(proxyList) > 0:
                return proxyList
            else:
                return ['127.0.0.1:8080']

    def requests_headers(self, headers):
        try:
            if len(headers['User-Agent']) > 0 and "X-Forwarded-For" not in headers:
                headers['X-Forwarded-For'] = '10.10.{}.{}'.format(str(random.randint(0, 255)), str(random.randint(0, 255)))
                return headers
        except:
            pass
        if headers == "" or headers is None:
            UA = random.choice(user_agent)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'User-Agent': UA,
                'X-Forwarded-For': '10.10.{}.{}'.format(str(random.randint(0, 255)), str(random.randint(0, 255))),
            }
        else:
            if "X-Forwarded-For" not in headers:
                headers['X-Forwarded-For'] = '10.10.{}.{}'.format(str(random.randint(0, 255)), str(random.randint(0, 255)))
            headers.update({'User-Agent': random.choice(user_agent)})
        return headers

    # 使用云函数代理
    def yunProxy(self, url, data, headers, method, files=None):
        yUrl = self.proxyList[random.randint(1, len(self.proxyList) - 1)].decode().strip()
        if data is None:
            data = ""
        body = url + "#####" + method + "#####" + str(headers) + "#####" + str(data)
        if method == "POST" and files is not None:
            body += "#####" + str(files)
        try:
            html = requests.post(url=yUrl, data=body, verify=False, timeout=20)
        except:
            return None
        text = html.text.split("#xy##%&*xy##")[0]
        headers = eval(html.text.split("#xy##%&*xy##")[1])
        status_code = int(html.text.split("#xy##%&*xy##")[2])
        cookies = html.text.split("#xy##%&*xy##")[3]
        htmlEncoding = html.text.split("#xy##%&*xy##")[4]
        res = Html(text, status_code, text.encode(), headers, cookies, htmlEncoding)
        return res

    def get(self, url, headers="", timeout=15, verify=False, data=None, allow_redirects=True):
        headers = self.requests_headers(headers)
        if len(self.proxyList) > 0:
            # 云代理获取web信息
            if self.proxyList[0] == "云":
                return self.yunProxy(url, data, headers, "GET")
            proxy = self.proxyList[random.randint(0, len(self.proxyList)-1)].decode().strip()
            proxies = {
                'http': proxy,  # 127.0.0.1:1080 shadowsocks
                'https': proxy  # 127.0.0.1:8080 BurpSuite
            }
        else:
            proxies = {}
        """获取web的信息"""
        try:
            res = requests.get(url=url, headers=headers, proxies=proxies, timeout=timeout, verify=verify, data=data, allow_redirects=allow_redirects)
            return res
        except Exception as e:
            #print(e)
            return None

    def sessionGet(self, url, headers="", timeout=15, verify=False, data=None):
        headers = self.requests_headers(headers)
        if len(self.proxyList) > 0:
            if self.proxyList[0] == "云":
                # 云代理获取web信息
                if self.proxyList[0] == "云":
                    return self.yunProxy(url, data, headers, "GET")
            proxy = self.proxyList[random.randint(0, len(self.proxyList)-1)].decode().strip()
            proxies = {
                'http': proxy,  # 127.0.0.1:1080 shadowsocks
                'https': proxy  # 127.0.0.1:8080 BurpSuite
            }
        else:
            proxies = {}
        """获取web的信息"""
        try:
            res = self.session.get(url=url, headers=headers, proxies=proxies, timeout=timeout, verify=verify, data=data)
            return res
        except Exception as e:
            return None

    # 分块接收数据
    def get_stream(self, url, headers=None, encoding='UTF-8', data=None):
        """分块接受数据"""
        headers = self.requests_headers(headers)
        if len(self.proxyList) > 0:
            # 云代理获取web信息
            if self.proxyList[0] == "云":
                return self.yunProxy(url, data, headers, "GET")
            proxy = self.proxyList[random.randint(0, len(self.proxyList)-1)].decode().strip()
            proxies = {
                'http': proxy,  # 127.0.0.1:1080 shadowsocks
                'https': proxy  # 127.0.0.1:8080 BurpSuite
            }
        else:
            proxies = {}
        html = list()
        try:
            lines = requests.get(url, headers=headers, stream=True, timeout=8, proxies=proxies)
            for line in lines.iter_lines():
                if b'\x00' in line:
                    break
                line = line.decode(encoding)
                html.append(line.strip())
            return '\r\n'.join(html).strip()
        except ChunkedEncodingError as e:
            return '\r\n'.join(html).strip()
        except ConnectTimeout as e:
            return "ERROR:" + "HTTP连接超时错误"
        except ConnectionError as e:
            return "ERROR:" + "HTTP连接错误"
        except Exception as e:
            return 'ERROR:' + str(e)

    def post_stream(self, url, data=None, headers=None, encoding='UTF-8', files=None):
        """分块接受数据"""
        headers = self.requests_headers(headers)
        if len(self.proxyList) > 0:
            # 云代理获取web信息
            if self.proxyList[0] == "云":
                return self.yunProxy(url, data, headers, "POST")
            proxy = self.proxyList[random.randint(0, len(self.proxyList)-1)].decode().strip()
            proxies = {
                'http': proxy,  # 127.0.0.1:1080 shadowsocks
                'https': proxy  # 127.0.0.1:8080 BurpSuite
            }
        else:
            proxies = {}
        html = list()
        try:
            lines = requests.post(url, data=data, headers=headers, timeout=8, stream=True, files=files, proxies=proxies)
            for line in lines.iter_lines():
                line = line.decode(encoding)
                html.append(line.strip())
            return '\r\n'.join(html).strip()
        except ChunkedEncodingError as e:
            return '\r\n'.join(html).strip()
        except ConnectTimeout as e:
            return "ERROR:" + "HTTP连接超时错误"
        except ConnectionError as e:
            return "ERROR:" + "HTTP连接错误"
        except Exception as e:
            return 'ERROR:' + str(e)

    def patch(self, url, headers="", timeout=15, verify=False, data=None, allow_redirects=True):
        headers = self.requests_headers(headers)
        if len(self.proxyList) > 0:
            # 云代理获取web信息
            if self.proxyList[0] == "云":
                return self.yunProxy(url, data, headers, "PATCH")
            proxy = self.proxyList[random.randint(0, len(self.proxyList)-1)].decode().strip()
            proxies = {
                'http': proxy,  # 127.0.0.1:1080 shadowsocks
                'https': proxy  # 127.0.0.1:8080 BurpSuite
            }
        else:
            proxies = {}
        """获取web的信息"""
        # try:
        res = requests.patch(url=url, headers=headers, proxies=proxies, timeout=timeout, verify=verify, data=data, allow_redirects=allow_redirects)
        return res
        # except Exception as e:
        #     print(e)
        #     return None

    # 命令解析，将要执行的命令解析为字符串格式
    def parse_cmd(self, cmd, type='string'):
        cmd = shlex.split(cmd)
        if type == 'string':
            cmd_str = '"' + '","'.join(cmd) + '"'
        elif type == 'xml':
            cmd_str = '<string>' + '</string><string>'.join(cmd) + '</string>'
        else:
            cmd_str = cmd
        return cmd_str

    def post(self, url, headers="", data=None, json=None, files=None, timeout=15, verify=False, allow_redirects=True):
        headers = self.requests_headers(headers)
        if len(self.proxyList) > 0:
            if self.proxyList[0] == "云":
                return self.yunProxy(url, data, headers, "POST", files)
            proxy = self.proxyList[random.randint(0, len(self.proxyList)-1)].decode().strip()
            proxies = {
                'http': proxy,  # 127.0.0.1:1080 shadowsocks
                'https': proxy  # 127.0.0.1:8080 BurpSuite
            }
        else:
            proxies = {}
        """获取web的信息"""
        try:
            res = requests.post(url=url, headers=headers, proxies=proxies, data=data, json=json, timeout=timeout, verify=verify, files=files, allow_redirects=allow_redirects)
            return res
        except requests.exceptions.ChunkedEncodingError as e:
            import http.client
            http.client.HTTPConnection._http_vsn = 10
            http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
            res = requests.post(url=url, headers=headers, proxies=proxies, data=data, json=json, timeout=timeout, verify=verify, stream=True, allow_redirects=allow_redirects)
            return res
        except Exception as e:
            return None

    def sessionPost(self, url, headers="", data=None, json=None, timeout=15, verify=False, files=None):
        headers = self.requests_headers(headers)
        if len(self.proxyList) > 0:
            if self.proxyList[0] == "云":
                return self.yunProxy(url, data, headers, "POST", files)
            proxy = self.proxyList[random.randint(0, len(self.proxyList)-1)].decode().strip()
            proxies = {
                'http': proxy,  # 127.0.0.1:1080 shadowsocks
                'https': proxy  # 127.0.0.1:8080 BurpSuite
            }
        else:
            proxies = {}
        """获取web的信息"""
        try:
            res = self.session.post(url=url, headers=headers, proxies=proxies, data=data, json=json, timeout=timeout, verify=verify, files=files)
            return res
        except requests.exceptions.ChunkedEncodingError as e:
            import http.client
            http.client.HTTPConnection._http_vsn = 10
            http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
            res = self.session.post(url=url, headers=headers, proxies=proxies, data=data, json=json, timeout=timeout, verify=verify, stream=True, files=files)
            return res
        except Exception as e:
            #print(e)
            return None

    def put(self, url, headers="", data=None, json=None, files=None, timeout=15, verify=False, allow_redirects=True):
        headers = self.requests_headers(headers)
        if len(self.proxyList) > 0:
            if self.proxyList[0] == "云":
                return self.yunProxy(url, data, headers, "PUT", files)
            proxy = self.proxyList[random.randint(0, len(self.proxyList)-1)].decode().strip()
            proxies = {
                'http': proxy,  # 127.0.0.1:1080 shadowsocks
                'https': proxy  # 127.0.0.1:8080 BurpSuite
            }
        else:
            proxies = {}
        """获取web的信息"""
        try:
            res = requests.put(url=url, headers=headers, proxies=proxies, data=data, json=json, timeout=timeout, verify=verify, files=files, allow_redirects=allow_redirects)
            return res
        except requests.exceptions.ChunkedEncodingError as e:
            import http.client
            http.client.HTTPConnection._http_vsn = 10
            http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
            res = requests.put(url=url, headers=headers, proxies=proxies, data=data, json=json, timeout=timeout, verify=verify, stream=True, allow_redirects=allow_redirects, files=files)
            return res
        except Exception as e:
            return None

    def getUrl(self, url):
        if self.baseUrl == False:
            if url[-1] == '/':
                return url[:-1]
            else:
                return url
        if parse.urlparse(url).netloc == "":
            url = "http://" + str(parse.urlparse(url).path.split("/")[0])
        elif parse.urlparse(url).scheme == "":
            url = "http://" + parse.urlparse(url).netloc
        else:
            url = parse.urlparse(url).scheme + "://" + parse.urlparse(url).netloc
        return url

    # 获取主机ip和端口
    def getServerIp(self, url):
        ip = parse.urlparse(url).netloc.split(":")[0]
        if len(parse.urlparse(url).netloc.split(":")) < 2:
            if parse.urlparse(url).scheme == "http":
                port = 80
            else:
                port = 443
        else:
            port = int(parse.urlparse(url).netloc.split(":")[1])
        return ip, port

    def misinformation(self, req, md):  # 用来处理echo被错误返回时的误报，代码小巧作用大
        bad_1 = "echo%20" + md
        bad_2 = "echo%2520" + md
        bad_3 = "echo+" + md
        bad_4 = "echo_" + md
        bad_5 = "echo " + md
        if bad_1 in req:
            return "misinformation"
        elif bad_2 in req:
            return "misinformation"
        elif bad_3 in req:
            return "misinformation"
        elif bad_4 in req:
            return "misinformation"
        elif bad_5 in req:
            return "misinformation"
        else:
            return req

    def check_echo(self, req, md):  # 用来处理echo被错误返回时的误报，代码小巧作用大
        bad_1 = "echo%20" + md
        bad_2 = "echo%2520" + md
        bad_3 = "echo+" + md
        bad_4 = "echo_" + md
        bad_5 = "echo " + md
        bad_6 = "echo%20%22" + md
        if bad_1 in req:
            return False
        elif bad_2 in req:
            return False
        elif bad_3 in req:
            return False
        elif bad_4 in req:
            return False
        elif bad_5 in req:
            return False
        elif bad_6 in req:
            return False
        elif md in req:
            return True
        else:
            return False

    def get_md5(seclf, c):
        m = hashlib.md5()
        m.update(c.encode('utf-8'))
        psw = m.hexdigest()
        return psw

    def get_random_str(self, randomlength=6):
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str