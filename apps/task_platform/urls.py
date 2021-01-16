from rest_framework import routers
from .views import script_project, script_file, ansible_project, ansible_playbook, ansible_parameter, task_recycle
from django.urls import path, include

router = routers.DefaultRouter()

# 脚本库相关URL
router.register(r'script-project', script_project.ScriptProjectViewSet)
router.register(r'script-file', script_file.ScriptFileViewSet)
router.register(r'ansible-project', ansible_project.AnsibleProjectViewSet)
router.register(r'ansible-playbook', ansible_playbook.AnsiblePlaybookViewSet)
router.register(r'ansible-parameter', ansible_parameter.AnsibleParameterViewSet)
router.register(r'recycle', task_recycle.TaskRecycleViewSet)
# # router.register(r'crontab', task_crontab.CrontabTsask, )
#
# urlpatterns = [
#     path('submit-playbook', task_submit.RunPlaybook.as_view({'post':'post'})),
#     path('crontab', task_crontab.CrontabTsaskView.as_view({ 'post': 'create', })),
#     # path('script/exec_cmd/', task_script.TaskScriptViewSet.as_view({'post': 'exec_cmd'})),
#
# ]
urlpatterns = router.urls
