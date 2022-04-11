# 该文件定义全局变量, 已经初始化获取POCS字典
import os
from queue import Queue

# 创建全局队列
ip_port = Queue()       # ip-port队列
ip_que = Queue()        # 存活探测ip队列
title_que = Queue()     # 获取title队列

open_port_list = []     # 开放端口列表
ip_list = []            # 存活ip列表
out_info_list = []      # 输出信息列表

finger_list = [
    {
        'pattern': '^HTTP/',
        'name': 'HTTP'
    },
    {
        "pattern": "^SSH-",
        "name": "SSH"
    },
    {
        'pattern': '^\\x15\\x03\\x03\\x00\\x02\\x02P',
        'name': 'HTTPS'
    }
]

# 常见端口指纹
port_list = [
    {
        'port': '80,443,8080',
        'name': 'HTTP'
    },
    {
        "port": "22",
        "name": "SSH"
    },
    {
        "port": "25",
        "name": "SMTP"
    },
    {
        'port': '21',
        'name': 'FTP'
    },
    {
        'port': '23',
        'name': 'Telnet'
    },
    {
        'port': '3306',
        'name': 'MYSQL'
    },
    {
        'port': '1433',
        'name': 'SQLServer'
    },
    {
        'port': '1521',
        'name': 'Oracle'
    },
    {
        'port': '445',
        'name': 'SMB'
    },
    {
        'port': '3389',
        'name': 'RDP'
    },
    {
        'port': '6379',
        'name': 'Redis'
    },
    {
        'port': '5900,5901',
        'name': 'VNC'
    },
    {
        'port': '5432',
        'name': 'PosterSQL'
    },
    {
        'port': '27017,27018',
        'name': 'MongoDB'
    },
    {
        'port': '2128',
        'name': 'Zookeeper'
    },
    {
        'port': '8068,8069',
        'name': 'Zabbix'
    },
    {
        'port': '11211',
        'name': 'Memcache'
    },
    {
        'port': '9200,9300',
        'name': 'Elasticsearch'
    },
    {
        'port': '50070',
        'name': 'Hadoop'
    },
    {
        'port': '8161',
        'name': 'Apache ActiveMQ'
    },
    {
        'port': '5984',
        'name': 'CouchDB'
    },
    {
        'port': '5632',
        'name': 'PyAnywhere'
    },
    {
        'port': '2375',
        'name': 'Docker'
    }
]

# 扫描常见端口
scan_port_list = [1,7,9,13,19,21,22,23,25,37,42,49,53,69,79,80,81,82,83,84,85,86,87,88,89,90,91,92,98,99,105,109,110,111,113,123,135,137,138,139,143,161,179,222,264,384,389,402,407,443,444,445,446,465,500,502,512,513,514,515,523,524,540,548,554,587,617,623,689,705,771,783,800,801,808,873,880,888,889,902,910,912,921,993,995,998,1000,1010,1024,1030,1035,1080,1081,1082,1090,1098,1099,1100,1101,1102,1103,1118,1128,1129,1158,1199,1211,1220,1234,1241,1300,1311,1352,1433,1434,1435,1440,1494,1521,1530,1533,1581,1582,1604,1720,1723,1755,1811,1888,1900,2000,2001,2008,2020,2049,2082,2083,2100,2103,2121,2199,2207,2222,2323,2362,2375,2379,2380,2381,2525,2533,2598,2601,2604,2638,2809,2947,2967,3000,3008,3037,3050,3057,3128,3200,3217,3273,3299,3306,3311,3312,3389,3460,3500,3505,3628,3632,3690,3780,3790,3817,4000,4322,4433,4444,4445,4659,4679,4848,5000,5038,5040,5051,5060,5061,5093,5168,5247,5250,5351,5353,5355,5400,5405,5432,5433,5498,5520,5521,5554,5555,5560,5580,5601,5631,5632,5666,5800,5814,5900,5901,5902,5903,5904,5905,5906,5907,5908,5909,5910,5920,5984,5985,5986,6000,6050,6060,6070,6080,6082,6101,6106,6112,6262,6379,6405,6502,6504,6542,6648,6660,6661,6667,6803,6868,6905,6988,7000,7001,7002,7003,7004,7005,7007,7008,7021,7070,7071,7074,7078,7080,7088,7144,7181,7200,7210,7443,7510,7579,7580,7680,7687,7688,7700,7770,7777,7778,7787,7800,7801,7879,7890,7902,8000,8001,8002,8003,8004,8006,8008,8009,8010,8011,8012,8014,8016,8018,8020,8023,8028,8030,8038,8042,8044,8046,8048,8053,8060,8069,8070,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,8092,8093,8094,8095,8096,8097,8098,8099,8100,8101,8108,8118,8161,8172,8180,8181,8200,8205,8222,8244,8258,8280,8288,8300,8303,8333,8360,8400,8443,8444,8448,8484,8503,8800,8812,8834,8838,8848,8858,8868,8879,8880,8881,8888,8889,8890,8899,8901,8902,8903,8983,8989,9000,9001,9002,9008,9010,9043,9060,9080,9081,9082,9083,9084,9085,9086,9087,9088,9089,9090,9091,9092,9093,9094,9095,9096,9097,9098,9099,9100,9111,9152,9200,9390,9391,9443,9448,9495,9800,9809,9810,9811,9812,9813,9814,9815,9855,9981,9986,9988,9998,9999,10000,10001,10002,10004,10008,10010,10050,10051,10080,10098,10162,10202,10203,10250,10443,10616,10628,11000,11099,11211,11234,11333,12018,12174,12203,12221,12345,12397,12401,12443,13364,13500,13838,14000,14330,15200,16080,16102,17185,17200,18000,18001,18002,18004,18008,18080,18082,18088,18090,18098,18881,19001,19300,19810,20000,20010,20031,20034,20101,20111,20171,20222,20720,20880,21000,21501,21502,22222,23472,23791,23943,25000,25025,26000,26122,27000,27017,27888,28018,28222,28784,30000,30718,31001,31099,32764,32913,34205,34443,37718,38080,38292,40007,41025,41080,41523,41524,44334,44818,45230,46823,46824,47001,47002,48899,49152,50000,50001,50002,50003,50004,50013,50500,50501,50502,50503,50504,52302,55553,57772,62078,62514,65535,1443,2443,3443,5443,11443,22443,60000]

# web指纹
web_finger_list = [
  {
    "name": "Dell-Printer",
    "rule": "title=\"Dell Laser Printer\"",
    "program": ""
  },
  {
    "name": "HP-OfficeJet-Printer",
    "rule": "title=\"HP Officejet\" || body=\"align=\"center\">HP Officejet\"",
    "program": ""
  },
  {
    "name": "Biscom-Delivery-Server",
    "rule": "body=\"/bds/stylesheets/fds.css\" || body=\"/bds/includes/fdsJavascript.do\"",
    "program": ""
  },
  {
    "name": "DD-WRT",
    "rule": "body=\"style/pwc/ddwrt.css\"",
    "program": ""
  },
  {
    "name": "ewebeditor",
    "rule": "body=\"/ewebeditor.htm?\"",
    "program": ""
  },
  {
    "name": "fckeditor",
    "rule": "body=\"new FCKeditor\"",
    "program": ""
  },
  {
    "name": "xheditor",
    "rule": "body=\"xheditor_lang/zh-cn.js\" || body=\"class=\"xheditor\" || body=\".xheditor(\"",
    "program": ""
  },
  {
    "name": "百为路由",
    "rule": "body=\"提交验证的id必须是ctl_submit\"",
    "program": ""
  },
  {
    "name": "锐捷NBR路由器",
    "rule": "body=\"free_nbr_login_form.png\"",
    "program": ""
  },
  {
    "name": "mikrotik",
    "rule": "title=\"RouterOS\" && body=\"mikrotik\"",
    "program": ""
  },
  {
    "name": "ThinkSNS",
    "rule": "body=\"/addons/theme/\" && body=\"全局变量\"",
    "program": ""
  },
  {
    "name": "h3c路由器",
    "rule": "title=\"Web user login\" && body=\"nLanguageSupported\"",
    "program": ""
  },
  {
    "name": "jcg无线路由器",
    "rule": "title=\"Wireless Router\" && body=\"http://www.jcgcn.com\"",
    "program": ""
  },
  {
    "name": "D-Link_VoIP_Wireless_Router",
    "rule": "title=\"D-Link VoIP Wireless Router\"",
    "program": ""
  },
  {
    "name": "arrisi_Touchstone",
    "rule": "title=\"Touchstone Status\" || body=\"passWithWarnings\"",
    "program": ""
  },
  {
    "name": "ZyXEL",
    "rule": "body=\"Forms/rpAuth_1\"",
    "program": ""
  },
  {
    "name": "Ruckus",
    "rule": "body=\"mon.  Tell me your username\" || title=\"Ruckus Wireless Admin\"",
    "program": ""
  },
  {
    "name": "Motorola_SBG900",
    "rule": "title=\"Motorola SBG900\"",
    "program": ""
  },
  {
    "name": "Wimax_CPE",
    "rule": "title=\"Wimax CPE Configuration\"",
    "program": ""
  },
  {
    "name": "Cisco_Cable_Modem",
    "rule": "title=\"Cisco Cable Modem\"",
    "program": ""
  },
  {
    "name": "Scientific-Atlanta_Cable_Modem",
    "rule": "title=\"Scientific-Atlanta Cable Modem\"",
    "program": ""
  },
  {
    "name": "rap",
    "rule": "body=\"/jscripts/rap_util.js\"",
    "program": ""
  },
  {
    "name": "ZTE_MiFi_UNE",
    "rule": "title=\"MiFi UNE 4G LTE\"",
    "program": ""
  },
  {
    "name": "ZTE_ZSRV2_Router",
    "rule": "title=\"ZSRV2路由器Web管理系统\" && body=\"ZTE Corporation. All Rights Reserved.\"",
    "program": ""
  },
  {
    "name": "百为智能流控路由器",
    "rule": "title=\"BYTEVALUE 智能流控路由器\" && body=\"<a href=\"http://www.bytevalue.com/\" target=\"_blank\">\"",
    "program": ""
  },
  {
    "name": "乐视路由器",
    "rule": "title=\"乐视路由器\" && body=\"<div class=\"login-logo\"></div>\"",
    "program": ""
  },
  {
    "name": "Verizon_Wireless_Router",
    "rule": "title=\"Wireless Broadband Router Management Console\" && body = \"verizon_logo_blk.gif\"",
    "program": ""
  },
  {
    "name": "Nexus_NX_router",
    "rule": "body=\"http://nexuswifi.com/\" && title=\"Nexus NX\"",
    "program": ""
  },
  {
    "name": "Verizon_Router",
    "rule": "title=\"Verizon Router\"",
    "program": ""
  },
  {
    "name": "小米路由器",
    "rule": "title=\"小米路由器\" ",
    "program": ""
  },
  {
    "name": "QNO_Router",
    "rule": "body=\"/QNOVirtual_Keyboard.js\" && body=\"/images/login_img01_03.gif\"",
    "program": ""
  },
  {
    "name": "爱快流控路由",
    "rule": "title=\"爱快\" && body=\"/resources/images/land_prompt_ico01.gif\"",
    "program": ""
  },
  {
    "name": "Django",
    "rule": "body=\"__admin_media_prefix__\" || body=\"csrfmiddlewaretoken\"",
    "program": ""
  },
  {
    "name": "axis2-web",
    "rule": "body=\"axis2-web/css/axis-style.css\"",
    "program": ""
  },
  {
    "name": "Apache-Wicket",
    "rule": "body=\"xmlns:wicket=\" || body=\"/org.apache.wicket.\"",
    "program": ""
  },
  {
    "name": "BEA-WebLogic-Server",
    "rule": "body=\"<h1>BEA WebLogic Server\" || body=\"WebLogic\"",
    "program": ""
  },
  {
    "name": "EDK",
    "rule": "body=\"<!-- /killlistable.tpl -->\"",
    "program": ""
  },
  {
    "name": "eDirectory",
    "rule": "body=\"target=\"_blank\">eDirectory&trade\" || body=\"Powered by <a href=\"http://www.edirectory.com\"",
    "program": ""
  },
  {
    "name": "Esvon-Classifieds",
    "rule": "body=\"Powered by Esvon\"",
    "program": ""
  },
  {
    "name": "Fluid-Dynamics-Search-Engine",
    "rule": "body=\"content=\"fluid dynamics\"",
    "program": ""
  },
  {
    "name": "mongodb",
    "rule": "body=\"<a href=\"/_replSet\">Replica set status</a></p>\"",
    "program": ""
  },
  {
    "name": "MVB2000",
    "rule": "title=\"MVB2000\" || body=\"The Magic Voice Box\"",
    "program": ""
  },
  {
    "name": "GPSweb",
    "rule": "title=\"GPSweb\"",
    "program": ""
  },
  {
    "name": "phpinfo",
    "rule": "title=\"phpinfo\" && body=\"Virtual Directory Support \"",
    "program": ""
  },
  {
    "name": "lemis管理系统",
    "rule": "body=\"lemis.WEB_APP_NAME\"",
    "program": ""
  },
  {
    "name": "FreeboxOS",
    "rule": "title=\"Freebox OS\" || body=\"logo_freeboxos\"",
    "program": ""
  },
  {
    "name": "Wimax_CPE",
    "rule": "title=\"Wimax CPE Configuration\"",
    "program": ""
  },
  {
    "name": "Scientific-Atlanta_Cable_Modem",
    "rule": "title=\"Scientific-Atlanta Cable Modem\"",
    "program": ""
  },
  {
    "name": "rap",
    "rule": "body=\"/jscripts/rap_util.js\"",
    "program": ""
  },
  {
    "name": "ZTE_MiFi_UNE",
    "rule": "title=\"MiFi UNE 4G LTE\"",
    "program": ""
  },
  {
    "name": "用友商战实践平台",
    "rule": "body=\"Login_Main_BG\" && body=\"Login_Owner\"",
    "program": ""
  },
  {
    "name": "moosefs",
    "rule": "body=\"mfs.cgi\" || body=\"under-goal files\"",
    "program": ""
  },
  {
    "name": "蓝盾BDWebGuard",
    "rule": "body=\"BACKGROUND: url(images/loginbg.jpg) #e5f1fc\"",
    "program": ""
  },
  {
    "name": "护卫神网站安全系统",
    "rule": "title=\"护卫神.网站安全系统\"",
    "program": ""
  },
  {
    "name": "phpDocumentor",
    "rule": "body=\"Generated by phpDocumentor\"",
    "program": ""
  },
  {
    "name": "Adobe_ CQ5",
    "rule": "body=\"_jcr_content\"",
    "program": ""
  },
  {
    "name": "Adobe_GoLive",
    "rule": "body=\"generator\" content=\"Adobe GoLive\"",
    "program": ""
  },
  {
    "name": "Adobe_RoboHelp",
    "rule": "body=\"generator\" content=\"Adobe RoboHelp\"",
    "program": ""
  },
  {
    "name": "Amaya",
    "rule": "body=\"generator\" content=\"Amaya\"",
    "program": ""
  },
  {
    "name": "OpenMas",
    "rule": "title=\"OpenMas\" || body=\"loginHead\"><link href=\"App_Themes\"",
    "program": ""
  },
  {
    "name": "recaptcha",
    "rule": "body=\"recaptcha_ajax.js\"",
    "program": ""
  },
  {
    "name": "TerraMaster",
    "rule": "title=\"TerraMaster\" && body=\"/js/common.js\"",
    "program": ""
  },
  {
    "name": "创星伟业校园网群",
    "rule": "body=\"javascripts/float.js\" && body=\"vcxvcxv\"",
    "program": ""
  },
  {
    "name": "正方教务管理系统",
    "rule": "body=\"style/base/jw.css\"",
    "program": ""
  },
  {
    "name": "UFIDA_NC",
    "rule": "(body=\"UFIDA\" && body=\"logo/images/\") || body=\"logo/images/ufida_nc.png\"",
    "program": ""
  },
  {
    "name": "北创图书检索系统",
    "rule": "body=\"opac_two\"",
    "program": ""
  },
  {
    "name": "北京清科锐华CEMIS",
    "rule": "body=\"/theme/2009/image\" && body=\"login.asp\"",
    "program": ""
  },
  {
    "name": "RG-PowerCache内容加速系统",
    "rule": "title=\"RG-PowerCache\"",
    "program": ""
  },
  {
    "name": "sugon_gridview",
    "rule": "body=\"/common/resources/images/common/app/gridview.ico\"",
    "program": ""
  },
  {
    "name": "SLTM32_Configuration",
    "rule": "title=\"SLTM32 Web Configuration Pages \"",
    "program": ""
  },
  {
    "name": "SHOUTcast",
    "rule": "title=\"SHOUTcast Administrator\"",
    "program": ""
  },
  {
    "name": "milu_seotool",
    "rule": "body=\"plugin.php?id=milu_seotool\"",
    "program": ""
  },
  {
    "name": "CISCO_EPC3925",
    "rule": "body=\"Docsis_system\" && body=\"EPC3925\"",
    "program": ""
  },
  {
    "name": "HP_iLO(HP_Integrated_Lights-Out)",
    "rule": "body=\"js/iLO.js\"",
    "program": ""
  },
  {
    "name": "Siemens_SIMATIC",
    "rule": "body=\"/S7Web.css\"",
    "program": ""
  },
  {
    "name": "Schneider_Quantum_140NOE77101",
    "rule": "body=\"indexLanguage\" && body=\"html/config.js\"",
    "program": ""
  },
  {
    "name": "lynxspring_JENEsys",
    "rule": "body=\"LX JENEsys\"",
    "program": ""
  },
  {
    "name": "Sophos_Web_Appliance",
    "rule": "title=\"Sophos Web Appliance\"",
    "program": ""
  },
  {
    "name": "Comcast_Business",
    "rule": "body=\"cmn/css/common-min.css\"",
    "program": ""
  },
  {
    "name": "Locus_SolarNOC",
    "rule": "title=\"SolarNOC - Login\"",
    "program": ""
  },
  {
    "name": "Everything",
    "rule": "(body=\"Everything.gif\"||body=\"everything.png\") && title=\"Everything\"",
    "program": ""
  },
  {
    "name": "honeywell NetAXS",
    "rule": "title=\"Honeywell NetAXS\"",
    "program": ""
  },
  {
    "name": "Symantec Messaging Gateway",
    "rule": "title=\"Messaging Gateway\"",
    "program": ""
  },
  {
    "name": "xfinity",
    "rule": "title=\"Xfinity\" || body=\"/reset-meyer-1.0.min.css\"",
    "program": ""
  },
  {
    "name": "网动云视讯平台",
    "rule": "title=\"Acenter\" || body=\"/js/roomHeight.js\" || body=\"meetingShow!show.action\"",
    "program": ""
  },
  {
    "name": "蓝凌EIS智慧协同平台",
    "rule": "body=\"/scripts/jquery.landray.common.js\" || body=\"v11_QRcodeBar clr\"",
    "program": ""
  },
  {
    "name": "金山KingGate",
    "rule": "body=\"/src/system/login.php\"",
    "program": ""
  },
  {
    "name": "天融信入侵检测系统TopSentry",
    "rule": "title=\"天融信入侵检测系统TopSentry\"",
    "program": ""
  },
  {
    "name": "天融信日志收集与分析系统",
    "rule": "title=\"天融信日志收集与分析系统\"",
    "program": ""
  },
  {
    "name": "天融信WEB应用防火墙",
    "rule": "title=\"天融信WEB应用防火墙\"",
    "program": ""
  },
  {
    "name": "天融信入侵防御系统TopIDP",
    "rule": "body=\"天融信入侵防御系统TopIDP\"",
    "program": ""
  },
  {
    "name": "天融信Web应用安全防护系统",
    "rule": "title=\"天融信Web应用安全防护系统\"",
    "program": ""
  },
  {
    "name": "天融信TopFlow",
    "rule": "body=\"天融信TopFlow\"",
    "program": ""
  },
  {
    "name": "汉码软件",
    "rule": "title=\"汉码软件\" || body=\"alt=\"汉码软件LOGO\" || body=\"content=\"汉码软件\"",
    "program": ""
  },
  {
    "name": "凡科",
    "rule": "body=\"凡科互联网科技股份有限公司\" || body=\"content=\"凡科\"",
    "program": ""
  },
  {
    "name": "易分析",
    "rule": "title=\"易分析 PHPStat Analytics\" || body=\"PHPStat Analytics 网站数据分析系统\"",
    "program": ""
  },
  {
    "name": "phpems考试系统",
    "rule": "title=\"phpems\" || body=\"content=\"PHPEMS\"",
    "program": ""
  },
  {
    "name": "智睿软件",
    "rule": "body=\"content=\"智睿软件\" || body=\"Zhirui.js\"",
    "program": ""
  },
  {
    "name": "Apabi数字资源平台",
    "rule": "body=\"Default/apabi.css\" || body=\"<link href=\"HTTP://apabi\" || title=\"数字资源平台\"",
    "program": ""
  },
  {
    "name": "Fortinet Firewall",
    "rule": "title=\"Firewall Notification\"",
    "program": ""
  },
  {
    "name": "WDlinux",
    "rule": "title=\"wdOS\"",
    "program": ""
  },
  {
    "name": "小脑袋",
    "rule": "body=\"http://stat.xiaonaodai.com/stat.php\"",
    "program": ""
  },
  {
    "name": "天融信ADS管理平台",
    "rule": "title=\"天融信ADS管理平台\"",
    "program": ""
  },
  {
    "name": "天融信异常流量管理与抗拒绝服务系统",
    "rule": "title=\"天融信异常流量管理与抗拒绝服务系统\"",
    "program": ""
  },
  {
    "name": "天融信网络审计系统",
    "rule": "body=\"onclick=\"dlg_download()\"",
    "program": ""
  },
  {
    "name": "天融信脆弱性扫描与管理系统",
    "rule": "title=\"天融信脆弱性扫描与管理系统\" || body=\"/js/report/horizontalReportPanel.js\"",
    "program": ""
  },
  {
    "name": "AllNewsManager_NET",
    "rule": "body=\"Powered by\" && body=\"AllNewsManager\"",
    "program": ""
  },
  {
    "name": "Advanced-Image-Hosting-Script",
    "rule": "(body=\"Powered by\" && body=\"yabsoft.com\") || body=\"Welcome to install AIHS Script\"",
    "program": ""
  },
  {
    "name": "SNB股票交易软件",
    "rule": "body=\"Copyright 2005–2009 <a href=\"http://www.s-mo.com\">\"",
    "program": ""
  },
  {
    "name": "AChecker Web accessibility evaluation tool",
    "rule": "body=\"content=\"AChecker is a Web accessibility\" || title=\"Checker : Web Accessibility Checker\"",
    "program": ""
  },
  {
    "name": "SCADA PLC",
    "rule": "body=\"/images/rockcolor.gif\" || body=\"/ralogo.gif\" || body=\"Ethernet Processor\"",
    "program": ""
  },
  {
    "name": ".NET",
    "rule": "body=\"content=\"Visual Basic .NET 7.1\"",
    "program": ""
  },
  {
    "name": "phpmoadmin",
    "rule": "title=\"phpmoadmin\"",
    "program": ""
  },
  {
    "name": "SOMOIDEA",
    "rule": "body=\"DESIGN BY SOMOIDEA\"",
    "program": ""
  },
  {
    "name": "Apache-Archiva",
    "rule": "title=\"Apache Archiva\" || body=\"/archiva.js\" || body=\"/archiva.css\"",
    "program": ""
  },
  {
    "name": "AM4SS",
    "rule": "body=\"Powered by am4ss\" || body=\"am4ss.css\"",
    "program": ""
  },
  {
    "name": "ASPThai_Net-Webboard",
    "rule": "body=\"ASPThai.Net Webboard\"",
    "program": ""
  },
  {
    "name": "Astaro-Command-Center",
    "rule": "body=\"/acc_aggregated_reporting.js\" || body=\"/js/_variables_from_backend.js?\"",
    "program": ""
  },
  {
    "name": "ASP-Nuke",
    "rule": "body=\"CONTENT=\"ASP-Nuke\" || body=\"content=\"ASPNUKE\"",
    "program": ""
  },
  {
    "name": "ASProxy",
    "rule": "body=\"Surf the web invisibly using ASProxy power\" || body=\"btnASProxyDisplayButton\"",
    "program": ""
  },
  {
    "name": "ashnews",
    "rule": "body=\"powered by\" && body=\"ashnews\"",
    "program": ""
  },
  {
    "name": "Arab-Portal",
    "rule": "body=\"Powered by: Arab\"",
    "program": ""
  },
  {
    "name": "AppServ",
    "rule": "body=\"appserv/softicon.gif\" || body=\"index.php?appservlang=th\"",
    "program": ""
  },
  {
    "name": "VZPP Plesk",
    "rule": "title=\"VZPP Plesk \"",
    "program": ""
  },
  {
    "name": "ApPHP-Calendar",
    "rule": "body=\"This script was generated by ApPHP Calendar\"",
    "program": ""
  },
  {
    "name": "BigDump",
    "rule": "title=\"BigDump\" || body=\"BigDump: Staggered MySQL Dump Importer\"",
    "program": ""
  },
  {
    "name": "BestShopPro",
    "rule": "body=\"content=\"www.bst.pl\"",
    "program": ""
  },
  {
    "name": "BASE",
    "rule": "body=\"<!-- Basic Analysis and Security Engine (BASE) -->\" || body=\"mailto:base@secureideas.net\"",
    "program": ""
  },
  {
    "name": "Basilic",
    "rule": "body=\"/Software/Basilic\"",
    "program": ""
  },
  {
    "name": "Basic-PHP-Events-Lister",
    "rule": "body=\"Powered by: <a href=\"http://www.mevin.com/\">\"",
    "program": ""
  },
  {
    "name": "AV-Arcade",
    "rule": "body=\"Powered by <a href=\"http://www.avscripts.net/avarcade/\"",
    "program": ""
  },
  {
    "name": "Auxilium-PetRatePro",
    "rule": "body=\"index.php?cmd=11\"",
    "program": ""
  },
  {
    "name": "Atomic-Photo-Album",
    "rule": "body=\"Powered by\" && body=\"Atomic Photo Album\"",
    "program": ""
  },
  {
    "name": "Axis-PrintServer",
    "rule": "body=\"psb_printjobs.gif\" || body=\"/cgi-bin/prodhelp?prod=\"",
    "program": ""
  },
  {
    "name": "TeamViewer",
    "rule": "body=\"This site is running\"&&body=\"TeamViewer\"",
    "program": ""
  },
  {
    "name": "BlueQuartz",
    "rule": "body=\"VALUE=\"Copyright (C) 2000, Cobalt Networks\" || title=\"Login - BlueQuartz\"",
    "program": ""
  },
  {
    "name": "BlueOnyx",
    "rule": "title=\"Login - BlueOnyx\" || body=\"Thank you for using the BlueOnyx\"",
    "program": ""
  },
  {
    "name": "BMC-Remedy",
    "rule": "title=\"Remedy Mid Tier\"",
    "program": ""
  },
  {
    "name": "BM-Classifieds",
    "rule": "body=\"<!-- START HEADER TABLE - HOLDS GRAPHIC AND SITE NAME -->\"",
    "program": ""
  },
  {
    "name": "Citrix-Metaframe",
    "rule": "body=\"window.location=\"/Citrix/MetaFrame\"",
    "program": ""
  },
  {
    "name": "Cogent-DataHub",
    "rule": "body=\"/images/Cogent.gif\" || title=\"Cogent DataHub WebView\"",
    "program": ""
  },
  {
    "name": "ClipShare",
    "rule": "body=\"<!--!!!!!!!!!!!!!!!!!!!!!!!!! Processing SCRIPT\" || body=\"Powered By <a href=\"http://www.clip-share.com\"",
    "program": ""
  },
  {
    "name": "CGIProxy",
    "rule": "body=\"<a href=\"http://www.jmarshall.com/tools/cgiproxy/\"",
    "program": ""
  },
  {
    "name": "CF-Image-Hosting-Script",
    "rule": "body=\"Powered By <a href=\"http://codefuture.co.uk/projects/imagehost/\"",
    "program": ""
  },
  {
    "name": "Censura",
    "rule": "body=\"Powered by: <a href=\"http://www.censura.info\"",
    "program": ""
  },
  {
    "name": "CA-SiteMinder",
    "rule": "body=\"<!-- SiteMinder Encoding\"",
    "program": ""
  },
  {
    "name": "Carrier-CCNWeb",
    "rule": "body=\"/images/CCNWeb.gif\" || body=\"<APPLET CODE=\"JLogin.class\" ARCHIVE=\"JLogin.jar\"",
    "program": ""
  },
  {
    "name": "cInvoice",
    "rule": "body=\"Powered by <a href=\"http://www.forperfect.com/\"",
    "program": ""
  },
  {
    "name": "Bomgar",
    "rule": "body=\"alt=\"Remote Support by BOMGAR\" || body=\"<a href=\"http://www.bomgar.com/products\" class=\"inverse\"",
    "program": ""
  },
  {
    "name": "cApexWEB",
    "rule": "body=\"/capexweb.parentvalidatepassword\" || body=\"name=\"dfparentdb\"",
    "program": ""
  },
  {
    "name": "CameraLife",
    "rule": "body=\"content=\"Camera Life\" || body=\"This site is powered by Camera Life\"",
    "program": ""
  },
  {
    "name": "CalendarScript",
    "rule": "title=\"Calendar Administration : Login\" || body=\"Powered by <A HREF=\"http://www.CalendarScript.com\"",
    "program": ""
  },
  {
    "name": "Cachelogic-Expired-Domains-Script",
    "rule": "body=\"href=\"http://cachelogic.net\">Cachelogic.net\"",
    "program": ""
  },
  {
    "name": "Burning-Board-Lite",
    "rule": "body=\"Powered by <b><a href=\"http://www.woltlab.de\" || body=\"Powered by <b>Burning Board\"",
    "program": ""
  },
  {
    "name": "Buddy-Zone",
    "rule": "body=\"Powered By <a href=\"http://www.vastal.com\" || body=\">Buddy Zone</a>\"",
    "program": ""
  },
  {
    "name": "Bulletlink-Newspaper-Template",
    "rule": "body=\"/ModalPopup/core-modalpopup.css\" || body=\"powered by bulletlink\"",
    "program": ""
  },
  {
    "name": "Brother-Printer",
    "rule": "body=\"<FRAME SRC=\"/printer/inc_head.html\" || body=\"<IMG src=\"/common/image/HL4040CN\"",
    "program": ""
  },
  {
    "name": "Daffodil-CRM",
    "rule": "body=\"Powered by Daffodil\" || body=\"Design & Development by Daffodil Software Ltd\"",
    "program": ""
  },
  {
    "name": "Cyn_in",
    "rule": "body=\"content=\"cyn.in\" || body=\"Powered by cyn.in\"",
    "program": ""
  },
  {
    "name": "Oracle_OPERA",
    "rule": "title=\"MICROS Systems Inc., OPERA\" || body=\"OperaLogin/Welcome.do\"",
    "program": ""
  },
  {
    "name": "DUgallery",
    "rule": "body=\"Powered by DUportal\" ||  body=\"DUgallery\"",
    "program": ""
  },
  {
    "name": "DublinCore",
    "rule": "body=\"name=\"DC.title\"",
    "program": ""
  },
  {
    "name": "DZCP",
    "rule": "body=\"<!--[ DZCP\"",
    "program": ""
  },
  {
    "name": "DVWA",
    "rule": "title=\"Damn Vulnerable Web App (DVWA) - Login\" || body=\"dvwa/css/login.css\" || body=\"dvwa/images/login_logo.png\"",
    "program": ""
  },
  {
    "name": "DORG",
    "rule": "title=\"DORG - \" || body=\"CONTENT=\"DORG\"",
    "program": ""
  },
  {
    "name": "VOS3000",
    "rule": "title=\"VOS3000\"||body=\"<meta name=\"keywords\" content=\"VOS3000\"||body=\"<meta name=\"description\" content=\"VOS3000\"||body=\"images/vos3000.ico\"",
    "program": ""
  },
  {
    "name": "Elite-Gaming-Ladders",
    "rule": "body=\"Powered by Elite\"",
    "program": ""
  },
  {
    "name": "Entrans",
    "rule": "title=\"Entrans\"",
    "program": ""
  },
  {
    "name": "GateQuest-PHP-Site-Recommender",
    "rule": "title=\"GateQuest\"",
    "program": ""
  },
  {
    "name": "Gallarific",
    "rule": "body=\"content=\"Gallarific\" || title=\"Gallarific > Sign in\"",
    "program": ""
  },
  {
    "name": "EZCMS",
    "rule": "body=\"Powered by EZCMS\" || body=\"EZCMS Content Management System\"",
    "program": ""
  },
  {
    "name": "Etano",
    "rule": "body=\"Powered by <a href=\"http://www.datemill.com\" || body=\"Etano</a>. All Rights Reserved.\"",
    "program": ""
  },
  {
    "name": "GeoServer",
    "rule": "body=\"/org.geoserver.web.GeoServerBasePage/\" || body=\"class=\"geoserver lebeg\"",
    "program": ""
  },
  {
    "name": "GeoNode",
    "rule": "body=\"Powered by <a href=\"http://geonode.org\" || (body=\"href=\"/catalogue/opensearch\" && body=\"GeoNode Search\")",
    "program": ""
  },
  {
    "name": "Help-Desk-Software",
    "rule": "body=\"target=\"_blank\">freehelpdesk.org\"",
    "program": ""
  },
  {
    "name": "GridSite",
    "rule": "body=\"<a href=\"http://www.gridsite.org/\">GridSite\" || body=\"gridsite-admin.cgi?cmd\"",
    "program": ""
  },
  {
    "name": "GenOHM-SCADA",
    "rule": "title=\"GenOHM Scada Launcher\" || body=\"/cgi-bin/scada-vis/\"",
    "program": ""
  },
  {
    "name": "Infomaster",
    "rule": "body=\"/MasterView.css\" || body=\"/masterView.js\" || body=\"/MasterView/MPLeftNavStyle/PanelBar.MPIFMA.css\"",
    "program": ""
  },
  {
    "name": "Imageview",
    "rule": "body=\"content=\"Imageview\" || body=\"By Jorge Schrauwen\" || body=\"href=\"http://www.blackdot.be\" || title=\"Blackdot.be\"",
    "program": ""
  },
  {
    "name": "Ikonboard",
    "rule": "body=\"content=\"Ikonboard\" || body=\"Powered by <a href=\"http://www.ikonboard.com\"",
    "program": ""
  },
  {
    "name": "i-Gallery",
    "rule": "title=\"i-Gallery\" || body=\"href=\"igallery.asp\"",
    "program": ""
  },
  {
    "name": "OrientDB",
    "rule": "title=\"Redirecting to OrientDB\"",
    "program": ""
  },
  {
    "name": "Solr",
    "rule": "title=\"Solr Admin\"||body=\"SolrCore Initialization Failures\"||body=\"app_config.solr_path\"",
    "program": ""
  },
  {
    "name": "Inout-Adserver",
    "rule": "body=\"Powered by Inoutscripts\"",
    "program": ""
  },
  {
    "name": "ionCube-Loader",
    "rule": "body=\"alt=\"ionCube logo\"",
    "program": ""
  },
  {
    "name": "Jamroom",
    "rule": "body=\"content=\"Talldude Networks\" || body=\"content=\"Jamroom\"",
    "program": ""
  },
  {
    "name": "Juniper-NetScreen-Secure-Access",
    "rule": "body=\"/dana-na/auth/welcome.cgi\"",
    "program": ""
  },
  {
    "name": "Jcow",
    "rule": "body=\"content=\"Jcow\" || body=\"content=\"Powered by Jcow\" || body=\"end jcow_application_box\"",
    "program": ""
  },
  {
    "name": "InvisionPowerBoard",
    "rule": "body=\"Powered by <a href=\"http://www.invisionboard.com\"",
    "program": ""
  },
  {
    "name": "teamportal",
    "rule": "body=\"TS_expiredurl\"",
    "program": ""
  },
  {
    "name": "VisualSVN",
    "rule": "title=\"VisualSVN Server\"",
    "program": ""
  },
  {
    "name": "Redmine",
    "rule": "body=\"Redmine\" && body=\"authenticity_token\"",
    "program": ""
  },
  {
    "name": "testlink",
    "rule": "body=\"testlink_library.js\"",
    "program": ""
  },
  {
    "name": "mantis",
    "rule": "body=\"browser_search_plugin.php?type=id\" || body=\"MantisBT Team\"",
    "program": ""
  },
  {
    "name": "Mercurial",
    "rule": "title=\"Mercurial repositories index\"",
    "program": ""
  },
  {
    "name": "activeCollab",
    "rule": "body=\"powered by activeCollab\" || body=\"<p id=\"powered_by\"><a href=\"http://www.activecollab.com/\"\"",
    "program": ""
  },
  {
    "name": "Collabtive",
    "rule": "title=\"Login @ Collabtive\"",
    "program": ""
  },
  {
    "name": "CGI:IRC",
    "rule": "title=\"CGI:IRC Login\" || body=\"<!-- This is part of CGI:IRC\" || body=\"<small id=\"ietest\"><a href=\"http://cgiirc.org/\"",
    "program": ""
  },
  {
    "name": "DotA-OpenStats",
    "rule": "body=\"content=\"dota OpenStats\" || body=\"content=\"openstats.iz.rs\"",
    "program": ""
  },
  {
    "name": "eLitius",
    "rule": "body=\"content=\"eLitius\"",
    "program": ""
  },
  {
    "name": "gCards",
    "rule": "body=\"<a href=\"http://www.gregphoto.net/gcards/index.php\"",
    "program": ""
  },
  {
    "name": "GpsGate-Server",
    "rule": "title=\"GpsGate Server - \"",
    "program": ""
  },
  {
    "name": "iScripts-ReserveLogic",
    "rule": "body=\"Powered by <a href=\"http://www.iscripts.com/reservelogic/\"",
    "program": ""
  },
  {
    "name": "jobberBase",
    "rule": "body=\"powered by\" && body=\"http://www.jobberbase.com\" || body=\"Jobber.PerformSearch\" || body=\"content=\"Jobberbase\"",
    "program": ""
  },
  {
    "name": "LuManager",
    "rule": "title=\"LuManager\"",
    "program": ""
  },
  {
    "name": "主机宝",
    "rule": "body=\"您访问的是主机宝服务器默认页\"",
    "program": ""
  },
  {
    "name": "wdcp管理系统",
    "rule": "title=\"wdcp服务器\" || title=\"lanmp_wdcp 安装成功\"",
    "program": ""
  },
  {
    "name": "LANMP一键安装包",
    "rule": "title=\"LANMP一键安装包\"",
    "program": ""
  },
  {
    "name": "UPUPW",
    "rule": "title=\"UPUPW环境集成包\"",
    "program": ""
  },
  {
    "name": "wamp",
    "rule": "title=\"WAMPSERVER\"",
    "program": ""
  },
  {
    "name": "easypanel",
    "rule": "body=\"/vhost/view/default/style/login.css\"",
    "program": ""
  },
  {
    "name": "awstats_admin",
    "rule": "body=\"generator\" content=\"AWStats\" || body=\"<frame name=\"mainleft\" src=\"awstats.pl?config=\"",
    "program": ""
  },
  {
    "name": "awstats",
    "rule": "body=\"awstats.pl?config=\"",
    "program": ""
  },
  {
    "name": "moosefs",
    "rule": "body=\"mfs.cgi\" || body=\"under-goal files\"",
    "program": ""
  },
  {
    "name": "护卫神主机管理",
    "rule": "title=\"护卫神·主机管理系统\"",
    "program": ""
  },
  {
    "name": "bacula-web",
    "rule": "title=\"Webacula\" || title=\"Bacula Web\" || title=\"Bacula-Web\" || title=\"bacula-web\"",
    "program": ""
  },
  {
    "name": "Webmin",
    "rule": "title=\"Login to Webmin\" || body=\"Webmin server on\"",
    "program": ""
  },
  {
    "name": "Synology_DiskStation",
    "rule": "title=\"Synology DiskStation\" || body=\"SYNO.SDS.Session\"",
    "program": ""
  },
  {
    "name": "Puppet_Node_Manager",
    "rule": "title=\"Puppet Node Manager\"",
    "program": ""
  },
  {
    "name": "wdcp",
    "rule": "title=\"wdcp服务器\"",
    "program": ""
  },
  {
    "name": "Citrix-XenServer",
    "rule": "body=\"Citrix Systems, Inc. XenServer\" || body=\"<a href=\"XenCenterSetup.exe\">XenCenter installer</a>\"",
    "program": ""
  },
  {
    "name": "DSpace",
    "rule": "body=\"content=\"DSpace\" || body=\"<a href=\"http://www.dspace.org\">DSpace Software\"",
    "program": ""
  },
  {
    "name": "dwr",
    "rule": "body=\"/dwr/engine.js\"",
    "program": ""
  },
  {
    "name": "eXtplorer",
    "rule": "title=\"Login - eXtplorer\"",
    "program": ""
  },
  {
    "name": "File-Upload-Manager",
    "rule": "title=\"File Upload Manager\" || body=\"<IMG SRC=\"/images/header.jpg\" ALT=\"File Upload Manager\">\"",
    "program": ""
  },
  {
    "name": "FileNice",
    "rule": "body=\"content=\"the fantabulous mechanical eviltwin code machine\" || body=\"fileNice/fileNice.js\"",
    "program": ""
  },
  {
    "name": "Glossword",
    "rule": "body=\"content=\"Glossword\"",
    "program": ""
  },
  {
    "name": "IBM-BladeCenter",
    "rule": "body=\"/shared/ibmbch.png\" || body=\"/shared/ibmbcs.png\" || body=\"alt=\"IBM BladeCenter\"",
    "program": ""
  },
  {
    "name": "iLO",
    "rule": "body=\"href=\"http://www.hp.com/go/ilo\" || title=\"HP Integrated Lights-Out\"",
    "program": ""
  },
  {
    "name": "Isolsoft-Support-Center",
    "rule": "body=\"Powered by: Support Center\"",
    "program": ""
  },
  {
    "name": "ISPConfig",
    "rule": "body=\"powered by <a HREF=\"http://www.ispconfig.org\"",
    "program": ""
  },
  {
    "name": "Kleeja",
    "rule": "body=\"Powered by Kleeja\"",
    "program": ""
  },
  {
    "name": "Kloxo-Single-Server",
    "rule": "body=\"src=\"/img/hypervm-logo.gif\" || body=\"/htmllib/js/preop.js\" || title=\"HyperVM\"",
    "program": ""
  },
  {
    "name": "易瑞授权访问系统",
    "rule": "body=\"/authjsp/login.jsp\" || body=\"FE0174BB-F093-42AF-AB20-7EC621D10488\"",
    "program": ""
  },
  {
    "name": "MVB2000",
    "rule": "title=\"MVB2000\" || body=\"The Magic Voice Box\"",
    "program": ""
  },
  {
    "name": "NetShare_VPN",
    "rule": "title=\"NetShare\" && title=\"VPN\"",
    "program": ""
  },
  {
    "name": "pmway_E4_crm",
    "rule": "title=\"E4\" && title=\"CRM\"",
    "program": ""
  },
  {
    "name": "srun3000计费认证系统",
    "rule": "title=\"srun3000\"",
    "program": ""
  },
  {
    "name": "Dolibarr",
    "rule": "body=\"Dolibarr Development Team\"",
    "program": ""
  },
  {
    "name": "Parallels Plesk Panel",
    "rule": "body=\"Parallels IP Holdings GmbH\"",
    "program": ""
  },
  {
    "name": "EasyTrace(botwave)",
    "rule": "title=\"EasyTrace\" && body=\"login_page\"",
    "program": ""
  },
  {
    "name": "管理易",
    "rule": "body=\"管理易\" && body=\"minierp\"",
    "program": ""
  },
  {
    "name": "亿赛通DLP",
    "rule": "body=\"CDGServer3\"",
    "program": ""
  },
  {
    "name": "huawei_auth_server",
    "rule": "body=\"75718C9A-F029-11d1-A1AC-00C04FB6C223\"",
    "program": ""
  },
  {
    "name": "瑞友天翼_应用虚拟化系统 ",
    "rule": "title=\"瑞友天翼－应用虚拟化系统\"",
    "program": ""
  },
  {
    "name": "360企业版",
    "rule": "body=\"360EntInst\"",
    "program": ""
  },
  {
    "name": "用友erp-nc",
    "rule": "body=\"/nc/servlet/nc.ui.iufo.login.Index\" || title=\"用友新世纪\"",
    "program": ""
  },
  {
    "name": "Array_Networks_VPN",
    "rule": "body=\"an_util.js\"",
    "program": ""
  },
  {
    "name": "juniper_vpn",
    "rule": "body=\"welcome.cgi?p=logo\"",
    "program": ""
  },
  {
    "name": "CEMIS",
    "rule": "body=\"<div id=\"demo\" style=\"overflow:hidden\" && title=\"综合项目管理系统登录\"",
    "program": ""
  },
  {
    "name": "zenoss",
    "rule": "body=\"/zport/dmd/\"",
    "program": ""
  },
  {
    "name": "OpenMas",
    "rule": "title=\"OpenMas\" || body=\"loginHead\"><link href=\"App_Themes\"",
    "program": ""
  },
  {
    "name": "Ultra_Electronics",
    "rule": "body=\"/preauth/login.cgi\" || body=\"/preauth/style.css\"",
    "program": ""
  },
  {
    "name": "NOALYSS",
    "rule": "title=\"NOALYSS\"",
    "program": ""
  },
  {
    "name": "ALCASAR",
    "rule": "body=\"valoriserDiv5\"",
    "program": ""
  },
  {
    "name": "orocrm",
    "rule": "body=\"/bundles/oroui/\"",
    "program": ""
  },
  {
    "name": "Adiscon_LogAnalyzer",
    "rule": "title=\"Adiscon LogAnalyzer\" || (body=\"Adiscon LogAnalyzer\" && body=\"Adiscon GmbH\")",
    "program": ""
  },
  {
    "name": "Munin",
    "rule": "body=\"Auto-generated by Munin\" || body=\"munin-month.html\"",
    "program": ""
  },
  {
    "name": "MRTG",
    "rule": "body=\"Command line is easier to read using \"View Page Properties\" of your browser\" || title=\"MRTG Index Page\" || body=\"commandline was: indexmaker\"",
    "program": ""
  },
  {
    "name": "元年财务软件",
    "rule": "body=\"yuannian.css\" || body=\"/image/logo/yuannian.gif\"",
    "program": ""
  },
  {
    "name": "UFIDA_NC",
    "rule": "(body=\"UFIDA\" && body=\"logo/images/\") || body=\"logo/images/ufida_nc.png\"",
    "program": ""
  },
  {
    "name": "Webmin",
    "rule": "title=\"Login to Webmin\" || body=\"Webmin server on\"",
    "program": ""
  },
  {
    "name": "锐捷应用控制引擎",
    "rule": "body=\"window.open(\"/login.do\",\"airWin\" || title=\"锐捷应用控制引擎\"",
    "program": ""
  },
  {
    "name": "Storm",
    "rule": "title=\"Storm UI\" || body=\"stormtimestr\"",
    "program": ""
  },
  {
    "name": "Centreon",
    "rule": "body=\"Generator\" content=\"Centreon - Copyright\" || title=\"Centreon - IT & Network Monitoring\"",
    "program": ""
  },
  {
    "name": "FortiGuard",
    "rule": "body=\"FortiGuard Web Filtering\" || title=\"Web Filter Block Override\" || body=\"/XX/YY/ZZ/CI/MGPGHGPGPFGHCDPFGGOGFGEH\"",
    "program": ""
  },
  {
    "name": "PineApp",
    "rule": "title=\"PineApp WebAccess - Login\" || body=\"/admin/css/images/pineapp.ico\"",
    "program": ""
  },
  {
    "name": "CDR-Stats",
    "rule": "title=\"CDR-Stats | Customer Interface\" || body=\"/static/cdr-stats/js/jquery\"",
    "program": ""
  },
  {
    "name": "GenieATM",
    "rule": "title=\"GenieATM\" || body=\"Copyright© Genie Networks Ltd.\" || body=\"defect 3531\"",
    "program": ""
  },
  {
    "name": "Spark_Worker",
    "rule": "title=\"Spark Worker at\"",
    "program": ""
  },
  {
    "name": "Spark_Master",
    "rule": "title=\"Spark Master at\"",
    "program": ""
  },
  {
    "name": "Kibana",
    "rule": "title=\"Kibana\" || body=\"kbnVersion\"",
    "program": ""
  },
  {
    "name": "UcSTAR",
    "rule": "title=\"UcSTAR 管理控制台\"",
    "program": ""
  },
  {
    "name": "i@Report",
    "rule": "body=\"ESENSOFT_IREPORT_SERVER\" || body=\"com.sanlink.server.Login\" || body=\"ireportclient\" || body=\"css/ireport.css\"",
    "program": ""
  },
  {
    "name": "帕拉迪统一安全管理和综合审计系统",
    "rule": "body=\"module/image/pldsec.css\"",
    "program": ""
  },
  {
    "name": "openEAP",
    "rule": "title=\"openEAP_统一登录门户\"",
    "program": ""
  },
  {
    "name": "Dorado",
    "rule": "title=\"Dorado Login Page\"",
    "program": ""
  },
  {
    "name": "金龙卡金融化一卡通网站查询子系统",
    "rule": "title=\"金龙卡金融化一卡通网站查询子系统\" || body=\"location.href=\"homeLogin.action\"",
    "program": ""
  },
  {
    "name": "一采通",
    "rule": "body=\"/custom/GroupNewsList.aspx?GroupId=\"",
    "program": ""
  },
  {
    "name": "埃森诺网络服务质量检测系统",
    "rule": "title=\"埃森诺网络服务质量检测系统 \"",
    "program": ""
  },
  {
    "name": "惠尔顿上网行为管理系统",
    "rule": "body=\"updateLoginPswd.php\" && body=\"PassroedEle\"",
    "program": ""
  },
  {
    "name": "ACSNO网络探针",
    "rule": "title=\"探针管理与测试系统-登录界面\"",
    "program": ""
  },
  {
    "name": "绿盟下一代防火墙",
    "rule": "title=\"NSFOCUS NF\"",
    "program": ""
  },
  {
    "name": "用友U8",
    "rule": "body=\"getFirstU8Accid\"",
    "program": ""
  },
  {
    "name": "华为（HUAWEI）安全设备",
    "rule": "body=\"sweb-lib/resource/\"",
    "program": ""
  },
  {
    "name": "网神防火墙",
    "rule": "title=\"secgate 3600\" || body=\"css/lsec/login.css\"",
    "program": ""
  },
  {
    "name": "cisco UCM",
    "rule": "body=\"/ccmadmin/\" || title=\"Cisco Unified\"",
    "program": ""
  },
  {
    "name": "panabit智能网关",
    "rule": "title=\"panabit\"",
    "program": ""
  },
  {
    "name": "久其通用财表系统",
    "rule": "body=\"<nobr>北京久其软件股份有限公司\" || body=\"/netrep/intf\" || body=\"/netrep/message2/\"",
    "program": ""
  },
  {
    "name": "soeasy网站集群系统",
    "rule": "body=\"EGSS_User\" || title=\"SoEasy网站集群\"",
    "program": ""
  },
  {
    "name": "畅捷通",
    "rule": "title=\"畅捷通\"",
    "program": ""
  },
  {
    "name": "科来RAS",
    "rule": "title=\"科来网络回溯\" || body=\"科来软件 版权所有\" || body=\"i18ninit.min.js\"",
    "program": ""
  },
  {
    "name": "科迈RAS系统",
    "rule": "title=\"科迈RAS\" || body=\"type=\"application/npRas\" || body=\"远程技术支持请求：<a href=\"http://www.comexe.cn\"",
    "program": ""
  },
  {
    "name": "单点CRM系统",
    "rule": "body=\"URL=general/ERP/LOGIN/\" || body=\"content=\"单点CRM系统\" ||title=\"客户关系管理-CRM\"",
    "program": ""
  },
  {
    "name": "中国期刊先知网",
    "rule": "body=\"本系统由<span class=\"STYLE1\" ><a href=\"http://www.firstknow.cn\" || body=\"<img src=\"images/logoknow.png\"\"",
    "program": ""
  },
  {
    "name": "loyaa信息自动采编系统",
    "rule": "body=\"/Loyaa/common.lib.js\"",
    "program": ""
  },
  {
    "name": "浪潮政务系统",
    "rule": "body=\"OnlineQuery/QueryList.aspx\" || title=\"浪潮政务\" || body=\"LangChao.ECGAP.OutPortal\"",
    "program": ""
  },
  {
    "name": "悟空CRM",
    "rule": "title=\"悟空CRM\" || body=\"/Public/js/5kcrm.js\"",
    "program": ""
  },
  {
    "name": "用友ufida",
    "rule": "body=\"/System/Login/Login.asp?AppID=\"",
    "program": ""
  },
  {
    "name": "金蝶EAS",
    "rule": "body=\"easSessionId\"",
    "program": ""
  },
  {
    "name": "金蝶政务GSiS",
    "rule": "body=\"/kdgs/script/kdgs.js\"",
    "program": ""
  },
  {
    "name": "网御上网行为管理系统",
    "rule": "title=\"Leadsec ACM\"",
    "program": ""
  },
  {
    "name": "ZKAccess 门禁管理系统",
    "rule": "body=\"/logoZKAccess_zh-cn.jpg\"",
    "program": ""
  },
  {
    "name": "福富安全基线管理",
    "rule": "body=\"align=\"center\">福富软件\"",
    "program": ""
  },
  {
    "name": "中控智慧时间安全管理平台",
    "rule": "title=\"ZKECO 时间&安全管理平台\"",
    "program": ""
  },
  {
    "name": "天融信安全管理系统",
    "rule": "title=\"天融信安全管理\"",
    "program": ""
  },
  {
    "name": "锐捷 RG-DBS",
    "rule": "body=\"/css/impl-security.css\" || body=\"/dbaudit/authenticate\"",
    "program": ""
  },
  {
    "name": "深信服防火墙类产品",
    "rule": "body=\"SANGFOR FW\"",
    "program": ""
  },
  {
    "name": "天融信网络卫士过滤网关",
    "rule": "title=\"天融信网络卫士过滤网关\"",
    "program": ""
  },
  {
    "name": "天融信网站监测与自动修复系统",
    "rule": "title=\"天融信网站监测与自动修复系统\"",
    "program": ""
  },
  {
    "name": "天融信 TopAD",
    "rule": "title=\"天融信 TopAD\"",
    "program": ""
  },
  {
    "name": "Apache-Forrest",
    "rule": "body=\"content=\"Apache Forrest\" || body=\"name=\"Forrest\"",
    "program": ""
  },
  {
    "name": "Advantech-WebAccess",
    "rule": "body=\"/bw_templete1.dwt\" || body=\"/broadweb/WebAccessClientSetup.exe\" || body=\"/broadWeb/bwuconfig.asp\"",
    "program": ""
  },
  {
    "name": "URP教务系统",
    "rule": "title=\"URP 综合教务系统\" || body=\"北京清元优软科技有限公司\"",
    "program": ""
  },
  {
    "name": "H3C公司产品",
    "rule": "body=\"service@h3c.com\" || (body=\"Copyright\" && body=\"H3C Corporation\") || body=\"icg_helpScript.js\"",
    "program": ""
  },
  {
    "name": "Huawei HG520 ADSL2+ Router",
    "rule": "title=\"Huawei HG520\"",
    "program": ""
  },
  {
    "name": "Huawei B683V",
    "rule": "title=\"Huawei B683V\"",
    "program": ""
  },
  {
    "name": "HUAWEI ESPACE 7910",
    "rule": "title=\"HUAWEI ESPACE 7910\"",
    "program": ""
  },
  {
    "name": "Huawei HG630",
    "rule": "title=\"Huawei HG630\"",
    "program": ""
  },
  {
    "name": "Huawei B683",
    "rule": "title=\"Huawei B683\"",
    "program": ""
  },
  {
    "name": "华为 MCU",
    "rule": "body=\"McuR5-min.js\" || body=\"MCUType.js\" || title=\"huawei MCU\"",
    "program": ""
  },
  {
    "name": "HUAWEI Inner Web",
    "rule": "title=\"HUAWEI Inner Web\" || body=\"hidden_frame.html\"",
    "program": ""
  },
  {
    "name": "HUAWEI CSP",
    "rule": "title=\"HUAWEI CSP\"",
    "program": ""
  },
  {
    "name": "华为 NetOpen",
    "rule": "body=\"/netopen/theme/css/inFrame.css\" || title=\"Huawei NetOpen System\"",
    "program": ""
  },
  {
    "name": "校园卡管理系统",
    "rule": "body=\"Harbin synjones electronic\" || body=\"document.FormPostds.action=\"xxsearch.action\" || body=\"/shouyeziti.css\"",
    "program": ""
  },
  {
    "name": "OBSERVA telcom",
    "rule": "title=\"OBSERVA\"",
    "program": ""
  },
  {
    "name": "汉柏安全网关",
    "rule": "title=\"OPZOON - \"",
    "program": ""
  },
  {
    "name": "b2evolution",
    "rule": "body=\"/powered-by-b2evolution-150t.gif\" || body=\"Powered by b2evolution\" || body=\"content=\"b2evolution\"",
    "program": ""
  },
  {
    "name": "AvantFAX",
    "rule": "body=\"content=\"Web 2.0 HylaFAX\" || body=\"images/avantfax-big.png\"",
    "program": ""
  },
  {
    "name": "Aurion",
    "rule": "body=\"<!-- Aurion Teal will be used as the login-time default\" || body=\"/aurion.js\"",
    "program": ""
  },
  {
    "name": "Cisco-IP-Phone",
    "rule": "body=\"Cisco Unified Wireless IP Phone\"",
    "program": ""
  },
  {
    "name": "Cisco-VPN-3000-Concentrator",
    "rule": "title=\"Cisco Systems, Inc. VPN 3000 Concentrator\"",
    "program": ""
  },
  {
    "name": "BugTracker.NET",
    "rule": "body=\"href=\"btnet.css\" || body=\"valign=middle><a href=http://ifdefined.com/bugtrackernet.html>\" || body=\"<div class=logo>BugTracker.NET\"",
    "program": ""
  },
  {
    "name": "BugFree",
    "rule": "body=\"id=\"logo\" alt=BugFree\" || body=\"class=\"loginBgImage\" alt=\"BugFree\" ||  title=\"BugFree\" || body=\"name=\"BugUserPWD\"",
    "program": ""
  },
  {
    "name": "cPassMan",
    "rule": "title=\"Collaborative Passwords Manager\"",
    "program": ""
  },
  {
    "name": "splunk",
    "rule": "body=\"Splunk.util.normalizeBoolean\"",
    "program": ""
  },
  {
    "name": "DrugPak",
    "rule": "body=\"Powered by DrugPak\" || body=\"/dplimg/DPSTYLE.CSS\"",
    "program": ""
  },
  {
    "name": "DMXReady-Portfolio-Manager",
    "rule": "body=\"/css/PortfolioManager/styles_display_page.css\" || body=\"rememberme_portfoliomanager\"",
    "program": ""
  },
  {
    "name": "eGroupWare",
    "rule": "body=\"content=\"eGroupWare\"",
    "program": ""
  },
  {
    "name": "eSyndiCat",
    "rule": "body=\"content=\"eSyndiCat\"",
    "program": ""
  },
  {
    "name": "Epiware",
    "rule": "body=\"Epiware - Project and Document Management\"",
    "program": ""
  },
  {
    "name": "eMeeting-Online-Dating-Software",
    "rule": "body=\"eMeeting Dating Software\" || body=\"/_eMeetingGlobals.js\"",
    "program": ""
  },
  {
    "name": "FreeNAS",
    "rule": "title=\"Welcome to FreeNAS\" || body=\"/images/ui/freenas-logo.png\"",
    "program": ""
  },
  {
    "name": "FestOS",
    "rule": "title=\"FestOS\" || body=\"css/festos.css\"",
    "program": ""
  },
  {
    "name": "eTicket",
    "rule": "body=\"Powered by eTicket\" || body=\"<a href=\"http://www.eticketsupport.com\" target=\"_blank\">\" || body=\"/eticket/eticket.css\"",
    "program": ""
  },
  {
    "name": "FileVista",
    "rule": "body=\"Welcome to FileVista\" || body=\"<a href=\"http://www.gleamtech.com/products/filevista/web-file-manager\"",
    "program": ""
  },
  {
    "name": "Google-Talk-Chatback",
    "rule": "body=\"www.google.com/talk/service/\"",
    "program": ""
  },
  {
    "name": "Flyspray",
    "rule": "body=\"Powered by Flyspray\"",
    "program": ""
  },
  {
    "name": "HP-StorageWorks-Library",
    "rule": "title=\"HP StorageWorks\"",
    "program": ""
  },
  {
    "name": "HostBill",
    "rule": "body=\"Powered by <a href=\"http://hostbillapp.com\" || body=\"<strong>HostBill\"",
    "program": ""
  },
  {
    "name": "IBM-Cognos",
    "rule": "body=\"/cgi-bin/cognos.cgi\" || body=\"Cognos &#26159; International Business Machines Corp\"",
    "program": ""
  },
  {
    "name": "iTop",
    "rule": "title=\"iTop Login\" || body=\"href=\"http://www.combodo.com/itop\"",
    "program": ""
  },
  {
    "name": "Kayako-SupportSuite",
    "rule": "body=\"Powered By Kayako eSupport\" || body=\"Help Desk Software By Kayako eSupport\"",
    "program": ""
  },
  {
    "name": "JXT-Consulting",
    "rule": "body=\"id=\"jxt-popup-wrapper\" || body=\"Powered by JXT Consulting\"",
    "program": ""
  },
  {
    "name": "Fastly cdn",
    "rule": "body=\"fastcdn.org\"",
    "program": ""
  },
  {
    "name": "JBoss_AS",
    "rule": "body=\"Manage this JBoss AS Instance\"",
    "program": ""
  },
  {
    "name": "oracle_applicaton_server",
    "rule": "body=\"OraLightHeaderSub\"",
    "program": ""
  },
  {
    "name": "Avaya-Aura-Utility-Server",
    "rule": "body=\"vmsTitle\">Avaya Aura&#8482;&nbsp;Utility Server\" || body=\"/webhelp/Base/Utility_toc.htm\"",
    "program": ""
  },
  {
    "name": "DnP Firewall",
    "rule": "body=\"Powered by DnP Firewall\" || body=\"dnp_firewall_redirect\"",
    "program": ""
  },
  {
    "name": "PaloAlto_Firewall",
    "rule": "body=\"Access to the web page you were trying to visit has been blocked in accordance with company policy\"",
    "program": ""
  },
  {
    "name": "梭子鱼防火墙",
    "rule": "body=\"http://www.barracudanetworks.com?a=bsf_product\" class=\"transbutton\" && body=\"/cgi-mod/header_logo.cgi\"",
    "program": ""
  },
  {
    "name": "IndusGuard_WAF",
    "rule": "title=\"IndusGuard WAF\" && body = \"wafportal/wafportal.nocache.js\"",
    "program": ""
  },
  {
    "name": "网御WAF",
    "rule": "body = \"<div id=\"divLogin\">\" && title=\"网御WAF\"",
    "program": ""
  },
  {
    "name": "NSFOCUS_WAF",
    "rule": "title=\"WAF NSFOCUS\" && body = \"/images/logo/nsfocus.png\"",
    "program": ""
  },
  {
    "name": "斐讯Fortress",
    "rule": "title=\"斐讯Fortress防火墙\" && body=\"<meta name=\"author\" content=\"上海斐讯数据通信技术有限公司\" />\"",
    "program": ""
  },
  {
    "name": "Sophos Web Appliance",
    "rule": "title=\"Sophos Web Appliance\" || body=\"resources/images/sophos_web.ico\" || body=\"url(resources/images/en/login_swa.jpg)\"",
    "program": ""
  },
  {
    "name": "Barracuda-Spam-Firewall",
    "rule": "title=\"Barracuda Spam & Virus Firewall: Welcome\" || body=\"/barracuda.css\" || body=\"http://www.barracudanetworks.com?a=bsf_product\"",
    "program": ""
  },
  {
    "name": "DnP-Firewall",
    "rule": "title=\"Forum Gateway - Powered by DnP Firewall\" || body=\"name=\"dnp_firewall_redirect\" ||  body=\"<form name=dnp_firewall\"",
    "program": ""
  },
  {
    "name": "H3C-SecBlade-FireWall",
    "rule": "body=\"js/MulPlatAPI.js\"",
    "program": ""
  },
  {
    "name": "锐捷NBR路由器",
    "rule": "body=\"free_nbr_login_form.png\"",
    "program": ""
  },
  {
    "name": "mikrotik",
    "rule": "title=\"RouterOS\" && body=\"mikrotik\"",
    "program": ""
  },
  {
    "name": "h3c路由器",
    "rule": "title=\"Web user login\" && body=\"nLanguageSupported\"",
    "program": ""
  },
  {
    "name": "jcg无线路由器",
    "rule": "title=\"Wireless Router\" && body=\"http://www.jcgcn.com\"",
    "program": ""
  },
  {
    "name": "Comcast_Business_Gateway",
    "rule": "body=\"Comcast Business Gateway\"",
    "program": ""
  },
  {
    "name": "AirTiesRouter",
    "rule": "title=\"Airties\"",
    "program": ""
  },
  {
    "name": "3COM NBX",
    "rule": "title=\"NBX NetSet\" || body=\"splashTitleIPTelephony\"",
    "program": ""
  },
  {
    "name": "H3C ER2100n",
    "rule": "title=\"ER2100n系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ICG 1000",
    "rule": "title=\"ICG 1000系统管理\"",
    "program": ""
  },
  {
    "name": "H3C AM8000",
    "rule": "title=\"AM8000\"",
    "program": ""
  },
  {
    "name": "H3C ER8300G2",
    "rule": "title=\"ER8300G2系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER3108GW",
    "rule": "title=\"ER3108GW系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER6300",
    "rule": "title=\"ER6300系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ICG1000",
    "rule": "title=\"ICG1000系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER3260G2",
    "rule": "title=\"ER3260G2系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER3108G",
    "rule": "title=\"ER3108G系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER2100",
    "rule": "title=\"ER2100系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER3200",
    "rule": "title=\"ER3200系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER8300",
    "rule": "title=\"ER8300系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER5200G2",
    "rule": "title=\"ER5200G2系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER6300G2",
    "rule": "title=\"ER6300G2系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER2100V2",
    "rule": "title=\"ER2100V2系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER3260",
    "rule": "title=\"ER3260系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER3100",
    "rule": "title=\"ER3100系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER5100",
    "rule": "title=\"ER5100系统管理\"",
    "program": ""
  },
  {
    "name": "H3C ER5200",
    "rule": "title=\"ER5200系统管理\"",
    "program": ""
  },
  {
    "name": "UBNT_UniFi系列路由",
    "rule": "title=\"UniFi\" && body=\"<div class=\"appGlobalHeader\">\"",
    "program": ""
  },
  {
    "name": "AnyGate",
    "rule": "title=\"AnyGate\" || body=\"/anygate.php\"",
    "program": ""
  },
  {
    "name": "Astaro-Security-Gateway",
    "rule": "body=\"wfe/asg/js/app_selector.js?t=\" || body=\"/doc/astaro-license.txt\" || body=\"/js/_variables_from_backend.js?t=\"",
    "program": ""
  },
  {
    "name": "Aruba-Device",
    "rule": "body=\"/images/arubalogo.gif\" || (body=\"Copyright\" && body=\"Aruba Networks\")",
    "program": ""
  },
  {
    "name": "ARRIS-Touchstone-Router",
    "rule": "(body=\"Copyright\" && body=\"ARRIS Group\") || body=\"/arris_style.css\"",
    "program": ""
  },
  {
    "name": "AP-Router",
    "rule": "title=\"AP Router New Generation\"",
    "program": ""
  },
  {
    "name": "Belkin-Modem",
    "rule": "body=\"content=\"Belkin\"",
    "program": ""
  },
  {
    "name": "Dell OpenManage Switch Administrator",
    "rule": "title=\"Dell OpenManage Switch Administrator\"",
    "program": ""
  },
  {
    "name": "EDIMAX",
    "rule": "title=\"EDIMAX Technology\" || body=\"content=\"Edimax\"",
    "program": ""
  },
  {
    "name": "eBuilding-Network-Controller",
    "rule": "title=\"eBuilding Web\"",
    "program": ""
  },
  {
    "name": "ipTIME-Router",
    "rule": "title=\"networks - ipTIME\" || body=\"href=iptime.css\"",
    "program": ""
  },
  {
    "name": "I-O-DATA-Router",
    "rule": "title=\"I-O DATA Wireless Broadband Router\"",
    "program": ""
  },
  {
    "name": "phpshe",
    "rule": "body=\"Powered by phpshe\" || body=\"content=\"phpshe\"",
    "program": ""
  },
  {
    "name": "ThinkSAAS",
    "rule": "body=\"/app/home/skins/default/style.css\"",
    "program": ""
  },
  {
    "name": "e-tiller",
    "rule": "body=\"reader/view_abstract.aspx\"",
    "program": ""
  },
  {
    "name": "DouPHP",
    "rule": "body=\"Powered by DouPHP\" || (body=\"controlBase\" && body=\"indexLeft\" && body=\"recommendProduct\")",
    "program": ""
  },
  {
    "name": "twcms",
    "rule": "body=\"/twcms/theme/\" && body=\"/css/global.css\"",
    "program": ""
  },
  {
    "name": "SiteServer",
    "rule": "(body=\"Powered by\" && body=\"http://www.siteserver.cn\" && body=\"SiteServer CMS\") || title=\"Powered by SiteServer CMS\" || body=\"T_系统首页模板\" || (body=\"siteserver\" && body=\"sitefiles\")",
    "program": ""
  },
  {
    "name": "Joomla",
    "rule": "body=\"content=\"Joomla\" || (body=\"/media/system/js/core.js\" && body=\"/media/system/js/mootools-core.js\")",
    "program": ""
  },
  {
    "name": "kesionCMS",
    "rule": "body=\"/ks_inc/common.js\" || body=\"publish by KesionCMS\"",
    "program": ""
  },
  {
    "name": "CMSTop",
    "rule": "body=\"/css/cmstop-common.css\" || body=\"/js/cmstop-common.js\" || body=\"cmstop-list-text.css\" || body=\"<a class=\"poweredby\" href=\"http://www.cmstop.com\"\"",
    "program": ""
  },
  {
    "name": "ESPCMS",
    "rule": "title=\"Powered by ESPCMS\" || body=\"Powered by ESPCMS\" || (body=\"infolist_fff\" && body=\"/templates/default/style/tempates_div.css\")",
    "program": ""
  },
  {
    "name": "74cms",
    "rule": "body=\"content=\"74cms.com\" || body=\"content=\"骑士CMS\" || body=\"Powered by <a href=\"http://www.74cms.com/\"\" || (body=\"/templates/default/css/common.css\" && body=\"selectjobscategory\")",
    "program": ""
  },
  {
    "name": "Foosun",
    "rule": "body=\"Created by DotNetCMS\" || body=\"For Foosun\" || body=\"Powered by www.Foosun.net,Products:Foosun Content Manage system\"",
    "program": ""
  },
  {
    "name": "PhpCMS",
    "rule": "(body=\"Powered by\" && body=\"http://www.phpcms.cn\") || body=\"content=\"Phpcms\" || body=\"Powered by Phpcms\" || body=\"data/config.js\" || body=\"/index.php?m=content&c=index&a=lists\" || body=\"/index.php?m=content&amp;c=index&amp;a=lists\"",
    "program": ""
  },
  {
    "name": "DedeCMS",
    "rule": "body=\"Power by DedeCms\" || (body=\"Powered by\" && body=\"http://www.dedecms.com/\" && body=\"DedeCMS\") || body=\"/templets/default/style/dedecms.css\" || title=\"Powered by DedeCms\" ",
    "program": ""
  },
  {
    "name": "ASPCMS",
    "rule": "title=\"Powered by ASPCMS\" || body=\"content=\"ASPCMS\" || body=\"/inc/AspCms_AdvJs.asp\"",
    "program": ""
  },
  {
    "name": "MetInfo",
    "rule": "title=\"Powered by MetInfo\" || body=\"content=\"MetInfo\" || body=\"powered_by_metinfo\" || body=\"/images/css/metinfo.css\"",
    "program": ""
  },
  {
    "name": "Npoint",
    "rule": "title=\"Powered by Npoint\"",
    "program": ""
  },
  {
    "name": "捷点JCMS",
    "rule": "body=\"Publish By JCms2010\"",
    "program": ""
  },
  {
    "name": "帝国EmpireCMS",
    "rule": "title=\"Powered by EmpireCMS\"",
    "program": ""
  },
  {
    "name": "JEECMS",
    "rule": "title=\"Powered by JEECMS\" || (body=\"Powered by\" && body=\"http://www.jeecms.com\" && body=\"JEECMS\")",
    "program": ""
  },
  {
    "name": "IdeaCMS",
    "rule": "body=\"Powered By IdeaCMS\" || body=\"m_ctr32\"",
    "program": ""
  },
  {
    "name": "TCCMS",
    "rule": "title=\"Power By TCCMS\" || (body=\"index.php?ac=link_more\" && body=\"index.php?ac=news_list\")",
    "program": ""
  },
  {
    "name": "webplus",
    "rule": "body=\"webplus\" && body=\"高校网站群管理平台\"",
    "program": ""
  },
  {
    "name": "Dolibarr",
    "rule": "body=\"Dolibarr Development Team\"",
    "program": ""
  },
  {
    "name": "Telerik Sitefinity",
    "rule": "body=\"Telerik.Web.UI.WebResource.axd\" || body=\"content=\"Sitefinity\"",
    "program": ""
  },
  {
    "name": "PageAdmin",
    "rule": "body=\"content=\"PageAdmin CMS\"\" || body=\"/e/images/favicon.ico\"",
    "program": ""
  },
  {
    "name": "sdcms",
    "rule": "title=\"powered by sdcms\" || (body=\"var webroot=\" && body=\"/js/sdcms.js\")",
    "program": ""
  },
  {
    "name": "EnterCRM",
    "rule": "body=\"EnterCRM\"",
    "program": ""
  },
  {
    "name": "易普拉格科研管理系统",
    "rule": "body=\"lan12-jingbian-hong\" || body=\"科研管理系统，北京易普拉格科技\"",
    "program": ""
  },
  {
    "name": "苏亚星校园管理系统",
    "rule": "body=\"/ws2004/Public/\"",
    "program": ""
  },
  {
    "name": "trs_wcm",
    "rule": "body=\"/wcm/app/js\" || body=\"0;URL=/wcm\" || body=\"window.location.href = \"/wcm\";\" || (body=\"forum.trs.com.cn\" && body=\"wcm\") || body=\"/wcm\" target=\"_blank\">网站管理\" || body=\"/wcm\" target=\"_blank\">管理\"",
    "program": ""
  },
  {
    "name": "we7",
    "rule": "body=\"/Widgets/WidgetCollection/\"",
    "program": ""
  },
  {
    "name": "1024cms",
    "rule": "body=\"Powered by 1024 CMS\" || body=\"generator\" content=\"1024 CMS (c)\"",
    "program": ""
  },
  {
    "name": "360webfacil_360WebManager",
    "rule": "(body=\"publico/template/\" && body=\"zonapie\") || body=\"360WebManager Software\"",
    "program": ""
  },
  {
    "name": "6kbbs",
    "rule": "body=\"Powered by 6kbbs\" || body=\"generator\" content=\"6KBBS\"",
    "program": ""
  },
  {
    "name": "Acidcat_CMS",
    "rule": "body=\"Start Acidcat CMS footer information\" || body=\"Powered by Acidcat CMS\"",
    "program": ""
  },
  {
    "name": "bit-service",
    "rule": "body=\"bit-xxzs\" || body=\"xmlpzs/webissue.asp\"",
    "program": ""
  },
  {
    "name": "云因网上书店",
    "rule": "body=\"main/building.cfm\" || body=\"href=\"../css/newscomm.css\"",
    "program": ""
  },
  {
    "name": "MediaWiki",
    "rule": "body=\"generator\" content=\"MediaWiki\" || body=\"/wiki/images/6/64/Favicon.ico\" || body=\"Powered by MediaWiki\"",
    "program": ""
  },
  {
    "name": "Typecho",
    "rule": "body=\"generator\" content=\"Typecho\" || (body=\"强力驱动\" && body=\"Typecho\")",
    "program": ""
  },
  {
    "name": "2z project",
    "rule": "body=\"Generator\" content=\"2z project\"",
    "program": ""
  },
  {
    "name": "phpDocumentor",
    "rule": "body=\"Generated by phpDocumentor\"",
    "program": ""
  },
  {
    "name": "微门户",
    "rule": "body=\"/tpl/Home/weimeng/common/css/\"",
    "program": ""
  },
  {
    "name": "webEdition",
    "rule": "body=\"generator\" content=\"webEdition\"",
    "program": ""
  },
  {
    "name": "orocrm",
    "rule": "body=\"/bundles/oroui/\"",
    "program": ""
  },
  {
    "name": "创星伟业校园网群",
    "rule": "body=\"javascripts/float.js\" && body=\"vcxvcxv\"",
    "program": ""
  },
  {
    "name": "BoyowCMS",
    "rule": "body=\"publish by BoyowCMS\"",
    "program": ""
  },
  {
    "name": "正方教务管理系统",
    "rule": "body=\"style/base/jw.css\"",
    "program": ""
  },
  {
    "name": "UFIDA_NC",
    "rule": "(body=\"UFIDA\" && body=\"logo/images/\") || body=\"logo/images/ufida_nc.png\"",
    "program": ""
  },
  {
    "name": "phpweb",
    "rule": "body=\"PDV_PAGENAME\"",
    "program": ""
  },
  {
    "name": "地平线CMS",
    "rule": "body=\"labelOppInforStyle\" || title=\"Powered by deep soon\" || (body=\"search_result.aspx\" && body=\"frmsearch\")",
    "program": ""
  },
  {
    "name": "HIMS酒店云计算服务",
    "rule": "(body=\"GB_ROOT_DIR\" && body=\"maincontent.css\") || body=\"HIMS酒店云计算服务\"",
    "program": ""
  },
  {
    "name": "Tipask",
    "rule": "body=\"content=\"tipask\"",
    "program": ""
  },
  {
    "name": "北创图书检索系统",
    "rule": "body=\"opac_two\"",
    "program": ""
  },
  {
    "name": "微普外卖点餐系统",
    "rule": "body=\"Author\" content=\"微普外卖点餐系统\" || body=\"Powered By 点餐系统\" || body=\"userfiles/shoppics/\"",
    "program": ""
  },
  {
    "name": "逐浪zoomla",
    "rule": "body=\"script src=\"http://code.zoomla.cn/\" || (body=\"NodePage.aspx\" && body=\"Item\") || body=\"/style/images/win8_symbol_140x140.png\"",
    "program": ""
  },
  {
    "name": "北京清科锐华CEMIS",
    "rule": "body=\"/theme/2009/image\" && body=\"login.asp\"",
    "program": ""
  },
  {
    "name": "asp168欧虎",
    "rule": "body=\"upload/moban/images/style.css\" || body=\"default.php?mod=article&do=detail&tid\"",
    "program": ""
  },
  {
    "name": "擎天电子政务",
    "rule": "body=\"App_Themes/1/Style.css\" || body=\"window.location = \"homepages/index.aspx\" || body=\"homepages/content_page.aspx\"",
    "program": ""
  },
  {
    "name": "北京阳光环球建站系统",
    "rule": "body=\"bigSortProduct.asp?bigid\"",
    "program": ""
  },
  {
    "name": "MaticsoftSNS_动软分享社区",
    "rule": "body=\"MaticsoftSNS\" || (body=\"maticsoft\" && body=\"/Areas/SNS/\")",
    "program": ""
  },
  {
    "name": "FineCMS",
    "rule": "body=\"Powered by FineCMS\" || body=\"dayrui@gmail.com\" || body=\"Copyright\" content=\"FineCMS\"",
    "program": ""
  },
  {
    "name": "Diferior",
    "rule": "body=\"Powered by Diferior\"",
    "program": ""
  },
  {
    "name": "国家数字化学习资源中心系统",
    "rule": "title=\"页面加载中,请稍候\" && body=\"FrontEnd\"",
    "program": ""
  },
  {
    "name": "某通用型政府cms",
    "rule": "body=\"/deptWebsiteAction.do\"",
    "program": ""
  },
  {
    "name": "万户网络",
    "rule": "body=\"css/css_whir.css\"",
    "program": ""
  },
  {
    "name": "rcms",
    "rule": "body=\"/r/cms/www/\" && body=\"jhtml\"",
    "program": ""
  },
  {
    "name": "全国烟草系统",
    "rule": "body=\"ycportal/webpublish\"",
    "program": ""
  },
  {
    "name": "O2OCMS",
    "rule": "body=\"/index.php/clasify/showone/gtitle/\"",
    "program": ""
  },
  {
    "name": "一采通",
    "rule": "body=\"/custom/GroupNewsList.aspx?GroupId=\"",
    "program": ""
  },
  {
    "name": "Dolphin",
    "rule": "body=\"bx_css_async\"",
    "program": ""
  },
  {
    "name": "wecenter",
    "rule": "body=\"aw_template.js\" || body=\"WeCenter\"",
    "program": ""
  },
  {
    "name": "phpvod",
    "rule": "body=\"Powered by PHPVOD\" || body=\"content=\"phpvod\"",
    "program": ""
  },
  {
    "name": "08cms",
    "rule": "body=\"content=\"08CMS\" || body=\"typeof(_08cms)\"",
    "program": ""
  },
  {
    "name": "tutucms",
    "rule": "body=\"content=\"TUTUCMS\" || body=\"Powered by TUTUCMS\" || body=\"TUTUCMS\"\"",
    "program": ""
  },
  {
    "name": "八哥CMS",
    "rule": "body=\"content=\"BageCMS\"",
    "program": ""
  },
  {
    "name": "mymps",
    "rule": "body=\"/css/mymps.css\" || title=\"mymps\" || body=\"content=\"mymps\"",
    "program": ""
  },
  {
    "name": "IMGCms",
    "rule": "body=\"content=\"IMGCMS\" || body=\"Powered by IMGCMS\"",
    "program": ""
  },
  {
    "name": "jieqi cms",
    "rule": "body=\"content=\"jieqi cms\" || title=\"jieqi cms\"",
    "program": ""
  },
  {
    "name": "eadmin",
    "rule": "body=\"content=\"eAdmin\" || title=\"eadmin\"",
    "program": ""
  },
  {
    "name": "opencms",
    "rule": "body=\"content=\"OpenCms\" || body=\"Powered by OpenCms\"",
    "program": ""
  },
  {
    "name": "infoglue",
    "rule": "title=\"infoglue\" || body=\"infoglueBox.png\"",
    "program": ""
  },
  {
    "name": "171cms",
    "rule": "body=\"content=\"171cms\" || title=\"171cms\"",
    "program": ""
  },
  {
    "name": "doccms",
    "rule": "body=\"Power by DocCms\"",
    "program": ""
  },
  {
    "name": "appcms",
    "rule": "body=\"Powerd by AppCMS\"",
    "program": ""
  },
  {
    "name": "niucms",
    "rule": "body=\"content=\"NIUCMS\"",
    "program": ""
  },
  {
    "name": "baocms",
    "rule": "body=\"content=\"BAOCMS\" || title=\"baocms\"",
    "program": ""
  },
  {
    "name": "PublicCMS",
    "rule": "title=\"publiccms\"",
    "program": ""
  },
  {
    "name": "JTBC(CMS)",
    "rule": "body=\"/js/jtbc.js\" || body=\"content=\"JTBC\"",
    "program": ""
  },
  {
    "name": "易企CMS",
    "rule": "body=\"content=\"YiqiCMS\"",
    "program": ""
  },
  {
    "name": "ZCMS",
    "rule": "body=\"_ZCMS_ShowNewMessage\" || body=\"zcms_skin\" || title=\"ZCMS泽元内容管理\"",
    "program": ""
  },
  {
    "name": "科蚁CMS",
    "rule": "body=\"keyicms：keyicms\" || body=\"Powered by <a href=\"http://www.keyicms.com\"",
    "program": ""
  },
  {
    "name": "苹果CMS",
    "rule": "body=\"maccms:voddaycount\"",
    "program": ""
  },
  {
    "name": "大米CMS",
    "rule": "title=\"大米CMS-\" || body=\"content=\"damicms\" || body=\"content=\"大米CMS\"",
    "program": ""
  },
  {
    "name": "phpmps",
    "rule": "body=\"Powered by Phpmps\" || body=\"templates/phpmps/style/index.css\"",
    "program": ""
  },
  {
    "name": "25yi",
    "rule": "body=\"Powered by 25yi\" || body=\"css/25yi.css\"",
    "program": ""
  },
  {
    "name": "kingcms",
    "rule": "title=\"kingcms\" || body=\"content=\"KingCMS\" || body=\"Powered by KingCMS\"",
    "program": ""
  },
  {
    "name": "易点CMS",
    "rule": "body=\"DianCMS_SiteName\" || body=\"DianCMS_用户登陆引用\"",
    "program": ""
  },
  {
    "name": "fengcms",
    "rule": "body=\"Powered by FengCms\" || body=\"content=\"FengCms\"",
    "program": ""
  },
  {
    "name": "phpb2b",
    "rule": "body=\"Powered By PHPB2B\"",
    "program": ""
  },
  {
    "name": "phpdisk",
    "rule": "body=\"Powered by PHPDisk\" || body=\"content=\"PHPDisk\"",
    "program": ""
  },
  {
    "name": "EduSoho开源网络课堂",
    "rule": "title=\"edusoho\" || body=\"Powered by <a href=\"http://www.edusoho.com\" || body=\"Powered By EduSoho\"",
    "program": ""
  },
  {
    "name": "phpok",
    "rule": "title=\"phpok\" || body=\"Powered By phpok.com\" || body=\"content=\"phpok\"",
    "program": ""
  },
  {
    "name": "dtcms",
    "rule": "title=\"dtcms\" || body=\"content=\"动力启航,DTCMS\"",
    "program": ""
  },
  {
    "name": "beecms",
    "rule": "(body=\"powerd by\" && body=\"BEESCMS\") || body=\"template/default/images/slides.min.jquery.js\"",
    "program": ""
  },
  {
    "name": "ourphp",
    "rule": "body=\"content=\"OURPHP\" || body=\"Powered by ourphp\"",
    "program": ""
  },
  {
    "name": "php云",
    "rule": "body=\"<div class=\"index_link_list_name\">\"",
    "program": ""
  },
  {
    "name": "贷齐乐p2p",
    "rule": "body=\"/js/jPackageCss/jPackage.css\" || body=\"src=\"/js/jPackage\"",
    "program": ""
  },
  {
    "name": "中企动力门户CMS",
    "rule": "body=\"中企动力提供技术支持\"",
    "program": ""
  },
  {
    "name": "destoon",
    "rule": "body=\"<meta name=\"generator\" content=\"Destoon\" || body=\"destoon_moduleid\"",
    "program": ""
  },
  {
    "name": "帝友P2P",
    "rule": "body=\"/js/diyou.js\" || body=\"src=\"/dyweb/dythemes\"",
    "program": ""
  },
  {
    "name": "海洋CMS",
    "rule": "title=\"seacms\" || body=\"Powered by SeaCms\" || body=\"content=\"seacms\"",
    "program": ""
  },
  {
    "name": "合正网站群内容管理系统",
    "rule": "body=\"Produced By\" && body=\"网站群内容管理系统\"",
    "program": ""
  },
  {
    "name": "OpenSNS",
    "rule": "(body=\"powered by\" && body=\"opensns\") || body=\"content=\"OpenSNS\"",
    "program": ""
  },
  {
    "name": "SEMcms",
    "rule": "body=\"semcms PHP\" || body=\"sc_mid_c_left_c sc_mid_left_bt\"",
    "program": ""
  },
  {
    "name": "Yxcms",
    "rule": "body=\"/css/yxcms.css\" || body=\"content=\"Yxcms\"",
    "program": ""
  },
  {
    "name": "NITC",
    "rule": "body=\"NITC Web Marketing Service\" || body=\"/images/nitc1.png\"",
    "program": ""
  },
  {
    "name": "wuzhicms",
    "rule": "body=\"Powered by wuzhicms\" || body=\"content=\"wuzhicms\"",
    "program": ""
  },
  {
    "name": "PHPMyWind",
    "rule": "body=\"phpMyWind.com All Rights Reserved\" || body=\"content=\"PHPMyWind\"",
    "program": ""
  },
  {
    "name": "SiteEngine",
    "rule": "body=\"content=\"Boka SiteEngine\"",
    "program": ""
  },
  {
    "name": "b2bbuilder",
    "rule": "body=\"content=\"B2Bbuilder\" || body=\"translateButtonId = \"B2Bbuilder\"",
    "program": ""
  },
  {
    "name": "农友政务系统",
    "rule": "body=\"1207044504\"",
    "program": ""
  },
  {
    "name": "dswjcms",
    "rule": "body=\"content=\"Dswjcms\" || body=\"Powered by Dswjcms\"",
    "program": ""
  },
  {
    "name": "FoxPHP",
    "rule": "body=\"FoxPHPScroll\" || body=\"FoxPHP_ImList\" || body=\"content=\"FoxPHP\"",
    "program": ""
  },
  {
    "name": "weiphp",
    "rule": "body=\"content=\"WeiPHP\" || body=\"/css/weiphp.css\"",
    "program": ""
  },
  {
    "name": "iWebSNS",
    "rule": "body=\"/jooyea/images/sns_idea1.jpg\" || body=\"/jooyea/images/snslogo.gif\"",
    "program": ""
  },
  {
    "name": "TurboCMS",
    "rule": "body=\"Powered by TurboCMS\" || body=\"/cmsapp/zxdcADD.jsp\" || body=\"/cmsapp/count/newstop_index.jsp?siteid=\"",
    "program": ""
  },
  {
    "name": "MoMoCMS",
    "rule": "body=\"content=\"MoMoCMS\" || body=\"Powered BY MoMoCMS\"",
    "program": ""
  },
  {
    "name": "Acidcat CMS",
    "rule": "body=\"Powered by Acidcat CMS\" || body=\"Start Acidcat CMS footer information\" || body=\"/css/admin_import.css\"",
    "program": ""
  },
  {
    "name": "WP Plugin All-in-one-SEO-Pack",
    "rule": "body=\"<!-- /all in one seo pack -->\"",
    "program": ""
  },
  {
    "name": "Aardvark Topsites",
    "rule": "body=\"Powered by\" && body=\"Aardvark Topsites\"",
    "program": ""
  },
  {
    "name": "1024 CMS",
    "rule": "body=\"Powered by 1024 CMS\" || body=\"content=\"1024 CMS\"",
    "program": ""
  },
  {
    "name": "68 Classifieds",
    "rule": "body=\"powered by\" && body=\"68 Classifieds\"",
    "program": ""
  },
  {
    "name": "武汉弘智科技",
    "rule": "body=\"研发与技术支持：武汉弘智科技有限公司\"",
    "program": ""
  },
  {
    "name": "北京金盘鹏图软件",
    "rule": "body=\"SpeakIntertScarch.aspx\"",
    "program": ""
  },
  {
    "name": "育友软件",
    "rule": "body=\"http://www.yuysoft.com/\" && body=\"技术支持\"",
    "program": ""
  },
  {
    "name": "STcms",
    "rule": "body=\"content=\"STCMS\" || body=\"DahongY<dahongy@gmail.com>\"",
    "program": ""
  },
  {
    "name": "青果软件",
    "rule": "title=\"KINGOSOFT\" || body=\"SetKingoEncypt.jsp\" || body=\"/jkingo.js\"",
    "program": ""
  },
  {
    "name": "DirCMS",
    "rule": "body=\"content=\"DirCMS\"",
    "program": ""
  },
  {
    "name": "牛逼cms",
    "rule": "body=\"content=\"niubicms\"",
    "program": ""
  },
  {
    "name": "南方数据",
    "rule": "body=\"/SouthidcKeFu.js\" || body=\"CONTENT=\"Copyright 2003-2015 - Southidc.net\" || body=\"/Southidcj2f.Js\"",
    "program": ""
  },
  {
    "name": "yidacms",
    "rule": "body=\"yidacms.css\"",
    "program": ""
  },
  {
    "name": "bluecms",
    "rule": "body=\"power by bcms\" || body=\"bcms_plugin\"",
    "program": ""
  },
  {
    "name": "taocms",
    "rule": "body=\">taoCMS<\"",
    "program": ""
  },
  {
    "name": "Tiki-wiki CMS",
    "rule": "body=\"jqueryTiki = new Object\"",
    "program": ""
  },
  {
    "name": "lepton-cms",
    "rule": "body=\"content=\"LEPTON-CMS\" || body=\"Powered by LEPTON CMS\"",
    "program": ""
  },
  {
    "name": "euse_study",
    "rule": "body=\"UserInfo/UserFP.aspx\"",
    "program": ""
  },
  {
    "name": "沃科网异网同显系统",
    "rule": "body=\"沃科网\" || title=\"异网同显系统\"",
    "program": ""
  },
  {
    "name": "Mixcall座席管理中心",
    "rule": "title=\"Mixcall座席管理中心\"",
    "program": ""
  },
  {
    "name": "DuomiCms",
    "rule": "body=\"DuomiCms\" || title=\"Power by DuomiCms\"",
    "program": ""
  },
  {
    "name": "ANECMS",
    "rule": "body=\"content=\"Erwin Aligam - ealigam@gmail.com\"",
    "program": ""
  },
  {
    "name": "Ananyoo-CMS",
    "rule": "body=\"content=\"http://www.ananyoo.com\"",
    "program": ""
  },
  {
    "name": "Amiro-CMS",
    "rule": "body=\"Powered by: Amiro CMS\" || body=\"-= Amiro.CMS (c) =-\"",
    "program": ""
  },
  {
    "name": "AlumniServer",
    "rule": "body=\"AlumniServerProject.php\" || body=\"content=\"Alumni\"",
    "program": ""
  },
  {
    "name": "AlstraSoft-EPay-Enterprise",
    "rule": "body=\"Powered by EPay Enterprise\" || body=\"/shop.htm?action=view\"",
    "program": ""
  },
  {
    "name": "AlstraSoft-AskMe",
    "rule": "body=\"<a href=\"pass_recover.php\">\" || (body=\"Powered by\" && body=\"http://www.alstrasoft.com\")",
    "program": ""
  },
  {
    "name": "Artiphp-CMS",
    "rule": "body=\"copyright Artiphp\"",
    "program": ""
  },
  {
    "name": "BIGACE",
    "rule": "body=\"content=\"BIGACE\" || body=\"Site is running BIGACE\"",
    "program": ""
  },
  {
    "name": "Biromsoft-WebCam",
    "rule": "title=\"Biromsoft WebCam\"",
    "program": ""
  },
  {
    "name": "BackBee",
    "rule": "body=\"<div id=\"bb5-site-wrapper\">\"",
    "program": ""
  },
  {
    "name": "Auto-CMS",
    "rule": "body=\"Powered by Auto CMS\" || body=\"content=\"AutoCMS\"",
    "program": ""
  },
  {
    "name": "STAR CMS",
    "rule": "body=\"content=\"STARCMS\" || body=\"<img alt=\"STAR CMS\"",
    "program": ""
  },
  {
    "name": "Zotonic",
    "rule": "body=\"powered by: Zotonic\" || body=\"/lib/js/apps/zotonic-1.0\"",
    "program": ""
  },
  {
    "name": "BloofoxCMS",
    "rule": "body=\"content=\"bloofoxCMS\" || body=\"Powered by <a href=\"http://www.bloofox.com\"",
    "program": ""
  },
  {
    "name": "BlognPlus",
    "rule": "body=\"Powered by\" && body=\"href=\"http://www.blogn.org\"",
    "program": ""
  },
  {
    "name": "bitweaver",
    "rule": "body=\"content=\"bitweaver\" || body=\"href=\"http://www.bitweaver.org\">Powered by\"",
    "program": ""
  },
  {
    "name": "ClanSphere",
    "rule": "body=\"content=\"ClanSphere\" || body=\"index.php?mod=clansphere&amp;action=about\"",
    "program": ""
  },
  {
    "name": "CitusCMS",
    "rule": "body=\"Powered by CitusCMS\" || body=\"<strong>CitusCMS</strong>\" || body=\"content=\"CitusCMS\"",
    "program": ""
  },
  {
    "name": "CMS-WebManager-Pro",
    "rule": "body=\"content=\"Webmanager-pro\" || body=\"href=\"http://webmanager-pro.com\">Web.Manager\"",
    "program": ""
  },
  {
    "name": "CMSQLite",
    "rule": "body=\"powered by CMSQLite\" || body=\"content=\"www.CMSQLite.net\"",
    "program": ""
  },
  {
    "name": "CMSimple",
    "rule": "body=\"Powered by CMSimple.dk\" || body=\"content=\"CMSimple\"",
    "program": ""
  },
  {
    "name": "CMScontrol",
    "rule": "body=\"content=\"CMScontrol\"",
    "program": ""
  },
  {
    "name": "Claroline",
    "rule": "body=\"target=\"_blank\">Claroline</a>\" || body=\"http://www.claroline.net\" rel=\"Copyright\"",
    "program": ""
  },
  {
    "name": "Car-Portal",
    "rule": "body=\"Powered by <a href=\"http://www.netartmedia.net/carsportal\" || body=\"class=\"bodyfontwhite\"><strong>&nbsp;Car Script\"",
    "program": ""
  },
  {
    "name": "chillyCMS",
    "rule": "body=\"powered by <a href=\"http://FrozenPepper.de\"",
    "program": ""
  },
  {
    "name": "BoonEx-Dolphin",
    "rule": "body=\"Powered by                    Dolphin - <a href=\"http://www.boonex.com/products/dolphin\"",
    "program": ""
  },
  {
    "name": "SilverStripe",
    "rule": "body=\"content=\"SilverStripe\"",
    "program": ""
  },
  {
    "name": "Campsite",
    "rule": "body=\"content=\"Campsite\"",
    "program": ""
  },
  {
    "name": "ischoolsite",
    "rule": "body=\"Powered by <a href=\"http://www.ischoolsite.com\"",
    "program": ""
  },
  {
    "name": "CafeEngine",
    "rule": "body=\"/CafeEngine/style.css\" || body=\"<a href=http://cafeengine.com>CafeEngine.com\"",
    "program": ""
  },
  {
    "name": "BrowserCMS",
    "rule": "body=\"Powered by BrowserCMS\" || body=\"content=\"BrowserCMS\"",
    "program": ""
  },
  {
    "name": "Contrexx-CMS",
    "rule": "body=\"powered by Contrexx\" || body=\"content=\"Contrexx\"",
    "program": ""
  },
  {
    "name": "ContentXXL",
    "rule": "body=\"content=\"contentXXL\"",
    "program": ""
  },
  {
    "name": "Contentteller-CMS",
    "rule": "body=\"content=\"Esselbach Contentteller CMS\"",
    "program": ""
  },
  {
    "name": "Contao",
    "rule": "body=\"system/contao.css\"",
    "program": ""
  },
  {
    "name": "CommonSpot",
    "rule": "body=\"content=\"CommonSpot\"",
    "program": ""
  },
  {
    "name": "CruxCMS",
    "rule": "body=\"Created by CruxCMS\" || title=\"CruxCMS\"",
    "program": ""
  },
  {
    "name": "锐商企业CMS",
    "rule": "body=\"href=\"/Writable/ClientImages/mycss.css\"",
    "program": ""
  },
  {
    "name": "coWiki",
    "rule": "body=\"content=\"coWiki\" || body=\"<!-- Generated by coWiki\"",
    "program": ""
  },
  {
    "name": "Coppermine",
    "rule": "body=\"<!--Coppermine Photo Gallery\"",
    "program": ""
  },
  {
    "name": "DaDaBIK",
    "rule": "body=\"content=\"DaDaBIK\" || body=\"class=\"powered_by_dadabik\"",
    "program": ""
  },
  {
    "name": "Custom-CMS",
    "rule": "body=\"content=\"CustomCMS\" || body=\"Powered by CCMS\"",
    "program": ""
  },
  {
    "name": "DT-Centrepiece",
    "rule": "body=\"content=\"DT Centrepiece\" || body=\"Powered By DT Centrepiece\"",
    "program": ""
  },
  {
    "name": "Edito-CMS",
    "rule": "body=\"content=\"edito\" || body=\"href=\"http://www.edito.pl/\"",
    "program": ""
  },
  {
    "name": "Echo",
    "rule": "body=\"powered by echo\" || body=\"/Echo2/echoweb/login\"",
    "program": ""
  },
  {
    "name": "Ecomat-CMS",
    "rule": "body=\"content=\"ECOMAT CMS\"",
    "program": ""
  },
  {
    "name": "EazyCMS",
    "rule": "body=\"powered by eazyCMS\" || body=\"<a class=\"actionlink\" href=\"http://www.eazyCMS.com\"",
    "program": ""
  },
  {
    "name": "easyLink-Web-Solutions",
    "rule": "body=\"content=\"easyLink\"",
    "program": ""
  },
  {
    "name": "EasyConsole-CMS",
    "rule": "body=\"Powered by EasyConsole CMS\" || body=\"Powered by <a href=\"http://www.easyconsole.com\"",
    "program": ""
  },
  {
    "name": "DotCMS",
    "rule": "body=\"/dotAsset/\" || body=\"/index.dot\"",
    "program": ""
  },
  {
    "name": "DBHcms",
    "rule": "body=\"powered by DBHcms\"",
    "program": ""
  },
  {
    "name": "Donations-Cloud",
    "rule": "body=\"/donationscloud.css\"",
    "program": ""
  },
  {
    "name": "Dokeos",
    "rule": "body=\"href=\"http://www.dokeos.com\" rel=\"Copyright\" || body=\"content=\"Dokeos\" || body=\"name=\"Generator\" content=\"Dokeos\"",
    "program": ""
  },
  {
    "name": "Elxis-CMS",
    "rule": "body=\"content=\"Elxis\"",
    "program": ""
  },
  {
    "name": "eFront",
    "rule": "body=\"<a href = \"http://www.efrontlearning.net\"",
    "program": ""
  },
  {
    "name": "eSitesBuilder",
    "rule": "body=\"eSitesBuilder. All rights reserved\"",
    "program": ""
  },
  {
    "name": "EPiServer",
    "rule": "body=\"content=\"EPiServer\" || body=\"/javascript/episerverscriptmanager.js\"",
    "program": ""
  },
  {
    "name": "Energine",
    "rule": "body=\"scripts/Energine.js\" || body=\"Powered by <a href= \"http://energine.org/\" || body=\"stylesheets/energine.css\"",
    "program": ""
  },
  {
    "name": "Gallery",
    "rule": "title=\"Gallery 3 Installer\" || body=\"/gallery/images/gallery.png\"",
    "program": ""
  },
  {
    "name": "FrogCMS",
    "rule": "body=\"target=\"_blank\">Frog CMS\" || body=\"href=\"http://www.madebyfrog.com\">Frog CMS\"",
    "program": ""
  },
  {
    "name": "Fossil",
    "rule": "body=\"<a href=\"http://fossil-scm.org\"",
    "program": ""
  },
  {
    "name": "FCMS",
    "rule": "body=\"content=\"Ryan Haudenschilt\" || body=\"Powered by Family Connections\"",
    "program": ""
  },
  {
    "name": "Fastpublish-CMS",
    "rule": "body=\"content=\"fastpublish\"",
    "program": ""
  },
  {
    "name": "F3Site",
    "rule": "body=\"Powered by <a href=\"http://compmaster.prv.pl\"",
    "program": ""
  },
  {
    "name": "Exponent-CMS",
    "rule": "body=\"content=\"Exponent Content Management System\" || body=\"Powered by Exponent CMS\"",
    "program": ""
  },
  {
    "name": "E-Xoopport",
    "rule": "body=\"Powered by E-Xoopport\" || body=\"content=\"E-Xoopport\"",
    "program": ""
  },
  {
    "name": "E-Manage-MySchool",
    "rule": "body=\"E-Manage All Rights Reserved MySchool Version\"",
    "program": ""
  },
  {
    "name": "glFusion",
    "rule": "body=\"by <a href=\"http://www.glfusion.org/\"",
    "program": ""
  },
  {
    "name": "GetSimple",
    "rule": "body=\"content=\"GetSimple\" || body=\"Powered by GetSimple\"",
    "program": ""
  },
  {
    "name": "HESK",
    "rule": "body=\"hesk_javascript.js\" || body=\"hesk_style.css\" || body=\"Powered by <a href=\"http://www.hesk.com\" || body=\"Powered by <a href=\"https://www.hesk.com\"",
    "program": ""
  },
  {
    "name": "GuppY",
    "rule": "body=\"content=\"GuppY\" || body=\"class=\"copyright\" href=\"http://www.freeguppy.org/\"",
    "program": ""
  },
  {
    "name": "FluentNET",
    "rule": "body=\"content=\"Fluent\"",
    "program": ""
  },
  {
    "name": "GeekLog",
    "rule": "body=\"Powered By <a href=\"http://www.geeklog.net/\"",
    "program": ""
  },
  {
    "name": "Hycus-CMS",
    "rule": "body=\"content=\"Hycus\" || body=\"Powered By <a href=\"http://www.hycus.com\"",
    "program": ""
  },
  {
    "name": "Hotaru-CMS",
    "rule": "body=\"content=\"Hotaru\"",
    "program": ""
  },
  {
    "name": "HoloCMS",
    "rule": "body=\"Powered by HoloCMS\"",
    "program": ""
  },
  {
    "name": "ImpressPages-CMS",
    "rule": "body=\"content=\"ImpressPages CMS\"",
    "program": ""
  },
  {
    "name": "iGaming-CMS",
    "rule": "body=\"Powered by\" && body=\"http://www.igamingcms.com/\"",
    "program": ""
  },
  {
    "name": "xoops",
    "rule": "body=\"include/xoops.js\"",
    "program": ""
  },
  {
    "name": "Intraxxion-CMS",
    "rule": "body=\"content=\"Intraxxion\" || body=\"<!-- site built by Intraxxion\"",
    "program": ""
  },
  {
    "name": "InterRed",
    "rule": "body=\"content=\"InterRed\" || body=\"Created with InterRed\"",
    "program": ""
  },
  {
    "name": "Informatics-CMS",
    "rule": "body=\"content=\"Informatics\"",
    "program": ""
  },
  {
    "name": "JagoanStore",
    "rule": "body=\"href=\"http://www.jagoanstore.com/\" target=\"_blank\">Toko Online\"",
    "program": ""
  },
  {
    "name": "Kandidat-CMS",
    "rule": "body=\"content=\"Kandidat-CMS\"",
    "program": ""
  },
  {
    "name": "Kajona",
    "rule": "body=\"content=\"Kajona\" || body=\"powered by Kajona\"",
    "program": ""
  },
  {
    "name": "JGS-Portal",
    "rule": "body=\"Powered by <b>JGS-Portal Version\" || body=\"href=\"jgs_portal_box.php?id=\"",
    "program": ""
  },
  {
    "name": "jCore",
    "rule": "body=\"JCORE_VERSION = \"",
    "program": ""
  },
  {
    "name": "EdmWebVideo",
    "rule": "title=\"EdmWebVideo\"",
    "program": ""
  },
  {
    "name": "edvr",
    "rule": "title=\"edvs/edvr\"",
    "program": ""
  },
  {
    "name": "Polycom",
    "rule": "title=\"Polycom\" && body=\"kAllowDirectHTMLFileAccess\"",
    "program": ""
  },
  {
    "name": "techbridge",
    "rule": "body=\"Sorry,you need to use IE brower\"",
    "program": ""
  },
  {
    "name": "NETSurveillance",
    "rule": "title=\"NETSurveillance\"",
    "program": ""
  },
  {
    "name": "nvdvr",
    "rule": "title=\"XWebPlay\"",
    "program": ""
  },
  {
    "name": "DVR camera",
    "rule": "title=\"DVR WebClient\"",
    "program": ""
  },
  {
    "name": "Macrec_DVR",
    "rule": "title=\"Macrec DVR\"",
    "program": ""
  },
  {
    "name": "OnSSI_Video_Clients",
    "rule": "title=\"OnSSI Video Clients\" || body=\"x-value=\"On-Net Surveillance Systems Inc.\"\"",
    "program": ""
  },
  {
    "name": "Linksys_SPA_Configuration ",
    "rule": "title=\"Linksys SPA Configuration\"",
    "program": ""
  },
  {
    "name": "eagleeyescctv",
    "rule": "body=\"IP Surveillance for Your Life\" || body=\"/nobody/loginDevice.js\"",
    "program": ""
  },
  {
    "name": "dasannetworks",
    "rule": "body=\"clear_cookie(\"login\");\"",
    "program": ""
  },
  {
    "name": "海康威视iVMS",
    "rule": "body=\"g_szCacheTime\" && body=\"iVMS\"",
    "program": ""
  },
  {
    "name": "佳能网络摄像头(Canon Network Cameras)",
    "rule": "body=\"/viewer/live/en/live.html\"",
    "program": ""
  },
  {
    "name": "NetDvrV3",
    "rule": "body=\"objLvrForNoIE\"",
    "program": ""
  },
  {
    "name": "SIEMENS IP Cameras",
    "rule": "title=\"SIEMENS IP Camera\"",
    "program": ""
  },
  {
    "name": "VideoIQ Camera",
    "rule": "title=\"VideoIQ Camera Login\"",
    "program": ""
  },
  {
    "name": "Honeywell IP-Camera",
    "rule": "title=\"Honeywell IP-Camera\"",
    "program": ""
  },
  {
    "name": "sony摄像头",
    "rule": "title=\"Sony Network Camera\" || body=\"inquiry.cgi?inqjs=system&inqjs=camera\"",
    "program": ""
  },
  {
    "name": "AJA-Video-Converter",
    "rule": "body=\"eParamID_SWVersion\"",
    "program": ""
  },
  {
    "name": "ACTi",
    "rule": "title=\"Web Configurator\" || body=\"ACTi Corporation All Rights Reserved\"",
    "program": ""
  },
  {
    "name": "Samsung DVR",
    "rule": "title=\"Samsung DVR\"",
    "program": ""
  },
  {
    "name": "Vicworl",
    "rule": "body=\"Powered by Vicworl\" || body=\"content=\"Vicworl\" || body=\"vindex_right_d\"",
    "program": ""
  },
  {
    "name": "AVCON6",
    "rule": "body=\"filename=AVCON6Setup.exe\" || title=\"AVCON6系统管理平台\" || body=\"language_dispose.action\"",
    "program": ""
  },
  {
    "name": "Axis-Network-Camera",
    "rule": "title=\"AXIS Video Server\" || body=\"/incl/trash.shtml\"",
    "program": ""
  },
  {
    "name": "Panasonic Network Camera",
    "rule": "body=\"MultiCameraFrame?Mode=Motion&Language\"",
    "program": ""
  },
  {
    "name": "BlueNet-Video",
    "rule": "body=\"/cgi-bin/client_execute.cgi?tUD=0\" || title=\"BlueNet Video Viewer Version\"",
    "program": ""
  },
  {
    "name": "ClipBucket",
    "rule": "body=\"content=\"ClipBucket\" || body=\"<!-- ClipBucket\" || body=\"<!-- Forged by ClipBucket\" || body=\"href=\"http://clip-bucket.com/\">ClipBucket\"",
    "program": ""
  },
  {
    "name": "ZoneMinder",
    "rule": "body=\"ZoneMinder Login\"",
    "program": ""
  },
  {
    "name": "DVR-WebClient",
    "rule": "body=\"259F9FDF-97EA-4C59-B957-5160CAB6884E\" || title=\"DVR-WebClient\"",
    "program": ""
  },
  {
    "name": "D-Link-Network-Camera",
    "rule": "body=\"DCS-950G\".toLowerCase()\" || title=\"DCS-5300\"",
    "program": ""
  },
  {
    "name": "DiBos",
    "rule": "title=\"DiBos - Login\" || body=\"style/bovisnt.css\"",
    "program": ""
  },
  {
    "name": "Evo-Cam",
    "rule": "body=\"value=\"evocam.jar\" || body=\"<applet archive=\"evocam.jar\"",
    "program": ""
  },
  {
    "name": "Intellinet-IP-Camera",
    "rule": "body=\"Copyright &copy;  INTELLINET NETWORK SOLUTIONS\" || body=\"http://www.intellinet-network.com/driver/NetCam.exe\"",
    "program": ""
  },
  {
    "name": "IQeye-Netcam",
    "rule": "title=\"IQEYE: Live Images\" || body=\"content=\"Brian Lau, IQinVision\" || body=\"loc = \"iqeyevid.html\"",
    "program": ""
  },
  {
    "name": "phpwind",
    "rule": "title=\"Powered by phpwind\" || body=\"content=\"phpwind\"",
    "program": ""
  },
  {
    "name": "discuz",
    "rule": "title=\"Powered by Discuz\" || body=\"content=\"Discuz\" || (body=\"discuz_uid\" && body=\"portal.php?mod=view\") || body=\"Powered by <strong><a href=\"http://www.discuz.net\"",
    "program": ""
  },
  {
    "name": "6kbbs",
    "rule": "body=\"Powered by 6kbbs\" || body=\"generator\" content=\"6KBBS\"",
    "program": ""
  },
  {
    "name": "IP.Board",
    "rule": "body=\"ipb.vars\"",
    "program": ""
  },
  {
    "name": "ThinkOX",
    "rule": "body=\"Powered By ThinkOX\" || title=\"ThinkOX\"",
    "program": ""
  },
  {
    "name": "bbPress",
    "rule": "body=\"<!-- If you like showing off the fact that your server rocks -->\" || body=\"is proudly powered by <a href=\"http://bbpress.org\"",
    "program": ""
  },
  {
    "name": "BlogEngine_NET",
    "rule": "body=\"pics/blogengine.ico\" || (body=\"Powered by\" && body=\"http://www.dotnetblogengine.net\")",
    "program": ""
  },
  {
    "name": "boastMachine",
    "rule": "body=\"powered by boastMachine\" || body=\"Powered by <a href=\"http://boastology.com\"",
    "program": ""
  },
  {
    "name": "BrewBlogger",
    "rule": "body=\"developed by <a href=\"http://www.zkdigital.com\"",
    "program": ""
  },
  {
    "name": "Dotclear",
    "rule": "body=\"Powered by <a href=\"http://dotclear.org/\"",
    "program": ""
  },
  {
    "name": "DokuWiki",
    "rule": "body=\"powered by DokuWiki\" || body=\"content=\"DokuWiki\" || body=\"<div id=\"dokuwiki\"",
    "program": ""
  },
  {
    "name": "DeluxeBB",
    "rule": "body=\"content=\"powered by DeluxeBB\"",
    "program": ""
  },
  {
    "name": "esoTalk",
    "rule": "body=\"generated by esoTalk\" || body=\"Powered by esoTalk\" || body=\"/js/esotalk.js\"",
    "program": ""
  },
  {
    "name": "Hiki",
    "rule": "body=\"content=\"Hiki\" || body=\"/hiki_base.css\" || body=\"by <a href=\"http://hikiwiki.org/\"",
    "program": ""
  },
  {
    "name": "Gossamer-Forum",
    "rule": "body=\"href=\"gforum.cgi?username=\" || title=\"Gossamer Forum\"",
    "program": ""
  },
  {
    "name": "Forest-Blog",
    "rule": "title=\"Forest Blog\"",
    "program": ""
  },
  {
    "name": "FluxBB",
    "rule": "body=\"Powered by <a href=\"http://fluxbb.org/\"",
    "program": ""
  },
  {
    "name": "Kampyle",
    "rule": "body=\"http://cf.kampyle.com/k_button.js\" || body=\"Start Kampyle Feedback Form Button\"",
    "program": ""
  },
  {
    "name": "KaiBB",
    "rule": "body=\"Powered by KaiBB\" || body=\"content=\"Forum powered by KaiBB\"",
    "program": ""
  },
  {
    "name": "fangmail",
    "rule": "body=\"/fangmail/default/css/em_css.css\"",
    "program": ""
  },
  {
    "name": "MDaemon",
    "rule": "body=\"/WorldClient.dll?View=Main\"",
    "program": ""
  },
  {
    "name": "网易企业邮箱",
    "rule": "body=\"frmvalidator\" && title=\"邮箱用户登录\"",
    "program": ""
  },
  {
    "name": "TurboMail",
    "rule": "body=\"Powered by TurboMail\" || body=\"wzcon1 clearfix\" || title=\"TurboMail邮件系统\"",
    "program": ""
  },
  {
    "name": "万网企业云邮箱",
    "rule": "body=\"static.mxhichina.com/images/favicon.ico\"",
    "program": ""
  },
  {
    "name": "bxemail",
    "rule": "title=\"百讯安全邮件系统\" || title=\"百姓邮局\" || body=\"请输入正确的电子邮件地址，如：abc@bxemail.com\"",
    "program": ""
  },
  {
    "name": "Coremail",
    "rule": "title=\"/coremail/common/assets\" || title=\"Coremail邮件系统\"",
    "program": ""
  },
  {
    "name": "Lotus",
    "rule": "title=\"IBM Lotus iNotes Login\" || body=\"iwaredir.nsf\"",
    "program": ""
  },
  {
    "name": "mirapoint",
    "rule": "body=\"/wm/mail/login.html\"",
    "program": ""
  },
  {
    "name": "U-Mail",
    "rule": "body=\"<BODY LINK=\"White\" VLINK=\"White\" ALINK=\"White\">\"",
    "program": ""
  },
  {
    "name": "Spammark邮件信息安全网关",
    "rule": "title=\"Spammark邮件信息安全网关\" || body=\"/cgi-bin/spammark?empty=1\"",
    "program": ""
  },
  {
    "name": "科信邮件系统",
    "rule": "body=\"/systemfunction.pack.js\" || body=\"lo_computername\"",
    "program": ""
  },
  {
    "name": "winwebmail",
    "rule": "title=\"winwebmail\" || body=\"WinWebMail Server\" || body=\"images/owin.css\"",
    "program": ""
  },
  {
    "name": "泰信TMailer邮件系统",
    "rule": "title=\"Tmailer\" || body=\"content=\"Tmailer\" || body=\"href=\"/tmailer/img/logo/favicon.ico\"",
    "program": ""
  },
  {
    "name": "richmail",
    "rule": "title=\"Richmail\" || body=\"/resource/se/lang/se/mail_zh_CN.js\" || body=\"content=\"Richmail\"",
    "program": ""
  },
  {
    "name": "iGENUS邮件系统",
    "rule": "body=\"Copyright by<A HREF=\"http://www.igenus.org\" || title=\"iGENUS webmail\"",
    "program": ""
  },
  {
    "name": "金笛邮件系统",
    "rule": "body=\"/jdwm/cgi/login.cgi?login\"",
    "program": ""
  },
  {
    "name": "迈捷邮件系统(MagicMail)",
    "rule": "body=\"/aboutus/magicmail.gif\"",
    "program": ""
  },
  {
    "name": "Atmail-WebMail",
    "rule": "body=\"Powered by Atmail\" || body=\"/index.php/mail/auth/processlogin\" || body=\"<input id=\"Mailserverinput\"",
    "program": ""
  },
  {
    "name": "FormMail",
    "rule": "body=\"/FormMail.pl\" || body=\"href=\"http://www.worldwidemart.com/scripts/formmail.shtml\"",
    "program": ""
  },
  {
    "name": "同城多用户商城",
    "rule": "body=\"style_chaoshi\"",
    "program": ""
  },
  {
    "name": "iWebShop",
    "rule": "body=\"/runtime/default/systemjs\"",
    "program": ""
  },
  {
    "name": "1und1",
    "rule": "body=\"/shop/catalog/browse?sessid=\"",
    "program": ""
  },
  {
    "name": "cart_engine",
    "rule": "body=\"skins/_common/jscripts.css\"",
    "program": ""
  },
  {
    "name": "Magento",
    "rule": "(body=\"/skin/frontend/\" && body=\"BLANK_IMG\") || body=\"Magento, Varien, E-commerce\"",
    "program": ""
  },
  {
    "name": "OpenCart",
    "rule": "body=\"Powered By OpenCart\" || body=\"catalog/view/theme\"",
    "program": ""
  },
  {
    "name": "hishop",
    "rule": "body=\"hishop.plugins.openid\" || body=\"Hishop development team\"",
    "program": ""
  },
  {
    "name": "Maticsoft_Shop_动软商城",
    "rule": "body=\"Maticsoft Shop\" || (body=\"maticsoft\" && body=\"/Areas/Shop/\")",
    "program": ""
  },
  {
    "name": "hikashop",
    "rule": "body=\"/media/com_hikashop/css/\"",
    "program": ""
  },
  {
    "name": "tp-shop",
    "rule": "body=\"mn-c-top\"",
    "program": ""
  },
  {
    "name": " 海盗云商(Haidao)",
    "rule": "body=\"haidao.web.general.js\"",
    "program": ""
  },
  {
    "name": "shopbuilder",
    "rule": "body=\"content=\"ShopBuilder\" || body=\"Powered by ShopBuilder\" || body=\"ShopBuilder版权所有\"",
    "program": ""
  },
  {
    "name": "v5shop",
    "rule": "title=\"v5shop\" || body=\"content=\"V5shop\" || body=\"Powered by V5Shop\"",
    "program": ""
  },
  {
    "name": "shopnc",
    "rule": "body=\"Powered by ShopNC\" || body=\"Copyright 2007-2014 ShopNC Inc\" || body=\"content=\"ShopNC\"",
    "program": ""
  },
  {
    "name": "shopex",
    "rule": "body=\"content=\"ShopEx\" || body=\"@author litie[aita]shopex.cn\"",
    "program": ""
  },
  {
    "name": "dbshop",
    "rule": "body=\"content=\"dbshop\"",
    "program": ""
  },
  {
    "name": "任我行电商",
    "rule": "body=\"content=\"366EC\"",
    "program": ""
  },
  {
    "name": "CuuMall",
    "rule": "body=\"Power by CuuMall\"",
    "program": ""
  },
  {
    "name": "javashop",
    "rule": "body=\"易族智汇javashop\" || body=\"javashop微信公众号\" || body=\"content=\"JavaShop\"",
    "program": ""
  },
  {
    "name": "TPshop",
    "rule": "body=\"/index.php/Mobile/Index/index.html\" || body=\">TPshop开源商城<\"",
    "program": ""
  },
  {
    "name": "MvMmall",
    "rule": "body=\"content=\"MvMmall\"",
    "program": ""
  },
  {
    "name": "AirvaeCommerce",
    "rule": "body=\"E-Commerce Shopping Cart Software\"",
    "program": ""
  },
  {
    "name": "AiCart",
    "rule": "body=\"APP_authenticate\"",
    "program": ""
  },
  {
    "name": "MallBuilder",
    "rule": "body=\"content=\"MallBuilder\" || body=\"Powered by MallBuilder\"",
    "program": ""
  },
  {
    "name": "e-junkie",
    "rule": "body=\"function EJEJC_lc\"",
    "program": ""
  },
  {
    "name": "Allomani",
    "rule": "body=\"content=\"Allomani\" || body=\"Programmed By Allomani\"",
    "program": ""
  },
  {
    "name": "ASPilot-Cart",
    "rule": "body=\"content=\"Pilot Cart\" || body=\"/pilot_css_default.css\"",
    "program": ""
  },
  {
    "name": "Axous",
    "rule": "body=\"content=\"Axous\" || body=\"Axous Shareware Shop\"",
    "program": ""
  },
  {
    "name": "CaupoShop-Classic",
    "rule": "body=\"Powered by CaupoShop\" || body=\"<!-- CaupoShop Classic\" || body=\"<a href=\"http://www.caupo.net\" target=\"_blank\">CaupoNet\"",
    "program": ""
  },
  {
    "name": "PretsaShop",
    "rule": "body=\"content=\"PrestaShop\"\"",
    "program": ""
  },
  {
    "name": "ComersusCart",
    "rule": "body=\"CONTENT=\"Powered by Comersus\" || body=\"href=\"comersus_showCart.asp\"",
    "program": ""
  },
  {
    "name": "Foxycart",
    "rule": "body=\"<script src=\"//cdn.foxycart.com\"",
    "program": ""
  },
  {
    "name": "DV-Cart",
    "rule": "body=\"class=\"KT_tngtable\"",
    "program": ""
  },
  {
    "name": "EarlyImpact-ProductCart",
    "rule": "body=\"fpassword.asp?redirectUrl=&frURL=Custva.asp\"",
    "program": ""
  },
  {
    "name": "Escenic",
    "rule": "body=\"content=\"Escenic\" || body=\"<!-- Start Escenic Analysis Engine client script -->\"",
    "program": ""
  },
  {
    "name": "ICEshop",
    "rule": "body=\"Powered by ICEshop\" || body=\"<div id=\"iceshop\">\"",
    "program": ""
  },
  {
    "name": "Interspire-Shopping-Cart",
    "rule": "body=\"content=\"Interspire Shopping Cart\" || body=\"class=\"PoweredBy\">Interspire Shopping Cart\"",
    "program": ""
  },
  {
    "name": "iScripts-MultiCart",
    "rule": "body=\"Powered by <a href=\"http://iscripts.com/multicart\"",
    "program": ""
  },
  {
    "name": "华天动力OA(OA8000)",
    "rule": "body=\"/OAapp/WebObjects/OAapp.woa\"",
    "program": ""
  },
  {
    "name": "通达OA",
    "rule": "body=\"<link rel=\"shortcut icon\" href=\"/images/tongda.ico\" />\" || (body=\"OA提示：不能登录OA\" && body=\"紧急通知：今日10点停电\") || body=\"Office Anywhere 2013\"|| body = \"<a href='http://www.tongda2000.com/' target='_black'>通达官网</a></div>\"",
    "program": ""
  },
  {
    "name": "OA(a8/seeyon/ufida)",
    "rule": "body=\"/seeyon/USER-DATA/IMAGES/LOGIN/login.gif\"",
    "program": ""
  },
  {
    "name": "yongyoufe",
    "rule": "title=\"FE协作\" || (body=\"V_show\" && body=\"V_hedden\")",
    "program": ""
  },
  {
    "name": "pmway_E4_crm",
    "rule": "title=\"E4\" && title=\"CRM\"",
    "program": ""
  },
  {
    "name": "Dolibarr",
    "rule": "body=\"Dolibarr Development Team\"",
    "program": ""
  },
  {
    "name": "PHPOA",
    "rule": "body=\"admin_img/msg_bg.png\"",
    "program": ""
  },
  {
    "name": "78oa",
    "rule": "body=\"/resource/javascript/system/runtime.min.js\" || body=\"license.78oa.com\" || title=\"78oa\"||body=\"src=\"/module/index.php\"",
    "program": ""
  },
  {
    "name": "WishOA",
    "rule": "body=\"WishOA_WebPlugin.js\"",
    "program": ""
  },
  {
    "name": "金和协同管理平台",
    "rule": "title=\"金和协同管理平台\"",
    "program": ""
  },
  {
    "name": "Lotus",
    "rule": "title=\"IBM Lotus iNotes Login\" || body=\"iwaredir.nsf\"",
    "program": ""
  },
  {
    "name": "OA企业智能办公自动化系统",
    "rule": "body=\"input name=\"S1\" type=\"image\"\" && body=\"count/mystat.asp\"",
    "program": ""
  },
  {
    "name": "ecwapoa",
    "rule": "body=\"ecwapoa\"",
    "program": ""
  },
  {
    "name": "ezOFFICE",
    "rule": "title=\"Wanhu ezOFFICE\" || body=\"EZOFFICEUSERNAME\" ||title=\"万户OA\" || body=\"whirRootPath\" || body=\"/defaultroot/js/cookie.js\"",
    "program": ""
  },
  {
    "name": "任我行CRM",
    "rule": "title=\"任我行CRM\" || body=\"CRM_LASTLOGINUSERKEY\"",
    "program": ""
  },
  {
    "name": "信达OA",
    "rule": "body=\"http://www.xdoa.cn</a>\" || body=\"北京创信达科技有限公司\"",
    "program": ""
  },
  {
    "name": "协众OA",
    "rule": "body=\"Powered by 协众OA\" || body=\"admin@cnoa.cn\" || body=\"Powered by CNOA.CN\"",
    "program": ""
  },
  {
    "name": "soffice",
    "rule": "title=\"OA办公管理平台\"",
    "program": ""
  },
  {
    "name": "海天OA",
    "rule": "body=\"HTVOS.js\"",
    "program": ""
  },
  {
    "name": "泛微OA",
    "rule": "body=\"/js/jquery/jquery_wev8.js\"||body=\"/login/Login.jsp?logintype=1\"",
    "program": "java"
  },
  {
    "name": "中望OA",
    "rule": "body=\"/app_qjuserinfo/qjuserinfoadd.jsp\" || body=\"/IMAGES/default/first/xtoa_logo.png\"",
    "program": ""
  },
  {
    "name": "睿博士云办公系统",
    "rule": "body=\"/studentSign/toLogin.di\" || body=\"/user/toUpdatePasswordPage.di\"",
    "program": ""
  },
  {
    "name": "一米OA",
    "rule": "body=\"/yimioa.apk\"",
    "program": ""
  },
  {
    "name": "泛普建筑工程施工OA",
    "rule": "body=\"/dwr/interface/LoginService.js\"",
    "program": ""
  },
  {
    "name": "正方OA",
    "rule": "body=\"zfoausername\"",
    "program": ""
  },
  {
    "name": "希尔OA",
    "rule": "body=\"/heeroa/login.do\"",
    "program": ""
  },
  {
    "name": "用友致远oa",
    "rule": "body=\"/seeyon/USER-DATA/IMAGES/LOGIN/login.gif\" || title=\"用友致远A\" || body=\"/yyoa/\" || body=\"/seeyon/common/all-min.js\"",
    "program": ""
  },
  {
    "name": "WordPress",
    "rule": "body=\"/wp-login.php?\"||body=\"wp-user\"",
    "program": "php"
  },
  {
    "name": "宝塔面板",
    "rule": "body=\"<title>安全入口校验失败</title>\" || body=\"https://www.bt.cn/bbs/thread-18367-1-1.html\"",
    "program": "python"
  },
  {
    "name": "Emlog",
    "rule": "body=\"/include/lib/js/common_tpl.js\"&&body=\"content/templates\"",
    "program": "PHP"
  }
]
