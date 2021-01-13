from utils.rest_framework.base_view import NewModelViewSet
from rest_framework.views import APIView
from utils.rest_framework.base_response import new_response
from ..models import AnsibleProject
from ..serializers import AnsibleProjectSerializer
from rest_framework.decorators import action
from utils.config.get_config_value import get_value
from utils.config.ansible_host_list import get_ansible_host_group, get_ansible_host_file
import os
from django.conf import settings
class AnsibleProjectViewSet(NewModelViewSet):
    queryset = AnsibleProject.objects.all().order_by('id')
    serializer_class = AnsibleProjectSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    filter_fields = ('id', 'online_status', )

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            if not os.path.exists(os.path.join(settings.PLAYBOOK_DIR, data['path'])):
                os.mkdir(os.path.join(settings.PLAYBOOK_DIR, data['path']))
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return new_response(data=serializer.data)
            else:
                return new_response(code='10200', data='项目路径以存在', message='项目目录以存在， 请尝试其他目录或删除相同目录项目。')
            # serializer = self.get_serializer(data=request.data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            # return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')


    @action(methods=['get'], detail=False)
    def hosts_group(self, request):
        host_list = get_ansible_host_group(get_value('ansible','ansible_host_path'))
        return new_response(data=host_list)

    @action(methods=['get'], detail=False)
    def hosts_file(self, request):
        host_list = get_ansible_host_file(get_value('ansible', 'ansible_host_path'))
        return new_response(data=host_list)

    def update(self, request, *args, **kwargs):

        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            os.rename(os.path.join(settings.PLAYBOOK_DIR, instance.path), os.path.join(settings.PLAYBOOK_DIR, request.data['path']),)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not os.listdir(os.path.join(settings.PLAYBOOK_DIR, instance.path)):
                os.rmdir(os.path.join(settings.PLAYBOOK_DIR, instance.path))
                instance.delete()
                return new_response()
            else:
                return new_response(code=10200 , data='删除项目错误', message='此项目不为空， 请先清空项目中的文件。')
        except Exception as e:
            return new_response(code=10200,data='eroor', message=f'ERROR: {str(e)}')