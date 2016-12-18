#!/usr/bin/env python
#--*coding: utf-8*--
#
## file:   spiderSmzdmBasic.py
## author: paldinzhang(paldinzhang@tencent.com)
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
reload(sys)
sys.setdefaultencoding('utf8')

def silentRemove(filename):
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
#糗事百科爬虫类
class QSBK:

    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        #初始化headers
        self.headers = { 'User-Agent' : self.user_agent }
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False
    #传入某一页的索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            #构建请求的request
            request = urllib2.Request(url,headers = self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接糗事百科失败,错误原因",e.reason
                return None


    #传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None
        pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                         'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        #用来存储每页的段子们
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            #是否含有图片
            haveImg = re.search("img",item[3])
            #如果不含有图片，把它加入list中
            if not haveImg:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR,"\n",item[1])
                #item[0]是一个段子的发布者，item[1]是内容，item[2]是发布时间,item[4]是点赞数
                pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[4].strip()])
        return pageStories

    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1
    
    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            input = raw_input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t发布时间:%s\t赞:%s\n%s" %(page,story[0],story[2],story[3],story[1])
    
    #开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)


if __name__ == "__main__":
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
        print "strCmd", strCmd
        os.system(strCmd)
        buf = open("curl.txt", "rU").read()
        pattern = re.compile('<div class="article-top-box clearfix">.*?<img itemprop="image" src="(.*?)" alt', re.S)
        images = re.findall(pattern, buf)
        print "images", images
        imageUrl = ''.join(images)
        print "imageUrl", imageUrl
        for image in images:
            print "image", image

        pattern = re.compile('<div class="article-right".*?<em itemprop="name">\n(.*?)</em>.*?<span class="red">(.*?)</span></em>', re.S)
        items = re.findall(pattern, buf)
        print "items", items
        for item in items:
            print "item ", item[0], item[1]

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

