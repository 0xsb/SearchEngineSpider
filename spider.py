#!/usr/bin/env python
#coding: utf-8 -*
import urllib2
import urllib
import simplejson
import sys
import urlparse
from bs4 import BeautifulSoup

'''
用于爬行百度、google的搜索结果
用法python spider.py keyword pageNo.
当运行爆出 NO module named XXX 则请使用pip.exe 安装所对应的模块
程序每运行一次，url.txt内容将会重写，请妥善保存结果。
'''
if len(sys.argv) < 2:
    print 'Usage:', os.path.basename(sys.argv[0]), 'keyword', 'page'
    sys.exit()
result = sys.path[0]+'\\'+'url.txt'#爬行结果保存文件
ktxt = sys.path[0]+'\\'+'keyword.txt'#关键词保存至该文件
wordtxt = open(ktxt,'a+')
for key in wordtxt.readlines():# 对搜索的关键词进行检查，
    key = key.strip()
    if key == sys.argv[1]:
        print '[!]This keyword has benn searched !'
        sys.exit()
wordtxt.writelines(str(sys.argv[1]+'\n'))
# 开始爬行百度部分
baidu =  'http://www.baidu.com/s'
print '[!] Start spider on Baidu search engine'
baidulist = []
pages = range(1,int(sys.argv[2]),1)
for page in pages:
    data = {'wd':urllib.quote(str(sys.argv[1])),'pn':str(page-1)+'0','tn':'baidurt','ie':'utf-8','bsst':'1'}
    data = urllib.urlencode(data)
    url = baidu+'?'+data
    print '[!] This is page:'+str(page)
    # 组合出url之后，开始访问页面并取出爬行出来的连接
    try:
        request = urllib2.Request(url)
            #print url
        response = urllib2.urlopen(request)
    except urllib2.HttpError,e:
        print e.code
        exit(0)
    except urllib2.URLError,e:
            #print e.reason
        exit(0)
    html = response.read()
    soup = BeautifulSoup(html,"html.parser")
    td = soup.find_all(class_='f')
    for t in td:
        #print t.h3.a.get_text()
        #print 'Got Url ==> '+t.h3.a['href']
        link = t.h3.a['href'].encode("utf-8")
        #print type(t.h3.a['href'])
        parse = urlparse.urlparse(link)
        baidulist.append(parse.hostname)#此处使用了urlparse匹配出url中的hostname字段，写入列表baidulist
# 百度爬行部分结束
'''
f1 = list(open('pre'))
f2 = list(set(f1))
for j in f2:#需要取出其域名，并进行去重复
    print j.strip()
    op.write(j.strip()+'\n')
op.close()
'''
print '[!] Baidu spider done.'
print '[!] Start to spider google search engine'
# 开始google 爬行部分
gkeyword = urllib.quote(str(sys.argv[1]))
glist = []
for x in range(1,int(sys.argv[2])):
    print "[!] This is page:%s"%(x+1)
    Num = x * 4
    url = ('https://ajax.googleapis.com/ajax/services/search/web'
                  '?v=1.0&q=%s&rsz=8&start=%s') % (urllib.quote(gkeyword),x)
    try:
        request = urllib2.Request(url, None, {'Referer': 'http://www.sina.com'})
        response = urllib2.urlopen(request)
        results = simplejson.load(response)
        infoaaa = results['responseData']['results']
    except Exception,e:
        print str(e)
    else:
        for minfo in infoaaa:
            #print minfo['url']
            uuu = minfo['url'].encode("utf-8")
            ttt = urlparse.urlparse(uuu)
            glist.append(ttt.hostname)
print '[!] Google spider done!'
print '[!] Take the url write to url.txt'
#google 爬行部分结束
rlist = list(set(baidulist+glist))
f = open(result,'w')
for name in rlist:
    print '[!]Got url ==>',name
    f.write(name+'\n')
f.close()
