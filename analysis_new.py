import vaparser as vap
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
# 文件列表
files = [
    "./lbq20211021/blank_n/blank_scan_n01.txt",
    "./lbq20211021/blank_n/blank_scan_n02.txt",
    "./lbq20211021/blank_n/blank_scan_n05.txt",
    "./lbq20211021/o2n/o2_ngs.txt",
    "./lbq20211021/o2n/o2_ngn.txt",
    "./lbq20211021/o2n/o2_nnn.txt",
    "./lbq20211021/meoh/meoh_2.txt"
]

# 定义数据表
data_v1 = []
data_a1 = []
data_v2 = []
data_a2 = []
data_v = []
data_a = []
data_para = []

# 读取数据
for i in range(len(files)):
    tmpdp, tmpdv1, tmpda1, tmpdv2, tmpda2 = vap.sepparser(files[i])
    data_v1.append(tmpdv1)
    data_v2.append(tmpdv2)
    data_a1.append(tmpda1)
    data_a2.append(tmpda2)
    data_para.append(tmpdp)
    data_v.append(tmpdv1+tmpdv2)
    data_v[i].append(tmpdv1[0])
    data_a.append(tmpda1+tmpda2)
    data_a[i].append(tmpda1[0])

# A1 不同搅拌速度氮气饱和硫酸溶液中Pt电极的CV曲线
for i in range(3):
    plt.plot(data_v[i+3], data_a[i], label="v=%sV/s"%data_para[i][4])
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("A1.png")
plt.show()
plt.clf()

# A2 氮气饱和硫酸溶液中Pt电极的CV曲线与双电层的计算
plt.plot(data_v[0],data_a[0], label="CV-Curve")
# 计算双电层范围
start_double_layer = 350
area = np.sum([(data_a[0][i+1]-data_a[0][start_double_layer])*np.abs(data_v[0][i+1]-data_v[0][i]) for i in range(start_double_layer)])
print(area,area/0.021e-3)
doublelayer_v = data_v[0][:start_double_layer]
doublelayer_a = [data_a[0][start_double_layer] for i in range(start_double_layer)]
plt.plot(doublelayer_v,doublelayer_a,linestyle="--")
plt.fill_between(doublelayer_v, doublelayer_a, data_a[0][:start_double_layer], color="pink", alpha=0.5, label=r"$Q_{H,desorp}$")
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("A2.png")
plt.show()
plt.clf()

# B1 氧气饱和硫酸溶液中Pt电极的LSV
labels = ["Ventilate & Stir", "Ventilate only", "Static"]
for i in range(3):
    plt.plot(data_v2[i+3],data_a2[i+3],label=labels[i])
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("B1.png")
plt.show()
plt.clf()

# B2 氧气饱和硫酸溶液中Pt电极ORR反应起始还原电位
plt.plot(data_v2[5],data_a2[5],label="O2")
plt.plot(data_v2[0],data_a2[0],label="blank")
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("B2.png")
plt.show()
plt.clf()

# B3 氧气饱和硫酸溶液中Pt电极ORR反应起始还原电位与空白之差
plt.plot(data_v2[0],[data_a2[5][i]-data_a2[0][i] for i in range(len(data_a2[0]))],label="O2 vs. blank")
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("B3.png")
plt.show()
plt.clf()


# B4 氧气饱和硫酸溶液中Pt电极的CV
labels = ["Ventilate & Stir vs. blank", "Ventilate only vs. blank", "Static vs. blank"]
for i in range(3):
    plt.plot(data_v[i+3],[data_a[i+3][j] - data_a[0][j] for j in range(len(data_a[0]))],label=labels[i])
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("B4.png")
plt.show()
plt.clf()

# C1 甲醇ORR
plt.plot(data_v[6],data_a[6],label="MeOH")
plt.plot(data_v[0],data_a[0],label="blank")
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("C1.png")
plt.show()
plt.clf()

# C2 甲醇扣背景ORR
plt.plot(data_v[6],[data_a[6][i]-data_a[0][i] for i in range(len(data_a[0]))],label="MeOH vs. blank")
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("C2.png")
plt.show()
plt.clf()

# C3 甲醇扣背景LSV-ORR
plt.plot(data_v1[6],[data_a1[6][i]-data_a1[0][i] for i in range(len(data_a1[0]))],label="MeOH vs. blank")
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("C3.png")
plt.show()
plt.clf()

# D1 甲醇-氧气
plt.plot(data_v1[6],[data_a1[6][i]-data_a1[0][i] for i in range(len(data_a1[0]))],label="MeOH vs. blank")
plt.plot(data_v2[0],[-data_a2[5][i]+data_a2[0][i] for i in range(len(data_a2[0]))],label="O2 vs. blank")
plt.legend()
plt.xlabel(r"Potential $U$/V vs. SHE")
plt.ylabel(r"Current $I$/A")
plt.savefig("D1.png")
plt.show()
plt.clf()

# D2 电压 vs. 电流
meohvb = [data_a1[6][i]-data_a1[0][i] for i in range(len(data_a1[0]))]
o2vb = [-data_a2[5][i]+data_a2[0][i] for i in range(len(data_a1[0]))]
start_current = 4.5686468e-6
end_current = 0.5e-6
# for i in range(len(meohvb)):
#     print(i,data_v1[6][i],meohvb[i],data_v2[5][i],o2vb[i])
meoh_start = 374
meoh_end = 704 
o2_start = 0
o2_end = 1000
ylst = [end_current+(start_current-end_current)/500*i for i in range(500)]
meoh_interpol = scipy.interpolate.interp1d(meohvb[meoh_start:meoh_end],data_v1[6][meoh_start:meoh_end])
o2_interpol = scipy.interpolate.interp1d(o2vb[o2_start:o2_end],data_v2[0][o2_start:o2_end])
meoh_v = meoh_interpol(ylst)
o2_v = o2_interpol(ylst)
plt.plot(ylst,meoh_v,label="MeOH vs. blank")
plt.plot(ylst,o2_v,label="O2 vs. blank")
plt.legend()
plt.ylabel(r"Potential $U$/V vs. SHE")
plt.xlabel(r"Current $I$/A")
plt.savefig("D2.png")
plt.show()
plt.clf()

# D3 功率输出曲线
potlst = [o2_v[i]-meoh_v[i] for i in range(len(o2_v))]
powlst = [potlst[i]*ylst[i] for i in range(len(ylst))]
plt.plot(potlst,powlst)
plt.xlabel(r"Potential $U$/V")
plt.ylabel(r"Power $P$/W")
plt.savefig("D3.png")
plt.show()
plt.clf()
print(max(powlst),potlst[powlst.index(max(powlst))])