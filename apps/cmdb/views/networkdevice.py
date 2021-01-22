from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import NetworkDeviceSerializer
from ..models import NetworkDevice, Asset


class NetworkDeviceViewSet(Base):
    queryset = NetworkDevice.objects.all().order_by('id')
    serializer_class = NetworkDeviceSerializer
    ordering_fields = ('id', 'hostname',)
    search_fields = ('hostname', 'manage_ip')
    filter_fields = ('id', 'asset_obj')

    def create(self, request, *args, **kwargs):
        try:
            hostname = request.data['hostname']
            type_id = request.data['type_id']
            # request.data.pop('type_id')
            if hostname and type_id:
                asset_obj = Asset.objects.create(title=hostname, device_type_id=int(type_id))
                asset_obj.save()
                request.data['asset_obj'] = asset_obj.id
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return json_ok_response(data=serializer.data)
            else:
                return json_error_response(message='hostname/type_id为必传参数')
        except Exception as e:
            return json_error_response(message=str(e))

    def update(self, request, *args, **kwargs):
        try:
            row_map = {'hostname': '名称', 'manage_ip': '管理IP', 'vlan_ip': 'Vlan_IP', 'intranet_ip': '内网IP',
                       'sn': 'DN号', 'manufacturer': '制造商', 'model': '型号', 'port_num': '端口数', 'device_detail': '配置详情'}
            record_list = []
            partial = kwargs.pop('partial', False)
            new_data = request.data
            instance = self.get_object()
            for k, v in new_data.items():
                value = getattr(instance, k)
                if v != value:
                    record_list.append(f' 名称{instance.hostname}: {row_map[k]},由{value if value else "Null"}变更为{v}.')
                    setattr(instance, k, v)
            print(record_list)
            instance.save()
            if record_list:
                print(record_list)
                content = ';  '.join(record_list)
                self.asset_record(request, '资产变更', content, instance.asset_obj.id)
            return json_ok_response(data=instance.hostname)
        except Exception as e:
            return json_error_response(message=str(e))
