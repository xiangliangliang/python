使用secureCRT运行脚本：

1. 为确保程序运行，请执行以下操作
1.1 使Linux的串口放在第一个tab
1.2 使升级设备的串口处于第二个tab
1.3 使电源的串口处于第三个tab 

2. 用文本编辑器打开“linux_loop_upgrade.py”
2.1 修改需要的升级文件名和升级版本号
upgrade_SW = "./sample_upgrade app_v3.3.bin\r\n"  //修改升级文件名，此处的文件名是“app_v3.3.bin”
check_version = '00.01.13'			  //修改相应的版本号，此处的版本号是“00.01.13”

3. 多版本循环升级 
打开script->run->\\file01\Import\QA\C201-D\Linux_loop_update\linux_loop_upgrade_1by1.py 

4.1个版本对多个版本循环升级
打开script->run->\\file01\Import\QA\C201-D\Linux_loop_update\linux_loop_upgrade_multiple.py 