from ..auth.jwt_auth import analysis_token
import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from utils.rest_framework.response import new_response
from django.http import JsonResponse
from .get_url import check_current_url
# from apps.rbac.auth.auth import
class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求刚进入时候出发执行
        :param request:
        :return:
        """
        current_url = request.path_info
        method = request.method
        # 第一步
        # 白名单中的URL无需权限验证即可访问
        if current_url == '/api/rbac/menus/' and method == 'GET':
            return None
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                return None

        # 第二部判断访问的 URL 是否在项目中 如果不在则返回 404
        ''' 获取当前路由检查当前路由是否在项目中'''
        check = check_current_url(current_url)
        print(check)
        if not check:
            res = {
                    'code': 400004,
                    'data': '404找不到路由',
                    'message': '访问的路由不在项目中'
                }
            return JsonResponse(res, status=404, json_dumps_params={'ensure_ascii': False}, )
        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        """
        # 第三步 判断用户角色
        # 如果是 admin 用户则无需进行以下匹配 通过analysis_token函数解析token
        user_info = analysis_token(request)
        if type(user_info) is not dict:
            return user_info
        if 'admin' in user_info['user_info']['roles']:
            return None

        # 第四步 验证用户权限
        # 下面是进行权限验证
        flag = False
        # item {'title': '权限查看', 'url': '/api/user/permissions', 'method': 'GET'} and item['method'] == method
        for item in user_info['permission']:
            reg = f"^{item['url']}$"
            print(reg, current_url)
            if re.match(reg, current_url) and method == item['method']:
                flag = True
                break
        if not flag:
            res = {
                'code': 40022,
                'data': '无权限访问',
                'message': f'页面部分权限无法使用. 请联系管理员获取URL:{str(check)}, 请求方法: {method}'
            }
            print(res)
            return JsonResponse(res, status=403, json_dumps_params={'ensure_ascii': False})
        else:
            return None

