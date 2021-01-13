from django.test import TestCase

import paramiko

ssh = paramiko.SSHClient()
policy = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(policy)
ssh.connect(
    hostname='127.0.0.1',  # 服务器的ip
    port=22,  # 服务器的端口
    username='root',  # 服务器的用户名
    password='devops'  # 用户名对应的密码
)
stdin, stdout, stderr = ssh.exec_command('ls /')

print(str(stderr.read(), encoding='utf-8'))
print(1111111111111)
print(str(stdout.read(), encoding='utf-8'))
