from my_celery.command.tasks import exec_command
from apps.task import models
from my_celery.script_task.tasks import script_task
from my_celery.paramiko_task.tasks import paramiko_ssh_task
import os
# name 'job_obj' is not defined
import pathlib
import datetime
def add_ansible_crontab(cmd,data):
    exec_result = script_task.delay(cmd)
    data['task_id'] = exec_result.id
    models.TaskHistory.objects.create(**data)



def add_ssh_crontab(cmd,data, abs_file_path, remote_file_path):
    exec_result = paramiko_ssh_task.delay(host_list=data['task_host'],
                                 local_file=abs_file_path,
                                 remote_file=remote_file_path,
                                 command=cmd)
    data['task_id'] = exec_result.id
    models.TaskHistory.objects.create(**data)