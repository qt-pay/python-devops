from utils.rest_framework.base_view import NewModelViewSet
from ..models import AnsibleExtravars
from ..serializers import AnsibleExtravarsSerializer

class AnsibleExtravarsViewSet(NewModelViewSet):
    queryset = AnsibleExtravars.objects.all().order_by('id')
    serializer_class = AnsibleExtravarsSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    filter_fields = ('id', 'online_status', )
