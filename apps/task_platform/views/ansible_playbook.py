from django.conf import settings
from .BaseViewSet import Base
from ..models import AnsiblePlaybook
from ..serializers import AnsiblePlaybookSerializer
from utils.rest_framework.base_response import new_response
import os


class AnsiblePlaybookViewSet(Base):
    queryset = AnsiblePlaybook.objects.all().order_by('id')
    serializer_class = AnsiblePlaybookSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name', 'file_name', 'online_status', 'src_user')
    filter_fields = ('id', 'project')
