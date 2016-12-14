#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @author MUA

import os
import time
import urllib2
import threading
from bs4 import BeautifulSoup

def getHtml(url, header, i):
    url = url + str(i)
    req = urllib2.Request(url, headers = header)
    con = urllib2.urlopen(req, timeout = 1)
    html = con.read()
    con.close()
    getContentOne(html)

def getContentOne(html):
    soup = BeautifulSoup(html)
    soup.prettify()
    one = soup.html.body.find_all('a', {'class' : 'mall'})
    getContentTwo(one)

def getContentTwo(html):
    for x in html:
        soup = BeautifulSoup(str(x))
        two = soup.get_text()
        print two

def doChore():
    time.sleep(0.5)

def booth(tid, url, header):
    global i
    global lock
    while True:
        lock.acquire()
        if i != 0:
            i = i - 1        
            print(tid,':Page:',i)
            getHtml(url, header, i)
            doChore()             
        else:
            print("Thread_id",tid," No more tasks")
            os._exit(0)           
        lock.release()

url = 'http://www.smzdm.com/p'
header = {'Host': 'www.smzdm.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'deflate',
        'Connection': 'keep-alive'}


i    = 30
lock = threading.Lock()

for k in range(10):
    new_thread = threading.Thread(target=booth,args=(k, url, header))   # Set up thread; target: the callable (function) to be run, args: the argument for the callable 
    new_thread.start()
