from django.conf import settings
from rest_framework.decorators import action

from .BaseViewSet import Base
from ..models import TaskRecycle, ScriptFile, ScriptProject, AnsibleProject, AnsiblePlaybook
from ..serializers import TaskRecycleSerializer
from utils.rest_framework.base_response import new_response
import os
import shutil
import pathlib


class TaskRecycleViewSet(Base):
    queryset = TaskRecycle.objects.all().order_by('-id')
    serializer_class = TaskRecycleSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('src_user', 'source_name', 'source_project_name', 'source_project_path', 'source_file_name')
    filter_fields = ('id', 'task_type')

    # @action(methods=['post'], detail=True)
    # def view_details(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     abs_file = os.path.join(settings.TASK_RECYCLE_BIN, instance.task_type, instance.source_project_path,
    #                             instance.path, instance.source_file_name)
    #     print(abs_file)
    #     if os.path.isfile(abs_file):
    #         import pathlib
    #         file_obj = pathlib.Path(abs_file)
    #         file_content = file_obj.read_text()
    #     else:
    #         return new_response(code=10200, data='文件不存在', message='文件不存在请检查后重试！')
    #     return new_response(data=file_content)

    @action(methods=['post'], detail=True)
    def file_retrieve(self, request, pk):
        try:
            instance = self.get_object()

            if instance.task_type == 0:
                # 还原脚本文件
                now_abs_path = os.path.join(settings.TASK_RECYCLE_BIN, 'script', instance.source_project_path,
                                            instance.path)
                now_abs_project_path = os.path.join(settings.TASK_RECYCLE_BIN, 'script', instance.source_project_path,
                                                    )
                project_obj = ScriptProject.objects.filter(path=instance.source_project_path).first()
                if not project_obj:
                    return new_response(code=10200, data='原项目找不到', message='原项目找不到，无法还原。')
                old_abs_file = os.path.join(settings.TASK_SCRIPT_DIR, instance.source_project_path,
                                            instance.source_file_name)
                new_abs_file = os.path.join(settings.TASK_RECYCLE_BIN, 'script', instance.source_project_path,
                                            instance.path, instance.source_file_name)
                if os.path.exists(old_abs_file):
                    return new_response(code=10200, data='文件已经存在', message='原项目中已经存在此项目，无法还原。')
                if not os.path.exists(new_abs_file):
                    return new_response(code=10200, data='文件找不到', message='回收站中找不到对应脚本，无法还原。')
                ScriptFile.objects.create(
                    name=instance.source_name,
                    file_name=instance.source_file_name,
                    project=project_obj,
                    src_user=self.get_user(request)
                )
                shutil.move(new_abs_file, os.path.dirname(old_abs_file))

            else:
                now_abs_path = os.path.join(settings.TASK_RECYCLE_BIN, 'playbook', instance.source_project_path,
                                            instance.path)
                now_abs_project_path = os.path.join(settings.TASK_RECYCLE_BIN, 'playbook', instance.source_project_path,
                                                    )
                project_obj = AnsibleProject.objects.filter(path=instance.source_project_path).first()
                if not project_obj:
                    return new_response(code=10200, data='原项目找不到', message='原项目找不到，无法还原。')
                if instance.source_file_name.endswith('.yaml'):
                    old_abs_file = os.path.join(settings.TASK_PLAYBOOK_DIR, instance.source_project_path,
                                                instance.source_file_name)
                    new_abs_file = os.path.join(now_abs_path, instance.source_file_name)
                    if os.path.exists(old_abs_file):
                        return new_response(code=10200, data='文件已经存在', message='原项目中已经存在此项目，无法还原。')
                    if not os.path.exists(new_abs_file):
                        return new_response(code=10200, data='文件找不到', message='回收站中找不到对应脚本，无法还原。')
                else:
                    old_abs_file = os.path.join(settings.TASK_PLAYBOOK_DIR, instance.source_project_path, )
                    new_abs_file = os.path.join(now_abs_path, instance.source_file_name.split('/')[1])
                    if os.path.exists(os.path.join(old_abs_file, instance.source_file_name.split('/')[1])):
                        return new_response(code=10200, data='文件已经存在', message='原项目中已经存在此项目，无法还原。')
                    if not os.path.exists(
                            os.path.join(settings.TASK_RECYCLE_BIN, 'playbook', instance.source_project_path,
                                         instance.path, ) + instance.source_file_name):
                        return new_response(code=10200, data='文件找不到', message='回收站中找不到对应脚本，无法还原。')

                AnsiblePlaybook.objects.create(
                    name=instance.source_name,
                    file_name=instance.source_file_name,
                    project=project_obj,
                    src_user=self.get_user(request)
                )

                shutil.move(new_abs_file, old_abs_file)
            # 清理数据
            if not os.listdir(now_abs_path):
                os.rmdir(now_abs_path)
                if not os.listdir(now_abs_project_path):
                    os.rmdir(now_abs_project_path)
            instance.delete()
            return new_response()
        except Exception as e:
            return new_response(code=10200, data='error', message=f'ERROR: {str(e)}')

    @action(methods=['get'], detail=True)
    def file_detail(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            file_type = ['script', 'playbook']
            if instance.source_file_name.endswith('.yml'):
                abs_file = os.path.join(settings.TASK_RECYCLE_BIN, file_type[instance.task_type],
                                        instance.source_project_path, instance.path) + instance.source_file_name
            else:
                abs_file = os.path.join(settings.TASK_RECYCLE_BIN, file_type[instance.task_type],
                                        instance.source_project_path, instance.path, instance.source_file_name)
            if os.path.isfile(abs_file):
                file_obj = pathlib.Path(abs_file)
                file_content = file_obj.read_text()
            else:
                return new_response(code=10200, data='文件不存在', message='文件不存在请检查后重试！')
            return new_response(
                data={'id': instance.id, 'file_name': instance.source_file_name, 'content': file_content})
        except Exception as e:
            return new_response(code='10200', data='获取文件详情出错', message=str(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            file_type = ['script', 'playbook']
            now_abs_project_path = os.path.join(settings.TASK_RECYCLE_BIN, file_type[instance.task_type],
                                                instance.source_project_path,
                                                )
            now_abs_path = os.path.join(now_abs_project_path,
                                        instance.path,
                                        )
            now_abs_file = os.path.join(now_abs_path,
                                        instance.source_file_name
                                        )
            if instance.source_file_name.endswith('.yml'):
                shutil.rmtree(os.path.join(now_abs_path, instance.source_file_name.split['/'][1]))
            else:
                os.remove(now_abs_file)
            if not os.listdir(now_abs_path):
                os.rmdir(now_abs_path)
                if not os.listdir(now_abs_project_path):
                    os.rmdir(now_abs_project_path)
            instance.delete()
            return new_response()
        except Exception as e:
            return new_response(code=10200, data='eroor', message=f'ERROR: {str(e)}')
