from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import CloudServerSerializer
from ..models import CloudServer, Asset, AssetRecord

class CloudServerViewSet(NewModelViewSet):
    queryset = CloudServer.objects.all().order_by('id')
    serializer_class = CloudServerSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title', 'model')
    filter_fields = ('id', 'asset_obj')

    def create(self, request, *args, **kwargs):
        try:
            hostname = request.data['instance_id']
            type_id = request.data['type_id']
            # request.data.pop('type_id')
            if hostname and type_id:
                asset_obj = Asset.objects.create(title=hostname, device_type_id=int(type_id))
                asset_obj.save()
                request.data['asset_obj'] = asset_obj.id
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return new_response(data=serializer.data)
            else:
                return new_response(code=10200, data='error', message='hostname/type_id为必传参数')
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')


    def update(self, request, *args, **kwargs):

        try:
            row_map = {'instance_id': '实例ID', 'instance_name': '实例名称',  'instance_type': '实例类型',  'manage_ip': '管理IP',
                       'cpu': 'CPU核心数', 'memory': '制造商', 'intranet_ip': '内网IP', 'public_ip': '公网IP', 'os_version': '系统版本',
            'security_groupids': '安全组', 'expired_time':'实例到期时间',  'created_time': '实例创建时间','latest_date': '更新时间', 'create_at': '创建时间', 'asset_obj': '关联资产'}
            record_list =  []
            partial = kwargs.pop('partial', False)
            new_data = request.data
            instance = self.get_object()
            print(instance)
            print(request.data)
            for k, v in new_data.items():
                print(k, v)
                value = getattr(instance, k)
                print(value)
                if v != value:
                    record_list.append(f' 实例ID:{instance.instance_id}: {row_map[k]},由{value if value else "Null"}变更为{v}.')
                    setattr(instance, k, v)

            instance.save()
            if len(record_list) != 0:
                content = ';  '.join(record_list)
                self.asset_record(request, '服务器基本信息变更', content, instance.asset_obj.id)
            return new_response(data=instance.instance_id)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')
