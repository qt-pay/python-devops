from apps.cmdb import models

import subprocess
from concurrent.futures import ThreadPoolExecutor
# import logging
class Base():
    def error_logging(self, server_obj, content, title):
        print(server_obj, content, title)
        models.AssetErrorLog.objects.create(asset_obj=server_obj.asset_obj,
                                       content=content,
                                       title=title)
    def access_logging(self,title, server_obj,content ):
        models.AssetRecord.objects.create(title=title, asset_obj=server_obj.asset_obj, content=content)

    def __ping_func(self, ip):
        try:
            status = subprocess.call(["ping", '-w', '2', '-n', '2', ip], stdout=subprocess.PIPE, timeout=5)
            if status == 0:
                return ip
        except Exception:
            return False

    def ping(self, ipaddr_list):
        try:
            connected_ip_list = []
            pool = ThreadPoolExecutor(5)
            connected_ip = pool.map(self.__ping_func, ipaddr_list)
            for ip in connected_ip:
                if ip:
                    connected_ip_list.append(ip)
            return connected_ip_list
        except Exception as e:
            return str(e)