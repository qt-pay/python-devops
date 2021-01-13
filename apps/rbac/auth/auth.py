import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from utils.rest_framework.base_response import new_response
from jwt import exceptions
class JwtQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        '''

        :param request:
        :return:
        '''
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        auth = authorization.split()

        salt = settings.SECRET_KEY
        try:
            if auth[0] != 'JWT' or len(auth) != 2:
                raise AuthenticationFailed({'code': 10002, 'error': '请先进行登录认证'})
            payload = jwt.decode(auth[1], salt, True)
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code': 1003, 'error': 'token已失效'})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code': 1004, 'error': 'token认证失败'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 1005, 'error': '请先进行登录认证'})
        if  payload:
            return(payload, authorization) # {'id': 1, 'name': 'devops', 'exp': 1605842288}

