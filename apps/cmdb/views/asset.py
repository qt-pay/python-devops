from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import AssetSerializer
from ..models import Asset, IDC, Tag, BusinessUnit, DeviceCategory, UserGrop
from rest_framework.decorators import action


class AssetViewSet(Base):
    queryset = Asset.objects.all().order_by('id')
    serializer_class = AssetSerializer
    ordering_fields = ('id', 'title',)
    filter_fields = ('id', 'business_unit', 'device_type', 'tag')
    search_fields = ('device_status_id', 'device_type__title', 'tag__title', 'latest_date')

    def update(self, request, *args, **kwargs):
        try:
            device_status_choices = (
                (1, '上线'),
                (2, '在线'),
                (3, '离线'),
                (4, '下架')
            )
            row_map = {'title': '名称', 'business_unit': '业务线', 'device_status_id': '状态', 'cabinet_num': '机柜编号',
                       'cabinet_order': '柜上编号', 'idc': '机房', 'tag': '标签', 'device_type': '设备类型',
                       'maintain_groups': '维护组'}
            record_list = []
            partial = kwargs.pop('partial', False)
            new_data = request.data
            instance = self.get_object()
            for k, v in new_data.items():
                value = getattr(instance, k)
                if k == 'idc':
                    v = IDC.objects.filter(id=v).first()
                    print(v, value)
                    if v != value:
                        record_list.append(
                            f' 名称{instance.title}: {row_map[k]},  由 {value.title if value else "Null"} 变更为 {v.title} ')
                        #
                        setattr(instance, k, v)
                    continue
                elif k == 'tag':
                    value = [tag.title for tag in instance.tag.all()]
                    v1 = [tag.title for tag in Tag.objects.filter(id__in=v)]
                    if v1 != value:
                        record_list.append(f' 名称{instance.title}: {row_map[k]},'
                                           f'由 {value}  变更为 {v} .')
                        v = Tag.objects.filter(id__in=v)
                        instance.tag.set(v)
                    continue
                elif k == 'business_unit':
                    v = BusinessUnit.objects.filter(id=v).first()
                    if v != value:
                        record_list.append(
                            f' 名称{instance.title}: {row_map[k]},{row_map[k]}, 由 {instance.business_unit.title if instance.business_unit else "Null"}  变更为 {v.title} .')
                        setattr(instance, k, v)
                    continue
                elif k == 'business_unit':
                    if v != value:
                        record_list.append(
                            f' 名称{instance.title}: {row_map[k]},{row_map[k]}, 由 {device_status_choices[instance.device_status_id - 1][1]}  变更为 {device_status_choices[v - 1][1]} .')
                        setattr(instance, k, v)
                    continue
                elif k == 'device_type':
                    v = DeviceCategory.objects.filter(id=v).first()
                    # print(v)
                    if v != value:
                        record_list.append(
                            f' 名称{instance.title}: {row_map[k]},由 {value.title if value else "Null"}  变更为 {v.title} .')
                        setattr(instance, k, v)
                elif k == 'maintain_groups':
                    v = UserGrop.objects.filter(id=v).first()
                    if v != value:
                        record_list.append(
                            f' 名称{instance.title}: {row_map[k]},由 {value.title if value else "Null"}  变更为 {v.title} .')
                        setattr(instance, k, v)
                else:
                    if v != value:
                        record_list.append(
                            f' 名称{instance.title}: {row_map[k]},由 {value if value else "Null"}  变更为 {v} .')
                        setattr(instance, k, v)

            instance.save()
            if record_list:
                content = ';  '.join(record_list)
                self.asset_record(request, '基本信息变更', content, instance.id)
            return json_ok_response(data=instance.title)
        except Exception as e:
            return json_error_response(message=str(e))

    @action(methods=['get'], detail=False)
    def task_asset(self, request):
        queryset = Asset.objects.filter(manage_ip__isnull=False, device_type__pid__in=[1, 2],
                                        device_status_id__in=[1, 2])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return json_ok_response(data=serializer.data)
