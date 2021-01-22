from .BaseViewSet import Base
from ..models import AnsibleParameter
from ..serializers import AnsibleParameterSerializer
from base.response import json_ok_response, json_error_response


class AnsibleParameterViewSet(Base):
    queryset = AnsibleParameter.objects.all().order_by('id')
    serializer_class = AnsibleParameterSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name', 'param', 'online_status', 'src_user')
    filter_fields = ('id', 'playbook', 'online_status')

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            data['src_user'] = self.get_user(request)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return json_ok_response(data=serializer.data)
        except Exception as e:
            return json_error_response(message=str(e))

    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            data['src_user'] = self.get_user(request)
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            return json_ok_response(data=serializer.data)
        except Exception as e:
            return json_error_response(message=str(e))
