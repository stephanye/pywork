# -*- coding: UTF-8 -*-

def getyi(n):
	a,b=0,1
	while a < n:
		yield a
		a,b = b,a+b


for i in getyi(10):
	print i

