# coding: utf-8
"""
Python版火车头采集器简版
主要实现功能：
1. 可对列表页分页进行批量采集
2. 提取内容页的标题和正文文本内容，站不支持内容分页采集
4. 结果只能保存为txt文件，每篇文章以空行分隔， 第一行为标题，接着是正文内容
需要安装的第三方库：
1. requests安装方法：pip install requests
2. pyquery安装方法：pip install pyquery
本脚本只支持在Python2.7.x版本下运行
作者：brooks
广告：来itseo，学习牛逼的SEO技术，带你装逼带你飞 地址：www.itseo.net
"""
from Queue import Queue
from getlist import get_chapter_urls
from getcontent import ContentSpider
import urlparse


if __name__ == '__main__':
    # 抓取配置
    # 结果保存文件, 无需手工创建，程序自动生成
    writer = open("shehuinews.txt", 'a')
    # 要抓取的url列表页配置
    start = 2  # 起始页
    end = 2  # 结束页
    step = 1  # 公差
    chapter_indexurl = 'http://www.mnw.cn/news/shehui/'  # 列表页首页，对于不符合分页规则的列表页首页可在此添加，符合的则留空
    chapter_url = "http://www.mnw.cn/news/shehui/index-{0}.html"  # 列表页规则配置 {0}为分页页码位置
    # 详情页url所在 css 路径
    url_pattern = '.list3 .item'
    # 详情页url后缀名
    suffix = '.html'
    # 详情页标题所在标签
    title_pattern = 'h1'
    # 详情页内容所在路径 精确到段落
    content_pattern = '.icontent p'
    # 网页编码，必须填写正确，否则会出现乱码
    encoding = 'utf-8'
    # 线程数量
    num_thread = 15

    # 主程序执行部分无需修改
    queue = Queue()
    chapter_url_list = [chapter_url.format(i) for i in xrange(start, end+1, step)]
    if chapter_indexurl: chapter_url_list.insert(0, chapter_indexurl)
    for chapter_url in chapter_url_list:
        host = "http://{0}".format(urlparse.urlparse(chapter_url).netloc)
        result_urls = {url for url in get_chapter_urls(host, chapter_url, encoding, url_pattern, suffix)}
        for url in result_urls:
            queue.put(url)
    total = queue.qsize()
    for i in range(num_thread):
        c = ContentSpider(queue, writer, title_pattern, content_pattern, encoding)
        c.setDaemon(True)
        c.start()
    queue.join()
    print '抓取完毕，共抓取{}条数据'.format(total)
