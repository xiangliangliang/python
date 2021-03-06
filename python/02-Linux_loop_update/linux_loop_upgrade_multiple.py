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

filename = re.sub(r'[^0-9]', '_', str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 0)
file_path = crt.Dialog.FileOpenDialog(title='Please select a text file', defaultFilename=filename+'_log.log',filter = 'Log Files (*.log)|*.log')

def main():

	new_version = 'app_v1.22.bin'
	upgrade_new = '00.01.22'
	versions = ['app_v3.8.bin','app_v1.20.bin']
	upgrade_SW = ['00.01.15','00.01.18','00.01.20']
	
	crt.Screen.Synchronous = True
	i=0
	
	
	
	while 1:
		
		initialTab = crt.GetScriptTab()
		
		for sw in versions:
				
		#更新新版本
			tab_1 = crt.GetTab(1)
			tab_1.Activate()
			tab_1.Screen.Send('\r\n')
			time.sleep(2)		
			tab_1.Screen.Send("./sample_upgrade "+ new_version + '\r\n')
			upgrade_success = upgrade_new
			result = tab_1.Screen.WaitForString('upgrade successed',150)
			
			if result == 1:
				filep = open(file_path, 'a+')
				filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+new_version+'   PASS'+'\r\n')
				i = i+1
			else:
				filep = open(file_path, 'a+')
				filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+new_version++'   Fail'+'\r\n')
				crt.Dialog.MessageBox("版本升级失败，请终止升级","session",32|3)
				break
				WEnd
			
		
			tab_1.Screen.Send('\r\n')
			tab_1.Screen.Send('\r\n')
			time.sleep(2)
		
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
			time.sleep(15)
			
		#更新旧版本
			tab_1.Activate()
			tab_1.Screen.Send('\r\n')
			time.sleep(2)		
			tab_1.Screen.Send("./sample_upgrade "+sw+ '\r\n')
			a = i%(len(upgrade_SW))
			upgrade_success = upgrade_SW[a]
			result = tab_1.Screen.WaitForString('upgrade successed',150)
			
			if result == 1:
				filep = open(file_path, 'a+')
				filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+sw+'   PASS'+'\r\n')
				i = i+1
			else:
				filep = open(file_path, 'a+')
				filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+sw+'   Fail'+'\r\n')
				i = i+1
				crt.Dialog.MessageBox("版本升级失败，请终止升级","session",32|3)
				
				break
				WEnd

	
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
			time.sleep(15)

		
		
	
main()