from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import TagSerializer
from ..models import Tag


class TagViewSet(NewModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title',)