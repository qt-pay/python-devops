from utils.rest_framework.base_response import new_response
from ..models import TaskScript, TaskProject, TaskRecycle
from ..serializers import TaskScriptSerializer
from rest_framework.decorators import action
from my_celery.script_task.tasks import script_task
from my_celery.paramiko_task.tasks import paramiko_ssh_task
import os
import pathlib
import shutil
from django.conf import settings
from utils.script.random_str import random_str
from .BaseViewSet import Base

class TaskScriptViewSet(Base):
    queryset = TaskScript.objects.all().order_by('id')
    serializer_class = TaskScriptSerializer
    ordering_fields = ('id', )
    filter_fields = ('id', 'project__path')
    search_fields = ('id', 'project__id')
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            script_file = data['sctiptFile']
            project = TaskProject.objects.filter(id=data['project']).first()
            res = self.save_file('script', script_file, project.path)
            if not res['status']:
                return new_response(code=10200, data='error', message=res['data'])

            new_data = {
                'name': data['name'],
                'file_name': script_file.name,
                'project': data['project'],
                'src_user': self.get_user(request)
            }
            serializer = self.get_serializer(data=new_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')


    # 删除
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            project_path = instance.project.path
            import datetime
            today = datetime.date.today()
            abs_path = os.path.join(settings.TASK_RECYCLE_BIN, 'script', project_path, str(today))
            old_abs_file = os.path.join(settings.TASK_SCRIPT_DIR,project_path,instance.file_name)

            if not os.path.exists(abs_path):
                os.makedirs(abs_path)
            shutil.move(old_abs_file, abs_path)

            TaskRecycle.objects.create(
                task_type = 'script',
                src_user = self.get_user(request),
                source_name= instance.name,
                source_project_path= project_path,
                source_file_name= instance.file_name,
                source_project_name= instance.project.name,
                path = str(today)
            )
            instance.delete()
            return new_response()
        except Exception as e:
            return new_response(code=10200,data='eroor', message=f'ERROR: {str(e)}')




    @action(methods=['post'], detail=False)
    def exec_cmd(self, request):
        data = request.data
        ramdom_str = random_str()
        # 找 project temp 对象
        project_obj = TaskProject.objects.filter(path='temp').first()
        if not project_obj:
            return new_response(code=10200, data='项目不存在', message='项目找不到，请创建路径为temp的项目。')

        # 判断脚本来源
        if data['script_source'] == 'local':
            script_file = data['local_scriptFile']
            res = self.save_file('script', script_file, 'temp')
            if not res['status']:
                return new_response(code=10200, data='error', message=res['data'])
            new_data = {
                'name': data['name'],
                'file_name': script_file.name,
                'project': project_obj.id,
                'src_user': self.get_user(request)
            }
            save = self.__save(new_data)
            if not save['status']:
                return new_response(code=10200, data='数据创建失败', message=save['data'])
            abs_file_path = res['data']


        # 判断脚本来源 是否是手动输入
        if data['script_source'] == 'manual':
            # 创建一个 pathlib 对象
            file_name = f"{data['name']}.{data['file_extension']}"
            abs_file_path = os.path.join(settings.TASK_SCRIPT_DIR, 'temp', file_name)
            if os.path.exists(abs_file_path):
                return new_response(code=10200, data='文件已存在', message='请更换任务名')
            file_obj = pathlib.Path(abs_file_path)
            file_obj.touch(mode=0o755)
            file_obj.write_text(data['command'])
            print(data['command'])
            # data = {'name': data['name'], 'script_name': file_name, }
            new_data = {
                'name': data['name'],
                'file_name': file_name,
                'project': project_obj.id,
                'src_user':  self.get_user(request)
            }
            save = self.__save(new_data)
            if not save['status']:
                return new_response(code=10200, data='数据创建失败', message=save['data'])

        # 判断脚本来源是否为服务器本地仓库
        if data['script_source'] == 'remote':
            file_name = data['remote_scriptFile']
            sctipt_obj = list(TaskScript.objects.filter(file_name=file_name,project__isnull=False).values('project__name','project__path'))
            abs_file_path = os.path.join(settings.TASK_SCRIPT_DIR, sctipt_obj[0]['project__path'], file_name)

        if not os.path.exists(abs_file_path):
            return new_response(code=10200, data='文件不存在', message=f'文件{abs_file_path} 文件不存在。')
        file_name = os.path.basename(abs_file_path)

        remote_file_path = f'/tmp/{file_name}-{ramdom_str}' # /temp/xxx.sh-JISAHOFH  用于SSH
        remote_file_name = f'{file_name}-{ramdom_str}'
        ''' ansible all -m script -a  '/data/touch.sh tmp' '''''
        if not data['host']:
            return new_response(code='10200', data='主机未选择', message='执行目标不能为空')
        host_list = data['host'].split(',')
        # 判断执行方式
        if data['type'] == 'Ansible':
            '''调用 celery ansible '''
            host = ','.join(host_list)
            if abs_file_path.endswith('.sh'):
                '''如果是sh脚本'''
                # get ansible 命令

                cmd = f"ansible {host} -m script -a '{abs_file_path} {data['args']}'"
                print(cmd)
            else:
                '''如果是 py 脚本'''
                copy_file_cmd = f'ansible {host} -m copy -a "src={abs_file_path} dest={remote_file_path} mode=766" '
                exec_cmd = f'ansible {host} -m shell -a "chdir=/tmp/ ./{remote_file_name} {data["args"]} && rm -f {remote_file_path}"  '
                cmd = f'{copy_file_cmd} && {exec_cmd}'

            # ansible 执行方式加入 celery 任务
            result = script_task.delay(cmd)
            self.record_log(request, data['name'], abs_file_path, result.id, host_list, data['type'])

        if data['type'] == 'SSH':
            ''' 调用 celery paramiko'''
            if file_name.endswith('.sh'):
                command = f'bash {remote_file_path}  {data["args"]} && rm -rf {remote_file_path}'
            else:
                command = f'python {remote_file_path} {data["args"]} && rm -rf {remote_file_path}'
            result = paramiko_ssh_task.delay(host_list=host_list,
                                             local_file=abs_file_path,
                                             remote_file=remote_file_path,
                                             command=command)
            self.record_log(request, data['name'], abs_file_path, result.id, host_list, data['type'])

        # TaskHistory.objects.create()
        return new_response(data='ok')





    def __save(self, data):
        res_dict = {'status': True, 'data': ''}
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            import sys
            exinfo = sys.exc_info()
            res_dict['status'] = False
            res_dict['data'] = exinfo
        return res_dict

