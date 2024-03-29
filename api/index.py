# -*- coding: UTF-8 -*-
import requests
import re
from http.server import BaseHTTPRequestHandler
import json

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]
def getdata(name):
    # 定义查询字符串参数
    headers = {
        'Accept': 'text/html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Cookie': '_octo=GH1.1.1243830600.1707011704; _device_id=225b8350efb22ccb9af0ae7c354b536f; saved_user_sessions=160836144%3AIUG6jQpqryWD7iPL5DB3oAF4BrO4v9YrixOn83RbXwIGnwwH; user_session=IUG6jQpqryWD7iPL5DB3oAF4BrO4v9YrixOn83RbXwIGnwwH; __Host-user_session_same_site=IUG6jQpqryWD7iPL5DB3oAF4BrO4v9YrixOn83RbXwIGnwwH; logged_in=yes; dotcom_user=yuhengwei2001; has_recent_activity=1; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; preferred_color_mode=dark; tz=Asia%2FShanghai; _gh_sess=Wwz8K%2FsLh9Zekf287Wuhrx6xrRarb2vEHLQxHLoL7l7CIN0wb0Oecva8lUIC7rXoFTtAcAxdQXFrreKtGluvfIz3DjVQdnBf%2BaA2VSJ%2BIIiNrxinL1kgJ2mUVvOA9TZotyqG5AIteQXgnICQguR6kinkeidW2RGui%2ByGFjfdLQjpkaweeJRip%2FdKSLkBeVdZAeoDe1CNYoE%2BBO1PSQR6kMndayVxRHkCBBZA92rhFjP6SFIW5jtLuFoz77Qj5ReLjmE49b5Q93jStcLpD%2FCeYIAmxU8AVG7QosVAIq4B7tACNa1BkIlcRxy8D1opsncIRqx6RbsN42dZCtIHZNlLv%2BdEvY5SNaxIbbJOF7PqpzOFHjCe9oWvBRdqz7h4bgRCD%2FnTpUGnn8Ph%2BKnTDL0gQkQUR5hdZY8qFO03Es%2BS0CpTmdS6tZ6irk%2F0d63En%2F7%2B9ONwMcyg7rwHYC6j4iwFuNzZkNWffLFJj0FhCfYTsWYjsRKw5ndIqNV3CTWnKyZEY4vqP0fis0rtW4GLcQa7JbLpXR7eedEZ--xzd%2BGBmBS01s9zpa--yl2WQeD2mmvFkNF36a9Aqw%3D%3D',
        'Pragma': 'no-cache',
        'Referer': 'https://github.com/yuhengwei2001',
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'X-Requested-With': 'XMLHttpRequest'
    }
    # 发送请求时使用 cookies 参数
    gitpage = requests.get("https://github.com/yuhengwei2001?action=show&controller=profiles&tab=contributions&user_id="+ name, headers=headers)

    data = gitpage.text
    with open("./github.html","w+",encoding="utf-8") as fp:
        fp.write(data)
    # 2023-11-22 更新正则 https://github.com/Zfour/python_github_calendar_api/issues/18
    datadatereg = re.compile(r'data-date="(.*?)" id="contribution-day-component')
    datacountreg = re.compile(r'data-level="(.*?)"')
    
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


print(getdata("yuhengwei2001"))