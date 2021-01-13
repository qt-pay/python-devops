from utils.rest_framework.base_view import NewModelViewSet
from ..models import Department
from ..serializers import DepartmentGroupSerializer


class DepartmentViewSet(NewModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentGroupSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('title', 'count')