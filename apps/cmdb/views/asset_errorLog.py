from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import AssetErrorLogSerializer
from ..models import AssetErrorLog


class AssetErrorLogViewSet(NewModelViewSet):
    queryset = AssetErrorLog.objects.all().order_by('-id')
    serializer_class = AssetErrorLogSerializer
    ordering_fields = ('id',)
    search_fields = ('title', 'content',)
    filter_fields = ('id', 'asset_obj', )
