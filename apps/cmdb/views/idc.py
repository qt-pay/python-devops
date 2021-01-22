from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import IDCSerializer
from ..models import IDC


class IDCViewSet(Base):
    queryset = IDC.objects.all().order_by('id')
    serializer_class = IDCSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title',)
    filter_fields = ('id',)
