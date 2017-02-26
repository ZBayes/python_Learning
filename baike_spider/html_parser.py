# coding:utf8
# html_parser.py: url网页解析器，运用BeautifulSoup进行网页解析

from bs4 import BeautifulSoup
import re
import urlparse

class HtmlParser(object):
    # 获取新url
    def _get_new_urls(self,page_url,soup):
        new_urls=set()
        # /view/123.html
        links=soup.find_all('a',href=re.compile(r"/view/\d+\.htm"))
        for link in links:
            new_url=link['href']
            new_full_url=urlparse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls

    # 获取新数据，解析链接内容
    def _get_new_data(self,page_url,soup):
        res_data={}

        # url
        res_data['url']=page_url

        # <dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>

        title_node=soup.find('dd',class_="lemmaWgt-lemmaTitle-title").find("h1")
        res_data['title']=title_node.get_text()

        #<div class="lemma-summary" label-module="lemmaSummary"> <div class="para" label-module="para">
        summary_node=soup.find('div',class_='lemma-summary')
        res_data['summary']=summary_node.get_text()

        return res_data

    # 规范化数据
    def parse(self,page_url,html_cont):
        if page_url is None or html_cont is None:
            return

        soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
        new_urls=self._get_new_urls(page_url,soup)
        new_data=self._get_new_data(page_url,soup)
        return new_urls,new_data