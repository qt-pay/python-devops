from .Base import Base
import datetime


class Basic(Base):
    def __init__(self, server_obj):
        self.row_map = {'os_platform': '系统类型', 'os_version': '系统版本', 'hostname': '主机名称', }
        self.server_obj = server_obj
        self.type = '系统信息'
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
        record_list = []
        new_basic_dict = content['data']
        for k, v in new_basic_dict.items():
            value = getattr(self.server_obj, k)
            if v != value:
                record_list.append(f'[ {self.row_map[k]} ] ,由 << {value} >> 变更为  << {v} >> .')
                setattr(self.server_obj, k, v)
        if record_list:
            self.server_obj.save()
            content = ';  '.join(record_list)
            self.access_logging(title=self.update_record, server_obj=self.server_obj, content=content)
        self.__change_last_data()

    def __change_last_data(self):
        to_day = datetime.date.today()
        old_day = self.server_obj.latest_date
        self.server_obj.latest_date = to_day
        self.server_obj.save()
        self.access_logging(title='采集日期变更', server_obj=self.server_obj, content=f'最后采集日期: <<{to_day}>>')
