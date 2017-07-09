# coding:utf8
# url_manager.py: url管理器，对新旧url进行管理。

class UrlManager(object):
    # 初始化
    def __init__(self):
        self.new_urls=set()
        self.old_urls=set()

    # 添加新链接
    def add_new_url(self,url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    # 批量添加新链接
    def add_new_urls(self,urls):
        if urls is None or len(urls)== 0:
            return
        for url in urls:
            self.add_new_url(url)

    # 验证该链接是否已在url池中
    def has_new_url(self):
        return len(self.new_urls)!=0

    # 获取新链接
    def get_new_url(self):
        new_url=self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url