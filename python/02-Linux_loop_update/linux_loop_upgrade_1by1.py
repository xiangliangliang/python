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

	upgrade_SW = ['201-v4.2_ar8020.bin','ar8020_bootupgrade.bin','201-v4.2_app.bin','201-v4.2_app.bin']   
	boot=['app0','app0','app1','app0']
	check_version = '00.01.24'

	
	crt.Screen.Synchronous = False
	i=0
	
	
	while 1:
		
		initialTab = crt.GetScriptTab()
		
		for sw in upgrade_SW:
			
			#升级full_image,bootload,app
			tab_1 = crt.GetTab(1)
			tab_1.Activate()
			tab_1.Screen.Send('\r\n')
			time.sleep(2)		
			tab_1.Screen.Send("./sample_upgrade "+sw+ '\r\n')
			a = i%(len(upgrade_SW))
			time.sleep(240)
		
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
			#boot_app = tab_1.Screen.WaitForString(boot[a],3)
			#crt.Dialog.MessageBox(str(boot_app))
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
				
			if (current_sw == check_version):
				filep = open(file_path, 'a+')
				filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+sw+'   PASS'+'\r\n')
				i = i+1
			else:
				filep = open(file_path, 'a+')
				filep.write(str(i)+'  '+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+sw+'   Fail'+'\r\n')
				i = i+1
				crt.Dialog.MessageBox("版本升级失败，请终止升级","session",32|3)
				time.sleep(1)
				break
				return
				WEnd
		
		
		
	
main()