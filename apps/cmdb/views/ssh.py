from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import SSHSerializer
from ..models import SSH


class TagViewSet(Base):
    queryset = SSH.objects.all().order_by('id')
    serializer_class = SSHSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
