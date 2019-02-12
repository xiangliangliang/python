# $language = "python"
# $interface = "1.0"

import re
import time
import datetime
import string
import random

filename = re.sub(r'[^0-9]', '_', str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 0)
file_path = crt.Dialog.FileOpenDialog(title='Please select a text file', defaultFilename=filename+'_log.log',filter = 'Log Files (*.log)|*.log')

def PWR_Reboot():                                                 # 定义电源重启，5s关，5s开
	initialTab = crt.GetScriptTab()
	tab_3 = crt.GetTab(3)										  # 重启平台，直流源的串口必须放在第三个tab,这个是定死的
	tab_3.Activate()
	time.sleep(2)
	tab_3.Screen.Send('\r\n')
	tab_3.Screen.Send('\r\n')
	
	on = str.upper('out')+'1'
	off = str.upper('out')+'0'
		
	tab_3.Screen.Send(off +'\r\n\r')
	time.sleep(5)
	tab_3.Screen.Send(on +'\r\n\r')
	time.sleep(5)

def Upgrade(sw,check_version,delay_time):							# 定义升级函数：sw 是要升级的文件，check_version是对应的文件版本号，delay_time是升级版本需要预留的时间。建议BootLoader "30",app "120", full image "180"
		
	initialTab = crt.GetScriptTab()									# upgrade 就是升级用的那个串口，要放在第一个tab，这个是定死的
	tab_1 = crt.GetTab(1)
	tab_1.Activate()
	tab_1.Screen.Send('\r\n')
	time.sleep(2)	
	tab_1.Screen.Send('sudo ./sample_upgrade '+sw+ '\r\n')          #sudo 是在Telnet下运行要使用的。另外，在linux中下，要‘chmod +x sample_upgrade’
	tab_1.Screen.Send('baohua'+'\r\n')
	time.sleep(delay_time)									  		 
						
	PWR_Reboot()											 
						
																		#打开8020串口，串口必须放在第二个
	tab_2 = crt.GetTab(2)
	tab_2.Activate()
	time.sleep(5)
	tab_2.Screen.Send('\r\n')
	tab_2.Screen.Send('getVersion'+'\r\n')
	version_result = tab_2.Screen.WaitForString('command_getVersion',5)
	if version_result == 1:											#检测版本是否存在，如果不存在，可能烧成砖了。如果存在，则提取版本号
		current_sw = tab_2.Screen.ReadString('CPU0').strip()
		current_sw = current_sw[:8]
		time.sleep(2)
				
	else:
		crt.Dialog.MessageBox("未检测到版本号。","session",32|3)
		time.sleep(100)
		return
					
	if (current_sw == check_version):								#版本检测，查看升级是否成功
		filep = open(file_path, 'a+')
		filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+check_version+'   PASS'+'\r\n')
			
	else:
		filep = open(file_path, 'a+')
		filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'check_version=  '+ check_version+ '  '+'current_sw=  ',+ current_sw+'   Fail'+'\r\n')
		crt.Dialog.MessageBox('check_version=  '+ check_version+ '  '+'current_sw=  ',+ current_sw,"session",32|3)
		time.sleep(100)
		return

	time.sleep(5)													#升级完毕后，等5秒
		
############################################################################################################################################	


	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	
upgrade_SW = ['app_16.bin','app_17.bin','app_18.bin','app_19.bin','app_20.bin','app_21.bin','app_22.bin','app_23.bin','app_24.bin','app_25.bin']
check_version = ['00.01.16','00.01.17','00.01.18','00.01.19','00.01.20','00.01.21','00.01.22','00.01.23','00.01.24','00.01.25']

upgrade_SW_8M = ['app_22_8M.bin','app_23_8M.bin','app_24_8M.bin','app_25_8M.bin']
upgrade_FULL_SW_8M = ['app_full_22_8M.bin','app_full_23_8M.bin','app_full_24_8M.bin','app_full_25_8M.bin']	
check_version_8M = ['00.01.22','00.01.23','00.01.24','00.01.25']

upgrade_boot=['boot_4M.bin','boot_8M.bin']
##############################################################################################################################################


def main():

x=0		 
	
while 1:
	
	initialTab = crt.GetScriptTab()          # 激活securecrt的tab页面
		
		
#############升级8M (0~8) app，再升级00.01.25，再随机随机一个full_image,最后升级4M BootLoader#################################################
		

		
	for i in range(random.randint(0,8)):  								#升级随机的<8个 8M_app.bin
		a = random.randint(0,(len(upgrade_SW_8M)-1))
		filep = open(file_path, 'a+')
		filep.write(str(x)+' 8M app  '+upgrade_SW_8M[a]+'\r\n')
		Upgrade(upgrade_SW_8M[a],check_version_8M[a],120)
		x = x+1
			
	Upgrade(upgrade_SW_8M[-1],check_version_8M[-1],120)					#升级到最新的那个版本
	filep = open(file_path, 'a+')
	filep.write(str(x)+' 最新版本'+'\r\n')
	x = x+1
		
	Upgrade(upgrade_FULL_SW_8M[a],check_version_8M[a],180) 				#升级随机一个8M_full_image.bin
	filep = open(file_path, 'a+')
	filep.write(str(x)+' 8M full image  '+upgrade_FULL_SW_8M[a]+'\r\n')
	x = x+1
		
	Upgrade('boot_4M.bin',check_version_8M[-1],30)						#升级4M BootLoader
	filep = open(file_path, 'a+')
	filep.write(str(x)+' 4M BootLoader'+'\r\n')
	x = x+1		
			
			
#############升级4M (0~8) app，再升级00.01.16，最后升级8M BootLoader##########################################################################

			
	for i in range(random.randint(0,8)):  								#升级随机的<8个 4M_app.bin
		a = random.randint(0,(len(upgrade_SW)-1))
		Upgrade(upgrade_SW[a],check_version[a],120)
		filep = open(file_path, 'a+')
		filep.write(str(x)+'  4M app  '+upgrade_SW[a]+'\r\n')
		x = x+1
			
	Upgrade(upgrade_SW[0],check_version[0],120)							#升级到最旧的那个版本
	filep = open(file_path, 'a+')
	filep.write(str(x)+'  00.01.16'+'\r\n')
	x = x+1
		
	Upgrade('boot_8M.bin',check_version[0],30)							#升级8M BootLoader
	filep = open(file_path, 'a+')
	filep.write(str(x)+' 8M BootLoader'+'\r\n')
	x = x+1	
	
		
main()