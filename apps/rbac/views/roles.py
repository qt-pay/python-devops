from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import RolesSerializer
from ..models import Roles


class RolesViewSet(NewModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title', )