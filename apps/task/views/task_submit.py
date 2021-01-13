from .BaseViewSet import Base
from utils.rest_framework.base_response import new_response
from my_celery.playbook_task.taks import ploybook_task

class RunPlaybook(Base):
    def post(self, request):
        data = request.data
        cmd_info = self.cmd('playbook', data)
        if cmd_info['status']:
            result = ploybook_task.delay(cmd_info['data'])
            self.record_log(request, task_name='xxx', abs_file=cmd_info['script_file'].split('tasks')[1], result_id=result.id,host_list=None, task_type='ansible-playbook' )
        else:
            return new_response(code=10200, data='剧本执行失败', message=cmd_info['data'])
        return new_response()








