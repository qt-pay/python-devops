
from rest_framework import  serializers
from .models import *




class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['project_name'] =  instance.project.name if instance.project else None
        return representation
class ExtravarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extravars
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['job_name'] = instance.job.name if instance.job else None
        return representation
