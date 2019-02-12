'''

# $language = "python"
# $interface = "1.0"
initialTab = crt.GetScriptTab()
tab_1 = crt.GetTab(2)
tab_1.Activate()
a = tab_1.Screen.WaitForString('Boot Version:',3)
crt.Dialog.MessageBox(str(a),"session",32|3)

'''
import os
import serial
import serial.tools.list_ports
import time
import win32gui, win32api, win32con
import os
import re
import datetime
import threading
import win32clipboard as w
import sys

def get_SW_files():	  # 输入升级软件的目录和文件
	sw_bin_1 = [] 
	sw_bin_2 = []
	sw_bin_3 = []
	sw_dict = {1:sw_bin_1,2:sw_bin_2,3:sw_bin_3}
	file_dir = input("\r\n请输入升级文件的目录（可以用复制粘贴）:  ")
	for root,dirs,files in os.walk(file_dir):
		for sw in files:
			if os.path.splitext(sw)[1] == '.bin':
				if os.path.getsize(root+'\\'+sw) >1500000:
					sw_bin_2.append(sw)
					sw_bin_3.append(sw)
				else:
					sw_bin_1.append(sw)
					sw_bin_3.append(sw)
		return root,files,sw_dict

root,files,sw_dict = get_SW_files()
print(sw_dict[1])



'''
def write_to_CF(upgrade_sw): #把升级的sw路径放到剪切板
	# 写入剪切板
	w.OpenClipboard()
	w.EmptyClipboard()
	w.SetClipboardData(win32con.CF_TEXT, upgrade_sw.encode(encoding='gbk'))
	w.CloseClipboard()

Upgrade_SW_Dir,Upgrade_SW_List = get_SW_files()

print("dir：  "+Upgrade_SW_Dir)
print(Upgrade_SW_List)
time.sleep(2)

upgrade_sw = Upgrade_SW_Dir+"\\"+Upgrade_SW_List[1] #获取升级版本
print(upgrade_sw)
write_to_CF(upgrade_sw)
time.sleep(2)

#D:\00-PC-TOOL\SW\ekb_8M

#D:\Profile\Desktop\Log\20190124

w.OpenClipboard()
d = w.GetClipboardData(win32con.CF_TEXT)
w.CloseClipboard()
win32api.keybd_event(17,0,0,0)      # crtl
win32api.keybd_event(86,0,0,0)     # v
win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
'''
