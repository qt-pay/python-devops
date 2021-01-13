from subprocess import Popen, PIPE
pcmd = Popen('cmd', stdout=PIPE, stderr=PIPE, shell=True)
data,error = pcmd.communicate()
retcode=pcmd.poll()
print(retcode)
print(error)
print(data[0])

# print(locals())
# print(type(data))
# print(str(data, encoding='utf-8'))
