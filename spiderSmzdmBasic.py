#!/usr/bin/env python
#--*coding: utf-8*--
#
## file:   spiderSmzdmBasic.py
## author: paldinzhang()
## date:   2016-12-17 18:40:41

'''
  Description:
'''
__author__ = 'CQC'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
#import requests
import os
import errno
import re
import sys
import subprocess
import logging
import logging.handlers
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

logPath = "."
logFileName = "error"
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()
fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, logFileName))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

def silentRemove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python spiderSmzdmBasic.py local|remote"
        quit()
    downloadLocal = sys.argv[1] == "local"
    silentRemove("tmp.txt")
    try:
        url = 'http://www.smzdm.com/p/6754962/'
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

#        r = requests.get(url)
#        print "r", r
        silentRemove("curl.txt")
        strCmd = "curl " + url + " >> curl.txt"
        logger.error("strCmd " + strCmd)
        os.system(strCmd)
        buf = open("curl.txt", "rU").read()
        pattern = re.compile('<div class="article-top-box clearfix">.*?<img itemprop="image" src="(.*?)" alt', re.S)
        images = re.findall(pattern, buf)
        imageUrl = ''.join(images)
        logger.error("imageUrl " + imageUrl)
        k = imageUrl.rfind("/")
        pureImageName = imageUrl[k+1 : ]
        logger.error("pureImageName " + pureImageName)
        if downloadLocal:
            downloadDir = "/var/www/html/pic"
        else:
            downloadDir = "~/Downloads"
        downloadCmd = "wget %s -P %s" %(imageUrl, downloadDir)
        logger.error("downloadCmd " + downloadCmd)
        #download to local
        os.system(downloadCmd)
        
        #push to server
        if not downloadLocal:
            scpCmd = "scp %s/%s root@64.137.186.10:/var/www/html/pic" %(downloadDir, pureImageName)
            logger.error("scpCmd " +  scpCmd)
            os.system(scpCmd)

        #use the file url pushed to server befor 
        imageUrl = "http://www.happystr.com/pic/" + pureImageName

        pattern = re.compile('<div class="article-right".*?<em itemprop="name">\n(.*?)</em>.*?<span class="red">&nbsp;&nbsp;&nbsp;(.*?)元.*?</span></em>', re.S)
        items = re.findall(pattern, buf)
#        print "items", items
#        for item in items:
#            logger.error("item " + item[0] + item[1])
        logger.error("title " + items[0][0])
        logger.error("price " + items[0][1])
        title = items[0][0]
        logger.error(title)
        price = float(items[0][1])

        pattern = re.compile('id="rating_worthy_num">\n(.*?)<\/span>.*?"rating_unworthy_num">\n(.*?)<\/span>', re.S)
        items = re.findall(pattern, buf)
        logger.error("worth " + items[0][0])
        logger.error("unworth " + items[0][1])
        worthyCount = int(items[0][0])
        unworthyCount = int(items[0][1])
        totalCount = worthyCount + unworthyCount

        trackID = "&ali_trackid=2:mm_67738872_18500907_65518477"

        pattern = re.compile('data-url=".*?" href="(.*?)"', re.S)
        items = re.findall(pattern, buf)
        logger.error("click_url " + items[0] + trackID)
        clickUrl = items[0] + trackID 
#
#        #构建请求的request
#        request = urllib2.Request(url,headers = header)
#        #利用urlopen获取页面代码
#        response = urllib2.urlopen(request)
#        #将页面转化为UTF-8编码
#        pageCode = response.read().decode('gb2312')
#        print "pageCode", pageCode
    except urllib2.URLError, e:
        if hasattr(e,"reason"):
            print u"连接什么值得买失败,错误原因",e.reason

    db = MySQLdb.connect("64.137.186.10","tt11","d123g224","tt11", charset='utf8' )
    cursor = db.cursor()
    cursor.execute("SET NAMES utf8")
    cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
    cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
    db.commit()

    cursor.execute("insert into item(title, click_url, img_url, price) VALUES (%s, %s, %s, %s)", (title, clickUrl, imageUrl, price))

    db.commit()
    cursor.close()
    db.close()
