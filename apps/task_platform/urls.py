from rest_framework import routers
from .views import script_project, script_file, ansible_project, ansible_playbook, ansible_parameter, task_recycle, \
    run_task, ansible_hosts, task_crontab, task_history
from django.urls import path, include

router = routers.DefaultRouter()

# 脚本库相关URL
router.register(r'script-project', script_project.ScriptProjectViewSet)
router.register(r'script-file', script_file.ScriptFileViewSet)
router.register(r'ansible-project', ansible_project.AnsibleProjectViewSet)
router.register(r'ansible-playbook', ansible_playbook.AnsiblePlaybookViewSet)
router.register(r'ansible-parameter', ansible_parameter.AnsibleParameterViewSet)
router.register(r'recycle', task_recycle.TaskRecycleViewSet)
router.register(r'crontab', task_crontab.TaskCrontabViewSet, )
router.register(r'history', task_history.TaskHistoryViewSet, )
#
urlpatterns = [
    path('run-task/exec-script/', run_task.ExecViewSet.as_view({'post': 'exec_script'})),
    path('run-task/exec-playbook/', run_task.ExecViewSet.as_view({'post': 'exec_playbook'})),
    path('run-task/exec-async/', run_task.ExecViewSet.as_view({'post': 'exec_async'})),
    path('ansible/host-group/', ansible_hosts.AnsibleGroup.as_view()),
    path('ansible/host-file/', ansible_hosts.AnsibleHosts.as_view()),
    # path('crontab/', task_crontab.TaskCrontabViewSet.as_view({'post': 'create', 'get': 'list'})),
]
urlpatterns = router.urls + urlpatterns
