# coding:utf-8
# spider_main.py: 入口程序，用于指导整个爬虫的运行
# from baike_spider import url_manager, html_downloader, html_parser, html_outputer
import url_manager, html_downloader, html_outputer, html_parser

class SpiderMain(object):
    def __init__(self):
        # 初始化
        self.urls=url_manager.UrlManager()
        self.downloader=html_downloader.HtmlDownloader()
        self.parser=html_parser.HtmlParser()
        self.outputer=html_outputer.HtmlOutputer()


    def craw(self,root_url):
        # 爬取内容
        count=1                             # 爬取的数据量
        self.urls.add_new_url(root_url)     # 添加入口链接
        while self.urls.has_new_url():      # 从url池中爬取数据和添加新的url到url池中
            try:
                new_url=self.urls.get_new_url()
                print 'craw %d : % s'%(count,new_url)
                html_cont=self.downloader.download(new_url)
                new_urls,new_data=self.parser.parse(new_url,html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count==1000:
                    break

                count=count+1
            except:                         # 防止链接失效等其他意外错误
                print 'craw failed'

        self.outputer.output_html()

if __name__=="__main__":                    # 主程序
    root_url="http://baike.baidu.com/view/21087.htm"
    obj_spider=SpiderMain()
    obj_spider.craw(root_url)