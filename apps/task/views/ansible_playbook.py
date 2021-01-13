from utils.rest_framework.base_view import NewModelViewSet
from utils.rest_framework.base_response import new_response
from ..models import AnsiblePlaybook, AnsibleProject, TaskRecycle
from ..serializers import AnsiblePlaybookSerializer
import json
import os
import zipfile
import shutil
import tarfile
from .BaseViewSet import Base
from django.conf import settings

class AnsiblePlaybookViewSet(Base):
    queryset = AnsiblePlaybook.objects.all().order_by('id')
    serializer_class = AnsiblePlaybookSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    filter_fields = ('id', 'online_status', 'project__path')

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            project_obj = AnsibleProject.objects.filter(id=data['project']).first()
            # 等于 true 则为注册
            if data['register_status'] == 'true':
                if os.path.isfile(os.path.join(settings.PLAYBOOK_DIR, project_obj.path, data['file_name'])):
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return new_response(data=serializer.data)
                else:
                    return new_response(code=10200, data='文件不存在', message='注册文件不存在，请检查后重新注册！')
            else:
                playbook_file = data['playbook_file']
                save_status = self.save_file('playbook', playbook_file, project_obj.path)
                if save_status['status']:
                    data['file_name'] = save_status['data']
                    data['src_user'] = self.get_user(request)
                    serializer = self.get_serializer(data=data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return new_response(data=serializer.data)
                else:
                    return new_response(code=10200, data='Playbook创建失败', message=save_status['data'])

        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')



    # 删除
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            project_path = instance.project.path
            import datetime
            today = datetime.date.today()
            abs_path = os.path.join(settings.TASK_RECYCLE_BIN, 'playbook', project_path, str(today))
            old_abs_file = os.path.join(settings.TASK_PLAYBOOK_DIR, project_path, instance.file_name)
            if not os.path.exists(abs_path):
                os.makedirs(abs_path)
            shutil.move(old_abs_file, abs_path)

            TaskRecycle.objects.create(
                task_type='playbook',
                src_user=self.get_user(request),
                source_name=instance.name,
                source_project_path=project_path,
                source_file_name=instance.file_name,
                source_project_name=instance.project.name,
                path=str(today)
            )
            instance.delete()
            return new_response()
        except Exception as e:
            return new_response(code=10200, data='eroor', message=f'ERROR: {str(e)}')
