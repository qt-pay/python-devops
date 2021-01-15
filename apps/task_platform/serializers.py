from rest_framework import serializers
from .models import ScriptProject, ScriptFile, AnsibleProject, AnsiblePlaybook, AnsibleParameter, TaskHistory


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


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = '__all__'
