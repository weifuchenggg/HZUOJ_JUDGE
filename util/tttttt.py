import re,os
s=""
p=[]
while 1:
    s=input()
    if s=="0":
        break
    s=s.strip(" ")
    s=s.strip("\t")
    if s!="":
        p.append(s)
print(len(p))
pre=""
pre2=""
sc=[]
mc=""
for i in p:

    s=i.split("\t")
    if(i=="数据元列表"):
        break
    mm=re.findall("表[0-9]{1,3}([　 、\w]{4,100}.*)",i)
    kk=len(mm)
    if kk>=1:
        print(i)
        mm[0]=mm[0].strip()
        mm[0]=mm[0].strip("0-9")
        mc=mm[0]
        print(mm)
    if(len(s)>=3 and s[0]!="序号"):
        s1=s[0]
        cnt=len(re.findall("\.",s1))
        if cnt==1:
            s[1]=pre[1].strip()+"_"+s[1].strip()
            u=pre[3]
            s[3].strip()
            if s[3]=="":
                s[3]=u
            ans=""

            for j in s:
                ans=ans+j.strip()+"\t"
            pre2=s
     #       print(ans)
            if len(s)<6:
                ans+=""+"\t"
            ans+=mc+"\t"
            sc.append(ans)
           # print(pre)
            pass
        elif cnt==2:
            s[1]=pre2[1].strip()+"_"+s[1].strip()
            u=pre2[3]
            s[3]=u
            ans=""
            for j in s:
                ans=ans+j.strip()+"\t"
            pre2=s
            if len(s)<6:
                ans+=""+"\t"
      #      print(ans)
            ans+=mc+"\t"
            sc.append(ans)
            pass
        else:
            if len(s)<6:
                i+=""+"\t"
            sc.append(i+"\t"+mc)
     #       print(i)
            pre=s
content=""
l=len(sc)
for i in range(0,l):
    if(i==l-1):
        content+=sc[i]+"\n"
    else:
        cnt1=len(re.findall("\.",sc[i]))
        cnt2=len(re.findall("\.",sc[i+1]))
        if cnt2<=cnt1:
            content+=sc[i]+"\n"
file=open("E:\\ts.txt","w+",encoding="gbk")
file.write(content)
file.close()
