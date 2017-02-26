# Python爬虫实例——spider_baike
## 目标：
- 抓取百度百科关于Python词条下1000个链接页面的数据，并输出到output.html文件。

## 目标细化：
- 实例目标：百度百科Python词条相关词条网页-标题和简介
- 入口页：http://baike.baidu.com/view/21087.htm
- URL格式：
    - 词条网页URL：/view/125370.htm
- 数据格式
    - 标题：`<dd class='lemmaWgt-lemmaTitle-title'><h1>**</h1></dd>`
    - 简介：`<div class='lemma-summary'>***<div>`
- 页面编码：UTF-8

## 需要的运行环境：
pycharm、Python2.7、BeautifulSoup4、urllib2等

## 组件的简要说明

### 主程序 spider_main.py
入口程序，用于指导整个爬虫的运行
> craw(root_url) 爬取内容

### url管理器 url_manager.py
url管理器，对新旧url进行管理
> \__init__() 初始化
> add_new_url(url) 添加新链接
> add_new_urls(urls) 批量添加新链接
> has_new_url() 验证该链接是否已在url池中
> get_new_url() 获取新链接

### 网页下载器 html_downloader.py
网页下载器，用urllib2进行下载
> download(url) urllib2对网页进行下载

### 网页解析器 html_parser.py
网页解析器，运用BeautifulSoup进行网页解析
> \_get_new_urls(page_url,soup) 获取新url
> \_get_new_data(page_url,soup) 获取新数据，解析链接内容
> parse(page_url,html_cont) 规范化数据

### 结果输出组件 html_outputer.py
结果输出组件，对爬取的结果进行输出。
> \__init__() 初始化
> collect_data(data) 数据收集
> output_html() 结果输出