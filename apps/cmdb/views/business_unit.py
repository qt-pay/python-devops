from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import BusinessUnitSerializer
from ..models import BusinessUnit


class BusinessUnitViewSet(Base):
    queryset = BusinessUnit.objects.all().order_by('id')
    serializer_class = BusinessUnitSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title',)
    filter_fields = ('id',)
