import os
import pathlib

from .BaseViewSet import Base
from ..models import ScriptFile, ScriptProject, AnsiblePlaybook
from my_celery.playbook_task.taks import ploybook_task
from my_celery.paramiko_task.tasks import paramiko_ssh_task
from my_celery.script_task.tasks import script_task
from base.response import json_ok_response, json_error_response

from django.conf import settings


class ExecViewSet(Base):

    def exec_script(self, request):
        try:
            data = request.data
            if data['script_source'] == 'library':
                script_file_obj = ScriptFile.objects.filter(id=data['script_id']).first()
                abs_file = os.path.join(settings.TASK_SCRIPT_DIR, script_file_obj.project.path,
                                        script_file_obj.file_name)
                if not os.path.join(abs_file):
                    return json_error_response(message=f'脚本库中找不到脚本名为{script_file_obj.file_name}的脚本')
            else:
                project_obj = ScriptProject.objects.filter(path='temp').first()
                if not project_obj:
                    return json_error_response(message='项目找不到，请创建路径为temp的项目。')

                file_name = f"{data['name']}.{data['script_extension']}"
                abs_file = os.path.join(settings.TASK_SCRIPT_DIR, 'temp', file_name)
                if os.path.exists(abs_file):
                    return json_error_response(message='请更换任务名')
                file_obj = pathlib.Path(abs_file)
                file_obj.touch(mode=0o755)
                file_obj.write_text(data['script_content'])

                new_data = {
                    'name': data['name'],
                    'file_name': file_name,
                    'project': project_obj,
                    'src_user': self.get_user(request)
                }
                ScriptFile.objects.create(**new_data)

            if data['run_type'] == 'ansible':
                cmd = self.ansible_cmd(abs_file, data)
                result = script_task.delay(cmd)
            else:
                cmd = self.ssh_cmd(abs_file, data)
                result = paramiko_ssh_task.delay(host_list=data['task_host_list'],
                                                 local_file=abs_file,
                                                 remote_file=cmd[1],
                                                 command=cmd[0])
            self.record_log(request, data['name'], abs_file, result.id, data['task_host_list'], 0, data['run_type'])
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=str(e))

    def exec_playbook(self, request):
        try:
            data = request.data
            playbook_obj = AnsiblePlaybook.objects.filter(id=data['playbook_id']).first()
            print(playbook_obj.file_name)
            if playbook_obj.file_name.endswith('yaml'):
                abs_file = os.path.join(settings.TASK_PLAYBOOK_DIR, playbook_obj.project.path, playbook_obj.file_name)
            else:
                abs_file = f'{os.path.join(settings.TASK_PLAYBOOK_DIR, playbook_obj.project.path)}{playbook_obj.file_name}'
            print(abs_file)
            if not os.path.isfile(abs_file):
                return json_error_response(message='所选项目或文件找不到')
            cmd = self.playbook_cmd(abs_file, data)
            result = ploybook_task.delay(cmd)
            self.record_log(request, data['name'], abs_file, result.id, None, 0, 'ansible')
            print(cmd)
            print(abs_file)
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=str(e))

    def exec_async(self, request):
        try:
            data = request.data
            if data['lib_type'] == 'script':
                script_obj = ScriptFile.objects.filter(id=data['script_id']).first()
                abs_file = os.path.join(settings.TASK_SCRIPT_DIR, script_obj.project.path, script_obj.file_name)
            else:
                playbook_obj = AnsiblePlaybook.objects.filter(id=data['script_id']).first()
                if playbook_obj.file_name.endswith('yaml'):
                    abs_file = os.path.join(settings.TASK_PLAYBOOK_DIR, playbook_obj.project.path,
                                            script_task.file_name)
                else:
                    abs_file = f'{os.path.join(settings.TASK_PLAYBOOK_DIR, playbook_obj.project.path)}{script_task.file_name}'

            if data['run_type'] == 'ansible':
                cmd = self.async_script_cmd(abs_file, data)
                result = script_task.delay(cmd)

            else:
                cmd = self.async_ssh_cmd(abs_file, data)
                result = paramiko_ssh_task.delay(host_list=data['task_host_list'],
                                                 local_file=abs_file,
                                                 remote_file=cmd[1],
                                                 command=cmd[0])
            self.record_log(request, data['name'], abs_file, result.id, data['middle_host'], 3, data['run_type'])
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=str(e))
