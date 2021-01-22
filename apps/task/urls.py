# from rest_framework import routers
# from django.urls import path, include
# from .views import task_script,  task_project, ansible_project, ansible_playbook, ansible_extravars, task_submit, recycle_bin, task_crontab
# router = routers.DefaultRouter()
#
# router.register(r'script', task_script.TaskScriptViewSet, )
#
# router.register(r'project', task_project.TaskProjectViewSet, )
# router.register(r'ansible-project', ansible_project.AnsibleProjectViewSet, )
# router.register(r'ansible-playbook', ansible_playbook.AnsiblePlaybookViewSet, )
# router.register(r'ansible-extravars', ansible_extravars.AnsibleExtravarsViewSet, )
# # router.register(r'ansible-recycle-bin', recycle_bin.TaskRecycleViewSet, )
# # router.register(r'crontab', task_crontab.CrontabTsask, )
#
# urlpatterns = [
#     path('submit-playbook', task_submit.RunPlaybook.as_view({'post':'post'})),
#     path('crontab', task_crontab.CrontabTsaskView.as_view({ 'post': 'create', })),
#     path('hosts-group', task_crontab.CrontabTsaskView.as_view({ 'post': 'create', })),
#     # path('script/exec_cmd/', task_script.TaskScriptViewSet.as_view({'post': 'exec_cmd'})),
#
# ]
# urlpatterns = router.urls + urlpatterns
#
