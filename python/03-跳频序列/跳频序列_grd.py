#F5
#W:cmd /k C:/Users/user/AppData/Local/Programs/Python/Python37-32/python.exe "$(FULL_CURRENT_PATH)"& PAUSE & EXIT
#CMD WINDOW:python -m ensurepip
# 安装matplotlib: python -m pip matplotlib
# -*- coding: utf-8 -*-  
import matplotlib.pyplot as plt
import operator
import re
import tkinter.filedialog
import sys
from dateutil.parser import parse
from collections import Counter
filename = tkinter.filedialog.askopenfilename(title='请选择测试文件:')    # 选择测试结果文件
filesave = tkinter.filedialog.askopenfilename(title='请选择保存文件:')	  #选择测试结果保存文件



i=1														
time = []					
random_rc = []
time_result = []

for line in open (filename,'r', encoding='utf-8'):
	if "rc_skip patten" in line: 
		random_rc_value = int(re.findall("\d+", line)[-2])        #获取RC序列号
		random_rc.append(random_rc_value)				  #-- RC序列值
		i=i+1					
open(filename).close()


a=Counter(random_rc)  										#按rc_pattern 出现次数统计
sorted_x=sorted(a.items(),key=operator.itemgetter(0))		#按rc pattern 出现次数由小到大排序
a = dict(sorted_x) 

with open(filesave, 'w') as save:				 			 #保存测试结果:rc_pattern出现次数
	for key,value in a.items():
		save.write(str(key)+':'+str(value)+'\t')
	save.write('\n')
	save.write('total times:' + str(len(random_rc)))


plt.figure(figsize=(20, 10))								#画布大小
x = a.keys()												#x轴是rc_pattern
y = a.values()												#y轴是rc_pattern 出现的次数		

plt.subplot(311)											#第一张图：每次启机的rc pattern	
plt.plot(random_rc)
plt.xlabel('Boot No.')
plt.ylabel('RC_Pattern')

plt.subplot(312)											#第二张图：每个rc pattern出现的次数
plt.plot(x,y,'o-',markerfacecolor='blue', markersize=3)
plt.xlabel('RC Pattern')
plt.ylabel('Counter')

for c, b in zip(x, y):										#纵坐标值
    plt.text(c, b, b, ha='center', va='bottom', fontsize=7)
	

plt.subplot(313)											#第三张图：每个rc pattern出现的百分比
d = a.copy()
for key in d.keys():										
	d[key] = round(d[key]/len(random_rc)*100,2)				#round(xx，2)，取2位小数

x1 = d.keys()												
y1 = d.values()
plt.plot(x1,y1,'d-',markerfacecolor='blue', markersize=3)
plt.xlabel('RC Pattern')
plt.ylabel('Percent(%)')

for e, f in zip(x1, y1):
    plt.text(e, f, f, ha='center', va='bottom', fontsize=7)


plt.show()


	
	
