from my_celery.run import app
from utils.script.subprocess_cmd import subexec_cmd
from my_celery.celery_base.task import BaseTask
from utils.script.subprocess_cmd import subexec_cmd

@app.task(base=BaseTask)
def ansible_py_task(cmd):
    result =  subexec_cmd(cmd)
    return result