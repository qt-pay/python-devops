import os
import importlib

from apps.cmdb import models
from base.views import BaseModelViewSet
from base.response import json_ok_response, json_error_response

from common.get_config_value import config, config_path


class EditConf(BaseModelViewSet):
    def list(self, request):
        try:
            cfg = config()
            conf_dic = {}
            for section in cfg.sections():
                item_dic = {}
                for item in cfg.items(section):
                    item_dic[item[0]] = item[1]
                conf_dic[section] = item_dic
            return json_ok_response(data=conf_dic)
        except Exception as e:
            return json_error_response(message=str(e))

    def update(self, request, *args, **kwargs):
        try:
            exists_list = []
            cfg = config()
            data = request.data
            exists_list.append(data['ansible']['ansible_host_path'])
            exists_list.append(data['ansible']['project_base_path'])
            for path in exists_list:
                if not os.path.exists(path):
                    return json_error_response(message=f'文件或目录不存在请核对后再试: {path}')
            for iname in data.keys():
                for k, v in data[iname].items():
                    cfg.set(iname, k, v)
            cfg.write(open(config_path, "w", encoding='utf-8'))
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=str(e))
