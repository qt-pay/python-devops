
from rest_framework import  serializers
from .models import *
import re
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'
    # def to_representation(self, instance):
        # representation = super().to_representation(instance)
    #     representation['permissions'] = None if not instance.permissions else [ permission.title for permission in instance.permissions.all()]
    #     representation['role'] = instance.roles_set()
    #     return representation

class PermissionsSerializer(serializers.ModelSerializer):
    # method_type = Choice
    method_name = serializers.CharField(read_only=True)
    class Meta:
        model = Permissions
        fields = '__all__'
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     # representation['method_name'] = instance.get_method_type_display()
    #     return representation


class MenusSerializer(serializers.ModelSerializer):
    hasChildren = serializers.SerializerMethodField(read_only=True)
    def get_hasChildren(self,  obj):
        if obj.pid == 0:
            return True
        else:
            return False
    class Meta:
        model = Menus
        fields = '__all__'
        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['role'] = instance.roles_set()
            return representation