from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import AssetRecordSerializer
from ..models import AssetRecord


class AssetRecordViewSet(NewModelViewSet):
    queryset = AssetRecord.objects.all().order_by('-id')
    serializer_class = AssetRecordSerializer
    ordering_fields = ('id',)
    search_fields = ('content',)
    filter_fields = ('id', 'asset_obj', )
    def list(self, request):
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
            return new_response(data=serializer.data)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')