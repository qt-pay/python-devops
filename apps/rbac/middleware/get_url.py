from django.utils.module_loading import import_string
from django.urls.resolvers import URLResolver, URLPattern
from django.conf import settings
import re
def recursion_urls( pre_url, urlpatterns, url_list):
    """
    递归的去获取URL
    :param per_namespace: namespace前缀，以后用户拼接name
    :param per_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:
        if re.match('admin/', str(item.pattern)):
            continue
        if isinstance(item, URLPattern):  # 非路由分发
            url = pre_url + str(item.pattern).replace('^', '',1)
            url_list.append(url)
        elif isinstance(item, URLResolver):
            recursion_urls( pre_url + str(item.pattern), item.url_patterns, url_list)

def get_all_url_list():
    """
    获取项目中所有的URL
    :return:
    """
    url_list = []
    md = import_string(settings.ROOT_URLCONF)
    recursion_urls('/', md.urlpatterns, url_list)  # 递归去获取所有的路由
    return url_list

def check_current_url(churrent_url):
    all_url = get_all_url_list()
    for url in all_url:

        if re.match(url, churrent_url):
            print(url, churrent_url)
            return url

    return False