
from rest_framework import  serializers
from .models import *
import re
class DepartmentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'department', 'roles', 'phone', 'remarks', 'create_time']
    extra_kwargs = {
        # 'password': {'write_only': True},
        'id': {'read_only': True},
        'roles': {'read_only': True},
        'department': {'read_only': True},
        'create_time': {'read_only': True},
    }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department'] = None if not instance.department else instance.department.title
        representation['roles'] = None if not instance.roles else [ role.title for role in instance.roles.all()]
        return representation

class UserManagerSerializer(serializers.ModelSerializer):
    # re_password = serializers.CharField(write_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'name','email', 'department','roles','is_active', 'phone' ,'remarks', 'create_time', ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department_title'] = None if not instance.department else instance.department.title
        representation['roles_list'] = None if not instance.roles else [ role.title for role in instance.roles.all()]
        return representation

    # def validate_phone(self, phone):
    #     # if self.request.data.get()
    #     if not re.match(r'0?(13|14|15|17|18|19)[0-9]{9}', phone):
    #         raise serializers.ValidationError('手机号不合法')
    #
    #     if self.Meta.model.objects.filter(phone=phone).all():
    #         raise serializers.ValidationError('手机号已被注册')
    #     return phone
    #
    # def validate_email(self, email):
    #     if not re.match(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', email):
    #         raise serializers.ValidationError('邮箱不合法')
    #
    #     if self.Meta.model.objects.filter(email=email).all():
    #         raise serializers.ValidationError('邮箱已经被注册')
    #     return email
    #
    #
    # def validate(self, attrs):
    #     print(attrs)
    #     if attrs['password'] != attrs['re_password']:
    #         raise serializers.ValidationError('两次密码不一致')
    #     attrs.pop("re_password")
    #     return attrs
