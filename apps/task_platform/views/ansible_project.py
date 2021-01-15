from django.conf import settings
from .BaseViewSet import Base
from ..models import AnsibleProject
from ..serializers import AnsibleProjectSerializer
from utils.rest_framework.base_response import new_response
import os


class AnsibleProjectViewSet(Base):
    queryset = AnsibleProject.objects.all().order_by('id')
    serializer_class = AnsibleProjectSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name', 'path', 'online_status')
    filter_fields = ('id', )