from django.conf import settings
from rest_framework.decorators import action
from .BaseViewSet import Base
from ..models import AnsibleParameter, ScriptProject, TaskRecycle
from ..serializers import AnsiblePlaybookSerializer
from utils.rest_framework.base_response import new_response
import os
import pathlib
import datetime
import shutil


class AnsibleParameterViewSet(Base):
    queryset = AnsibleParameter.objects.all().order_by('id')
    serializer_class = AnsiblePlaybookSerializer
    ordering_fields = ('id', 'script_filename',)
    search_fields = ('name', 'param', 'online_status', 'src_user')
    filter_fields = ('id', 'playbook')