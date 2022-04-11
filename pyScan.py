import gevent
from gevent import monkey
monkey.patch_all(thread=False)
from plugins import Port_Scan
from plugins import Icmp
from plugins import Ips_ip
from plugins import Out_excel
from com import variable
import time
import sys
import os
import argparse


def banner():
    print(r"""

               _________                     
______ ___.__./   _____/ ____ _____    ____  
\____ <   |  |\_____  \_/ ___\\__  \  /    \ 
|  |_> >___  |/        \  \___ / __ \|   |  \
|   __// ____/_______  /\___  >____  /___|  /
|__|   \/            \/     \/     \/     \/ 


    """)


def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print("Error: " + errmsg)
    sys.exit()


def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -ip 127.0.0.1")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-ip', help="目标ip最大支持B段,支持格式：127.0.0.1;127.0.0.0/24;127.0.0.1-110", default=True)
    parser.add_argument('-ipf', help="目标ip文件路径", default=True)
    parser.add_argument('-nop', help="默认ICMP存活探测", nargs='?', default=True)
    parser.add_argument('-icmp', help="只进行存ICMP活探测", nargs='?', default=True)
    parser.add_argument('-p', help='扫描端口，默认扫描常见端口，支持格式：80;80-88;80,81', default=True)
    parser.add_argument('-c', help='开启协程数，默认开启2000', type=int, default=2000)
    parser.add_argument('-o', help='保存扫描信息，存活IP默认live_ip.xlsx，扫描信息默认info.xlsx', nargs='?', default=False)
    return parser.parse_args()


if __name__ == '__main__':
    banner()
    args = parse_args()
    # 解析ip
    if (args.ipf is True and args.ip is True) or (args.ipf is not True and args.ip is not True):
        exit()
    ips_ip = Ips_ip.Ips_ip()
    ip_list = []
    if args.ip is not True:
        ip_list = ips_ip.ips_ip(args.ip)
    elif os.path.isfile(args.ipf) or os.path.isfile(os.path.join(os.getcwd(), args.ipf)):
        with open(args.ipf, "rb") as f:
            ips = f.readlines()
            for ip in ips:
                try:
                    ip_list += ips_ip.ips_ip(ip.decode().strip())
                except:
                    pass
    else:
        exit()
    # 解析port
    port_list = ips_ip.ports_port(args.p)
    t1 = int(time.time())
    # 只进行ICMP存活探测
    icmp_func = Icmp.Icmp()
    out_excel = Out_excel.Out_excel()
    if args.icmp is not True:
        icmp_func.star_icmp(ip_list)
        if args.o is not False:
            out_excel.out_excel("live_ip", variable.ip_list, ["ip"])
        print('end main total time:', int(time.time()) - t1)
        exit()
    # 是否进行存活探测
    if args.nop:
        icmp_func.star_icmp(ip_list)
        ip_list = variable.ip_list
    # ip+port加入扫描队列
    for ip in ip_list:
        for port in port_list:
            variable.ip_port.put([ip, port])
    # 如果扫描队列长度小于默认进程长度，进程最小化开启
    cor_num = args.c
    if variable.ip_port.qsize() < args.c:
        cor_num = variable.ip_port.qsize()
    pScan = Port_Scan.Port_Scan(cor_num)
    pScan.coroutines()
    if args.o is not False:
        out_excel.out_excel("live_ip", variable.ip_list, ["ip"])
        out_excel.out_excel("info", variable.open_port_list, ["ip", "port", "finger", "code", "title", "web_finger"])
    print( 'end main total time:', int(time.time())-t1)