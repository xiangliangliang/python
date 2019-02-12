# $language = "python"
# $interface = "1.0"


import re
import time
import datetime
import string
import random
import sys


filename = re.sub(r'[^0-9]', '_', str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 0)
file_path = crt.Dialog.FileOpenDialog(title='Please select a text file', defaultFilename=filename+'_log.log',filter = 'Log Files (*.log)|*.log')


def Upgrade(sw,delay_time,file_path):	# 升级：sw 是要升级的文件，delay_time是升级版本需要预留的时间 (tab_1)
		
	initialTab = crt.GetScriptTab()						# upgrade 就是升级用的那个串口，要放在第一个tab，这个是定死的
	tab_1 = crt.GetTab(1)
	tab_1.Activate()
	tab_1.Screen.Send('\r\n')
	time.sleep(2)	
	filep = open(file_path, 'a+')
	filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'普通升级！'+'\r\n')
	#tab_1.Screen.Send('sudo ./sample_upgrade '+sw+ '\r\n')          #sudo 是在Telnet下运行要使用的。另外，在linux中下，要‘chmod +x sample_upgrade’
	
	################################################################################################################################################
	tab_1.Screen.Send('./sample_upgrade '+'/mnt/ekb-sw-8003s/'+sw+ '\r\n')   # 注意！！！注意！！！注意！！！ 这里要根据实际情况修改
	################################################################################################################################################
	#tab_1.Screen.Send('baohua'+'\r\n')
	if (tab_1.Screen.WaitForStrings('get file size: 0',2)):
		crt.Dialog.MessageBox(str(sw) + "  该版本不存在!","session",32|3)
		filep = open(file_path, 'a+')
		filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+sw+' 不存在'+'\r\n')
		crt.Dialog.MessageBox(check_version+ '  '+'current_sw=  ',+ current_sw,"session",32|3)      
		time.sleep(100)
		sys.exit(0)
		
		
	if (tab_1.Screen.WaitForString('upgrade failed',delay_time)):
		crt.Dialog.MessageBox(str(sw) + "  升级失败!","session",32|3)
		#filep = open(file_path, 'a+')
	    #filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+sw+' 升级失败'+'\r\n')
		crt.Dialog.MessageBox(check_version+ '  '+'current_sw=  ',+ current_sw,"session",32|3)      
		time.sleep(100)
		sys.exit(0)
	#time.sleep(delay_time)
	tab_2 = crt.GetTab(2)
	tab_2.Activate()
		
def destory_Upgrade(sw,file_path):	#破坏升级，时限（1~30s）(tab_1)

	initialTab = crt.GetScriptTab()									# upgrade 就是升级用的那个串口，要放在第一个tab，这个是定死的
	tab_1 = crt.GetTab(1)
	tab_1.Activate()
	tab_1.Screen.Send('\r\n')
	time.sleep(2)
	filep = open(file_path, 'a+')
	filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'破坏升级！'+'\r\n')	
	#tab_1.Screen.Send('sudo ./sample_upgrade '+sw+ '\r\n')          #sudo 是在Telnet下运行要使用的。另外，在linux中下，要‘chmod +x sample_upgrade’
	
	################################################################################################################################################
	tab_1.Screen.Send('./sample_upgrade '+'/mnt/ekb-sw-8003s/'+sw+ '\r\n')   # 注意！！！注意！！！注意！！！ 这里要根据实际情况修改
	################################################################################################################################################
	#tab_1.Screen.Send('baohua'+'\r\n')
	if (tab_1.Screen.WaitForStrings('get file size: 0',2)):
		crt.Dialog.MessageBox(str(sw) + "  该版本不存在!","session",32|3)
		crt.Dialog.MessageBox(check_version+ '  '+'current_sw=  ',+ current_sw,"session",32|3)      
		time.sleep(100)
		sys.exit(0)
	
	random_time = random.randint(1,30)
	time.sleep(random_time)
	tab_2 = crt.GetTab(2)
	tab_2.Activate()
	filep = open(file_path, 'a+')
	filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'destory_Upgrade'+'\r\n')
		
def PWR(file_path):	#开关电源:关机                                                                                                    4s，开机停2s (tab_3)
	initialTab = crt.GetScriptTab()	
	tab_3 = crt.GetTab(3)
	filep = open(file_path, 'a+')
	filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'重启！'+'\r\n')	
	tab_3.Screen.Send('out0'+'\r\n')
	time.sleep(4)
	tab_3.Screen.Send('out1'+'\r\n')
	
def Info(file_path):	# 获取BootLoader，app_part 和 sw_version,如果10s未检测到信息，退出程序 (tab_2)
	initialTab = crt.GetScriptTab()
	tab_2 = crt.GetTab(2)
	tab_2.Activate()
	
	run_time = datetime.datetime.now()
	current_time = datetime.datetime.now()
	time_diff = (current_time-run_time).seconds
	get_info = tab_2.Screen.WaitForString('Boot Version:',10)	#10s检测，如果未检测到信息，程序终止
	
	if str(get_info) == "0":
		crt.Dialog.MessageBox("未获得版本号，请检测启机是否成功！","session",32|3)
		crt.Dialog.MessageBox(check_version+ '  '+'current_sw=  ',+ current_sw,"session",32|3)      
		time.sleep(100)
		sys.exit(0)
	else:
		info = tab_2.Screen.ReadString('CPU0: main').strip()
		info = info.split()
		bootloader = str(info[0][0:8])
		app_part = str(info[4])
		sw_version = str(info[-1][-8:])
	
	return(bootloader,app_part,sw_version)
	
def check_Result(sw_version,check_version,bootloader,app_part,file_path):	#版本检测，查看升级是否成功
	
	if (sw_version == check_version):								
		filep = open(file_path, 'a+')
		filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'bootloader='+str(bootloader)+'  '+'app part= '+str(app_part)+' check_version=  '+str(check_version)+'  '+'upgrade_sw=  '+str(sw_version)+'   Pass'+'\r\n')
		app_part = str(app_part)
		app_temp = app_part
		#crt.Dialog.MessageBox(app_part,"session",32|3)
		time.sleep(5)
			
	else:
		filep = open(file_path, 'a+')
		filep.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'  '+'bootloader='+str(bootloader)+'  '+'app part= '+str(app_part)+' check_version=  '+str(check_version)+ '  '+'upgrade_sw=  '+str(sw_version)+'   Fail'+'\r\n')
		
		crt.Dialog.MessageBox('check_version=  '+check_version+' '+'current_sw= '+sw_version,"session",32|3)
		crt.Dialog.MessageBox(check_version+'  '+'current_sw=  '+current_sw,"session",32|3)      
		time.sleep(100)
		sys.exit(0)
	return(app_temp)
	
############################################################################################################################################	


	#### ---- $$$$$$ 默认是8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是8M BootLoader 开始做loop upgrade $$$$$$----####
	#### ---- $$$$$$ 默认是8M BootLoader 开始做loop upgrade $$$$$$----####
	
upgrade_SW = ['app_16.bin','app_17.bin','app_18.bin','app_19.bin','app_20.bin','app_21.bin','app_22.bin','app_23.bin','app_24.bin','app_25.bin','app_26.bin']
check_version = ['00.01.16','00.01.17','00.01.18','00.01.19','00.01.20','00.01.21','00.01.22','00.01.23','00.01.24','00.01.25','00.01.26']

upgrade_SW_8M = ['app_22_8M.bin','app_23_8M.bin','app_24_8M.bin','app_25_8M.bin','app_26_8M.bin']
upgrade_FULL_SW_8M = ['app_full_22_8M.bin','app_full_23_8M.bin','app_full_24_8M.bin','app_full_25_8M.bin','app_full_26_8M.bin']	
check_version_8M = ['00.01.22','00.01.23','00.01.24','00.01.25','00.01.26']

upgrade_boot=['boot_4M.bin','boot_8M.bin']
##############################################################################################################################################	


def main():     
	
	
	app_part = ''
		
	while 1:
	
		initialTab = crt.GetScriptTab()          # 激活securecrt的tab页面
		
		
		
#############（1）升级8M (0~8个) app，（2）进行一次破坏性升级，（3）升级最新8M app版本，（4）升级full_image, （5）最后升级4M BootLoader#################################################
			
		for i in range(random.randint(1,8)):  											#（1）升级随机<8个 8M_app.bin
			a = random.randint(0,(len(upgrade_SW_8M)-1))
			Upgrade(upgrade_SW_8M[a],50,file_path)
			PWR(file_path)
			bootloader,app_part,sw_version = Info(file_path)
			check_Result(sw_version,check_version_8M[a],bootloader,app_part,file_path)
			
			destory_Upgrade(upgrade_SW_8M[-1],file_path)								#（2）执行一次破坏性升级到最新版本
			PWR(file_path)
			bootloader,app_part,sw_version = Info(file_path)
			check_Result(sw_version,check_version_8M[a],bootloader,app_part,file_path)
			time.sleep(240)
			
		Upgrade(upgrade_SW_8M[-1],50,file_path)											#（3）升级到最新的那个版本
		PWR(file_path)
		bootloader,app_part,sw_version = Info(file_path)
		check_Result(sw_version,check_version_8M[-1],bootloader,app_part,file_path)

	
		Upgrade(upgrade_FULL_SW_8M[-1],100,file_path) 									#（4）升级8M_full_image.bin
		PWR(file_path)
		bootloader,app_part,sw_version = Info(file_path)
		check_Result(sw_version,check_version_8M[-1],bootloader,app_part,file_path)
		
		if (app_part == 'app0'): 
			Upgrade(upgrade_SW_8M[-1],50,file_path)               						# 为了确保bootloader在app0升级
			PWR(file_path)
			bootloader,app_part,sw_version = Info(file_path)
			check_Result(sw_version,check_version_8M[-1],bootloader,app_part,file_path)
		
		Upgrade(upgrade_SW[-1],50,file_path)											#  升级到4M最新的版本，且处于app0
		PWR(file_path)
		bootloader,app_part,sw_version = Info(file_path)
		check_Result(sw_version,check_version[-1],bootloader,app_part,file_path)
		
		Upgrade('boot_4M.bin',20,file_path)												# （5）升级4M BootLoader
		PWR(file_path)
			
#############（1）升级4M (0~8) app，（2）进行一下破坏升级，（3）升级到00.01.16，（4）最后升级8M BootLoader##########################################################################

			
		for i in range(random.randint(1,8)):  											
																						#（1）升级随机的<8个 4M_app.bin
			a = random.randint(0,(len(upgrade_SW)-1))
			Upgrade(upgrade_SW[a],50,file_path)
			PWR(file_path)
			bootloader,app_part,sw_version = Info(file_path)
			check_Result(sw_version,check_version[a],bootloader,app_part,file_path)
			
			destory_Upgrade(upgrade_SW[-1],file_path)									#（2）执行一次破坏性升级到最新版本
			PWR(file_path)
			bootloader,app_part,sw_version = Info(file_path)
			check_Result(sw_version,check_version[a],bootloader,app_part,file_path)
			time.sleep(240)
		
		Upgrade(upgrade_SW[0],50,file_path)												#（3）升级到最旧的那个版本
		PWR(file_path)
		bootloader,app_part,sw_version = Info(file_path)
		check_Result(sw_version,check_version[0],bootloader,app_part,file_path)
		
		Upgrade('boot_8M.bin',20,file_path)												#（4）升级8M BootLoader
		PWR(file_path)
		
		
main()

