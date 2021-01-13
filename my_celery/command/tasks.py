
import logging
import subprocess
from my_celery.run import app
from utils.script.subprocess_cmd import subexec_cmd
from my_celery.celery_base.task import BaseTask
@app.task(base=BaseTask)
def exec_command(command):
    try:
        output = subexec_cmd(command)
    except Exception as e:
        output = str(e)
    return output