import gevent
from gevent import monkey
monkey.patch_all(thread=False)
from com import variable
from plugins import Web_Finger
from socket import *
import re

class Port_Scan(object):
    def __init__(self, cor):
        self.cor = cor
        self.web_finger = Web_Finger.Web_Finger()

    def port_scan(self, ip, port):
        try:
            sock = socket(family=AF_INET, type=SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((ip, port))
            sock.send("hello".encode())
            flag_str = sock.recv(3096).decode('utf-8').encode()
            find_finger = False
            for finger in variable.finger_list:
                pattern = finger["pattern"].encode()
                re_search = re.search(pattern, flag_str, re.I)  # 匹配字符串不区分大小
                if re_search is not None:
                    if finger["name"] == "HTTP":
                        # 获取访问状态和title
                        code, title, web_finger = self.web_finger.web_finger(ip, port)
                        variable.open_port_list.append([ip, port, finger["name"], code, title, web_finger])
                        print("[+]{}:{} open {} {} {} {}".format(ip, port, finger["name"], code, title, web_finger))
                    else:
                        variable.open_port_list.append([ip, port, finger["name"], "", "", ""])
                        print("[+]{}:{} open {} {} {} {}".format(ip, port, finger["name"], "", "", ""))
                    sock.close()
                    find_finger = True
                    break
            if find_finger is False:
                self.port_finger(ip, port)
                sock.close()
        except:
            try:
                s = socket(AF_INET, SOCK_STREAM)
                s.settimeout(4)
                s.connect((ip, port))
                self.port_finger(ip, port)
                s.close()
            except:
                #print(ip,":",port)
                pass

    def port_finger(self, ip, port):
        for port_d in variable.port_list:
            port_s = port_d["port"].split(",")
            if str(port) in port_s:
                if port_d["name"] == "HTTP":
                    # 获取访问状态和title
                    code, title, web_finger = self.web_finger.web_finger(ip, port)
                    variable.open_port_list.append([ip, port, port_d["name"], code, title, web_finger])
                    print("[+]{}:{} open {} {} {} {}".format(ip, port, port_d["name"], code, title, web_finger))
                else:
                    variable.open_port_list.append([ip, port, port_d["name"], "", "", ""])
                    print("[+]{}:{} open {} {} {} {}".format(ip, port, port_d["name"], "", "", ""))
                return
        variable.open_port_list.append([ip, port, "", "", "", ""])
        print("[+]{}:{} open {} {} {} {}".format(ip, port, "", "", "", ""))

    def star_scan(self):
        while True:
            if variable.ip_port.qsize() == 0:
                break
            ip_port = variable.ip_port.get()
            self.port_scan(ip_port[0], int(ip_port[1]))

    def coroutines(self):
        # 开启多协程
        cos = []
        for i in range(self.cor):
            # 调用工作函数
            cor = gevent.spawn(self.star_scan)
            cos.append(cor)
        gevent.joinall(cos)

