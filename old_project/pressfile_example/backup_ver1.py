import os
import time

source = [u'C:\\Users\\深海里的猫\\Desktop\\GraduationPro\\helloworld']
target_dir = u'C:\\Users\\深海里的猫\\Desktop\\GraduationPro'

target = target_dir + os.sep + \
time.strftime('%Y%m%d%H%M%S') + '.zip'
if not os.path.exists(target_dir):
    os.mkdir(target_dir) # 创建目录
    print('文件创建成功')
# 5. 我们使用 zip 命令将文件打包成 zip 格式
zip_command = 'zip -r {0} {1}'.format(target,
' '.join(source))
# 运行备份
print('Zip command is:')
print(zip_command)
print('Running:')
if os.system(zip_command) == 0:
    print('Successful backup to', target)
else:
    print('Backup FAILED')
