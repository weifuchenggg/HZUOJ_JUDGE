#coding=utf-8
import pymysql
localhost="localhost"
username="root"
password="root"
dataname="test"
def execute(sql):
    db = pymysql.connect(localhost,username,password,dataname,charset='utf8')
    cursor=db.cursor()
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return results
def executeVoid(sql):
    db = pymysql.connect(localhost,username,password,dataname,charset='utf8')
    cursor=db.cursor()
    cursor.execute(sql)
    cursor.close()
    db.commit()
    db.close()
def decode(kind,code):
    db = pymysql.connect(localhost,username,password,dataname,charset='utf8')
    cursor=db.cursor()
    cursor.execute("select * from dictionary where kind='"+kind+"' AND code='"+code+"'")
    results=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return results
# show columns from 表名;
# describe 表名;
# show create table 表名;
#
# use information_schema
# select * from columns where table_name='表名';