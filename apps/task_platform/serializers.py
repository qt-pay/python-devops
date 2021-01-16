from rest_framework import serializers
from .models import ScriptProject, ScriptFile, AnsibleProject, AnsiblePlaybook, AnsibleParameter, TaskRecycle, \
    TaskHistory


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


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = '__all__'
