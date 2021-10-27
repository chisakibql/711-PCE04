def skip(fp,n):
    # 跳n行
    for i in range(n):
        fp.readline()
    return

def skipto(fp, creteria):
    # 直到读取行s含有creteria时停止读取
    # 换言之，相当于跳跃到creteria下一行
    while True:
        s = fp.readline()
        if creteria in s:
            break
    return

def readsegment(fp):
    # SCE -> SHE
    sce2she = 0.241
    # 定义列表，电量数据我们不要
    lstv = []
    lsta = []

    # 读掉Segment行
    fp.readline()
    
    # 读取数据，将格式转换存入列表，直到空行
    while True:
        s = fp.readline()[:-1]
        if s == "\n" or s == "":
            break
        s = s.split(",")
        lstv.append(float(s[0])+sce2she)
        lsta.append(-float(s[1]))   # 纵坐标相差一个负号，标准不同
    
    # 返回电压、电流数据
    return lstv, lsta

def parser(path):
    # 打开路径为path的文件，模式为只读
    fp = open(path,"r")

    # 跳过8行
    skip(fp,8)

    # 定义参数列表
    paralst = []
    
    # 对接下来的9行逐行读取，按照空格分割字符串，并将最后一部分存入参数列表
    for i in range(9):
        s = fp.readline().split()
        paralst.append(s[-1])
    
    # 读取直到出现Potential/V, Current/A, Charge/C
    # 这里的代码比较冒险，但总而言之也是可以接受的，毕竟我们相信工作站软件会输出一行这个
    skipto(fp, "Potential/V, Current/A, Charge/C\n")
    # 再跳一行
    fp.readline()
    
    # 那么，现在光标所在的是Segment 1:的行首。
    # 已知第六个Parameter（对应paralst[5]）是Segment的字符串
    # 进行数据格式转换，转换为整数
    number_of_segment = int(paralst[5])
    
    # 将除了最后2个之外的弃去
    for i in range(number_of_segment - 2):
        readsegment(fp)
    # 读取最后2个
    tmplv1, tmpla1 = readsegment(fp)
    tmplv2, tmpla2 = readsegment(fp)

    # 连接最后两个segment的列表
    tmplv1.extend(tmplv2)
    tmpla1.extend(tmpla2)
    tmplv1.append(tmplv1[0])
    tmpla1.append(tmpla1[0])

    # 关闭fp
    fp.close()
    
    # 返回参数列、v、a
    return paralst, tmplv1, tmpla1


def sepparser(path):
    # 打开路径为path的文件，模式为只读
    fp = open(path,"r")

    # 跳过8行
    skip(fp,8)

    # 定义参数列表
    paralst = []
    
    # 对接下来的9行逐行读取，按照空格分割字符串，并将最后一部分存入参数列表
    for i in range(9):
        s = fp.readline().split()
        paralst.append(s[-1])
    
    # 读取直到出现Potential/V, Current/A, Charge/C
    # 这里的代码比较冒险，但总而言之也是可以接受的，毕竟我们相信工作站软件会输出一行这个
    skipto(fp, "Potential/V, Current/A, Charge/C\n")
    # 再跳一行
    fp.readline()
    
    # 那么，现在光标所在的是Segment 1:的行首。
    # 已知第六个Parameter（对应paralst[5]）是Segment的字符串
    # 进行数据格式转换，转换为整数
    number_of_segment = int(paralst[5])
    
    # 将除了最后2个之外的弃去
    for i in range(number_of_segment - 2):
        readsegment(fp)
    # 读取最后2个
    tmplv1, tmpla1 = readsegment(fp)
    tmplv2, tmpla2 = readsegment(fp)

    # 关闭fp
    fp.close()
    
    # 返回参数列、v、a
    return paralst, tmplv1, tmpla1, tmplv2, tmpla2
