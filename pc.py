#coding=utf-8
from urllib import request
response=request.urlopen("https://wenku.baidu.com/view/a7624331443610661ed9ad51f01dc281e53a560e.html")
print(response.read().decode("gbk"))