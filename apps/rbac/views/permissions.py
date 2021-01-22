from base.views import BaseModelViewSet
from base.response import json_ok_response, json_error_response
from ..serializers import PermissionsSerializer
from ..models import Permissions


class PermissionsViewSet(BaseModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionsSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title', 'url', 'method_type')

    def list(self, request, *args, **kwargs):
        try:
            pid = request.query_params.get('pid', '')
            if pid == '':
                childrens = []
                top_data = list(self.queryset.filter(pid=0).values())
                for menu in top_data:
                    menu["children"] = list(self.queryset.filter(pid=menu['id']).values())
                    childrens.append(menu)
                return json_ok_response(data=childrens)
            elif int(pid) == 0:
                queryset = self.queryset.filter(pid=pid)
                serializer = self.get_serializer(queryset, many=True)
                return json_ok_response(data=serializer.data)
            else:
                if self.queryset.filter(id=pid):
                    queryset = self.queryset.filter(pid=pid)
                    serializer = self.get_serializer(queryset, many=True)
                    return json_ok_response(data=serializer.data)
                else:
                    return json_error_response(message='pid不存在')
        except Exception as e:
            return json_error_response(message=f'error: {str(e)}')
