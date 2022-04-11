from lib.requests.requests import *
from com import variable
from lxml import etree

class Web_Finger(object):
    def __init__(self):
        self.requests = Requests()

    def web_finger(self, ip, port):
        url = "http://" + ip + ":" + str(port)
        try:
            res = self.requests.get(url, timeout=4)
            if res == None:
                url = url.replace('http', 'https')
                res = self.requests.get(url, timeout=4, allow_redirects=False)
            if res.encoding.lower() != 'utf-8':
                htmlObj = etree.HTML(res.text.encode(res.encoding))
            else:
                htmlObj = etree.HTML(res.text)
            # 指纹识别
            #context = self.get_context(res.text)
            title = str(htmlObj.xpath("//title/text()")[0]).strip()
            finger_str = ""
            for web_finger in variable.web_finger_list:
                if self.check_rule(web_finger['rule'], res.text.lower(), title.lower()):
                    finger_str = web_finger['name']
                    break
            return res.status_code, title, finger_str
        except Exception as e:
            return "", "", ""

    def check_rule(self, rule, body, title):
        rule_str = rule.replace("\\", "").replace('title="', "title.find('''").replace('body="', "body.find('''").replace('" ||', "'''.lower())!=-1 or ").replace('" &&', "'''.lower())!=-1 and ").replace('") &&', "'''.lower())!=-1) and").replace('") ||', "'''.lower())!=-1) or")
        rule_str = rule_str.replace('title = "', "title.find('''").replace('body = "', "body.find('''").replace('"||', "'''.lower())!=-1 or ").replace('"&&', "'''.lower())!=-1 and ").replace('")&&', "''').lower())!=-1 and ")
        if rule_str.endswith(")"):
            rule_str = rule_str[0:-2] + "'''.lower())!=-1)"
        else:
            rule_str = rule_str[0:-1] + "'''.lower())!=-1"
        return eval(rule_str)



