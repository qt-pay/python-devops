from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import MemorySerializer
from ..models import Memory


class MemoryViewSet(NewModelViewSet):
    queryset = Memory.objects.all().order_by('id')
    serializer_class = MemorySerializer
    ordering_fields = ('id', 'slot',)
    search_fields = ('capacity', 'sn')
    filter_fields = ('id', 'server_obj')
    def create(self, request, *args, **kwargs):
        try:
            asset_id = request.data.pop('asset_id')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.asset_record(request, '新增内存', f'内存槽位: {request.data["slot"]}, 内存容量: {request.data["capacity"]} ', asset_id)
            return new_response(data=serializer.data)

        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')
    def update(self, request, *args, **kwargs):

        try:
            row_map = {'slot': '内存槽位', 'manufacturer': '内存品牌',  'model': '内存型号',  'capacity': '内存容量',
                       'sn': '内存SN号', 'speed': '内存速率', 'latest_date': '更新时间', 'create_at': '创建时间', 'server_obj': '关联设备'}
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
                    record_list.append(f' 槽位{instance.slot}: {row_map[k]},由{value}  变更为{v}.')
                    setattr(instance, k, v)
            instance.save()
            if len(record_list) != 0:
                content = ';  '.join(record_list)
                self.asset_record(request, '内存变更记录', content,asset_id)
            return new_response(data=instance.slot)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            asset_id = instance.server_obj.asset_obj.id
            instance.delete()
            self.asset_record(request, '内存移除记录', f'名称{instance.slot}, 内存容量{instance.capacity}', asset_id)
            return new_response()
        except Exception as e:
            return new_response(code=10200,data='eroor', message=f'ERROR: {str(e)}')
