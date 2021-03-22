import math
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
from scipy import stats
from sympy import *
from colorama import Fore, Back, Style


#-----讀入檔案並轉為list，建立 ln(數值) 的list-----#
file = pd.read_excel("M13.xlsx")
shape = file.shape
S = shape[0]

dic = {} #建立偏差量變化的dic
DACC = [] #建立偏差量變化的list
Pre0 = []
Pro0 = []
for a in range(0,S):
    Pro0.append(file['孔隙率(%)'][a])
    Pre0.append(file['圍壓(Mpa)'][a])

Pre = []
Pro = []
for a in range(0,S):
    Pre.append(math.log(Pre0[a]))
    Pro.append(math.log(Pro0[a]))
#-----讀入檔案並轉為list，建立 ln(數值) 的list-----#


#=====由此處進入計算=====#


#-----建立過壓密曲線與正常壓密曲線的list-----#
for z in range(2, int(S/2-0.5)):
    print(Fore.BLACK +'%f MPa ~ %f MPa' % (Pre0[z-1],Pre0[z]))

    PreG = []   #過壓密的壓力list
    ProG = []   #過壓密的孔隙率list
    for a in range(0,z):
        PreG.append(Pre[a])
        ProG.append(Pro[a])

    PreN = []   #正常壓密的壓力list
    ProN = []   #正常壓密的孔隙率list
    for a in range(z,int(S/2+0.5)):
        PreN.append(Pre[a])
        ProN.append(Pro[a])
#-----建立過壓密曲線與正常壓密曲線的list-----#

#-----過壓密線性迴歸-----
    slope, intercept, r_value, p_value, std_err = stats.linregress(PreG, ProG)
    s1 = slope
    i1 = intercept
    r21 = r_value**2
#-----過壓密線性迴歸-----#

#-----正常壓密線性迴歸-----#
    slope, intercept, r_value, p_value, std_err = stats.linregress(PreN, ProN)
    s2 = slope
    i2 = intercept
    r22 = r_value**2
#-----正常壓密線性迴歸-----#

#-----尋找兩線交點-----#
    x = Symbol('x')
    y = Symbol('y')
    f1 = -s1*x + 1*y - i1
    f2 = -s2*x + 1*y - i2
    sol = solve((f1, f2), x, y)
#-----尋找兩線交點-----#

#-----判斷以及轉換-----#
    MCP = math.e**sol[x]
    MPRO = math.e**sol[y]
    ACC = abs(MCP - ((Pre0[z-1] + Pre0[z])/2)) - ((Pre0[z] - Pre0[z-1])/2)
    DACC.append(ACC) #偏差量變化list的寫入
    dic[Pre0[z-1],Pre0[z]] = ACC
    
    if Pre0[z-1] < MCP < Pre0[z]:
        print(Fore.RED + '合理')
    else:
        print(Fore.BLACK + '不合理')
        print('偏差量: ',ACC)
        
    print('最大有效圍壓:',MCP)
    print('最小正常壓密孔隙率:',MPRO)
    print('過壓密R平方 :',r21)
    print('正常壓密R平方:',r22)
    print('R平方總和:',r22+r21)
    print('')
#-----判斷以及轉換-----#


number = list(range(1,int(S/2-1.5)))

print('偏差量變化(list):',DACC)
print('')
print('偏差量變化(dic):',dic)
plt.plot(number,DACC,'r-')