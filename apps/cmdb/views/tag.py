from .base_view import Base
from base.response import json_ok_response, json_error_response
from ..serializers import TagSerializer
from ..models import Tag


class TagViewSet(Base):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
    ordering_fields = ('id', 'title',)
    search_fields = ('title',)
