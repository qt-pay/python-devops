from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import UserProfileSerializer, UserGropSerializer
from ..models import UserGrop, UserProfile


class UserViewSet(NewModelViewSet):
    queryset = UserProfile.objects.all().order_by('id')
    serializer_class = UserProfileSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name', 'email', 'phone', 'mobile')
    filter_fields = ('id', )

class UserGroupViewSet(NewModelViewSet):
    queryset = UserGrop.objects.all().order_by('id')
    serializer_class = UserGropSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('title', 'remark')
    filter_fields = ('id', )