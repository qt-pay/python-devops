from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import AssetErrorLogSerializer
from ..models import AssetErrorLog


class AssetErrorLogViewSet(Base):
    queryset = AssetErrorLog.objects.all().order_by('-id')
    serializer_class = AssetErrorLogSerializer
    ordering_fields = ('id',)
    search_fields = ('title', 'content',)
    filter_fields = ('id', 'asset_obj',)
