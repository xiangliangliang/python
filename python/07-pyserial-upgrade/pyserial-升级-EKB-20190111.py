#F5
#W:cmd /k C:/Users/user/AppData/Local/Programs/Python/Python37-32/python.exe "$(FULL_CURRENT_PATH)"& PAUSE & EXIT  --- alt + x
# -*- coding: utf-8 -*-  

import serial
import serial.tools.list_ports
import time
import win32gui, win32api, win32con
import os
import re
import datetime
import threading


def get_COM_Port():
	port = list(serial.tools.list_ports.comports())  # 获取串口号内容
	port_list = []

	for i in range(len(port)):                       # 将可用串口置入 port_list
		port_list.append(port[i][0])
	print('可用串口号： '+str(port_list))

	ser = input ('请输入SKY的串口号：COM   （输入1,2,3....）: ')
	ser_port = serial.Serial('COM'+ser,115200,timeout=1)
	print('您选择了： '+ser_port.port+'\r\n')
	time.sleep(0.5)
	'''
	ser_grd = input ('请输入GRD的串口号：COM   （输入1,2,3....）: ')
	ser_port_grd = serial.Serial('COM'+ser_grd,115200,timeout=1)
	print('您选择了： '+ser_port_grd.port+'\r\n')
	time.sleep(0.5)
	'''
	return ser_port

def get_version(ser_port):
	
	run_time = datetime.datetime.now() 
	input_str = 'getVersion \r\n'
	ser_port.write(input_str.encode())

	search = 1
	while search:
		current_time = datetime.datetime.now()
		time_diff = (current_time-run_time).seconds
		current_sw = str(ser_port.readline())
		print(current_sw)
		if 'command_getVersion' in current_sw:
			current_sw_info = (current_sw.split())[1][-8:]
			print(current_sw_info+'\r\n\r\n')
			f.write('---------------current sw:'+str(current_sw_info)+'-----------'+'\r\n\r\n')
			search = 0
			version_info = current_sw_info
		elif time_diff>3:
			print('No version found   \r\n\r\n')
			f.write('---------------current sw: NULL -----------'+'\r\n\r\n')
			search = 0
			version_info = ''
	return 	version_info

def upgrade_result(ser_port):


	#ser_port = get_COM_Port()
	
	run_time = datetime.datetime.now() 
	search = 1
	while search:
		
		current_time = datetime.datetime.now()
		time_diff = (current_time-run_time).seconds
		
		log_info = str(ser_port.readline())
		print(log_info)
		f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'  '+log_info+'\r\n'))
		
		if 'upgrade flash success' in log_info:
			print('upgrade flash success' + '\r\n')
			result = True
			search = 0
		elif 'upgrade ok' in log_info:
			print('upgrade flash success' + '\r\n')
			result = True
			search = 0
		elif 'fail' in log_info:
			print('upgrade failed' +'\r\n')
			result = False
			search = 0
		elif 'lose data count overflow' in log_info:
			print('upgrade failed' +'\r\n')
			result = False
			search = 0

		elif time_diff > 600:
			print('TimeOut' +'\r\n')
			result = False
			search = 0
	#print(result)
	time.sleep(5)
	return result

def PC_TOOL_Upgrade(Upgrade_method):
	#win32api.ShellExecute(0, 'open', r'D:\00-PC-TOOL\4.4.6\Artosyn8020PCTool-v4.4.6.exe', '','',1)    # 具体位置
	#win32api.ShellExecute(0, 'open', r'D:\4.4.6\Artosyn8020PCTool-v4.4.6.exe', '','',1) 	
	DialogName = 'Artosyn Test System_4.4.6'
	win = win32gui.FindWindow(None,DialogName)
	while win == 0:
		win = win32gui.FindWindow(None,DialogName)    # PC-TOOL 句柄
		win32gui.SetForegroundWindow (win)
	
	win32gui.SetWindowPos(win, win32con.HWND_TOPMOST, 50, 100, 1200, 1000, win32con.SWP_NOSIZE | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE | win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)
	
	time.sleep(1) # 休眠1秒

	# PC-TOOL 坐标
	(left,top,right,bottom) = win32gui.GetWindowRect(win)
	
	
	if Upgrade_method == '1':
		y_pos = 680
	elif Upgrade_method == '2':
		y_pos = 710
	elif Upgrade_method == '3':
		y_pos = 733

	# 鼠标点击 Device Info
	Device_Info_Pos_x = left + 1010
	Device_Info_Pos_y = top + 264
	
	#光标定位
	win32api.SetCursorPos([Device_Info_Pos_x,Device_Info_Pos_y]) 
	time.sleep(0.5)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
	time.sleep(0.05)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	time.sleep(0.5)
		
	# 鼠标点击 '升级'
	upgrade_x = left + 808
	upgrade_y = top + y_pos
	
	#光标定位
	win32api.SetCursorPos([upgrade_x,upgrade_y]) 
	time.sleep(0.5)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
	time.sleep(0.05)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	time.sleep(0.5)
		
	# 移走光标
	win32api.SetCursorPos([left,top]) 
	
def PWR():
	ser_PWR = serial.Serial('COM41',9600,timeout=0.1)
	ser_PWR.write(('out0'+'\r\n').encode())
	time.sleep(4)
	ser_PWR.write(('out1'+'\r\n').encode())
	time.sleep(2)

# 获取串口
ser_port = get_COM_Port() 

# 升级方式
Upgrade_method = str(input('请选择升级方式：'+'\r\n'+'  1: 本地app升级'+'\r\n'+'  2: 本地full image 升级'+'\r\n'+'  3: 远程升级'+'\r\n'))

# 保存SKY log
filename = re.sub(r'[^0-9]', '_', str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 0)
save_file_path = 'D:/Profile/Desktop/Log/20190115/'+filename+'_sky.txt'
f = open(save_file_path, 'a+')
'''
save_file_path_grd = 'D:/Profile/Desktop/Log/20190111/'+filename+'_grd.txt'
f_grd = open(save_file_path_grd, 'a+')
'''

run = 1
n=0
while run:
	
	n = n+1
	f.write('---------------upgrade:'+str(n)+'-----------'+'\r\n\r\n')
	
	PC_TOOL_Upgrade(Upgrade_method) # 根据升级方式升级 1：app 2：full image 3：OTA
	
	result = upgrade_result(ser_port)
	if result == True:
		PWR()
		PWR()
				
		version_info = get_version(ser_port)
		if version_info == '':
			run = 0
	else:
		run = 0

	time.sleep(2)
	


