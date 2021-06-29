import threading,re
from typing import Collection
from bs4 import BeautifulSoup as bs
import timerAa

import requests

class multi_thread():
    def nolock_task(self,url) -> Collection:
        session = requests.session()
        req = session.get(url)
        encoding = req.encoding
        #print(encoding)
        #if encoding!="utf-8":print(req.content)
        title = str(bs(req.content.decode(encoding="utf-8"),'html.parser').title)
        if encoding!="utf-8":print(title)
        with open("./multi_thread.txt","a",encoding="UTF-8") as f:
            f.write((title+"\n"))
        return title


if __name__ == "__main__":
    txt = requests.get("https://www.bilibili.com").text
    #print(txt)
    urls = []
    for _ in bs(txt, 'html.parser').find_all('a'):
        href = _.get('href')
        if href == None or href == "":
            continue
        if href[0] == '/':
            href = "https:" + href
        if re.match("[a-zA-z]+://[^\s]*",href):
            urls.append(href)
    #print(urls)
    tester = multi_thread()
    threads_list = []

    @timerAa.timer
    def test_multi_thread():
        for i in urls:
            t = threading.Thread(target=tester.nolock_task, args=(str(i),))
            threads_list.append(t)
        for t in threads_list:
            t.start()
            t.join()
    test_multi_thread()
    
    

    