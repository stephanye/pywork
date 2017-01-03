# coding: utf-8
from pyquery import PyQuery
import requests
import threading
import os

class ContentSpider(threading.Thread):

    def __init__(self, queue, writer, title_pattern, content_pattern, encoding):
        super(ContentSpider, self).__init__()
        self.queue = queue
        self.writer = writer
        self.title_pattern = title_pattern
        self.content_pattern = content_pattern
        self.encoding = encoding
        self.headers = {'User-Agent': 'YisouSpider'}

    def run(self):
        while True:
            url = self.queue.get()
            html = self.get_html(url)
            title = self.parse_title(html, self.title_pattern).encode('utf-8').strip()
            content_list = self.parse_content(html, self.content_pattern)
            self.writer.write(title + os.linesep)
            for p in self.process_content(content_list):
                if len(p.strip()) > 0:
                    self.writer.write(p + os.linesep)
                    self.writer.flush()

            self.writer.write(os.linesep)
            self.queue.task_done()

    def get_html(self, url, num_retries = 3):
        print 'Downloading:', url
        try:
            r = requests.get(url, headers=self.headers, timeout=30)
        except Exception as e:
            print e
            html = ''
            if num_retries > 0:
                return self.get_html(url, num_retries - 1)
        else:
            r.encoding = self.encoding
            html = r.text

        return html

    def parse_title(self, html, pattern):
        try:
            d = PyQuery(html)
        except Exception:
            title = ''
        else:
            title = d(pattern).text()

        return title

    def parse_content(self, html, pattern):
        try:
            d = PyQuery(html)
        except Exception:
            content = ''
        else:
            content = d(pattern)

        return content

    def process_content(self, content_list):
        for content in content_list:
            content = PyQuery(content).text().encode('utf-8').lower().strip()
            yield content
