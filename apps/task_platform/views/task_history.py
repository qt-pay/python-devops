from .BaseViewSet import Base
from ..models import TaskHistory
from ..serializers import TaskHistorySerializer


class TaskHistoryViewSet(Base):
    queryset = TaskHistory.objects.all().order_by('-id')
    serializer_class = TaskHistorySerializer
    ordering_fields = ('id', 'task_name',)
    search_fields = ('task_name', 'src_user', 'src_ip', 'task_status')
    filter_fields = ('run_type', 'task_type', 'task_status')
