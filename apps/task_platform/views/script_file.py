import os
import pathlib
import datetime
import shutil

from .BaseViewSet import Base
from ..models import ScriptFile, ScriptProject, TaskRecycle
from ..serializers import ScriptFileSerializer
from base.response import json_ok_response, json_error_response

from django.conf import settings
from rest_framework.decorators import action


class ScriptFileViewSet(Base):
    queryset = ScriptFile.objects.all().order_by('id')
    serializer_class = ScriptFileSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name', 'file_name', 'exec_unm', 'src_user')
    filter_fields = ('id', 'project')

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            save_file_info = self.script_save(data)
            if not save_file_info['status']:
                return json_error_response(message=save_file_info['data'])
            data['file_name'] = save_file_info['data']
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
            project_obj = ScriptProject.objects.filter(id=data['project']).first()
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            old_project_path = instance.project.path
            new_project_path = project_obj.path
            if os.path.exists(os.path.join(settings.TASK_SCRIPT_DIR, new_project_path, instance.file_name)):
                return json_error_response(message='新项目中已经存在同名脚本，请检查后重试。')
            shutil.move(os.path.join(settings.TASK_SCRIPT_DIR, old_project_path, instance.file_name),
                        os.path.join(settings.TASK_SCRIPT_DIR, new_project_path, instance.file_name))
            data['src_user'] = self.get_user(request)
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return json_ok_response(data=serializer.data)
        except Exception as e:
            return json_error_response(message=str(e))

    @action(methods=['get'], detail=True)
    def script_detail(self, request, pk):
        try:
            instance = self.get_object()
            abs_file = os.path.join(settings.TASK_SCRIPT_DIR, instance.project.path, instance.file_name)
            if os.path.isfile(abs_file):
                file_obj = pathlib.Path(abs_file)
                file_content = file_obj.read_text(encoding='utf-8')

                return json_ok_response(
                    data={'id': instance.id, 'file_name': instance.file_name, 'content': file_content})
            else:
                return json_error_response(message='读取的文件不存在。')
        except Exception as e:
            return json_error_response(message=str(e))

    @action(methods=['put'], detail=True)
    def script_alter(self, request, pk):
        try:
            instance = self.get_object()
            content = request.data.get('content')
            file_name = request.data.get('file_name')
            if file_name.endswith('.sh') or file_name.endswith('.py'):
                old_abs_file = os.path.join(settings.TASK_SCRIPT_DIR, instance.project.path, instance.file_name)
                new_abs_file = os.path.join(settings.TASK_SCRIPT_DIR, instance.project.path, file_name)
                os.remove(old_abs_file)
                file_obj = pathlib.Path(new_abs_file)
                instance.file_name = file_name
                instance.src_user = self.get_user(request)
                instance.save()
                file_obj.write_text(content, encoding='utf-8')
                return json_ok_response(data='文件更新成功')
            else:
                return json_error_response(message='文件名不合法，暂只支持 .sh/.py 结尾文件。')
        except Exception as e:
            return json_error_response(message=str(e))

    # 删除
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            project_path = instance.project.path
            abs_path = os.path.join(settings.TASK_RECYCLE_BIN, 'script', project_path, str(datetime.date.today()))
            old_abs_file = os.path.join(settings.TASK_SCRIPT_DIR, project_path, instance.file_name)

            if not os.path.exists(abs_path):
                os.makedirs(abs_path)

            TaskRecycle.objects.create(
                task_type=0,
                src_user=self.get_user(request),
                source_name=instance.name,
                source_project_path=project_path,
                source_file_name=instance.file_name,
                source_project_name=instance.project.name,
                path=str(datetime.date.today())
            )
            shutil.move(old_abs_file, abs_path)
            instance.delete()
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=f'ERROR: {str(e)}')
