from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import SSHSerializer
from ..models import SSH


class TagViewSet(NewModelViewSet):
    queryset = SSH.objects.all().order_by('id')
    serializer_class = SSHSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)