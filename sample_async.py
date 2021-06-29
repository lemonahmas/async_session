import asyncio
import httpx,requests #async an non-async
from bs4 import BeautifulSoup as bs
import re, time, logging

import timerAa


class async_tests(object):
    def __init__(self):
        print("|| Abandon all hope ye who enter here. ||")


    def set_url(self, url:list):
        try:
            self.url = url
            print("#Url set done")
        except:
            print("Error")
            raise Exception


    def set_proxies(self, proxies:dict):
        self.proxies = proxies


    async def fetch_url(self,url):
        req = await self.async_client.get(url)
        return str(bs(req.content.decode("utf-8"),'html.parser').title)


    async def async_rest_calls(self):
        logging.basicConfig(filename="./asynclog.txt",filemode='w')
        logging.getLogger("asyncio").setLevel(logging.DEBUG)
        tasks = []
        self.async_client = httpx.AsyncClient(timeout=300)
        title = []
        for url in self.url:
            tasks.append(self.fetch_url(url))
        title.extend(await asyncio.gather(*tasks))
        await self.async_client.aclose()
        with open("./async.txt","wb") as f:
            for i in title:
                f.write((i+"\n").encode())
        return title


    def sync_rest_calls(self):
        session = requests.session()
        title = []
        for url in self.url:
            req = session.get(url)
            title.append(str(bs(req.content.decode("utf-8"),'html.parser').title))
        with open("./sync.txt","wb") as f:
            for i in title:
                f.write((i+"\n").encode())
        return title


if __name__ == "__main__":
    txt = requests.get("https://www.bilibili.com").text
    print(txt)
    urls = []
    for _ in bs(txt, 'html.parser').find_all('a'):
        href = _.get('href')
        if href == None or href == "":
            continue
        if href[0] == '/':
            href = "https:" + href
        if re.match("[a-zA-z]+://[^\s]*",href):
            urls.append(href)
    print(urls)
    tester = async_tests()
    tester.set_url(urls)
    #tester.set_proxies(proxies)

    @timerAa.timer
    def test_async():
        asyncio.run(tester.async_rest_calls(),debug=True)
    test_async()

    @timerAa.timer
    def test_sync():
        tester.sync_rest_calls()
    test_sync()



