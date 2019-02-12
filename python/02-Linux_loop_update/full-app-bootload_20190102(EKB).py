# $language = "python"
# $interface = "1.0"


import re
import time
import datetime
import string
import random


filename = re.sub(r'[^0-9]', '_', str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 0)
file_path = crt.Dialog.FileOpenDialog(title='Please select a text file', defaultFilename=filename+'_log.log',filter = 'Log Files (*.log)|*.log')


def Info():     # 获取BootLoader，app_part 和 sw_version
	initialTab = crt.GetScriptTab()
	tab_2 = crt.GetTab(2)
	tab_2.Activate()

	tab_2.Screen.WaitForString('Boot Version:')
	info = tab_2.Screen.ReadString('CPU0: main').strip()
	info = info.split()
	bootloader = str(info[0][0:8])
	app_part = str(info[4])
	sw_version = str(info[-1][-8:])
	return(bootloader,app_part,sw_version)

def Upgrade(sw,check_version,delay_time,file_path):		# 定义升级函数：sw 是要升级的文件，check_version是对应的文件版本号，delay_time是升级版本需要预留的时间,file_path是文件保存
		
	initialTab = crt.GetScriptTab()						# upgrade 就是升级用的那个串口，要放在第一个tab，这个是定死的
	tab_1 = crt.GetTab(1)
	tab_1.Activate()
	tab_1.Screen.Send('\r\n')
	time.sleep(2)	
	#tab_1.Screen.Send('sudo ./sample_upgrade '+sw+ '\r\n')          #sudo 是在Telnet下运行要使用的。另外，在linux中下，要‘chmod +x sample_upgrade’
	
	################################################################################################################################################
	tab_1.Screen.Send('./sample_upgrade '+'/mnt/ekb-sw-8003s/'+sw+ '\r\n')   # 注意！！！注意！！！注意！！！ 这里要根据实际情况修改
	################################################################################################################################################
	#tab_1.Screen.Send('baohua'+'\r\n')
	if (tab_1.Screen.WaitForStrings('get file size: 0',2)):
		crt.Dialog.MessageBox(str(sw) + "  该版本不存在!","session",32|3)
		crt.Dialog.MessageBox(check_version+ '  '+'current_sw=  ',+ current_sw,"session",32|3)      #### 无意义：用来终止程序
		time.sleep(100)
		
		
	if (tab_1.Screen.WaitForString('upgrade failed',delay_time)):
		crt.Dialog.MessageBox(str(sw) + "  升级失败!","session",32|3)
		crt.Dialog.MessageBox(check_version+ '  '+'current_sw=  ',+ current_sw,"session",32|3)      #### 无意义：用来终止程序
		time.sleep(100)
		
	else:	
		tab_2 = crt.GetTab(2)
		tab_2.Activate()
		
		
	bootloader,app_part,sw_version = Info()  
	#crt.Dialog.MessageBox(bootloader,"session",32|3)

	
	
	if (sw_version == check_version):								#版本检测，查看升级是否成功
		filep = open(file_path, 'a+')
		filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'bootloader='+str(bootloader)+'  '+'app part= '+str(app_part)+' check_version=  '+str(check_version)+'  '+'upgrade_sw=  '+str(sw)+'   Pass'+'\r\n')
		app_part = str(app_part)
		app_temp = app_part
		#crt.Dialog.MessageBox(app_part,"session",32|3)
		time.sleep(5)
			
	else:
		filep = open(file_path, 'a+')
		filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'bootloader='+str(bootloader)+'  '+'app part= '+str(app_part)+' check_version=  '+str(check_version)+ '  '+'upgrade_sw=  '+str(sw)+'   Fail'+'\r\n')
		
		crt.Dialog.MessageBox('check_version=  '+check_version+' '+'current_sw= '+sw_version,"session",32|3)
		crt.Dialog.MessageBox(check_version+'  '+'current_sw=  '+current_sw,"session",32|3)      #### 无意义：用来终止程序
		time.sleep(100)
	return(app_temp)
	
############################################################################################################################################	


	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是感悟8M BootLoader 开始做loop upgrade $$$$$$----####
	
upgrade_SW = ['app_16.bin','app_17.bin','app_18.bin','app_19.bin','app_20.bin','app_21.bin','app_22.bin','app_23.bin','app_24.bin']
check_version = ['00.01.16','00.01.17','00.01.18','00.01.19','00.01.20','00.01.21','00.01.22','00.01.23','00.01.24']

upgrade_SW_8M = ['app_22_8M.bin','app_23_8M.bin','app_24_8M.bin']
upgrade_FULL_SW_8M = ['app_full_22_8M.bin','app_full_23_8M.bin','app_full_24_8M.bin']	
check_version_8M = ['00.01.22','00.01.23','00.01.24']

upgrade_boot=['boot_4M.bin','boot_8M.bin']
##############################################################################################################################################	


def main():     
	
	
	app_part = ''
	
	while 1:
	
		initialTab = crt.GetScriptTab()          # 激活securecrt的tab页面
		
		
#############升级8M (0~8) app，再升级00.01.25，再随机随机一个full_image,最后升级4M BootLoader#################################################
			
		for i in range(random.randint(1,8)):  											#升级随机的<8个 8M_app.bin
			a = random.randint(0,(len(upgrade_SW_8M)-1))
			Upgrade(upgrade_SW_8M[a],check_version_8M[a],50,file_path)

			
		Upgrade(upgrade_SW_8M[-1],check_version_8M[-1],50,file_path)					#升级到最新的那个版本
		

		#a = random.randint(0,(len(upgrade_FULL_SW_8M)-1))								#升级随机一个8M_full_image.bin
		
		app_temp = Upgrade(upgrade_FULL_SW_8M[-1],check_version_8M[-1],100,file_path) 				
		app_temp = str(app_temp)

		
		if (app_temp == 'app0'): 
			Upgrade(upgrade_SW_8M[-1],check_version_8M[-1],50,file_path)               # 确保bootloader在app0升级

		
		Upgrade(upgrade_SW[-1],check_version[-1],50,file_path)							#升级到4M最新的那个版本
		Upgrade('boot_4M.bin',check_version_8M[-1],20,file_path)						#升级4M BootLoader

			
#############升级4M (0~8) app，再升级00.01.16，最后升级8M BootLoader##########################################################################

			
		for i in range(random.randint(1,8)):  											
																						#升级随机的<8个 4M_app.bin
			a = random.randint(0,(len(upgrade_SW)-1))
			Upgrade(upgrade_SW[a],check_version[a],50,file_path)

		Upgrade(upgrade_SW[0],check_version[0],50,file_path)							#升级到最旧的那个版本

		Upgrade('boot_8M.bin',check_version[0],20,file_path)							#升级8M BootLoader
	
	
		
main()

