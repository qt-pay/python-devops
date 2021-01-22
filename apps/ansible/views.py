import os

from .serializers import *
from .models import *
from base.views import BaseModelViewSet, BaseApiView
from base.response import json_ok_response, json_error_response

from common.get_config_value import get_ansible_host_list, get_value
from common.get_config_value import get_value
from common.subprocess_cmd import subexec_cmd

from rest_framework.decorators import action
from rest_framework.views import APIView


class ProjectViewSet(BaseModelViewSet):
    queryset = Project.objects.all().order_by('id')
    serializer_class = ProjectSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    filter_fields = ('id', 'online_status',)

    @action(methods=['get'], detail=False)
    def host_list(self, request):
        host_list = get_ansible_host_list(get_value('ansible_host_path'))
        print(host_list)
        return json_ok_response(data=host_list)


#
class JobViewSet(BaseModelViewSet):
    queryset = Job.objects.all().order_by('id')
    serializer_class = JobSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    filter_fields = ('id', 'project', 'online_status',)


class ExtravarsViewSet(BaseModelViewSet):
    queryset = Extravars.objects.all().order_by('id')
    serializer_class = ExtravarsSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    filter_fields = ('id', 'job', 'online_status',)


class HistoryViewSet(BaseModelViewSet):
    queryset = History.objects.all().order_by('-id')
    serializer_class = HistorySerializer
    ordering_fields = ('id', 'task_name',)
    search_fields = ('task_name',)


class Task_SubmitView(BaseApiView):
    '''
    host: Array(2)
        0: "127.0.0.1"
        1: "127.0.0.1"
        length: 2
        __ob__: Observer {value: Array(2), dep: Dep, vmCount: 0}
        __proto__: Array
        path: "test"
        playbook: "test"
        vers: "version=v1.1"
    '''

    def post(self, request):
        ''' 解密 加数据校验 '''
        # {'path': 'test', 'playbook': 'test', 'vers': 'version=v1.1', 'host': ['127.0.0.1']}
        data = request.data
        cmd = self.__cmd(data)
        res = subexec_cmd(cmd)
        # res = get_connection('127.0.0.1', 'root', 'devops', cmd,22)
        return json_ok_response(data=res['data'])

    def __cmd(self, data_dic):
        project_base_path = get_value('project_base_path')
        # print(os.path.join(project_base_path, data['path'],  data['playbook']))
        if project_base_path.endswith("/"):
            project_path = get_value('project_base_path') + data_dic['path']
        else:
            project_path = get_value('project_base_path') + '/' + data_dic['path']

        if project_path.endswith("/"):
            abs_playbook_path = project_path + data_dic['playbook']
        else:
            abs_playbook_path = project_path + '/' + data_dic['playbook']
        if not data_dic['host'] and not data_dic['vers']:
            cmd = f'{get_value("abs_playbook_command")} {abs_playbook_path} '

        elif not data_dic['host']:
            vers = data_dic['vers']
            cmd = f'{get_value("abs_playbook_command")} {abs_playbook_path} -e {vers}'

        elif not data_dic['vers']:
            host_base_path = get_value('ansible_host_path')
            if os.path.isfile(host_base_path):
                host_path = host_base_path
            else:
                if host_base_path.endswith('/'):
                    host_path = host_base_path + data_dic['host']
                else:
                    host_path = host_base_path + '/' + data_dic['host']
            cmd = f'{get_value("abs_playbook_command")} {abs_playbook_path} -i {host_path}'
        else:
            vers = data_dic['vers']
            host_base_path = get_value('ansible_host_path')
            if os.path.isfile(host_base_path):
                host_path = host_base_path
            else:
                if host_base_path.endswith('/'):
                    host_path = host_base_path + data_dic['host']
                else:
                    host_path = host_base_path + '/' + data_dic['host']
            cmd = f'{get_value("abs_playbook_command")} {abs_playbook_path} -i {host_path} -e {vers}'
        return cmd
