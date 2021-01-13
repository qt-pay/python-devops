from subprocess import Popen, PIPE, STDOUT, call
import json
def sub_command(cmd):


    cmd_dict = {
        'cmd_result': 'success',
        'cmd_detail': '',
    }
    pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    data = pcmd.communicate()
    retcode = pcmd.poll()
    if retcode != 0:
        cmd_dict['cmd_result'] = 'failed'
    cmd_dict['cmd_dict'] = str(data[0], encoding="utf-8").strip()
    return json.dumps(cmd_dict)

l = sub_command('ansible all -m ping')
print(json.loads(l))