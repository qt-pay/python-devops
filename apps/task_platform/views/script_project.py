import os

from .BaseViewSet import Base
from ..models import ScriptProject
from ..serializers import ScriptProjectSerializer
from base.response import json_ok_response, json_error_response

from django.conf import settings


class ScriptProjectViewSet(Base):
    queryset = ScriptProject.objects.all().order_by('id')
    serializer_class = ScriptProjectSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    filter_fields = ('id', 'name')

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            project_path = data['path']
            abs_path = os.path.join(settings.TASK_SCRIPT_DIR, project_path)

            if os.path.exists(abs_path):
                return json_error_response(message='项目文件夹已经存在，请检查后重测。')

            os.mkdir(abs_path)
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
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            old_dir_path = instance.path
            new_dir_path = data['path']
            abs_path = os.path.join(settings.TASK_SCRIPT_DIR, new_dir_path)
            if os.path.exists(abs_path):
                return json_error_response(message='项目路径已经存在请更换路径。', )
            data['src_user'] = self.get_user(request)
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            os.rename(os.path.join(settings.TASK_SCRIPT_DIR, old_dir_path),
                      os.path.join(settings.TASK_SCRIPT_DIR, new_dir_path))
            return json_ok_response(data=serializer.data)
        except Exception as e:
            return json_error_response(message=str(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            project_path = instance.path
            if not os.listdir(os.path.join(settings.TASK_SCRIPT_DIR, project_path)):
                os.rmdir(os.path.join(settings.TASK_SCRIPT_DIR, project_path))
                instance.delete()
            else:
                return json_error_response(message='目标文件夹不为空，请先清理其数据！')
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=f'ERROR: {str(e)}')
