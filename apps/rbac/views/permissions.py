from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import PermissionsSerializer
from ..models import Permissions


class PermissionsViewSet(NewModelViewSet):
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
                return new_response(data=childrens)
            elif int(pid) == 0:
                queryset = self.queryset.filter(pid=pid)
                serializer = self.get_serializer(queryset, many=True)
                return new_response(data=serializer.data)
            else:
                if self.queryset.filter(id=pid):
                    queryset = self.queryset.filter(pid=pid)
                    serializer = self.get_serializer(queryset, many=True)
                    return new_response(data=serializer.data)
                else:
                    return new_response(code=10200, data='error', message='pid不存在')
        except Exception as e:
            return new_response(code=10200, data='error', message=f'error: {str(e)}')