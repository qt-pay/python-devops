from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import UserProfileSerializer, UserGropSerializer
from ..models import UserGrop, UserProfile


class UserViewSet(Base):
    queryset = UserProfile.objects.all().order_by('id')
    serializer_class = UserProfileSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name', 'email', 'phone', 'mobile')
    filter_fields = ('id',)


class UserGroupViewSet(Base):
    queryset = UserGrop.objects.all().order_by('id')
    serializer_class = UserGropSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('title', 'remark')
    filter_fields = ('id',)
