from ..serializers import UserProfileSerializer, UserManagerSerializer
from ..models import UserProfile
from base.response import json_ok_response, json_error_response
from base.views import BaseModelViewSet
from apps.rbac.auth.jwt_auth import create_token, analysis_token

from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.decorators import action


class UserProfileViewSet(BaseModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    ordering_fields = ['id']
    search_fields = ['email', 'phone', 'name', 'role']

    def list(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if token != '':
            user_info = analysis_token(request)
            try:
                queryset = UserProfile.objects.filter(email=user_info['user_info']['email'],
                                                      name=user_info['user_info']['username']).first()
                serializer = self.get_serializer(queryset)
                return json_ok_response(data=serializer.data)
            except Exception as e:
                return json_error_response(message=str(e))
        else:
            return json_error_response(message='token 不能为空')

    @action(methods=['post'], detail=True)
    def reset_password(self, request, pk):
        '''
        重置密码
        '''
        email = request.data.get('email')
        old_pwd = request.data.get('old_password')
        new_pwd = request.data.get('new_password')
        if email and old_pwd and new_pwd:
            user_obj = auth.authenticate(request, email=email, password=old_pwd)
            if user_obj:
                user_obj.set_password(new_pwd)
                user_obj.save()
                return json_ok_response(data=f'{user_obj.email} 账户密码修改成功!')
            else:
                return json_error_response(message='用户或密码错误,请检查重试!')
        else:
            return json_error_response(message='<email>,<old_password>,<new_password>为必传参数.')
    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return new_response(data=serializer.data)


class UserManagerViewSet(BaseModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserManagerSerializer
    ordering_fields = ['id']
    search_fields = ['email', 'phone', 'name', 'role']

    def create(self, request, *args, **kwargs):
        try:
            serializer = UserManagerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = serializer.save()
            user_obj.set_password(request.data.get('password'))
            user_obj.save()
            return json_ok_response(data=serializer.data)
        except Exception as e:
            return json_error_response(message=str(e))

    @action(methods=['put'], detail=True)
    def reset_password(self, request, pk):
        instance = self.get_object()
        new_pwd = request.data.get('new_password')
        if new_pwd:
            instance.set_password(new_pwd)
            instance.save()
            return json_ok_response(data=f'{instance.email} 账户密码修改成功!')
        else:
            return json_error_response(message='<email>,<new_password>为必传参数.')


class LoginViewSet(APIView):
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email', '')
        pwd = request.data.get('password', '')
        if email != '' or pwd != '':
            user_obj = auth.authenticate(request, email=email, password=pwd)
            if user_obj:
                permission_queryset = user_obj.roles.filter(permissions__isnull=False, permissions__pid__gt=0).values(
                    "permissions__id",
                    "permissions__title",
                    "permissions__url",
                    "permissions__method",
                )
                permission_list = []
                # item {'permissions__id': 4, 'permissions__title': '测试权限子', 'permissions__slug': 'test2', 'permissions__remarks': None}
                for item in permission_queryset:
                    permission_dic = {
                        'title': item['permissions__title'],
                        'url': item['permissions__url'],
                        'method': item['permissions__method'],
                    }
                    permission_list.append(permission_dic)
                user_info = {
                    'email': user_obj.email,
                    'username': user_obj.name,
                    'roles': [role.title for role in user_obj.roles.all()]
                }
                token = create_token({'permission': permission_list, 'user_info': user_info})
                print(token)
                return json_ok_response(data=token)
            return json_error_response(message='用户名或密码错误,请重试!', )
        return json_error_response(message='email和password为必传参数!', )


class UserInfoViewSet(APIView):
    pass


class LogoutViewSet(APIView):
    def post(self, request):
        return json_ok_response(data='注销成功')
