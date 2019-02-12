#F5
#W:cmd /k C:/Users/user/AppData/Local/Programs/Python/Python37-32/python.exe "$(FULL_CURRENT_PATH)"& PAUSE & EXIT
# -*- coding: utf-8 -*-  

import csv
import re
import tkinter.filedialog

filename = tkinter.filedialog.askopenfilename(title='请选择测试文件:')      # 选择测试结果文件

filesave = tkinter.filedialog.askopenfilename(title='请选择保存文件:')	  #选择测试结果保存文件

i=1							#判断是命令行还是结果行，奇数表示命令行，偶数表示结果行
index=1						#行号
Result=[]					#结果



# 命令-结果 对应关系			
		
dict_1 = {
		'set_freq_band 5.8G':'Band:5.8G',
		'set_freq_band 2.4G':'Band:2.4G',
		'vt_link_func fixed':'itHopMode:VT Fixed',
		'vt_link_func hopping':'itHopMode:VT Auto',
		'rc_link_func hopping':'rcHopping:RC Auto',
		'rc_link_func fixed':'rcHopping:RC Fixed',
		'vt_test_mode enter':'lock state:unlock',
		'vt_test_mode exit':'lock state:lock',
		'mcs_switch_mode manual':'lock state:lock',
		'mcs_switch_mode auto':'lock state:lock',
		'set_vt_bandwidth 20M':'Bandwidth:20M',
		'set_vt_bandwidth 10M':'Bandwidth:10M',
		'set_vt_qam bpsk':'mcs:0',
		'set_vt_qam qpsk':'mcs:2',
		'set_vt_qam 16qam':'mcs:3',
		'set_vt_qam 64qam':'mcs:4',
		'module_rematch':'lock state:unlock',
		'set_sys_sleep_lever 0':'lock state:lock',
		'set_sys_sleep_lever 1':'lock state:lock',
		'set_sys_sleep_lever 2':'lock state:unlock',
		'set_sys_sleep_lever 3':'lock state:unlock',
		'band_switch_mode auto':'lock state:lock',
		'band_switch_mode manual':'lock state:lock',
		'set_rt_ldpc 2/3':'lock state:unlock',
		'set_rt_ldpc 1/2':'lock state:lock'		
		}
		
		
		
		
with open(filename,encoding='gb18030', errors='ignore') as f:
	reader = csv.reader(f)
	for line in reader:
		if i%2 == 1:																		#判断是否是命令行
			cmd = line[0];																	#是命令则放入cmd
			if cmd in dict_1.keys():														#如果命令在dict中
				cmd_name = (str(index)+':   '+'Command: '+cmd+'   Right->'+dict_1[cmd])
				print(cmd_name+'\n\n')														#打印命令和判定标准
				Result.append(cmd_name)
				i+=1																		#到下一行去
				index+=1

			
			else:																			#判断是否是命令行：否
				cmd_name=(str(index)+':   '+cmd + '---no refer result')
				print(cmd_name+'\n\n')														#打印不支持的命令
				Result.append(cmd_name)
				cmd = 0
				i+=2																		#到下两行去
				index+=1
				
		else:
			line_result=line[1].strip().replace('\t','').split(';')							#将原文中的结果去除空格，去除tab，然后按；做成list,作为正确值的判断
			
			if dict_1[cmd] in line_result:
				result_name = (str(index)+':   ----pass----')
				print(result_name+'\n\n')
				Result.append(result_name)
				i+=1
				index+=1
				
			else:
			
				line_result_fail = re.split(';|:',line[1])									#将原文中的结果用正则表达式，以‘；‘和’：’分割成list，作为错误值的显示
				key = dict_1[cmd].split(':')[0]												#取出判断的内容
				key_index = line_result_fail.index(key)										#取出判断内容的索引值
				fail_result= line_result_fail[key_index+1]									#取出结果
				result_name=(str(index)+':   ----fail----'+'     '+key+':'+fail_result)
				print(result_name+'\n\n')
				Result.append(result_name)
				i+=1
				index+=1

	
	
				
with open(filesave,'w',newline='') as save:
	writer=csv.writer(save)
	writer.writerows(Result)
	save.close()

with open(filesave, 'r') as save:
	content = save.read()
	content = content.strip().replace(',', '').replace('\t', '')

with open(filesave, 'w') as save:
    save.write(content+'\n')
	
