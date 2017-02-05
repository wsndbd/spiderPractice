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

if __name__ == "__main__":
    fCurl = open("curl.txt.test", "rU")
    buf = fCurl.read()
    fCurl.close()
    pattern = re.compile('<div class="article-right".*?<em itemprop="name">\n(.*?)</em>.*?<span class="red">&nbsp;&nbsp;&nbsp;(.*?)</span></em>', re.S)
    items = re.findall(pattern, buf)
    print "items", items
    for item in items:
        logger.error("item " + item[0] + item[1])
    logger.error("title " + items[0][0])
    logger.error("price " + items[0][1])
    string = items[0][1] 
    string = string.decode("utf-8")
    filtrate = re.compile(u'[0-9.]')#非中文
    print ''.join(re.findall(filtrate, items[0][1]))
    filtrate = re.compile(u'[\u4E00-\u9FA5]')#非中文
    items1 =  re.findall(filtrate, items[0][1])
    print "items1", items1
    print "len(items1)", items1, items1[0]
    filtered_str = filtrate.sub(r' ', string)#replace
    print filtered_str
    title = items[0][0]
    logger.error(title)
    price = float(filtered_str)
    
