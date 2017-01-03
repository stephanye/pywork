# coding: utf-8
from pyquery import PyQuery
import requests
import re
import urlparse
headers = {'User-Agent': 'YisouSpider'}

def get_html(url, encoding, num_retries = 3):
    print '\xe6\xad\xa3\xe5\x9c\xa8\xe6\x8a\x93\xe5\x8f\x96\xef\xbc\x9a', url,
    try:
        r = requests.get(url, headers=headers, timeout=30)
    except Exception as e:
        html = ''
        if num_retries > 0:
            return get_html(url, num_retries - 1)
    else:
        print '\xe7\x8a\xb6\xe6\x80\x81\xe7\xa0\x81', r.status_code
        r.encoding = encoding
        html = r.text

    return html


def get_links(host, html, pattern):
    url_list = re.findall('<a[^>]+href=["\\\'](.*?)["\\\']', html, re.IGNORECASE)
    for url in url_list:
        loc = urlparse.urlparse(url).netloc
        if not loc:
            url = host + url
        if re.match(pattern, url):
            yield url


def get_diy_links(host, html, pattern, suffix):
    d = PyQuery(html)
    pattern = '{} a'.format(pattern)
    try:
        link_list = d(pattern)
    except Exception:
        yield
    else:
        for link in link_list:
            href = PyQuery(link).attr('href').encode('utf-8')
            loc = urlparse.urlparse(href).netloc
            if not loc:
                href = host + href
            if href.endswith(suffix):
                yield href


def get_chapter_urls(host, url, encoding, pattern, suffix):
    html = get_html(url, encoding)
    return get_diy_links(host, html, pattern, suffix)


