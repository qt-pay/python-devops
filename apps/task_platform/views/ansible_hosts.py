import os
import re

from base.views import BaseApiView
from common.get_config_value import get_value
from base.response import json_ok_response, json_error_response


class AnsibleGroup(BaseApiView):
    def get(self, request):
        try:
            file = get_value('ansible', 'ansible_host_path')
            host_list = [{'name': 'all', 'children': [{'name': 'all'}]}]
            if os.path.isfile(file):
                host_dic = {'name': '', 'children': []}
                host_dic['name'] = os.path.basename(file)
                with open(file) as f:
                    for line in f:
                        hosts = re.match('^\s*\[(?P<host>.*)\]', line)
                        if hosts:
                            host_dic['children'].append({'name': hosts.group('host')})
                    host_list.append(host_dic)
            else:
                host_file_list = os.listdir(file)
                for item in host_file_list:
                    abs_file = os.path.join(file, item)
                    host_dic = {'name': '', 'children': []}
                    host_dic['name'] = os.path.basename(abs_file)
                    if os.path.isfile(abs_file):
                        with open(abs_file) as f:
                            for line in f:
                                hosts = re.match('^\s*\[(?P<host>.*)\]', line)
                                if hosts:
                                    host_dic['children'].append({'name': hosts.group('host')})
                            host_list.append(host_dic)
            return json_ok_response(data=host_list)
        except Exception as e:
            return json_error_response(message=str(e))


class AnsibleHosts(BaseApiView):
    def get(self, request):
        try:
            file = get_value('ansible', 'ansible_host_path')
            host_list = []
            if os.path.isfile(file):
                host_list.append({'name': host_list.append(os.path.basename(file))})
            else:
                host_file_list = os.listdir(file)
                for files in host_file_list:
                    if os.path.isfile(os.path.join(file, files)):
                        host_list.append({'name': files})
            return json_ok_response(data=host_list)
        except Exception as e:
            return json_error_response(message=str(e))
