from subprocess import Popen, PIPE
import sys

def subexec_cmd(cmd):
    ret_dic = {'code': 0, 'data': ''}
    try:
        ret_dic = {'code': 0, 'data': ''}
        pcmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = pcmd.communicate()
        print(stdout, stderr)
        retcode = pcmd.poll()
        if retcode != 0:
            ret_dic['code'] = 10200

        if  stdout:
            ret_dic['data'] = stdout.decode('utf-8')
        else:
            ret_dic['data'] = stderr.decode('utf-8')
    except Exception as e:
        ret_dic['code'] = 10200
        ret_dic['data'] = str(e)
    return ret_dic

