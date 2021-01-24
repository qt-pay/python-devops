from .BaseViewSet import Base
from ..models import TaskRecycle, ScriptFile, ScriptProject, AnsibleProject, AnsiblePlaybook
from ..serializers import TaskRecycleSerializer
from base.response import json_ok_response, json_error_response
from common.file import File

from django.conf import settings
from rest_framework.decorators import action


class TaskRecycleViewSet(Base):
    queryset = TaskRecycle.objects.all().order_by('-id')
    serializer_class = TaskRecycleSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('src_user', 'source_name', 'source_project_name', 'source_project_path', 'source_file_name')
    filter_fields = ('id', 'task_type')

    @action(methods=['post'], detail=True)
    def file_retrieve(self, request, pk):
        try:
            instance = self.get_object()

            if instance.task_type == 0:
                # 还原脚本文件
                now_abs_path = File.get_join_path(settings.TASK_RECYCLE_BIN,
                                                  'script',
                                                  instance.source_project_path,
                                                  instance.path)
                now_abs_project_path = File.get_join_path(settings.TASK_RECYCLE_BIN,
                                                          'script',
                                                          instance.source_project_path,
                                                          )
                project_obj = ScriptProject.objects.filter(path=instance.source_project_path).first()
                if not project_obj:
                    return json_error_response(message='原项目找不到，无法还原。')
                old_abs_file = File.get_join_path(settings.TASK_SCRIPT_DIR,
                                                  instance.source_project_path,
                                                  instance.source_file_name)
                new_abs_file = File.get_join_path(settings.TASK_RECYCLE_BIN,
                                                  'script',
                                                  instance.source_project_path,
                                                  instance.path,
                                                  instance.source_file_name)
                if File.if_dir_exists(old_abs_file):
                    return json_error_response(message='原项目中已经存在此项目，无法还原。')
                if not File.if_dir_exists(new_abs_file):
                    return json_error_response(message='回收站中找不到对应脚本，无法还原。')
                ScriptFile.objects.create(
                    name=instance.source_name,
                    file_name=instance.source_file_name,
                    project=project_obj,
                    src_user=self.get_user(request)
                )
                File.move_file(new_abs_file, File.get_file_name(old_abs_file))

            else:
                now_abs_path = File.get_join_path(settings.TASK_RECYCLE_BIN,
                                                  'playbook',
                                                  instance.source_project_path,
                                                  instance.path
                                                  )
                now_abs_project_path = File.get_join_path(settings.TASK_RECYCLE_BIN,
                                                          'playbook',
                                                          instance.source_project_path,
                                                          )
                project_obj = AnsibleProject.objects.filter(path=instance.source_project_path).first()
                if not project_obj:
                    return json_error_response(message='原项目找不到，无法还原。')
                if instance.source_file_name.endswith('.yaml'):
                    old_abs_file = File.get_join_path(settings.TASK_PLAYBOOK_DIR,
                                                      instance.source_project_path,
                                                      instance.source_file_name
                                                      )
                    new_abs_file = File.get_join_path(now_abs_path,
                                                      instance.source_file_name
                                                      )
                    if File.if_dir_exists(old_abs_file):
                        return json_error_response(message='原项目中已经存在此项目，无法还原。')
                    if not File.if_dir_exists(new_abs_file):
                        return json_error_response(message='回收站中找不到对应脚本，无法还原。')
                else:
                    old_abs_file = File.get_join_path(settings.TASK_PLAYBOOK_DIR,
                                                      instance.source_project_path,
                                                      )
                    new_abs_file = File.get_join_path(now_abs_path,
                                                      instance.source_file_name.split('/')[1]
                                                      )
                    if File.if_dir_exists(File.get_join_path(old_abs_file, instance.source_file_name.split('/')[1])):
                        return json_error_response(message='原项目中已经存在此项目，无法还原。')
                    if not File.if_dir_exists(
                            File.get_join_path(settings.TASK_RECYCLE_BIN,
                                               'playbook',
                                               instance.source_project_path,
                                               instance.path
                                               ) + instance.source_file_name):
                        return json_error_response(message='回收站中找不到对应脚本，无法还原。')

                AnsiblePlaybook.objects.create(
                    name=instance.source_name,
                    file_name=instance.source_file_name,
                    project=project_obj,
                    src_user=self.get_user(request)
                )

                File.move_file(new_abs_file, old_abs_file)
            # 清理数据
            if not File.get_dir_list(now_abs_path):
                File.rm_dir(now_abs_path)
                if not File.get_dir_list(now_abs_project_path):
                    File.rm_dir(now_abs_project_path)
            instance.delete()
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=f'ERROR: {str(e)}')

    @action(methods=['get'], detail=True)
    def file_detail(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            file_type = ['script', 'playbook']
            if instance.source_file_name.endswith('.yml'):
                abs_file = File.get_join_path(settings.TASK_RECYCLE_BIN,
                                              file_type[instance.task_type],
                                              instance.source_project_path,
                                              instance.path
                                              ) + instance.source_file_name
            else:
                abs_file = File.get_join_path(settings.TASK_RECYCLE_BIN,
                                              file_type[instance.task_type],
                                              instance.source_project_path,
                                              instance.path,
                                              instance.source_file_name)
            if File.if_file_exists(abs_file):
                file_content = File.read_file(abs_file)
            else:
                return json_error_response(message='文件不存在请检查后重试！')
            return json_ok_response(
                data={'id': instance.id, 'file_name': instance.source_file_name, 'content': file_content})
        except Exception as e:
            return json_error_response(message=str(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            file_type = ['script', 'playbook']
            now_abs_project_path = File.get_join_path(settings.TASK_RECYCLE_BIN,
                                                      file_type[instance.task_type],
                                                      instance.source_project_path,
                                                      )
            now_abs_path = File.get_join_path(now_abs_project_path,
                                              instance.path,
                                              )
            now_abs_file = File.get_join_path(now_abs_path,
                                              instance.source_file_name
                                              )
            if instance.source_file_name.endswith('.yml'):
                File.rm_dirs(File.get_join_path(now_abs_path,
                                                instance.source_file_name.split['/'][1]
                                                ))
            else:
                File.rm_dir(now_abs_file)
            if not File.get_dir_list(now_abs_path):
                File.rm_dir(now_abs_path)
                if not File.get_dir_list(now_abs_project_path):
                    File.rm_dir(now_abs_project_path)
            instance.delete()
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=f'ERROR: {str(e)}')
