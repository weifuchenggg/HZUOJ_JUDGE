#coding=utf-8
from util import fileutil,sqlcrud,judge
import time
def fun():
    sql="select * from result WHERE state='0' ORDER BY CREATEtime asc limit 0,1"
    result=sqlcrud.execute(sql)

    #没有答案就休眠  保持一下性能
    if result==None or len(result)==0:
        time.sleep(1)
        print("未发现用户提交代码\n")
    else:
        judge.exe(result[0])
        time.sleep(0.1)
        print("判题结束\n")

while True:
    fun()