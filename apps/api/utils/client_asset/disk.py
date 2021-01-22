from apps.cmdb import models
from .Base import Base


class Disk(Base):
    def __init__(self, server_obj):
        self.row_map = {'capacity': '容量', 'pd_type': '类型', 'model': '型号', 'slot': '槽位'}
        self.server_obj = server_obj
        self.type = '磁盘'
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
        new_disk_dict = content['data']
        old_disk_list = models.Disk.objects.filter(server_obj=self.server_obj)
        # # 取到所有新数据内存的槽位
        new_slot_list = list(new_disk_dict.keys())
        # # 取到所有旧数据内存的槽位
        old_slot_list = [old_obj.slot for old_obj in old_disk_list]
        # # 取交集 要更新的数据
        update_slot_list = set(new_slot_list).intersection(old_slot_list)
        # # 差集 要创建的数据
        create_slot_list = set(new_slot_list).difference(old_slot_list)
        # # 差集 要删除的数据
        delete_slot_list = set(old_slot_list).difference(new_slot_list)
        if create_slot_list:
            self.__create_data(create_slot_list, new_disk_dict)
        if update_slot_list:
            self.__update_data(update_slot_list, new_disk_dict)
        if delete_slot_list:
            self.__delete_data(delete_slot_list)

    def __create_data(self, create_slot_list, new_disk_dict):
        record_list = []
        for slot in create_slot_list:
            # 新数据
            disk_dict = new_disk_dict[slot]
            disk_dict['server_obj'] = self.server_obj
            models.Disk.objects.create(**disk_dict)
            temp = f': 槽位: << {slot} >>, 容量: << {disk_dict["capacity"]} >>, 类型: << {disk_dict["pd_type"]} >>, 型号: << {disk_dict["model"]} >>'
            record_list.append(temp)
        # 记录日志
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title=self.create_record, server_obj=self.server_obj, content=content)

    def __update_data(self, update_slot_list, new_disk_dict):
        record_list = []
        for slot in update_slot_list:
            # 新数据
            new_dict_row = new_disk_dict[slot]
            old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=self.server_obj).first()
            for k, v in new_dict_row.items():
                value = getattr(old_disk_row, k)
                if v != value:
                    record_list.append(f' 槽位:　<< {slot} >> {self.row_map[k]},由 << {value} >> 变更为: << {v} >>.')
                    setattr(old_disk_row, k, v)
            old_disk_row.save()
        # 记录日志
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(server_obj=self.server_obj, content=content)

    def __delete_data(self, delete_slot_list):
        record_list = []
        delete_disk_obj = models.Disk.objects.filter(server_obj=self.server_obj, slot__in=delete_slot_list)
        for obj in delete_disk_obj:
            record_list.append(
                f'槽位: << {obj.slot} >>, 容量: << {obj.capacity} >> , 类型:<< {obj.pd_type} >> , 型号:<< {obj.model} >>')
        delete_disk_obj.delete()
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title=self.delete_record, server_obj=self.server_obj, content=content)
