# -* coding:utf-8 -*-
import difflib

query_title='都市狐仙养成记'
query_list = ['都市狐仙养成记','韩娱命运','狐仙养成记','最强网络神豪','都市狐仙','都市狐仙养成记2']

for title in query_list:
	xsd = difflib.SequenceMatcher(None,query_title,title).quick_ratio()
	if xsd>0.5:
		print xsd