import gevent
from gevent import monkey
monkey.patch_all(thread=False)
from com import variable
import platform
import subprocess


class Icmp(object):
    def __init__(self):
        pass

    # 多协程进行存活探测
    def star_icmp(self, ip_list):
        cor_num = 256
        if len(ip_list) < cor_num:
            cor_num = len(ip_list)
        for ip in ip_list:
            # print(ip)
            variable.ip_que.put(ip)
        # 开启多协程
        cos = []
        for i in range(cor_num):
            # 调用工作函数
            c = gevent.spawn(self.icmp_func)
            cos.append(c)
        gevent.joinall(cos)

    # 主机存活探测
    def icmp_func(self):
        while True:
            if variable.ip_que.qsize() == 0:
                break
            ip = variable.ip_que.get()
            # ip存活探测
            if (platform.system() == 'Windows'):
                p = subprocess.Popen('ping -n 1 {}'.format(ip), shell=False, close_fds=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            else:
                p = subprocess.Popen('ping -c 1 {}'.format(ip), shell=False, close_fds=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            try:
                out, err = p.communicate(timeout=8)
                if 'ttl' in out.decode('gbk').lower():
                    print(ip, "is live")
                    variable.ip_list.append(ip)
            except:
                pass
            p.kill()