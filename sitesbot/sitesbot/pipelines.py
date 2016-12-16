# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

# class SitesbotPipeline(object):
#     def process_item(self, item, spider):
#         return item

# class MySQLStoreCnblogsPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool

#     @classmethod
#     def from_settings(cls, settings):
#         dbargs = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset='utf8',
#             cursorclass = MySQLdb.cursors.DictCursor,
#             use_unicode= True,
#         )
#         dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
#         return cls(dbpool)

#     #pipeline默认调用
#     def process_item(self, item, spider):
#         d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
#         d.addErrback(self._handle_error, item, spider)
#         d.addBoth(lambda _: item)
#         return d

#     #将每行更新或写入数据库中
#     def _do_upinsert(self, conn, item, spider):
#         linkmd5id = self._get_linkmd5id(item)
#         #print linkmd5id
#         now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
#         conn.execute("""
#                 select 1 from cnblogsinfo where linkmd5id = %s
#         """, (linkmd5id, ))
#         ret = conn.fetchone()

#         if ret:
#             conn.execute("""
#                 update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
#             """, (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id))
#             #print """
#             #    update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
#             #""", (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id)
#         else:
#             conn.execute("""
#                 insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated) 
#                 values(%s, %s, %s, %s, %s, %s)
#             """, (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now))
#             #print """
#             #    insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
#             #    values(%s, %s, %s, %s, %s, %s)
#             #""", (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now)

#     #获取url的md5编码
#     def _get_linkmd5id(self, item):
#         #url进行md5处理，为避免重复采集设计
#         return md5(item['link']).hexdigest()
#     #异常处理
#     def _handle_error(self, failue, item, spider):
#         log.err(failure)   


class MySQLStoreDmozPipeline(object):
	def __init__(self,dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls,settings):
		dbargs = dict(
			host = settings['MYSQL_HOST'],
			db = settings['MYSQL_DBNAME'],
			user = settings['MYSQL_USER'],
			passwd = settings['MYSQL_PASSWD'],
			charset = 'utf-8',
			cursorclass = MySQLdb.cursors.DictCursor,
			use_unicode = True,
			)
		dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)
		return cls(dbpool)

	def process_item(self,item,spider):
		print '------------------------uninsert-------------------------------------------'
		# d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
		linkmd5id = 1
		now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
		conn.execute("""
			select 1 from cnblogsinfo where linkmd5id = %s
		""",(linkmd5id, ))
		ret = conn.fetchone()

		if ret:
			conn.execute("""
				update cnblogsinfo set title =%s,description =%s,link = %s, listUrl =%s,updated=%s where linkmd5id =%s
			""",(item['title'],item['desc'],item['link'],item['link'],now,linkmd5id))
		else:
		    conn.execute("""
		        insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated) 
		        values(%s, %s, %s, %s, %s, %s)
		    """, (linkmd5id, item['title'], item['desc'], item['link'], item['link'], now))
		print '------------------------222222222222-------------------------------------------'
		d.addErrback(self._handle_error,item, spider)
		d.addBoth(lambda _: item)
		return d
	
	def _do_upinsert(self,conn,item,spider):
		# linkmd5id = self._get_linkmd5id(item)
		print '------------------------35665656565-------------------------------------------'
		linkmd5id = 1
		now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
		conn.execute("""
			select 1 from cnblogsinfo where linkmd5id = %s
		""",(linkmd5id, ))
		ret = conn.fetchone()

		if ret:
			conn.execute("""
				update cnblogsinfo set title =%s,description =%s,link = %s, listUrl =%s,updated=%s where linkmd5id =%s
			""",(item['title'],item['desc'],item['link'],item['link'],now,linkmd5id))
		else:
		    conn.execute("""
		        insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated) 
		        values(%s, %s, %s, %s, %s, %s)
		    """, (linkmd5id, item['title'], item['desc'], item['link'], item['link'], now))

	#获取url的md5编码
	def _get_linkmd5id(self, item):
		return md5(item['link']).hexdigest()
	#异常处理
	def _handle_error(self, failue, item, spider):
		log.err(failure)






