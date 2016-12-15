# -*- coding: UTF-8 -*-


import urllib2  
from sgmllib import SGMLParser  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import traceback
import MySQLdb
import time


# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","testpython",charset='utf8')

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据库。
data = cursor.fetchone()

print "Database version : %s " % data



class ListName(SGMLParser):  
    def __init__(self):  
        SGMLParser.__init__(self)  
        self.is_p = ""  
        self.name = []  
    def start_p(self, attrs):  
        self.is_p = 1  
    def end_p(self):  
        self.is_p = ""  
    def handle_data(self, text):  
        if self.is_p == 1:  
            self.name.append(text)  
   

def div_list(ls,n):  
    if not isinstance(ls,list) or not isinstance(n,int):  
        return []  
    ls_len = len(ls)  
    if n<=0 or 0==ls_len:  
        return []  
    if n > ls_len:  
        return []  
    elif n == ls_len:  
        return [[i] for i in ls]  
    else:  
        j = ls_len/n  
        k = ls_len%n  
        ### j,j,j,...(前面有n-1个j),j+k  
        #步长j,次数n-1  
        ls_return = []  
        for i in xrange(0,(n-1)*j,j):  
            ls_return.append(ls[i:i+j])  
        #算上末尾的j+k  
        ls_return.append(ls[(n-1)*j:])  
        return ls_return 


# content = urllib2.urlopen('content_01.txt').read()  
#读取段落
fo = open('content_01.txt','r')
content = fo.read()
fo.close()

#读取图片
piclist = []
piccontent = open('pic.txt')
for pic in piccontent:
	pic=pic.strip()
	piclist.append(pic)

print piclist

listname = ListName()  
listname.feed(content)  
contents = []
for item in listname.name:  
    # item=item.decode('utf8').encode('gbk')
    contents.append(item)
    # print item.decode('utf8').encode('gbk')

# 打乱段落
random.shuffle(contents)

#读取标题
titlelist = []
titles = open('title.txt')
for title in titles:
    title=title.strip()
    titlelist.append(title)

# 设置每篇文章段落数 count_size   统计能生成几篇文章 count_p
count_all = len(contents)
count_size=random.randrange(30,60,1)
count_p = count_all/count_size
print 'count_p:%s' %count_p

#切割文章
p_list = div_list(contents,count_p)
count = len(p_list)
count =1
for p in range(count):
    print p
    con_list = p_list[p]
    try:
        #随机插入图片
        pic_count = random.randrange(3,10,1)
        for i in range(pic_count):
        	rand_pic = random.randrange(0,len(piclist),1)
        	str_pic = '<img src="%s" />' %piclist[rand_pic]
        	con_list.append(str_pic)

        random.shuffle(con_list)
        str_content  = '</p><p>'.join(con_list)
        str_content = '<p>'+str_content+'</p>'

        
        rand_pic = random.randrange(0,len(piclist),1)
        title = titlelist[random.randrange(0,len(titlelist),1)]+','+titlelist[random.randrange(0,len(titlelist),1)]+','+titlelist[random.randrange(0,len(titlelist),1)]
        desc = titlelist[random.randrange(0,len(titlelist),1)]+title
        # 判断标题是否重复
        sql = """SELECT id FROM sys_cms_content WHERE title ='%s' """%(title)
        cursor.execute(sql)
        rowcount=cursor.rowcount
        print 'rowcount:%s' % rowcount
        if rowcount == 0:
            # 插入文章信息
            sql = """INSERT INTO sys_cms_content(cid,title,newsdate,description,headimage)
                     VALUES (%d,'%s',%d,'%s','%s')""" %(1,title,time.time(),desc,piclist[rand_pic])
            print sql
            cursor.execute(sql)
            insertid=db.insert_id()
            print insertid
            # SQL 插入文章内容
            sql = """INSERT INTO sys_cms_content_data_01(id,cid, content)
                     VALUES (%d,%d,'%s')""" %(insertid,1,str_content)

            # 执行sql语句
            cursor.execute(sql)

            # 提交到数据库执行
            db.commit()

		# print '-------------------------------------------------------------------------the %s---------------------------------------------------------------------' %p
		# print str_content
    except Exception,e:
    	str_content = 'error'
    	print ' error  '
        print e.args


# 关闭数据库连接
db.close()