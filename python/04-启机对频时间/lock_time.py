#F5
#W:cmd /k C:/Users/user/AppData/Local/Programs/Python/Python37-32/python.exe "$(FULL_CURRENT_PATH)"& PAUSE & EXIT  -- alt+w
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
import time
filename = tkinter.filedialog.askopenfilename(title='请选择测试文件:')    # 选择测试结果文件
filesave = tkinter.filedialog.askopenfilename(title='请选择保存文件:')	  #选择测试结果保存文件

												
time_result = []
BootTime = []
TimeLock = []
i=0 
j=0
with open(filesave, 'w') as save:
	save.write(str(time.asctime( time.localtime(time.time()) ))+'\r\n')
	
for line in open (filename,'r', encoding='utf-8'):
	with open(filesave, 'a') as save:
		if "boot app" in line:
			bootup_time = line[:19]						  #获取启机时间戳 
			boottime_parse = parse(bootup_time)				  #解析启机时间戳
			BootTime.append(boottime_parse)					#启机时间序列
			#print(str(i)+'- boot -'+str(BootTime[i]))
			save.write(str(i)+': boot -'+str(BootTime[i])+'\n')
			i=i+1

			
		elif "Lock=0x3" in line: 
			#random_rc_value = re.findall("\d+", line)[-2]     
			lock_time = line[:19]							  #获取lock时间
			locktime_parse = parse(lock_time)				  #解析lock时间戳
			TimeLock.append(locktime_parse)					  #lock时间序列
			time_diffent = str((TimeLock[j]-BootTime[i-1]).seconds)
			time_result.append(time_diffent)
			#print(str(j)+'！lock ！'+str(TimeLock[j]))
			#print((TimeLock[j]-BootTime[i-1]).seconds)
			#print('\n')
			save.write(str(j)+': lock -'+str(TimeLock[j])+'\n')
			save.write('lock time: '+time_diffent+'\r\n\r\n')
				
			j =j+1

			

a=Counter(time_result)  								  
sorted_x=sorted(a.items(),key=operator.itemgetter(0))	  #按lock 出现次数由小到大排序
a = dict(sorted_x) 

with open(filesave, 'a') as save:				 		  #保存测试结果:lock出现次数
	save.write(str(time_result)+'\r\n')
	for key,value in a.items():
		save.write(str(key)+':'+str(value)+'\t')
	save.write('\n')
	save.write('total times:' + str(len(time_result)))

