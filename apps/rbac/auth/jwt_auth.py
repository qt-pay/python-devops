from django.conf import settings
import jwt
import datetime
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from jwt import exceptions
def create_token(payload):
    salt = settings.SECRET_KEY
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_TIMEOUT)
    # 构造 header
    headers = {
        'typ': 'jwt',
        'alp': 'HS256'
    }

    payload['exp'] = exp
    # return jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers).decode('utf-8')
    return jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers)

def analysis_token(request):
    '''
    :param request:
    :return:
    '''
    authorization = request.META.get('HTTP_AUTHORIZATION', '')
    if authorization != '':
        auth = authorization.split()
        salt = settings.SECRET_KEY
        try:
            if auth[0] != 'JWT' or len(auth) != 2:
                return JsonResponse({'code': 10002, 'data': 'token不合法', 'message': 'token 不合法!请重新登录'},json_dumps_params={'ensure_ascii': False}, status=500)
            payload = jwt.decode(auth[1], salt,  algorithms=['HS256'])
        except exceptions.ExpiredSignatureError:
            return JsonResponse({'code': 10003, 'data': 'token已失效', 'message': 'token已失效'},json_dumps_params={'ensure_ascii': False}, status=500)
        except jwt.DecodeError:
            return JsonResponse({'code': 1004, 'data': 'token认证失败', 'message': 'token认证失败'},json_dumps_params={'ensure_ascii': False}, status=500)
        except jwt.InvalidTokenError:
            return JsonResponse({'code': 1005, 'data': '请先进行登录认证', 'message': '请先进行登录认证'},json_dumps_params={'ensure_ascii': False}, status=500)
        if payload:
            return payload # {'id': 1, 'name': 'devops', 'exp': 1605842288}
    else:
        return JsonResponse({'code': 1005, 'data': '请先进行登录认证', 'message': '请先进行登录认证'},json_dumps_params={'ensure_ascii': False}, status=500)
    # payload = jwt.decode(auth[1], salt, True)
    # if payload:
    #     return payload
