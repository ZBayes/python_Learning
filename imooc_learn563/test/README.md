# Python开发简单爬虫
根据慕课网的学习记下的笔记和程序。  
链接：[Python开发简单爬虫](http://www.imooc.com/learn/563)  
最后更新日期：2017-2-26

[TOC]

## 基础知识
**爬虫**：自动从互联网上获取数据

简单的爬虫架构：
![wormConstruction_simple](https://raw.githubusercontent.com/ZBayes/pic4markdown/master/wormConstruction_simple.png)

简单爬虫运行流程
![wormConstruction_steps](https://raw.githubusercontent.com/ZBayes/pic4markdown/master/wormConstruction_steps.png)

## URL管理器
URL管理器：管理待抓取的URL集合和已抓取URL集合。
- 添加新URL到待爬集合中。
- 判断待添加URL是否在容器中。
- 获取待爬取URL。
- 判断是否还有待爬取URL。
- 将待爬取URL移动到已爬取。

实现方式：
1. 内存：python的set集合
2. 关系数据库，MySQL,urls(url, is_crawled)
3. 缓存数据库：redis的set集合

## 网页下载器
网页下载器：将互联网上URL对应网页下载到本地的工具。
![wormConstruction_downloader](https://raw.githubusercontent.com/ZBayes/pic4markdown/master/wormConstruction_downloader.png)

python的网页下载器
- urllib2-python-官方基础模块
- requests-第三方更强大
- 
urllab2下载器使用方法：

1. 最简捷方法
```python
import urllib2

# 直接请求
response=urllib2.urlopen('http://www.baidu.com')

# 获取状态吗，如果是200表示成功
print response.getcode()

#读取内容
cont=response.read()
```
2. 添加data、http helper
```python
import urllib2

# 创建Request对象
request urllib2.Request(url)

# 添加数据
request.add_data('a','1')
# 添加http的header
request.add_header('User-Agent','Mozilla/5.0')

# 发送请求获取结果
response=urllib2.urlopen(request)
```
3. 添加特殊情景处理器
```python
import urllib2, cookielib

# 创建cookie容器

# 创建一个opener
opener=urllib.build_opener(urllib2.HTTPCookieProcessor(cj))

# 给urllib2安装opener
urllib2.install_opener(opener)

# 使用带有cookie的urllib2访问网页
response=urllib2.urlopen(request)
```

运行实例：
```python
# coding:utf-8
import urllib2,cookielib

url="http://www.baidu.com"

print '方法1'
response1=urllib2.urlopen(url)
print response1.getcode()
print len(response1.read())

print '方法2'
request=urllib2.Request(url)
request.add_header("user-agent","Mozilla/5.0")
response2=urllib2.urlopen(request)
print response2.getcode()
print len(response2.read())

print '方法3'
cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
response3=urllib2.urlopen(request)
print response3.getcode()
print cj
print response3.read()
```
## 网页解析器
网页解析器：从网页中提取有价值数据的工具。
![wormConstruction_analysiser](https://raw.githubusercontent.com/ZBayes/pic4markdown/master/wormConstruction_analysiser.png)

### Beautiful Soup
- python第三方库，用于从HTML或者XML中提取数据，有自己的[官网](https://www.crummy.com/software/BeautifulSoup/)，同时还有[API文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)。
- 其下载方式可在API文档中找到。

用法介绍如下图所示：
![wormConstruction_beautifulSoup](https://raw.githubusercontent.com/ZBayes/pic4markdown/master/wormConstruction_beautifulSoup.png)

对一个标签：
```html
<a href='123.html' class='article_link'>python</a>
```

能有三种方式搜索
1. 节点名称：a
2. 节点属性："href='123.html'，和class=article_link"
3. 节点内容python

语法使用如下：
```python
from bs4 import BeautifulSoup

# 根据HTML网页字符串创建BeautifulSoup对象
soup=BeautifulSoup(
html_doc,               # HTML文档字符串
'html.parser'           # HTML解析器
from_encoding='utf-8'    # HTML文档编码
)

# 搜索节点
# 方法：find_all(name,attrs,string)

# 查找所有标签为a的节点
soup.find_all('a')

# 查找所有标签为a，链接符合/view/123.htm形式的节点
soup.find_all('a',href='/view/123.htm')
soup.find_all('a',href=re.compile(r'/view/\d+\.htm'))

# 查找所有标签为div，class为abc，文字为python节点
soup.find_all('div',class_='abc',string='python')

# 访问节点信息
# 得到节点信息：<a href='1.html'>python<a>

# 获取查找到的a节点的href属性
node.name

# 获取查找到的a节点的href属性
node['href']

# 获取查找到的a节点的链接文字
node.get_text()
```

下面是具体的案例：
```python
# coding:utf-8

# # 测试BeautifulSoup的程序
# import bs4
# print bs4

from bs4 import BeautifulSoup
import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup=BeautifulSoup(html_doc,'html.parser',from_encoding='utf-8')

print '获取所有的链接'
links=soup.find_all('a')
for link in links:
    print link.name,link['href'],link.get_text()


print '获取Lacie的链接'
link_node=soup.find('a',href='http://example.com/lacie')
print link_node,link_node['href'],link_node.get_text()

print '正则匹配'
link_node=soup.find('a',href=re.compile(r"ill"))
print link_node,link_node['href'],link_node.get_text()

print '获取P段落文字'
p_node=soup.find('p',class_="title")
print p_node.name,p_node.get_text()
```

## 最后强调一点
这只是最简单的爬虫，在对某些网址，还有登录、验证码、Ajax、服务器防爬虫、多线程、分布式等问题。有待进一步研究。
