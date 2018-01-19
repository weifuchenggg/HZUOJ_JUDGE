#coding=utf-8
from util import fileutil,sqlcrud
from threading import Thread
import time,os,subprocess,signal,uuid
def exe(result):
    print(result)
    #语言
    language=result[5]
    #代码
    content=result[6]
    systemid=result[0]
    num=str(result[1])
    username=result[2]
    competname=result[8]

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
    sqlcrud.executeVoid("update result SET state='"+str(k)+"' where systemid='"+systemid+"'")
    if k==7:
        return

    #查找测试用例
    sql="select * from testcase where problemid="+num
    testcase=sqlcrud.execute(sql)
    dex=1
    for tcone in testcase:
        #运行
        testInput=tcone[2]
        k=running(filetype,testInput)
        if k==4 or k==6:
            print("用例 "+str(dex)+":运行错误 或者 超时 ！！")
            sqlcrud.executeVoid("update result SET state='"+str(k)+"' where systemid='"+systemid+"'")
            return
        test_output=tcone[3]
        #判断答案是否对
        k=judgeAns(k,test_output)
        if k==3:
            print("用例 "+str(dex)+":答案错误！！！")
            sqlcrud.executeVoid("update result SET state='"+str(k)+"' where systemid='"+systemid+"'")
            return
        print("用例 "+str(dex)+":通过！！！")
        dex+=1
    print("恭喜  ac  ！！ ")
    sqlcrud.executeVoid("update result SET state='0' where systemid='"+systemid+"'")
    sql="select COUNT(1) from accept WHERE num="+num+" and  username='"+username+"'"
    rs=sqlcrud.execute(sql)
    cnt=rs[0][0]
    if cnt==0:
        myid=str(uuid.uuid1())
        if competname==None:
            competname=""
        sql="INSERT INTO `accept` VALUES ('"+myid+"', '"+username+"', '"+num+"', '"+competname+"')"
        sqlcrud.executeVoid(sql)
        sql="UPDATE USER SET ac=ac+1 WHERE username='"+username+"'"
        sqlcrud.executeVoid(sql)
        if competname!="" and competname!=None:
            sql="UPDATE register SET ac=ac+1 WHERE username='"+username+"' AND  competname='"+competname+"'"
            sqlcrud.executeVoid(sql)
            pass
        print("用户"+username+" ac 增加1")
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
    p=os.system(command)
    if p==0:
        print("编译成功")
        return 1
    print("编译失败")
    return 7

s=[]
def run(p,testInput):
    global s
    s=p.communicate(testInput.encode('gbk'))
    pass

#执行
def running(filetype,testInput=""):
    global s
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
    t=Thread(target=run,args=(p,testInput))
    t.start()
    t.join(1)
    #运行超时
    if p.returncode==None:
        #os.kill(p.pid,signal.SIGKILL)

        #强制结束进程
        #print('taskkill.exe /F /T /pid:'+str(p.pid))
        pp=subprocess.Popen('taskkill.exe /F /T /pid:'+str(p.pid), stdin = subprocess.PIPE,
                         stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
        print("运行超时")
        return 6
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