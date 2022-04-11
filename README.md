# pyScan

快速综合探测工具，一键自动化存活探测、指纹识别。   

支持主机存活探测、端口扫描、web指纹识别等功能。

## 免责声明

本工具仅供学习使用，如您需要测试本工具的可用性，请自行搭建靶机环境。

在使用本工具进行检测时，确保符合当地的法律法规，并且已经取得授权。**请勿对非授权目标进行扫描。**

如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。

## 主要功能

* 存活探测(icmp)
* 端口扫描
* web指纹识别

## 使用方法

简单用法

``` 
pyScan.exe -ip 127.0.0.1/24  默认icmp存活探测，识别web指纹
pyScan.exe -ip 127.0.0.1/16  B段扫描
```

参数

```
  -h, --help    show this help message and exit
  -ip IP        目标ip最大支持B段,支持格式：127.0.0.1;127.0.0.0/24;127.0.0.1-110
  -ipf IPF      目标ip文件路径
  -nop [NOP]    默认ICMP存活探测
  -icmp [ICMP]  只进行存ICMP活探测
  -p P          扫描端口，默认扫描常见端口，支持格式：80;80-88;80,81
  -c C          开启协程数，默认开启2000
  -o [O]        保存扫描信息，存活IP默认live_ip.xlsx，扫描信息默认info.xlsx
```



## 最近更新

2022/4/11 端口扫描+指纹识别 

## 更新计划

定向漏洞探测+漏洞利用+弱口令爆破

## 运行截图
![image-20220411175446914](https://user-images.githubusercontent.com/82521860/162714605-1178ef60-85b7-4e20-be97-a219a456a6f8.png)

![image-20220411175042564](https://user-images.githubusercontent.com/82521860/162714487-c7751c73-3124-4d2c-bc62-e1f7b7f9f3f2.png)

![image-20220411175158802](https://user-images.githubusercontent.com/82521860/162714661-85bdbcf0-1762-4bf0-bdbe-4aabfa459d91.png)

![image-20220411175246207](https://user-images.githubusercontent.com/82521860/162714746-2e9d41b7-88bd-4b63-84de-e712fb71a07e.png)

