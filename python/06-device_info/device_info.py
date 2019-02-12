#F5
#W:cmd /k C:/Users/user/AppData/Local/Programs/Python/Python37-32/python.exe "$(FULL_CURRENT_PATH)"& PAUSE & EXIT  --- alt + x
# -*- coding: utf-8 -*-  
#pip install pywin32

import win32gui, win32api, win32con
import os
import time
import serial

'''
ShellExecute(hwnd, op , file , params , dir , bShow )
其参数含义如下所示。

hwnd：父窗口的句柄，如果没有父窗口，则为0。
op：要进行的操作，为“open”、“print”或者为空。
file：要运行的程序，或者打开的脚本。
params：要向程序传递的参数，如果打开的为文件，则为空。
dir：程序初始化的目录。
bShow：是否显示窗口。
'''

#win32api.ShellExecute(0, 'open', r'D:\00-PC-TOOL\4.4.6\Artosyn8020PCTool-v4.4.6.exe', '','',1)    # 具体位置
#win32api.ShellExecute(0, 'open', r'D:\4.4.6\Artosyn8020PCTool-v4.4.6.exe', '','',1) 

#os.system("taskkill /F /IM Artosyn8020PCTool-v4.4.6.exe")
def OTA():
	DialogName = 'Artosyn Test System_4.4.6'
	win = win32gui.FindWindow(None,DialogName)
	while win == 0:
		win = win32gui.FindWindow(None,DialogName)    # 窗口句柄号
		win32gui.SetForegroundWindow (win)
	
	if(win32gui.IsIconic(win)):
#     win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
		win32gui.ShowWindow(win, 8)
		time.sleep(0.5)
	
	win32gui.SetWindowPos(win, win32con.HWND_TOPMOST, 50, 100, 1200, 1000, win32con.SWP_NOSIZE | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE | win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)
	
	time.sleep(1) # 休眠1秒

	# PC-TOOL 坐标
	(left,top,right,bottom) = win32gui.GetWindowRect(win)


	# 鼠标点击 Device Info
	Device_Info_Pos_x = left + 1010
	Device_Info_Pos_y = top + 264
	win32api.SetCursorPos([Device_Info_Pos_x,Device_Info_Pos_y]) #光标定位
	time.sleep(0.5)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
	time.sleep(0.05)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	time.sleep(2)
	
	'''
	# 鼠标点击 OTA
	OTA_x = left + 808
	OTA_y = top + 733
	win32api.SetCursorPos([OTA_x,OTA_y]) #光标定位
	time.sleep(0.5)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
	time.sleep(0.05)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
	time.sleep(1)
	'''
	
	# 移走光标
	win32api.SetCursorPos([left,top]) #光标定位
	time.sleep(0.5)


def PWR():
	on = str.upper('out')+'1'+'\r\n'
	off = str.upper('out')+'0'+'\r\n'
	ser = serial.Serial('COM40',9600,timeout=0.1)
	ser.write(off.encode())

	
	
i = 1
while i<10:
	OTA()
	i=i+1