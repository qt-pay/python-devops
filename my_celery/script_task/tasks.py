from my_celery.run import app
from my_celery.celery_base.task import BaseTask
from utils.script.subprocess_cmd import subexec_cmd

@app.task(base=BaseTask)
def script_task(cmd):
    return subexec_cmd(cmd)