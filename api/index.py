# -*- coding: UTF-8 -*-
import requests
import re
from http.server import BaseHTTPRequestHandler
import json

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]
def getdata(name):
    gitpage = requests.get("https://github.com/" + name)
    data = gitpage.text
    
    # 2023-11-22 更新正则 https://github.com/Zfour/python_github_calendar_api/issues/18
    datadatereg = re.compile(r'data-date="(.*?)" id="contribution-day-component')
    datacountreg = re.compile(r'<tool-tip .*?class="sr-only position-absolute">(.*?) contribution')
    
    datadate = datadatereg.findall(data)
    datacount = datacountreg.findall(data)
    datacount = list(map(int, [0 if i == "No" else i for i in datacount]))

    # 检查datadate和datacount是否为空
    if not datadate or not datacount:
        # 处理空数据情况
        return {"total": 0, "contributions": []}
        
    # 将datadate和datacount按照字典序排序
    sorted_data = sorted(zip(datadate, datacount))
    datadate, datacount = zip(*sorted_data)
    
    contributions = sum(datacount)
    datalist = []
    for index, item in enumerate(datadate):
        itemlist = {"date": item, "count": datacount[index]}
        datalist.append(itemlist)
    datalistsplit = list_split(datalist, 7)
    returndata = {
        "total": contributions,
        "contributions": datalistsplit
    }
    return returndata
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 2024-03-15 规范接口的传参方式 https://github.com/Zfour/python_github_calendar_api/issues/20#issuecomment-1999115747
        path = self.path
        spl=path.split('?')[1:]
        for kv in spl:
            key,user=kv.split("=")
            if key=="user": break
        data = getdata(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return
