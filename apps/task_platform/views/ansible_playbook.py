import datetime

from .BaseViewSet import Base
from ..models import AnsiblePlaybook, AnsibleProject, TaskRecycle
from ..serializers import AnsiblePlaybookSerializer
from base.response import json_ok_response, json_error_response
from common.file import File

from django.conf import settings
from rest_framework.decorators import action


class AnsiblePlaybookViewSet(Base):
    queryset = AnsiblePlaybook.objects.all().order_by('id')
    serializer_class = AnsiblePlaybookSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name', 'file_name', 'online_status', 'src_user')
    filter_fields = ('id', 'project', 'online_status')

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            file_name, status = self.playbook_save(data)
            if not status:
                return json_error_response(message=data)
            data['file_name'] = file_name
            data['src_user'] = self.get_user(request)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return json_ok_response(data=serializer.data)

        except Exception as e:
            return json_error_response(message=str(e))

    def update(self, request, *args, **kwargs):

        try:
            data = request.data
            data['src_user'] = self.get_user(request)
            project_obj = AnsibleProject.objects.filter(id=data['project']).first()
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            old_project_path = instance.project.path
            new_project_path = project_obj.path
            if File.if_file_exists(File.get_join_path(settings.TASK_PLAYBOOK_DIR,
                                                      new_project_path,
                                                      instance.file_name)):
                return json_error_response(message='新项目中已经存在同名脚本，请检查后重试。')

            if File.if_file_endswith(instance.file_name, '.yaml'):
                File.move_file(File.get_join_path(settings.TASK_PLAYBOOK_DIR, old_project_path, instance.file_name),
                               File.get_join_path(settings.TASK_PLAYBOOK_DIR, new_project_path, ))
            else:
                File.move_file(
                    File.get_join_path(settings.TASK_PLAYBOOK_DIR, old_project_path, instance.file_name.split('/')[1]),
                    File.get_join_path(settings.TASK_PLAYBOOK_DIR, new_project_path, ))

            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return json_ok_response(data=serializer.data)
        except Exception as e:
            return json_error_response(message=str(e))

    @action(methods=['get'], detail=True)
    def playbook_detail(self, request, pk):
        try:
            instance = self.get_object()
            if File.if_file_endswith(instance.file_name, '.yaml'):
                abs_file = File.get_join_path(settings.TASK_PLAYBOOK_DIR, instance.project.path, instance.file_name)
            else:
                abs_file = File.get_join_path(settings.TASK_PLAYBOOK_DIR, instance.project.path, ) + instance.file_name
            if File.if_file_exists(abs_file):
                file_content = File.read_file(abs_file)

                return json_ok_response(
                    data={'id': instance.id, 'file_name': instance.file_name, 'content': file_content})
            else:
                return json_error_response(message='读取的文件不存在。')
        except Exception as e:
            return json_error_response(message=str(e))

    @action(methods=['put'], detail=True)
    def playbook_alter(self, request, pk):
        try:
            instance = self.get_object()
            content = request.data.get('content')
            file_name = request.data.get('file_name')
            if File.if_file_endswith(file_name, '.yaml'):
                old_abs_file = File.get_join_path(settings.TASK_PLAYBOOK_DIR, instance.project.path, instance.file_name)
                new_abs_file = File.get_join_path(settings.TASK_PLAYBOOK_DIR, instance.project.path, file_name)
                File.rm_dir(old_abs_file)
                instance.file_name = file_name
            elif File.if_file_endswith(file_name, '.yml'):
                new_abs_file = File.get_join_path(settings.TASK_PLAYBOOK_DIR,
                                                  instance.project.path, ) + instance.file_name
                File.rm_dir(new_abs_file)
            else:
                return json_error_response(message='文件名不合法，暂只支持 .yaml 结尾文件。')
            File.write_file(new_abs_file, content)
            instance.src_user = self.get_user(request)
            instance.save()
            return json_ok_response(data='文件更新成功')
        except Exception as e:
            return json_error_response(message=str(e))

    # 删除
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            project_path = instance.project.path
            abs_path = File.get_join_path(settings.TASK_RECYCLE_BIN, 'playbook', project_path,
                                          str(datetime.date.today()))
            if not File.if_file_exists(abs_path):
                File.create_dirs(abs_path)
            TaskRecycle.objects.create(
                task_type=1,
                src_user=self.get_user(request),
                source_name=instance.name,
                source_project_path=project_path,
                source_file_name=instance.file_name,
                source_project_name=instance.project.name,
                path=str(datetime.date.today())
            )
            if File.if_file_endswith(instance.file_name, '.yaml'):
                old_abs_file = File.get_join_path(settings.TASK_PLAYBOOK_DIR, project_path, instance.file_name)
            else:
                old_abs_file = File.get_join_path(settings.TASK_PLAYBOOK_DIR, project_path,
                                                  instance.file_name.split('/')[1])
            File.move_file(old_abs_file, abs_path)
            instance.delete()
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=f'ERROR: {str(e)}')
