# 定时任务
from .BaseViewSet import Base
from rest_framework.views import APIView
from utils.rest_framework.base_response import new_response
from utils.config.get_config_value import get_value
from utils.script.random_str import random_str
from .add_ansible import add_ansible_crontab, add_ssh_crontab
from ..models import CrontabTask
import uuid
# 实例化
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore())    # 指定存储
scheduler.start()
import os
from django.conf import settings
from .BaseViewSet import Base
class CrontabTsaskView(Base):
    permission_classes = []
    # def list(self, request, *args, **kwargs):
    #     res = {
    #         "code": 200,
    #         "msg": "success",
    #         "data": []
    #     }
    #     try:
    #         '''定时任务列表'''
    #         task_list = []
    #         job_list = scheduler.get_jobs()
    #         for job in job_list:
    #             tmp_dic = {
    #                 "id": job.id,
    #                 "next_run_time": job.next_run_time,
    #                 "task_title": "",
    #                 "task_remarks": ""
    #             }
    #             job_info_list = CrontabTask.objects.filter(task_id=job.id)
    #             if len(job_info_list) > 0:
    #                 tmp_dic["task_title"] = job_info_list[0].task_name
    #                 tmp_dic["task_remarks"] = job_info_list[0].task_remarks
    #             task_list.append(tmp_dic)
    #
    #         res["data"] = task_list
    #     except Exception as e:
    #         res["code"] = -1
    #         res["msg"] = e.args[0]
    #     return Response(res)
    def create(self, request, *args, **kwargs):
        data = request.data
        # {
        # 'name': '测试定时任务', 'run_type': 'ansible',  'task_lib': 'script',
        # 'ansible_type': 'CMDB', 'task_hosts': ['127.0.0.1'],
        # 'task_type': 'script', 'task_project': 'public', 'task_file': 'date.sh', 'task_args': '',
        # 'task_remarks': '',
        # 'execution_way': {'year': '*',
        # 'day_of_week': '*', 'month': '*', 'day': '*',
        # 'hour': '*', 'minute': 1, 'second': '*'}}
        file_path_info = self.get_abs_file(data)
        try:
            if file_path_info['status']:
                abs_file_path = file_path_info['data']
            else:
                return new_response(code=10200, data='文件未找到', message=file_path_info['data'])

            if  data['run_type'] == 'ansible':
                cmd = self.ansible_cmd(abs_file_path, data=data)
            else:
                cmd = self.ssh_cmd(abs_file_path, data)
            print(cmd)
            # print(cmd)
            # print(abs_file_path)
            # '''创建定时任务'''
            # task_title = request.data.get('task_title', '')
            # task_name = request.data.get('task_name', '')
            # task_remarks = request.data.get('task_remarks', '')
            # execution_way = request.data.get('execution_way', '')
            # if task_name == '' or execution_way == '':
            #     res["data"] = 'task_name和execution_way 参数必须传递'
            # else:
            task_id = uuid.uuid4().hex
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            # 注册定时任务
            print(cmd)
            history_data = {
                'src_user': self.get_user(request),
                'src_ip': ip,
                'task_type':'crontab',
                'task_host': data["task_hosts"],
                'task_name': data['name'],
                'crontab_id': task_id,
            }
            if data['run_type'] == 'ansible':
                scheduler.add_job(
                    add_ansible_crontab,
                    'cron',
                    args=[cmd, history_data],
                    id=task_id,
                    **data['execution_way'],
                )
            else:
                scheduler.add_job(
                    add_ssh_crontab,
                    'cron',
                    args=[cmd[0], history_data, abs_file_path, cmd[1]],
                    id=task_id,
                    **data['execution_way'],
                )
            # 注册任务
            register_events(scheduler)

            CrontabTask.objects.create(**{
                "name": data['name'],
                "task_id": task_id,
                "run_type": data['run_type'],
                "task_lib": data['task_lib'],
                "project": data['task_project'],
                "task_file": data["task_file"],
                "task_args": data["task_args"],
                "task_hosts": data["task_hosts"],
                "hosts_file": data["hosts_file"],
                "remarks": data['task_remarks'],
            })
            #     # 注册定时任务
            #     scheduler.add_job(
            #         add_execute_task,
            #         'cron',
            #         args=[os.path.join(os.getcwd(),'scripts',task_name), task_title],
            #         id=task_id,
            #         ** execution_way,
            #     )
            #     # 注册任务
            #     register_events(scheduler)
            #
            #
            #     CrontabTask.objects.create(**{
            #         "task_id": task_id,
            #         "task_name": task_title,
            #         "task_remarks": task_remarks,
            #     })
            return new_response()

            # ramdom_str = random_str()
            # file_name = abs_file_path.split('/')[-1]
            # remote_file_path = f'/tmp/{file_name}-{ramdom_str}'
            # if data['run_type'] == 'ansible':
            #     # cmd =
            #     ansible  = get_value("ansible", "abs_ansible_command")
            #     ansible_playbook = get_value("ansible", "abs_playbook_command")
            #     task_hosts = ','.join(data['task_hosts'])
            #     if abs_file_path.endswith('.sh'):
            #         command = f"{ansible} {task_hosts} -m script -a '{abs_file_path} {data['task_args']}'"
            #     elif abs_file_path.endswith('.py'):
            #         copy_file_cmd = f'ansible {task_hosts} -m copy -a "src={abs_file_path} dest={remote_file_path} mode=766" '
            #         exec_cmd = f'ansible {task_hosts} -m shell -a "chdir=/tmp/ ./{file_name} {data["args"]} && rm -f {remote_file_path}"  '
            #         command = f'{copy_file_cmd} && {exec_cmd}'
            #     elif abs_file_path.endswith('yaml') or abs_file_path.endswith('yml'):
            #         pass
            # elif data['run_type'] == 'SSH':
            #     ''' 调用 celery paramiko'''
            #     file_name = abs_file_path.split('/')[-1]
            #     remote_file_path = f'/tmp/{file_name}-{ramdom_str}'
            #     if abs_file_path.endswith('.sh'):
            #         command = f'bash {abs_file_path}  {data["task_args"]} && rm -rf {remote_file_path}'
            #     else:
            #         command = f'python {remote_file_path} {data["task_args"]} && rm -rf {remote_file_path}'
            # else:
            #     return new_response()
            # cmd = abs_file_path + ' ' + data['task_args']
            # print(cmd)
            # print(abs_file_path)
            # '''创建定时任务'''
            # task_title = request.data.get('task_title', '')
            # task_name = request.data.get('task_name', '')
            # task_remarks = request.data.get('task_remarks', '')
            # execution_way = request.data.get('execution_way', '')
            # if task_name == '' or execution_way == '':
            #     res["data"] = 'task_name和execution_way 参数必须传递'
            # else:
            #     task_id = uuid.uuid4().hex
            #     # 注册定时任务
            #     scheduler.add_job(
            #         add_execute_task,
            #         'cron',
            #         args=[os.path.join(os.getcwd(),'scripts',task_name), task_title],
            #         id=task_id,
            #         ** execution_way,
            #     )
            #     # 注册任务
            #     register_events(scheduler)
            #
            #
            #     CrontabTask.objects.create(**{
            #         "task_id": task_id,
            #         "task_name": task_title,
            #         "task_remarks": task_remarks,
            #     })
            return new_response()
        except Exception as e:

            return new_response(code=10200, message=str(e))
    # def update(self, request, *args, **kwargs):
    #     res = {
    #         "code": 200,
    #         "msg": "success",
    #         "data": []
    #     }
    #     try:
    #         task_id = request.data.get('task_id', '')
    #         task_status = request.data.get('task_status', -1)
    #         if task_status == 1:
    #             scheduler.resume_job(task_id)
    #             res["data"] = f'{task_id} 任务开启成功'
    #         elif task_status == 0:
    #             scheduler.pause_job(task_id)
    #             res["data"] = f'{task_id} 任务停止成功'
    #     except Exception as e:
    #         res["code"] = -1
    #         res["msg"] = e.args[0]
    #     return Response(res)
    # def delete(self, request, *args, **kwargs):
    #     res = {
    #         "code": 200,
    #         "msg": "success",
    #         "data": []
    #     }
    #     try:
    #         task_id = request.data.get('task_id', '')
    #         if task_id != '':
    #             scheduler.remove_job(task_id)
    #     except Exception as e:
    #         res["code"] = -1
    #         res["msg"] = e.args[0]
    #     return Response(res)