from base.response import json_ok_response, json_error_response
from base.views import BaseModelViewSet
from apps.cmdb import models
import importlib
from ..utils.api_decode import decrypt_get, decrypt_post
from ..utils.client_asset.conf import clean_data_path
from django.db.models import Q


class ClentAsset(BaseModelViewSet):
    # permission_classes = []
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        try:
            ''' 判断token值 '''
            client_md5_token = request.META.get('HTTP_TOKEN')
            if not client_md5_token:
                return json_error_response(message='必须传递: HTTP_TOKEN')

            result = decrypt_get(client_md5_token)
            if result['code'] != 2000:
                return json_error_response(message=request['message'])
            '''  业务代码 '''
            import datetime
            server_list = list(models.Server.objects.filter(
                Q(latest_date__lt=datetime.date.today()) | Q(latest_date__isnull=True)).values_list('hostname',
                                                                                                    'manage_ip'))
            return json_ok_response(data=server_list)

        except Exception as e:
            return json_error_response(message=str(e))

    def create(self, request, *args, **kwargs):
        try:

            ''' 解密 加数据校验 '''
            data = request.data.get('data')
            if not data:
                return json_error_response(message='data 必须传递')
            result_dic = decrypt_post(data)
            if not result_dic:
                return json_error_response(message='数据格式不正确')

            ''' 业务逻辑 '''
            hostname = result_dic['basic']['data']['hostname']
            server_obj = models.Server.objects.filter(hostname=hostname).first()
            if server_obj:
                # 循环数据处理插件
                for k, v in clean_data_path.items():
                    if k in result_dic:
                        module_path, class_name = v.rsplit('.', 1)
                        m = importlib.import_module(module_path)
                        if hasattr(m, class_name):
                            cls = getattr(m, class_name)
                            if hasattr(cls, 'initial'):
                                obj = cls.initial(server_obj)
                            else:
                                obj = cls()
                            obj.parse(result_dic[k], )
                return json_ok_response()
            else:
                return json_error_response(message=f'{hostname} 资产必须先录入', )
        except Exception as e:
            return json_error_response(message=str(e))
