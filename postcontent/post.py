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
import math
import difflib


#配置： 地址 用户名 密码 数据库名  class_id classename cid catname content pic title 生成文章数(count)
# db_list = [
#             ["127.0.0.1","root","xxx1024p2p","8spocom",2,'toutiao',1194,'头条','content_01.txt','pic.txt','title.txt',5]
#         ]

db_list = [
            ["127.0.0.1","root","root","testpython",2,'toutiao',1198,'头条','content_01.txt','pic.txt','title.txt',5],
            ["127.0.0.1","root","root","cnblogsdb",1,'hot',10,'热门','content_02.txt','pic.txt','title2.txt',1]
        ]

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

def main(site):
    # 打开数据库连接
    host =site[0]
    user =site[1]
    pwd =site[2]
    dbname =site[3]
    db = MySQLdb.connect(host,user,pwd,dbname,charset='utf8')

    # 发布对应栏目
    class_id = site[4]
    classename=site[5]
    cid = site[6]
    catname = site[7]
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # 使用execute方法执行SQL语句
    cursor.execute("SELECT VERSION()")

    # 使用 fetchone() 方法获取一条数据库。
    data = cursor.fetchone()

    print "Database version : %s " % data

    # content = urllib2.urlopen('content_01.txt').read()  
    #读取段落
    content_file = 'data\%s' %site[8]
    if site[8]=='':
        content_file='data\content_01.txt'
    fo = open(content_file,'r')
    content = fo.read()
    fo.close()

    #读取图片
    piclist = []
    pic_file = 'data\%s' %site[9]
    if site[9]=='':
        pic_file='data\pic.txt'
    piccontent = open(pic_file)
    for pic in piccontent:
        pic=pic.strip()
        piclist.append(pic)


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
    title_file = 'data\%s' %site[10]
    if site[10]=='':
        title_file='data\\title.txt'
    titles = open(title_file)
    for title in titles:
        title=title.strip()
        titlelist.append(title)

    # 设置每篇文章段落数 count_size   统计能生成几篇文章 count_p
    count_all = len(contents)
    count_size=random.randrange(15,40,1)
    count_p = count_all/count_size
    # print 'count_p:%s' %count_p

    #切割文章
    p_list = div_list(contents,count_p)
    # count = len(p_list)
    count = site[11]
    for p in range(count):
        con_list = p_list[p]
        try:
            # 查找标题相关
            title1=titlelist[random.randrange(0,len(titlelist),1)]
            title2=titlelist[random.randrange(0,len(titlelist),1)]
            if title1==title2:
                title2=titlelist[random.randrange(0,len(titlelist),1)]
            title1_about=[]
            title2_about=[]
            for tit in titlelist:
                ratio1 = difflib.SequenceMatcher(None,title1,tit).quick_ratio()
                ratio2 = difflib.SequenceMatcher(None,title2,tit).quick_ratio()
                if ratio1>0.6 and ratio1<1:
                    title1_about.append(tit)

                if ratio2>0.6 and ratio2<1:
                    title2_about.append(tit)
            
            if len(title1_about)==0:
                title1_about.append(title1.decode('utf8')[1:len(title1)-1].encode('utf8'))

            if len(title2_about)==0:
                title2_about.append(title2.decode('utf8')[0:len(title2)-2].encode('utf8'))

            title = title1+','+title2
            desc = title1_about[random.randrange(0,len(title1_about),1)]+title+','+title2_about[random.randrange(0,len(title2_about),1)]
            #随机插入图片
            pic_count = random.randrange(5,12,1)
            for i in range(pic_count):
                rand_pic = random.randrange(0,len(piclist),1)
                str_pic = '<img src="%s" alt="%s" />' %(piclist[rand_pic],title1_about[random.randrange(0,len(title1_about),1)]+','+title2_about[random.randrange(0,len(title2_about),1)])
                con_list.append(str_pic)

            random.shuffle(con_list)
            str_content  = '</p><p>'.join(con_list)
            str_content = '<p>'+str_content+'</p>'

            
            rand_pic = random.randrange(0,len(piclist),1)

            # 判断标题是否重复
            sql = """SELECT id FROM sys_cms_content WHERE title ='%s' """%(title)
            cursor.execute(sql)
            rowcount=cursor.rowcount
            print 'rowcount:%s' % rowcount
            if rowcount == 0:
                # 插入文章信息
                sql = """INSERT INTO sys_cms_content(class_id,catname,cid,title,newsdate,description,headimage,classename)
                         VALUES (%d,'%s',%d,'%s',%d,'%s','%s','%s')""" %(class_id,catname,cid,title,time.time(),desc,piclist[rand_pic],classename)
                cursor.execute(sql)
                insertid=db.insert_id()
                print insertid
                print title
                print '\r'
                # SQL 插入文章内容
                tableindex = '01'
                tableindex = math.ceil(float(insertid)/100000)
                tableindex = int(tableindex)
                if tableindex<10:
                    tableindex = '0'+str(tableindex)
                sql = """INSERT INTO sys_cms_content_data_%s(id,cid, content)
                         VALUES (%d,%d,'%s')""" %(tableindex,insertid,cid,str_content)

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

if __name__=='__main__':
    for i in range(len(db_list)):
        site=db_list[i]
        main(site)
    # main()