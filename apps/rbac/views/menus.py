from base.views import BaseModelViewSet
from base.response import json_ok_response, json_error_response
from ..serializers import MenusSerializer
from ..models import Menus


class MenusViewSet(BaseModelViewSet):
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title', 'url')

    def list(self, request, *args, **kwargs):
        try:
            pid = request.query_params.get('pid', '')
            if pid == '':
                childrens = []
                top_data = self.queryset.filter(pid=0)
                for menu in top_data:
                    dic = {
                        'id': menu.id,
                        'url': menu.url,
                        'title': menu.title,
                        'icon': menu.icon,
                        'roles': [role.title for role in menu.roles_set.all()],
                        'children': []
                    }
                    children = self.queryset.filter(pid=menu.id)
                    if children:
                        for children_item in children:
                            dic['children'].append({
                                'id': children_item.id,
                                'url': children_item.url,
                                'title': children_item.title,
                                'icon': children_item.icon,
                                'roles': [role.title for role in children_item.roles_set.all()]
                            })
                    childrens.append(dic)
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
