#coding=utf-8
from util import fileutil,sqlcrud,judge
import time

sql="select * from result WHERE state='0' ORDER BY CREATEtime asc limit 0,1"
result=sqlcrud.execute(sql)

#没有答案就休眠  保持一下性能
if result==None or len(result)==0:
    time.sleep(0.5)
else:
    judge.exe(result[0])