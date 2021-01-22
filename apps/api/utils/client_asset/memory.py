from apps.cmdb import models
from .Base import Base


class Memory(Base):
    def __init__(self, server_obj):
        self.row_map = {'slot': '插槽位', 'manufacturer': '制造商', 'model': '型号', 'capacity': '容量', 'sn': '内存sn',
                        'speed': '速率'}
        self.server_obj = server_obj
        self.type = '内存'
        self.error_message = f'[{self.server_obj.hostname}]-<{self.type}>收集信息出错'
        self.update_record = f'<{self.type}变更记录>'
        self.delete_record = f'<{self.type}移除记录>'
        self.create_record = f'<{self.type}新增记录>'

    @classmethod
    def initial(cls, server_obj):
        return cls(server_obj)

    def parse(self, content):
        print(content)
        print('刚进来')
        if not content['status']:
            '''出错记录日志不做处理'''
            self.error_logging(server_obj=self.server_obj, content=content['data'], title=self.error_message)
            return None
        self.__clent_data(content)

    def __clent_data(self, content):
        print('处理数据')
        new_memory_dict = content['data']
        print(new_memory_dict)
        old_memory_list = models.Memory.objects.filter(server_obj=self.server_obj)
        print(old_memory_list)
        # # 取到所有新数据内存的槽位
        new_slot_list = list(new_memory_dict.keys())
        print(new_slot_list)
        # # 取到所有旧数据内存的槽位
        old_slot_list = [old_obj.slot for old_obj in old_memory_list]
        print(old_slot_list)
        # # 取交集 要更新的数据
        update_slot_list = set(new_slot_list).intersection(old_slot_list)
        # # 差集 要创建的数据
        create_slot_list = set(new_slot_list).difference(old_slot_list)
        # # 差集 要删除的数据
        delete_slot_list = set(old_slot_list).difference(new_slot_list)
        if create_slot_list:
            self.__create_data(create_slot_list, new_memory_dict)
        if update_slot_list:
            self.__update_data(update_slot_list, new_memory_dict)
        if delete_slot_list:
            self.__delete_data(delete_slot_list)

    def __create_data(self, create_slot_list, new_memory_dict):
        print(new_memory_dict)
        record_list = []
        for slot in create_slot_list:
            # 新数据
            memory_dict = new_memory_dict[slot]
            memory_dict['server_obj'] = self.server_obj
            models.Memory.objects.create(**memory_dict)
            temp = f': 槽位: << {slot} >>, 容量: << {memory_dict["capacity"]} >>, 速率: <<{memory_dict["speed"]} >>, sn号: << {memory_dict["sn"]} >> , 制造商: << {memory_dict["manufacturer"]} >> , 型号: << {memory_dict["model"]} >>'
            record_list.append(temp)
        # 记录日志
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title=self.create_record, server_obj=self.server_obj, content=content)

    def __update_data(self, update_slot_list, new_memory_dict):
        record_list = []
        for slot in update_slot_list:
            # 新数据
            new_dict_row = new_memory_dict[slot]
            old_memory_row = models.Memory.objects.filter(slot=slot, server_obj=self.server_obj).first()
            for k, v in new_dict_row.items():
                value = getattr(old_memory_row, k)
                if v != value:
                    record_list.append(f' 槽位置 << {slot} >>: {self.row_map[k]}, 由 << {value} >>变更为: << {v} >>.')
                    setattr(old_memory_row, k, v)
            old_memory_row.save()
        # 记录日志
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title=self.update_record, server_obj=self.server_obj, content=content)

    def __delete_data(self, delete_slot_list):
        record_list = [f'{self.delete_record}', ]
        delete_memory_obj = models.Memory.objects.filter(server_obj=self.server_obj, slot__in=delete_slot_list)
        for obj in delete_memory_obj:
            record_list.append(
                f'槽位 << {obj.slot} >>: 容量:<< {obj.capacity} >>, sn号: << {obj.sn} >>, 制造商: << {obj.manufacturer} >>, 型号: << {obj.model} >>.')
        delete_memory_obj.delete()
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title=self.delete_record, server_obj=self.server_obj, content=content)
