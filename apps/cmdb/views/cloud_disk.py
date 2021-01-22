from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import CloudDiskSerializer
from ..models import CloudDisk


class CloudDiskViewSet(Base):
    queryset = CloudDisk.objects.all().order_by('id')
    serializer_class = CloudDiskSerializer
    ordering_fields = ('id', 'slot',)
    search_fields = ('capacity',)
    filter_fields = ('id', 'server_obj')

    def create(self, request, *args, **kwargs):
        try:
            asset_id = request.data.pop('asset_id')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.asset_record(request, '新增磁盘',
                              f'磁盘ID: {request.data["disk_id"]}, 容量: {request.data["capacity"]} 类型: {request.data["disk_type"]} ',
                              asset_id)
            return json_ok_response(data=serializer.data)

        except Exception as e:
            return json_error_response(message=str(e))

    def update(self, request, *args, **kwargs):

        try:
            row_map = {'disk_type': '磁盘类型', 'disk_id': '磁盘ID', 'capacity': '磁盘容量', }
            record_list = []
            partial = kwargs.pop('partial', False)
            new_data = request.data
            asset_id = request.data.pop('asset_id')
            instance = self.get_object()
            for k, v in new_data.items():
                if k == 'server_obj':
                    continue
                value = getattr(instance, k)
                if v != value:
                    record_list.append(f' 磁盘ID{instance.disk_id}: {row_map[k]},由{value}  变更为{v}.')
                    setattr(instance, k, v)
            instance.save()
            if len(record_list) != 0:
                content = ';  '.join(record_list)
                self.asset_record(request, '磁盘信息变更', content, asset_id)
            return json_ok_response(data=instance.disk_id)
        except Exception as e:
            return json_error_response(message=str(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            asset_id = instance.server_obj.asset_obj.id
            instance.delete()
            self.asset_record(request, '磁盘移除', f'磁盘ID{instance.disk_id}, 容量{instance.capacity}, 类型{instance.disk_type}',
                              asset_id)
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=f'ERROR: {str(e)}')
