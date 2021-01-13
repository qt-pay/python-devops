from utils.rest_framework.base_view import NewModelViewSet
from rest_framework.views import APIView
from utils.rest_framework.base_response import new_response
from ..models import TaskRecycle
from ..serializers import TaskRecycleSerializer, TaskScript, AnsiblePlaybook, TaskProject, AnsibleProject
from rest_framework.decorators import action
from utils.config.get_config_value import get_value
from utils.config.ansible_host_list import get_ansible_host_group, get_ansible_host_file
import os
import shutil
from django.conf import settings
from .BaseViewSet import Base


class TaskRecycleViewSet(Base):
    queryset = TaskRecycle.objects.all().order_by('-id')
    serializer_class = TaskRecycleSerializer
    ordering_fields = ('id', 'path',)
    search_fields = ('source_name',)
    filter_fields = ('id', 'task_type',)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            now_abs_project_path = os.path.join(settings.TASK_RECYCLE_BIN,
                                                data['task_type'],
                                                data['source_project_path'],
                                                )
            now_abs_path = os.path.join(now_abs_project_path, data['path'])
            now_abs_file = os.path.join(now_abs_path,
                                        data['source_file_name']
                                        )
            if not os.path.isfile(now_abs_file):
                return new_response(code=10200, data='数据还原出错', message='回收站中找不到相应的文件，请检查后重试！')

            # {'id': 3, 'task_type': 'playbook', 'src_user': '闫世成', 'source_name': '查看时间', 'source_project_name': None,
            # 'source_project_path': 'public1', 'source_file_name': 'date.yaml', 'path': '2021-01-09'}

            if data['task_type'] == 'script':
                scr_abs_path = os.path.join(settings.TASK_SCRIPT_DIR, data['source_project_path'])
                if not os.path.isdir(scr_abs_path):
                    return new_response(code=10200, data='数据还原出错', message='目标项目路径找不到，无法还原！')
                if os.path.exists(os.path.join(scr_abs_path, data['source_file_name'])):
                    return new_response(code=10200, data='数据还原出错', message='原项目中已存在目标文件，无法还原！')
                project_obj = TaskProject.objects.filter(path=data['source_project_path']).first()
                shutil.move(now_abs_file, scr_abs_path)

                TaskScript.objects.create(name=data['source_name'],
                                          file_name=data['source_file_name'],
                                          project=project_obj,
                                          src_user=self.get_user(request))


            elif data['task_type'] == 'playbook':
                scr_abs_path = os.path.join(settings.TASK_PLAYBOOK_DIR, data['source_project_path'])
                if not os.path.isdir(scr_abs_path):
                    return new_response(code=10200, data='数据还原出错', message='目标项目路径找不到，无法还原！')
                if os.path.exists(os.path.join(scr_abs_path, data['source_file_name'])):
                    return new_response(code=10200, data='数据还原出错', message='原项目中已存在目标文件，无法还原！')
                project_obj = AnsibleProject.objects.filter(path=data['source_project_path']).first()
                shutil.move(now_abs_file, scr_abs_path)
                AnsiblePlaybook.objects.create(name=data['source_name'],
                                               file_name=data['source_file_name'],
                                               project=project_obj,
                                               src_user=self.get_user(request)
                                               )

            else:
                return new_response(code=10200, data='数据还原出错', message='还原类型未定义，请检查后重试！')

            # 清理数据
            if not os.listdir(now_abs_path):
                os.rmdir(now_abs_path)
                if not os.listdir(now_abs_project_path):
                    os.rmdir(now_abs_project_path)
            TaskRecycle.objects.filter(id=data['id']).delete()
            return new_response(data='还原成功')
        except Exception as e:
            return new_response(code=10200, message=str(e), data='数据还原出错')

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            now_abs_project_path = os.path.join(settings.TASK_RECYCLE_BIN, instance.task_type,
                                                instance.source_project_path,
                                                )
            now_abs_path = os.path.join(now_abs_project_path,
                                        instance.path,
                                        )
            now_abs_file = os.path.join(now_abs_path,
                                        instance.source_file_name
                                        )
            if os.path.isfile(now_abs_file):
                os.remove(now_abs_file)
            if not os.listdir(now_abs_path):
                os.rmdir(now_abs_path)
                if not os.listdir(now_abs_project_path):
                    os.rmdir(now_abs_project_path)
            instance.delete()
            return new_response()
        except Exception as e:
            return new_response(code=10200, data='eroor', message=f'ERROR: {str(e)}')

    # ansible - recycle - bin / view_details /$
    @action(methods=['get'], detail=True)
    def view_details(self, request, *args, **kwargs):
        instance = self.get_object()
        abs_file = os.path.join(settings.TASK_RECYCLE_BIN, instance.task_type,  instance.source_project_path, instance.path, instance.source_file_name)
        print(abs_file)
        if os.path.isfile(abs_file):
            import pathlib
            file_obj = pathlib.Path(abs_file)
            file_content = file_obj.read_text()
        else:
            return new_response(code=10200, data='文件不存在', message='文件不存在请检查后重试！')
        return new_response(data=file_content)


    def retrieve(self, request, *args, **kwargs):
        # 封装的 get_object 拿对象
        print('aaaaaaaaaaaaaaa')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return new_response(serializer.data)