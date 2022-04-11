import IPy
import re
from com import variable

class Ips_ip(object):
    def __init__(self):
        pass

    # 参数1为list，参数2为步长;将列表等分为几个列表
    def list_of_groups(self, init_list, childern_list_len):
        list_of_groups = zip(*(iter(init_list),) * childern_list_len)
        end_list = [list(i) for i in list_of_groups]
        count = len(init_list) % childern_list_len
        end_list.append(init_list[-count:]) if count != 0 else end_list
        return end_list

    # 获取掩码内所有IP
    def get_all_ip(self, ip):
        Iplist = []
        num = ip.split('/')[1]
        length = len(IPy.IP('127.0.0.0/{}'.format(num)))
        endiplists = self.list_of_groups(range(0, 256), length)
        for endiplist in endiplists:
            if int(ip.split('/')[0].split('.')[-1].strip()) in endiplist:
                for endip in endiplist:
                    Iplist.append('.'.join(ip.split('/')[0].split('.')[:-1]) + '.{}'.format(endip))
                break
        return Iplist

    # 获取ip列表
    def ips_ip(self, ip):
        newIplist = []
        if "-" in ip:
            startip = ip.strip().split("-")[0]
            endip = ip.strip().split("-")[-1]
            for i in range(int(startip.split('.')[-1]), int(endip.split('.')[-1]) + 1):
                newIplist.append('.'.join(startip.split('.')[:-1]) + '.{}'.format(i))
        elif "/" in ip:
            if int(ip.split("/")[1]) >= 24:
                newIplist = self.get_all_ip(ip)
            elif int(ip.split("/")[1]) >= 16:
                new_ip = ip.split(".")[0] + "." + ip.split(".")[1] + ".0.0/{}".format(ip.split("/")[1])
                ips = IPy.IP(new_ip)
                for i in ips:
                    newIplist.append(str(i))
            else:
                new_ip = ip.split(".")[0] + ".0.0.0/{}".format(ip.split("/")[1])
                ips = IPy.IP(new_ip)
                for i in ips:
                    newIplist.append(str(i))
        elif re.match(r'^\d{0,3}.\d{0,3}.\d{0,3}.\d{0,3}$', ip) != None:
            newIplist.append(ip)
        return newIplist

    # 获取端口列表
    def ports_port(self, ports):
        port_list = []
        if ports is True:
            port_list = variable.scan_port_list
        elif "," in ports:
            port_list = ports.split(",")
        elif "-" in ports:
            for p in range(int(ports.split("-")[0]), int(ports.split("-")[1]) + 1):
                port_list.append(p)
        else:
            port_list.append(ports)
        return port_list