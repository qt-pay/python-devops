from apps.cmdb import models
from .Base import Base


class Network(Base):
    def __init__(self, server_obj):
        self.row_map = {'title': '名称', 'hwaddr': '网卡Mac地址', 'netmask': '子网掩码', 'ipaddress': '槽位', 'up': '网卡好状态'}
        self.server_obj = server_obj
        self.type = '网卡'
        self.error_message = f'[{self.server_obj.hostname}]-<{self.type}>收集信息出错'
        self.update_record = f'<{self.type}变更记录>'
        self.delete_record = f'<{self.type}移除记录>'
        self.create_record = f'<{self.type}新增记录>'

    @classmethod
    def initial(cls, server_obj):
        return cls(server_obj)

    def parse(self, content):
        if not content['status']:
            '''出错记录日志不做处理'''
            self.error_logging(server_obj=self.server_obj, content=content['data'], title=self.error_message)
            return None
        self.__clent_data(content)

    def __clent_data(self, content):
        new_network_dict = content['data']
        old_network_list = models.Network.objects.filter(server_obj=self.server_obj)
        # # 取到所有新数据网卡的槽位
        new_title_list = list(new_network_dict.keys())
        # # 取到所有旧数据网卡的槽位
        old_title_list = [old_obj.title for old_obj in old_network_list]
        # # 取交集 要更新的数据
        update_title_list = set(new_title_list).intersection(old_title_list)
        # # 差集 要创建的数据
        create_title_list = set(new_title_list).difference(old_title_list)
        # # 差集 要删除的数据
        delete_title_list = set(old_title_list).difference(new_title_list)
        if create_title_list:
            self.__create_data(create_title_list, new_network_dict)
        if update_title_list:
            self.__update_data(update_title_list, new_network_dict)
        if delete_title_list:
            self.__delete_data(delete_title_list)

    def __create_data(self, create_title_list, new_network_dict):
        record_list = []
        ip_list = []
        for title in create_title_list:
            new_dict_row = new_network_dict[title]
            network_dict = {'title': title,
                            'up': new_dict_row['up'],
                            'hwaddr': new_dict_row["hwaddr"],
                            'netmask': new_dict_row["netmask"],
                            'ipaddress': new_dict_row["ipaddress"],
                            'broadcast': new_dict_row["broadcast"],
                            'server_obj': self.server_obj
                            }
            ip_list.append(network_dict['ipaddress'])
            models.Network.objects.create(**network_dict)
            temp = f'名称: << {title} >>, IP地址: << {network_dict["ipaddress"]} >>, Mac地址: << {network_dict["hwaddr"]} >>, 状态: << {network_dict["up"]} >>'
            record_list.append(temp)
        # 配置管理IP
        if ip_list:
            self.__manage_ipaddr(ip_list)
        # 记录日志
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title=self.create_record, server_obj=self.server_obj, content=content)

    def __update_data(self, update_title_list, new_network_dict):
        record_list = []
        ip_list = []
        for title in update_title_list:
            new_dict_row = new_network_dict[title]
            network_dict = {'title': title,
                            'up': new_dict_row['up'],
                            'hwaddr': new_dict_row["hwaddr"],
                            'netmask': new_dict_row["netmask"],
                            'ipaddress': new_dict_row["ipaddress"],
                            'broadcast': new_dict_row["broadcast"],
                            }
            old_network_row = models.Network.objects.filter(title=title, server_obj=self.server_obj).first()
            for k, v in network_dict.items():
                value = getattr(old_network_row, k)
                if v != value:
                    record_list.append(f' 名称 << {title} >>: {self.row_map[k]}, 由 << {value} >> 变更为: << {v} >>.')
                    setattr(old_network_row, k, v)
                    ip_list.append(network_dict['ipaddress'])
            old_network_row.save()
        # 配置管理IP
        if ip_list:
            self.__manage_ipaddr(ip_list)
        # 记录日志
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title=self.update_record, server_obj=self.server_obj, content=content)
        return None

    def __delete_data(self, delete_title_list):
        record_list = []
        ip_list = []
        delete_network_obj = models.Network.objects.filter(server_obj=self.server_obj, title__in=delete_title_list)
        for obj in delete_network_obj:
            record_list.append(
                f': 名称: << {obj.title} >>, IP地址: << {obj.ipaddress} >>, Mac地址: << {obj.hwaddr} >>, 状态: << {obj.up} >>.')
            ip_list.append(obj.ipaddress)
        delete_network_obj.delete()
        # 配置管理IP
        if ip_list:
            self.__manage_ipaddr(ip_list)
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title=self.delete_record, server_obj=self.server_obj, content=content)

    def __manage_ipaddr(self, ipaddr_list):
        ipaddr_list = ipaddr_list
        old_manage_ip = self.server_obj.manage_ip
        if old_manage_ip:
            ipaddr_list.insert(0, old_manage_ip)
        connected_list = self.ping(ipaddr_list)
        if isinstance(connected_list, list) and len(connected_list) > 0:
            new_manage_ip = connected_list[0]
            self.server_obj.manage_ip = new_manage_ip
            self.server_obj.save()
            if old_manage_ip:
                self.access_logging(title=f"<<管理IP变更>>", server_obj=self.server_obj,
                                    content=f'管理IP由: << {old_manage_ip} >>, 变更为: << {new_manage_ip} >>.')
            else:
                self.access_logging(title=f"<<新增管理IP>>", server_obj=self.server_obj,
                                    content=f'管理IP设置为: << {new_manage_ip} >>')
        else:
            self.error_logging(server_obj=self.server_obj,
                               content=f'[管理IP变更===>:] 管理IP设置失败没有可用IP,IP表为: [{ipaddr_list}]', title=self.error_message)
