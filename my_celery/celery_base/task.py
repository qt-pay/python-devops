import celery
from celery.result import AsyncResult
from apps.task.models import TaskHistory
from my_celery.run import app
from apps.task.models import TaskHistory
import datetime
class BaseTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        task_obj = TaskHistory.objects.filter(task_id=task_id).first()
        star_time = task_obj.create_time
        end_time = datetime.datetime.now()
        run_time = (end_time - star_time).seconds
        args = str(args) + str(kwargs)  # 执行参数
        result_status = AsyncResult(id=task_id, app=app).status
        result_dic = {
            'task_code': retval['code'],
            'task_result': retval['data'],
            'task_status': result_status,
            'run_time': run_time,
            'script_cmd': args,
        }
        for k,v in result_dic.items():
            setattr(task_obj, k, v)
        task_obj.save()
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass