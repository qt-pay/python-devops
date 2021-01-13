from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import NetworkSerializer
from ..models import Network


class NetworkViewSet(NewModelViewSet):
    queryset = Network.objects.all().order_by('id')
    serializer_class = NetworkSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('ipaddress', 'hwaddr', 'up')
    filter_fields = ('id', 'server_obj')

    def create(self, request, *args, **kwargs):
        try:
            asset_id = request.data.pop('asset_id')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.asset_record(request, '新增网卡', f'网卡名: {request.data["title"]}, 管理IP: {request.data["ipaddress"]} ', asset_id)
            return new_response(data=serializer.data)

        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')
    def update(self, request, *args, **kwargs):

        try:
            row_map = {'title': '网卡名称', 'hwaddr': 'MAC地址',  'netmask': '子网掩码',  'ipaddress': '管理IP',
                       'broadcast': '广播地址', 'up': '网卡状态', 'latest_date': '更新时间', 'create_at': '创建时间', 'server_obj': '关联设备'}
            record_list =  []
            partial = kwargs.pop('partial', False)
            new_data = request.data
            asset_id = request.data.pop('asset_id')
            instance = self.get_object()
            for k, v in new_data.items():
                if k == 'server_obj':
                    continue
                value = getattr(instance, k)
                if v != value:
                    record_list.append(f' 名称{instance.title}: {row_map[k]},由{value}  变更为{v}.')
                    setattr(instance, k, v)
            instance.save()
            if len(record_list) != 0:
                content = ';  '.join(record_list)
                self.asset_record(request, '服务器基本信息变更', content,asset_id)
            return new_response(data=instance.title)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            asset_id = instance.server_obj.asset_obj.id
            instance.delete()
            self.asset_record(request, '网卡移除', f'名称{instance.title}, 管理IP{instance.ipaddress}', asset_id)
            return new_response()
        except Exception as e:
            return new_response(code=10200,data='eroor', message=f'ERROR: {str(e)}')
