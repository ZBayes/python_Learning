# coding:utf8
# html_downloader.py: 网页下载器，用urllib2进行下载
import urllib2

class HtmlDownloader(object):
    # urllib2对网页进行下载
    def download(self,url):
        if url is None:
            return None

        response=urllib2.urlopen(url)

        if response.getcode()!=200:
            return None

        return  response.read()
