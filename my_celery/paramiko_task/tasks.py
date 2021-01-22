from my_celery.run import app
from my_celery.celery_base.task import BaseTask
from common.ssh_paramiko import Paramiko

@app.task(base=BaseTask)
def paramiko_ssh_task(host_list, local_file, remote_file, command):
    ssh_client = Paramiko(host_list=host_list,  command=command,  local_file=local_file, remote_file=remote_file,)
    return ssh_client.ssh_exec()






