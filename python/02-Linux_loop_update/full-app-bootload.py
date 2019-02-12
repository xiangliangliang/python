'''
为确保程序运行，请执行以下操作
1. 使Linux的串口放在第一个tab
2. 使升级设备处于第二个tab
3. 使电源串口处于第三个tab

'''

# $language = "python"
# $interface = "1.0"

import re
import time
import datetime
import string
import random

filename = re.sub(r'[^0-9]', '_', str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 0)
file_path = crt.Dialog.FileOpenDialog(title='Please select a text file', defaultFilename=filename+'_log.log',filter = 'Log Files (*.log)|*.log')

def main():

	upgrade_SW = ['app_16.bin','app_17.bin','app_18.bin','app_19.bin','app_20.bin','app_22.bin','app_23.bin','app_24.bin','app_25.bin','app_26.bin']
	upgrade_FULL_SW = ['app_full_16.bin','app_full_17.bin','app_full_18.bin','app_full_19.bin','app_full_20.bin','app_full_22.bin','app_full_23.bin','app_full_24.bin','app_full_25.bin','app_full_26.bin']	
	upgrade_boot=['boot_8M.bin','boot_8M.bin']
	check_version = ['00.01.24','00.01.24','00.01.24','00.01.24','00.01.24','00.01.24','00.01.24','00.01.24','00.01.24']
	#check_version = ['00.01.16','00.01.17','00.01.18','00.01.19','00.01.20','00.01.21','00.01.22','00.01.23','00.01.24']

	
	crt.Screen.Synchronous = False
	i=0
	boot_count=0
	
	
	while 1:
		
		initialTab = crt.GetScriptTab()
		tab_1 = crt.GetTab(1)
		tab_1.Activate()
		tab_1.Screen.Send('\r\n')
		#tab_1.Screen.Send("./sample_upgrade "+sw+ '\r\n')  # --------------改改改
		if (boot_count%2) == 0:
			tab_1.Screen.Send("boot_8M.bin" + '\r\n')           # 升级8M BootLoader
			boot_count = boot_count +1
			filep = open(file_path, 'a+')
			filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+check_version[i]+'   PASS'+'\r\n')
			i = i+1
		else:
			tab_1.Screen.Send("boot_4M.bin" + '\r\n')
			filep = open(file_path, 'a+')
			filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+check_version[i]+'   PASS'+'\r\n')
			i = i+1
		time.sleep(4)
		
		tab_3 = crt.GetTab(3)
		tab_3.Activate()
		time.sleep(2)
		tab_3.Screen.Send('\r\n')
		tab_3.Screen.Send('\r\n')
		
		on = str.upper('out')+'1'
		off = str.upper('out')+'0'
		
		tab_3.Screen.Send(off +'\r\n\r')
		time.sleep(5)
		tab_3.Screen.Send(on +'\r\n\r')
		
		for i in range(8) :  #-----------随机升级app8次
			
			#升级app
			tab_1 = crt.GetTab(1)
			tab_1.Activate()
			tab_1.Screen.Send('\r\n')
			time.sleep(2)		
			#tab_1.Screen.Send("./sample_upgrade "+sw+ '\r\n') # --------------改改改
			a = random.randint(0,10)
			tab_1.Screen.Send(upgrade_SW[a]+ '\r\n')           # --------------升级app
			time.sleep(2)									   # --------------改改改
		
			#重启平台，直流源的串口必须放在第三个tab
			tab_3 = crt.GetTab(3)
			tab_3.Activate()
			time.sleep(2)
			tab_3.Screen.Send('\r\n')
			tab_3.Screen.Send('\r\n')
		
			on = str.upper('out')+'1'
			off = str.upper('out')+'0'
		
			tab_3.Screen.Send(off +'\r\n\r')
			time.sleep(5)
			tab_3.Screen.Send(on +'\r\n\r')
					
			#打开C201-D串口，串口必须放在第二个
			tab_2 = crt.GetTab(2)
			tab_2.Activate()
			time.sleep(5)
			tab_2.Screen.Send('\r\n')
			tab_2.Screen.Send('getVersion'+'\r\n')
			version_result = tab_2.Screen.WaitForString('command_getVersion',5)
			if version_result == 1:
				current_sw = tab_2.Screen.ReadString('CPU0').strip()
				current_sw = current_sw[:8]
				#crt.Dialog.MessageBox(current_sw)
				time.sleep(2)
				#crt.Dialog.MessageBox(check_version)
			else:
				crt.Dialog.MessageBox("版本升级失败，请终止升级","session",32|3)
				time.sleep(1)
				break
				return
				WEnd
				
			if (current_sw == check_version[a]):
				filep = open(file_path, 'a+')
				filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+check_version[i]+'   PASS'+'\r\n')
				i = i+1
			else:
				filep = open(file_path, 'a+')
				filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+check_version[i]+'   Fail'+'\r\n')
				i = i+1
				crt.Dialog.MessageBox("版本升级失败，请终止升级","session",32|3)
				time.sleep(1)
				break
				return
				WEnd
				
		tab_1 = crt.GetTab(1)
		tab_1.Activate()
		tab_1.Screen.Send('\r\n')
		#tab_1.Screen.Send("./sample_upgrade "+sw+ '\r\n')  # --------------改改改
		tab_1.Screen.Send("app_25.bin" + '\r\n')           # 升级app_25.bin
		time.sleep(2)	                                    # ------改改改
		
		tab_3 = crt.GetTab(3)
		tab_3.Activate()
		time.sleep(2)
		tab_3.Screen.Send('\r\n')
		tab_3.Screen.Send('\r\n')
		
		on = str.upper('out')+'1'
		off = str.upper('out')+'0'
		
		tab_3.Screen.Send(off +'\r\n\r')
		time.sleep(5)
		tab_3.Screen.Send(on +'\r\n\r')
				
		tab_2 = crt.GetTab(2)
		tab_2.Activate()
		time.sleep(5)
		tab_2.Screen.Send('\r\n')
		tab_2.Screen.Send('getVersion'+'\r\n')
		version_result = tab_2.Screen.WaitForString('command_getVersion',5)
		if version_result == 1:
			current_sw = tab_2.Screen.ReadString('CPU0').strip()
			current_sw = current_sw[:8]
			#crt.Dialog.MessageBox(current_sw)
			time.sleep(2)
			#crt.Dialog.MessageBox(check_version)
		else:
			crt.Dialog.MessageBox("版本升级失败，请终止升级","session",32|3)
			time.sleep(1)
			break
			return
			WEnd
			
		if (current_sw == '00.01.25'):
			filep = open(file_path, 'a+')
			filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'00.01.25 app'+'   PASS'+'\r\n')
			i = i+1
		else:
			filep = open(file_path, 'a+')
			filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'00.01.25 app'+'   Fail'+'\r\n')
			i = i+1
			crt.Dialog.MessageBox("版本升级失败，请终止升级","session",32|3)
			time.sleep(1)
			break
			return		
			
		tab_1 = crt.GetTab(1)
		tab_1.Activate()
		tab_1.Screen.Send('\r\n')
		#tab_1.Screen.Send("./sample_upgrade "+sw+ '\r\n')  # --------------改改改
		ij=random.randint(0.10)
		tab_1.Screen.Send(upgrade_FULL_SW[ij] + '\r\n')           # 升级随机一个full image.bin
		time.sleep(2)										# --------------改改改
		
		tab_3 = crt.GetTab(3)
		tab_3.Activate()
		time.sleep(2)
		tab_3.Screen.Send('\r\n')
		tab_3.Screen.Send('\r\n')
		
		on = str.upper('out')+'1'
		off = str.upper('out')+'0'
		
		tab_3.Screen.Send(off +'\r\n\r')
		time.sleep(5)
		tab_3.Screen.Send(on +'\r\n\r')
				
		tab_2 = crt.GetTab(2)
		tab_2.Activate()
		time.sleep(5)
		tab_2.Screen.Send('\r\n')
		tab_2.Screen.Send('getVersion'+'\r\n')
		version_result = tab_2.Screen.WaitForString('command_getVersion',5)
		if version_result == 1:
			current_sw = tab_2.Screen.ReadString('CPU0').strip()
			current_sw = current_sw[:8]
			#crt.Dialog.MessageBox(current_sw)
			time.sleep(2)
			#crt.Dialog.MessageBox(check_version)
		else:
			crt.Dialog.MessageBox("版本升级失败，请终止升级","session",32|3)
			time.sleep(1)
			break
			return
			WEnd
			
		if (current_sw == check_version[ij]):
			filep = open(file_path, 'a+')
			filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+check_version[ij]+'   PASS'+'\r\n')
			i = i+1
		else:
			filep = open(file_path, 'a+')
			filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+check_version[ij]+'   Fail'+'\r\n')
			i = i+1
			crt.Dialog.MessageBox("版本升级失败，请终止升级","session",32|3)
			time.sleep(1)
			break
			return		
				
		
		
main()
			