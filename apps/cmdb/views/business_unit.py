
from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import BusinessUnitSerializer
from ..models import BusinessUnit


class BusinessUnitViewSet(NewModelViewSet):
    queryset = BusinessUnit.objects.all().order_by('id')
    serializer_class = BusinessUnitSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title',)
    filter_fields = ('id', )