import re

#获取类型
def gettype(tp):
    if "bigint"==tp:
        tp="Long"
    elif re.search("varchar",tp):
        tp="String"
    elif re.search("int",tp):
        tp="Integer"
    elif re.search("date",tp) or re.search("time",tp)!=None or re.search("year",tp):
        tp="Date"
    elif re.search("decimal",tp) or re.search("numeric",tp):
        tp='BigDecimal'
    elif re.search("bit",tp):
        tp="Boolean"
    else:
        tp=tp[0].upper()+tp[1:]
    return tp

#获取get方法 参数类型和字段名
def getget(lx,zdm):
    s="\tpublic "
    s+=lx+" get"
    s+=zdm[0].upper()+zdm[1:]+"(){\n"
    s+="\t\treturn this."+zdm+";\n\t}\n\n"
    return s
#获取set方法 参数 类型和字段名
def getset(lx,zdm=""):
    s="\tpublic "
    s+='void'+" set"
    s+=zdm[0].upper()+zdm[1:]+'('+lx+' '+zdm+'){\n'
    s+="\t\tthis."+zdm+" = "+zdm+";\n\t}\n\n"
    return s
