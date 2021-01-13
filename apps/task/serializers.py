
from rest_framework import  serializers
from .models import TaskScript, AnsibleProject, TaskProject, AnsiblePlaybook, AnsibleExtravars, TaskRecycle



class TaskScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskScript
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['project_name'] = instance.project.name if instance.project else None
        return representation

class TaskProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskProject
        fields = '__all__'

class AnsibleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnsibleProject
        fields = '__all__'

class AnsiblePlaybookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnsiblePlaybook
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['project_name'] = instance.project.name if instance.project else None
        return representation


class AnsibleExtravarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnsibleExtravars
        fields = '__all__'

class TaskRecycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRecycle
        fields = '__all__'