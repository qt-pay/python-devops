from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from rest_framework import serializers
from .models import ScriptProject, ScriptFile, AnsibleProject, AnsiblePlaybook, AnsibleParameter, TaskRecycle, \
    TaskHistory, TaskCrontab


class ScriptProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptProject
        fields = '__all__'


class ScriptFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptFile
        fields = '__all__'


class AnsibleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnsibleProject
        fields = '__all__'


class AnsiblePlaybookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnsiblePlaybook
        fields = '__all__'


class AnsibleParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnsibleParameter
        fields = '__all__'


class TaskRecycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRecycle
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['task_type'] = instance.get_task_type_display()
        return representation


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore())  # 指定存储
scheduler.start()

class TaskCrontabSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCrontab
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        job_list = scheduler.get_job(instance.task_id)
        representation['next_run_time'] = job_list.next_run_time if job_list else None
        return representation


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = '__all__'
