#coding=utf-8
import os
def readfile(dir):
    file=open(dir,"r+",encoding="utf-8")
    s=file.read()
    file.close()
    return s
def writefile(path,filename,content):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    isExists=os.path.exists(path)
    if isExists==False:
        os.makedirs(path)
    file=open(path+"\\"+filename,"w+",encoding="utf8")
    file.write(content)
    file.close()
#writefile('E:\\test\\aa','hh.java',"dasdas")