#coding=utf-8
from util import fileutil,sqlcrud
import time,os,subprocess
def exe(result):
    print(result)
    #语言
    language=result[5]
    #代码
    content=result[6]
    systemid=result[0]
    num=str(result[1])

    #类型解码
    typeresult=sqlcrud.decode("oj_language",language)
    if len(typeresult)==0:
        return 0
    typeresult=typeresult[0]
    #文件类型
    filetype=typeresult[4]
    #文件名
    filename="Main"

    #执行的目录
    filepath=os.getcwd()

    #写入文件  进行编译
    fileutil.writefile(filepath,filename+"."+filetype,content)

    #编译
    k=compile(filepath,filetype)
    #sqlcrud.executeVoid("update result SET state='"+str(k)+"' where systemid='"+systemid+"'")
    if k==7:
        return

    #查找测试用例
    sql="select * from testcase where problemid="+num
    testcase=sqlcrud.execute(sql)
    for tcone in testcase:
        #运行
        print(tcone)
        testInput=tcone[2]
        k=running(filetype,testInput)
        if k==4:
            print("运行错误")
            #sqlcrud.executeVoid("update result SET state='"+str(k)+"' where systemid='"+systemid+"'")
            return
        print("运行成功")
        test_output=tcone[3]
        #判断答案是否对
        k=judgeAns(k,test_output)
        if k==3:
            print("答案错误")
            #sqlcrud.executeVoid("update result SET state='"+str(k)+"' where systemid='"+systemid+"'")
            #return
    print(typeresult)

#编译
def compile(filepath,filetype):
    command=""
    if filetype=='java':
        command='javac '+filepath+'\\Main.java'
    elif filetype=='cpp':
        command='gcc '+filepath+'\\Main.cpp'
    elif filetype=='c':
        command='gcc '+filepath+'\\Main.c'
    else:
        return 7
    print(command)
    p=os.system(command)
    if p==0:
        print("编译成功")
        return 1
    print("编译失败")
    return 7

#执行
def running(filetype,testInput=""):
    command=""
    if filetype=='java':
        command='java Main'
    elif filetype=='cpp':
        command='gcc Main'
    elif filetype=='c':
        command='gcc Main'
    else:
        return 7
    p = subprocess.Popen(command, stdin = subprocess.PIPE,
                         stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    p.stdin.flush()
    s=p.communicate(testInput.encode('gbk'))
    p.kill()
    if str(s[1])=="b''" and s[1]!=None:
        return s[0].decode("utf-8")
    else:
        return 4

#判断答案是否正确
def judgeAns(str1,str2):
    str1=str1.strip("\n")
    str2=str2.strip("\n")
    str1=str1.split("\n")
    str2=str2.split("\n")
    if len(str1)!=len(str2):
        return 3
    for dex in range(0,len(str1)):
        i=str1[dex]
        j=str2[dex]
        i=i.rstrip("\r")
        j=j.rstrip("\r")
        i=i.rstrip(" ")
        j=j.rstrip(" ")
        if i!=j:
            return 3
    return 2
    pass