from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import IDCSerializer
from ..models import IDC


class IDCViewSet(NewModelViewSet):
    queryset = IDC.objects.all().order_by('id')
    serializer_class = IDCSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title',)
    filter_fields = ('id', )