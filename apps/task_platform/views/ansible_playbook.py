from django.conf import settings
from .BaseViewSet import Base
from ..models import AnsiblePlaybook, AnsibleProject
from ..serializers import AnsiblePlaybookSerializer
from utils.rest_framework.base_response import new_response
import os
import shutil


class AnsiblePlaybookViewSet(Base):
    queryset = AnsiblePlaybook.objects.all().order_by('id')
    serializer_class = AnsiblePlaybookSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name', 'file_name', 'online_status', 'src_user')
    filter_fields = ('id', 'project')

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            save_file_info = self.save_file('playbook', data)
            if not save_file_info['status']:
                return new_response(code=10200, data='数据保存失败', message=save_file_info['data'])
            data['file_name'] = save_file_info['data']
            data['src_user'] = self.get_user(request)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return new_response(data=serializer.data)

        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')

    def update(self, request, *args, **kwargs):

        try:
            data = request.data
            project_obj = AnsibleProject.objects.filter(id=data['project']).first()
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            old_project_path = instance.project.path
            new_project_path = project_obj.path
            if os.path.exists(os.path.join(settings.TASK_SCRIPT_DIR, new_project_path, instance.file_name)):
                return new_response(code=10200, data='脚本已经存在', message='新项目中已经存在同名脚本，请检查后重试。')
            shutil.move(os.path.join(settings.TASK_SCRIPT_DIR, old_project_path, instance.file_name),
                        os.path.join(settings.TASK_SCRIPT_DIR, new_project_path, instance.file_name))
            data['src_user'] = self.get_user(request)
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')
