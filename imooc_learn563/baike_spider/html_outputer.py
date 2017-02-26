# coding:utf8
# html_outputer.py: 结果输出器
class HtmlOutputer(object):
    # 初始化
    def __init__(self):
        self.datas=[]

    # 数据收集
    def collect_data(self,data):
        if data is None:
            return
        self.datas.append(data)

    # 结果输出
    def output_html(self):
        fout=open('output.html','w')

        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")

        # 补充：需要将ascii转为utf-8
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
            fout.write("<td>%s</td>" % data['summary'].encode('utf-8'))
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

        fout.close()