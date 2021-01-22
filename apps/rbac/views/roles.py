from base.views import BaseModelViewSet
from base.response import json_ok_response, json_error_response
from ..serializers import RolesSerializer
from ..models import Roles


class RolesViewSet(BaseModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title',)
