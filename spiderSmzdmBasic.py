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
import requests
import os
import errno
import re
import sys
import subprocess
import datetime
import logging
import logging.handlers
import MySQLdb
import pytz

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

def PageExist(buf):
    #can't find sig <title>404</title>
    pattern = re.compile('<title>404</title>', re.S)
    pageExist = re.findall(pattern, buf) 
    logger.error(pageExist)
    if len(pageExist) <= 0:
        logger.error("page exist")
        return True
    else:
        logger.error("page not exist")
        return False 

def downloadImageAndPushToSever(buf, downloadLocal):
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
    os.system(downloadCmd)

    #push to server
    if not downloadLocal:
        scpCmd = "scp %s/%s root@64.137.186.10:/var/www/html/pic" %(downloadDir, pureImageName)
        logger.error("scpCmd " +  scpCmd)
        os.system(scpCmd)
    #use the file url pushed to server befor 
    imageUrl = "http://www.happystr.com/pic/" + pureImageName
    
    return imagUrl

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python spiderSmzdmBasic.py local|remote lastPFileName"
        quit()

    #是否将图片直接下载到服务器目录，在服务器上运行时为true，否则需要再scp push到服务器指定目录
    downloadLocal = sys.argv[1] == "local"
    pFile = open(sys.argv[2], "r")
    page = pFile.readline().strip()
    logger.error("page " + page)
    pFile.close()
    
    try:
        url = 'http://www.smzdm.com/p/' + page + '/'
        silentRemove("curl.txt")
        strCmd = "curl " + url + " >> curl.txt"
        logger.error("strCmd " + strCmd)
        os.system(strCmd)
        fCurl = open("curl.txt", "rU")
        buf = fCurl.read()
        fCurl.close()

        #judge page exist
        if not PageExist(buf):
            quit() 

        serverImageUrl = downloadImageAndPushToSever(buf, downloadLocal)

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

        pattern = re.compile('<span>更新时间：(.*?)</span>', re.S)
        items = re.findall(pattern, buf)
        #smzdm时间是北京时间gmt+8
        urlDate = datetime.datetime.strptime(items[0], "%Y-%m-%d %H:%M")
        #服务器时间，将来要修改TODO
        localTz = pytz.timezone('Asia/Shanghai')
        localTs = int(time.time())
        localDt = datetime.datetime.fromtimestamp(localTs)
        #使用localize保险
        localDt = localTz.localize(localDt)
        logger.error("localDt " + localDt.__str__())

        smzdmTz = pytz.timezone('Asia/Shanghai')
        smzdmDt = smzdmTz.localize(urlDate)
        smzdmDt.astimezone(smzdmTz)
        logger.error("smzdmDt " + smzdmDt.__str__())

        #数据必须在1小时内
        totalSeconds = (localDt - smzdmDt).total_seconds()

        logger.error("totalSeconds " + str(totalSeconds))
        trackID = "&ali_trackid=2:mm_67738872_18500907_65518477"

        pattern = re.compile('data-url=".*?" href="(.*?)"', re.S)
        items = re.findall(pattern, buf)
        logger.error("click_url " + items[0] + trackID)
        clickUrl = items[0] + trackID 
    except urllib2.URLError, e:
        if hasattr(e,"reason"):
            print u"连接什么值得买失败,错误原因",e.reason

    db = MySQLdb.connect("64.137.186.10","tt11","d123g224","tt11", charset='utf8' )
    cursor = db.cursor()
    cursor.execute("SET NAMES utf8")
    cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
    cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
    db.commit()

    cursor.execute("insert into item(title, click_url, img_url, price) VALUES (%s, %s, %s, %s)", (title, clickUrl, serverImageUrl, price))

    db.commit()
    cursor.close()
    db.close()
