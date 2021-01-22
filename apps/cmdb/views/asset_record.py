from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import AssetRecordSerializer
from ..models import AssetRecord


class AssetRecordViewSet(Base):
    queryset = AssetRecord.objects.all().order_by('-id')
    serializer_class = AssetRecordSerializer
    ordering_fields = ('id',)
    search_fields = ('content',)
    filter_fields = ('id', 'asset_obj',)

    def list(self, request, *args, **kwargs):
        try:
            ordering = request.query_params.get('ordering', '')
            ordering = ordering.replace('+', '').strip()
            if ordering:
                if self.serializer_class is None:
                    queryset = self.filter_queryset(self.get_serializer_class().Meta.model.objects.order_by(ordering))
                else:
                    queryset = self.filter_queryset(self.serializer_class.Meta.model.objects.order_by(ordering))
            else:
                queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return json_ok_response(data=serializer.data)
        except Exception as e:
            return json_error_response(message=str(e))
