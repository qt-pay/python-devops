from base.views import BaseApiView
from base.response import json_ok_response, json_error_response
from common.ansible import Ansible


class AnsibleGroup(BaseApiView):
    def get(self, request, *args, **kwargs):
        """ return all ansible inventory group """
        try:
            return json_ok_response(data=Ansible.get_group())
        except Exception as e:
            return json_error_response(message=str(e))


class AnsibleHosts(BaseApiView):
    def get(self, request):
        """ return all ansible inventory hosts file"""
        try:
            return json_ok_response(data=Ansible.get_hosts())
        except Exception as e:
            return json_error_response(message=str(e))
