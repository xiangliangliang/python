# $language = "python"
# $interface = "1.0"
import random
import re
import time
import datetime
import string


def main():
	
	vt_no = random.randint(0,6) # 2g-10m：7个信道
	initialTab = crt.GetScriptTab()
	#tab_1 = crt.GetTab(1)
	#tab_1.Activate()
	#tab_1.Screen.Send('\r\n')
	
	while 1:

		# UART 切换图传信道命令：
		# SetSubBBch <ch>
		# 2g-10m: 7个信道
		# 5g-10m: 10个信道
		# 2g-20m: 3个信道
		# 5g-20m: 5个信道
				
		sleeptime = 30

		random_num = random.randint(0,6)
	
		if vt_no == random_num:
			random_num = random.randint(0,6)
			if vt_no != random_num:
				vt_no = random_num
				text_tx = 'SetSubBBch ' + str(vt_no) + '\r\n'
				crt.Screen.Send(text_tx)
				time.sleep(sleeptime)
	
		else:
			vt_no = random_num
			text_tx = 'SetSubBBch ' + str(vt_no) + '\r\n'
			crt.Screen.Send(text_tx)
			time.sleep(sleeptime)
	
main()