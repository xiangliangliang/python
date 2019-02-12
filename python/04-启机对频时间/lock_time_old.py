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

												
time_result = []
BootTime = []
TimeLock = []

for line in open (filename,'r', encoding='utf-8'):
	if "boot app" in line:
		bootup_time = line[:19]						  #获取启机时间戳 ----------------------改改改
		boottime_parse = parse(bootup_time)				  #解析启机时间戳
		BootTime.append(boottime_parse)					  #启机时间序列

		
	elif "Lock=0x3" in line: 
		random_rc_value = re.findall("\d+", line)[-2]     
		lock_time = line[:19]							  #获取lock时间----------------------改改改
		locktime_parse = parse(lock_time)				  #解析lock时间戳
		TimeLock.append(locktime_parse)				  	  #lock时间序列
			
open(filename).close()
print(BootTime[0])
print(TimeLock[0])


for i in range(len(BootTime)):
	time_diff = (TimeLock[i]-BootTime[i]).seconds
	time_result.append(time_diff)						  # -- 时间差

#print(time_result)
a=Counter(time_result)  								  #按rc_pattern 出现次数统计
sorted_x=sorted(a.items(),key=operator.itemgetter(0))	  #按rc pattern 出现次数由小到大排序
a = dict(sorted_x) 

with open(filesave, 'w') as save:				 		  #保存测试结果:rc_pattern出现次数
	for key,value in a.items():
		save.write(str(key)+':'+str(value)+'\t')
	save.write('\n')
	save.write('total times:' + str(len(time_result)))


plt.figure(figsize=(10, 8))								  #画布大小
x = a.keys()												#x轴是rc_pattern
y = a.values()												#y轴是rc_pattern 出现的次数		

plt.subplot(311)											#第一张图：每次lock的时间	
plt.plot(time_result)
plt.xlabel('Boot No.')
plt.ylabel('Lock_Time(s)')

plt.subplot(312)											#第二张图：每个出现的次数
plt.plot(x,y,'o-',markerfacecolor='blue', markersize=3)
plt.xlabel('Lock_Time')
plt.ylabel('Counter')

for c, b in zip(x, y):										#纵坐标值
    plt.text(c, b, b, ha='center', va='bottom', fontsize=7)
	

plt.subplot(313)											#第三张图：每个rc pattern出现的百分比
d = a.copy()
for key in d.keys():										
	d[key] = round(d[key]/len(time_result)*100,2)			#round(xx，2)，取2位小数

x1 = d.keys()												
y1 = d.values()
plt.plot(x1,y1,'d-',markerfacecolor='blue', markersize=3)
plt.xlabel('Lock_Time')
plt.ylabel('Percent(%)')

for e, f in zip(x1, y1):
    plt.text(e, f, f, ha='center', va='bottom', fontsize=7)


plt.show()