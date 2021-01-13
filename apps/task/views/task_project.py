from utils.rest_framework.base_view import NewModelViewSet
from ..models import TaskProject
from ..serializers import TaskProjectSerializer
from utils.rest_framework.base_response import new_response
import os
from django.conf import settings
class TaskProjectViewSet(NewModelViewSet):
    queryset = TaskProject.objects.all().order_by('id')
    serializer_class = TaskProjectSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    filter_fields = ('id', )

    def create(self, request, *args, **kwargs):
        try:
            project_path = request.data.get('path')
            abs_path = os.path.join(settings.BASE_DIR, 'scripts', project_path)
            if not os.path.exists(abs_path):
                os.mkdir(abs_path)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            old_dir_name = instance.path
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            new_dir_name = serializer.data['path']
            os.rename(os.path.join(settings.BASE_DIR, 'scripts', old_dir_name), os.path.join(settings.BASE_DIR, 'scripts', new_dir_name))
            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            dir_name = instance.path
            if not os.listdir(os.path.join(settings.BASE_DIR,'scripts', dir_name)):
                instance.delete()
            else:
                return new_response(code=10200, data='删除出错', message='目标文件夹不为空，请先清理其数据！')
            #
            return new_response()
        except Exception as e:
            return new_response(code=10200, data='eroor', message=f'ERROR: {str(e)}')