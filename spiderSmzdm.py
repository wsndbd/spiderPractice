#!/usr/bin/python
# -*- coding: utf-8 -*- 
# @author MUA

import os
import errno
import time
import urllib2
import threading
from bs4 import BeautifulSoup

def silentRemove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

def getHtml(url, header, i):
    url = url + '/' + str(i) + "/"
    print "url", url
#    req = urllib2.Request(url, headers = header)
#    con = urllib2.urlopen(req, timeout = 1)
#    html = con.read()
#    print "html", html
#    con.close()

    strCmd = "curl " + url + " >> curl.txt"
    print "strCmd", strCmd
    os.system(strCmd)
    buf = open("curl.txt", "rU").read()
    getContentOne(buf)

def getContentOne(html):
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()
    print "soup", soup
#    one = soup.html.body.find_all('a', {'class' : 'mall'})
    ar = soup.html.body.find_all('div', class_ = 'article-right')
    print "ararar", ar
#    getContentTwo(ar)

def getContentTwo(html):
    for x in html:
        soup = BeautifulSoup(str(x))
        two = soup.get_text()
        print "twotwotwo", two

def doChore():
    time.sleep(0.5)

def booth(tid, url, header):
    global i
    global lock
    if True:
        lock.acquire()
        if i != 0:
            print(tid,':Page:',i)
            getHtml(url, header, i)
            doChore()             
            i = i - 1        
        else:
            print("Thread_id",tid," No more tasks")
            os._exit(0)           
        lock.release()

url = 'http://www.smzdm.com/p'

if __name__ == "__main__":
    silentRemove("tmp.txt")
    silentRemove("curl.txt")
    header = \
    {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'smzdm_user_source=7990A03AD65DB60A2F455FBB515BF170; __gads=ID=b0c06b1ba0f1c4fe:T=1454079839:S=ALNI_MYEy-ry7FAu4Vg_5x_jyWv8_Ytl4w; bdshare_firstime=1454079843620; AJSTAT_ok_times=4; userId=8166376030; __jsluid=8bd3efcd9180066749abfe076c483f28; smzdm_user_view=D268849003A4B08B81AC611B6306A65C; wt3_eid=%3B999768690672041%7C2146194024900415599%232148181478000775469; s_his=%E6%B7%98%E5%AE%9D; PHPSESSID=72dl6hl5h0j3t4f0i317fg7q87; isFirstUser=yes; Hm_lvt_9b7ac3d38f30fe89ff0b8a0546904e58=1479739640,1480253948,1481814133,1481896561; Hm_lpvt_9b7ac3d38f30fe89ff0b8a0546904e58=1481969874; _ga=GA1.2.1882084856.1454079834; amvid=5c2daa8c6279bf120d0b5c86b8f1a274',
        'Host':'www.smzdm.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

    i    = 6754962
    lock = threading.Lock()

    booth(0, url, header)
    #for k in range(10):
    #    new_thread = threading.Thread(target=booth,args=(k, url, header))   # Set up thread; target: the callable (function) to be run, args: the argument for the callable 
    #    new_thread.start()
