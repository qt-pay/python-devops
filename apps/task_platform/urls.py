from rest_framework import routers
from django.urls import path, include
from .views import script_project, script_file, ansible_project, ansible_playbook

router = routers.DefaultRouter()

# 脚本库相关URL
router.register(r'script-project', script_project.ScriptProjectViewSet, )

router.register(r'script-file', script_file.ScriptFileViewSet, )
router.register(r'ansible-project', ansible_project.AnsibleProjectViewSet, )
router.register(r'ansible-playbook', ansible_playbook.AnsiblePlaybookViewSet, )
# router.register(r'ansible-extravars', ansible_extravars.AnsibleExtravarsViewSet, )
# router.register(r'ansible-recycle-bin', recycle_bin.TaskRecycleViewSet, )
# # router.register(r'crontab', task_crontab.CrontabTsask, )
#
# urlpatterns = [
#     path('submit-playbook', task_submit.RunPlaybook.as_view({'post':'post'})),
#     path('crontab', task_crontab.CrontabTsaskView.as_view({ 'post': 'create', })),
#     # path('script/exec_cmd/', task_script.TaskScriptViewSet.as_view({'post': 'exec_cmd'})),
#
# ]
urlpatterns = router.urls

print(urlpatterns)
