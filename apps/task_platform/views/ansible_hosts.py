from rest_framework.views import APIView
from utils.rest_framework.base_response import new_response
import os
import re
from utils.config.get_config_value import get_value


# def get_ansible_host_group(file):
#     host_list = [{'name': 'all', 'children': [{'name': 'all'}]}]
#     if os.path.isfile(file):
#         host_dic = {'name': '', 'children': []}
#         host_dic['name'] = os.path.basename(file)
#         with open(file) as f:
#             for line in f:
#                 hosts = re.match('^\s*\[(?P<host>.*)\]', line)
#                 if hosts:
#                     host_dic['children'].append({'name': hosts.group('host')})
#             host_list.append(host_dic)
#     else:
#         host_file_list = os.listdir(file)
#         for item in host_file_list:
#             abs_file = os.path.join(file, item)
#             host_dic = {'name': '', 'children': []}
#             host_dic['name'] = os.path.basename(abs_file)
#             if os.path.isfile(abs_file):
#                 with open(abs_file) as f:
#                     for line in f:
#                         hosts = re.match('^\s*\[(?P<host>.*)\]', line)
#                         if hosts:
#                             host_dic['children'].append({'name': hosts.group('host')})
#                     host_list.append(host_dic)
#     return host_list
#
#
# def get_ansible_host_file(file):
#     host_list = []
#     if os.path.isfile(file):
#         host_list.append({'name': host_list.append(os.path.basename(file))})
#     else:
#         host_file_list = os.listdir(file)
#         for files in host_file_list:
#             if os.path.isfile(os.path.join(file, files)):
#                 host_list.append({'name': files})
#     return host_list


class AnsibleGroup(APIView):
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
            return new_response(data=host_list)
        except Exception as e:
            return new_response(code='10200', data='error', message=str(e))


class AnsibleHosts(APIView):
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
            return new_response(data=host_list)
        except Exception as e:
            return new_response(code='10200', data='error', message=str(e))
