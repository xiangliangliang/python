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



def get_COM_Port():
	port = list(serial.tools.list_ports.comports())  # 获取串口号内容
	port_list = []

	for i in range(len(port)):                       # 将可用串口置入 port_list
		port_list.append(port[i][0])
	print('可用串口号： '+str(port_list))

	ser = input ('请输入8020的串口号：COM   （输入1,2,3....）: ')
	ser_port = serial.Serial('COM'+ser,115200,timeout=1)
	print('您选择了： '+ser_port.port+'\r\n')
	time.sleep(0.5)
	return ser_port


def get_version(ser_port):
	
	#ser_port = get_COM_Port()
	#ser_port.open()
	input_str = 'getVersion \r\n'
	ser_port.write(input_str.encode())

	search = 1
	while search:
		current_sw = str(ser_port.readline())
		if 'command_getVersion' in current_sw:
			current_sw_info = (current_sw.split())[1][-8:]
			print(current_sw_info)
			search = 0
		
	#ser_port.close()

def upgrade_result(ser_port):


	#ser_port = get_COM_Port()
	
	#f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\r\n')
	search = 1
	while search:
		
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
		elif 'lose data count overflow 314' in log_info:
			print('upgrade failed' +'\r\n')
			result = False
			search = 0
			#win32api.MessageBox(0, str(result)+' ：请重启设备', "升级结果",win32con.MB_OK)

	#print(result)
	time.sleep(5)
	return result


# -- 升级 --
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
	time.sleep(2)
		
	# 鼠标点击 '升级'
	upgrade_x = left + 808
	upgrade_y = top + y_pos
	
	#光标定位
	win32api.SetCursorPos([upgrade_x,upgrade_y]) 
	time.sleep(0.5)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
	time.sleep(0.05)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	time.sleep(1)
		
	# 移走光标
	win32api.SetCursorPos([left,top]) 
	
def PWR():
	ser_PWR = serial.Serial('COM40',9600,timeout=0.1)
	ser_PWR.write(('out0'+'\r\n').encode())
	time.sleep(2)
	ser_PWR.write(('out1'+'\r\n').encode())

# 获取串口
ser_port = get_COM_Port() 

# 升级方式
Upgrade_method = str(input('请输入升级方式：'+'\r\n'+'  1: 本地app升级'+'\r\n'+'  2: 本地full image 升级'+'\r\n'+'  3: 远程升级'+'\r\n'))
PC_TOOL_Upgrade(Upgrade_method) # 根据升级方式升级 1：app 2：full image 3：OTA

filename = re.sub(r'[^0-9]', '_', str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 0)
save_file_path = 'D:/Profile/Desktop/Log/20190110/'+filename+'.txt'
f = open(save_file_path, 'a+')
n = 1

while n < 5:
	print(n)
	n = n+1
	f.write('---------------upgrade:'+str(n)+'-----------'+'\r\n\r\n')
	result = upgrade_result(ser_port) 
	print(str(result))
	if result == True:
		PWR()
ser_port.close()


