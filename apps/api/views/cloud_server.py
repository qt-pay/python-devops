from base.response import json_ok_response, json_error_response
from base.views import BaseApiView
from apps.cmdb import models
from ..utils.api_decode import decrypt_get, decrypt_post
import datetime


class CloudServerView(BaseApiView):
    def post(self, request):
        ''' 解密 加数据校验 '''
        data = request.data.get('data')
        if not data:
            return json_error_response(message='data 必须传递')
        result_dic = decrypt_post(data)
        if not result_dic:
            return json_error_response(message='数据格式不正确')
        for item in result_dic:
            # 检查数据是否创建还是修改
            cloud_server_obj = models.CloudServer.objects.filter(instance_id=item['baseic']['instance_id']).first()
            if not cloud_server_obj:
                status = self.__create_server(item)
                if not status:
                    return json_error_response(message='实例创建失败')
            else:
                to_day = datetime.date.today()
                cloud_server_obj.latest_date = to_day
                cloud_server_obj.save()
                self.__updae_server(item, cloud_server_obj)
        return json_ok_response()

    def __updae_server(self, content, server_obj):
        row_map = {'instance_id': '实例ID', 'instance_name': '实例名称', 'instance_type': '实例类型',
                   'manage_ip': '管理IP', 'cpu': 'CPU', 'memory': '内存', 'intranet_ip': '内网IP',
                   'public_ip': '外网IP', 'os_version': '系统版本', 'security_groupids': '安全组', 'created_time': '创建时间',
                   'expired_time': '到期时间'}
        record_list = []
        baseic = content['baseic']
        ''' 判断云服务器基本信息是否变更 '''
        for k, v in baseic.items():
            value = getattr(server_obj, k)
            if k == 'expired_time' or k == 'created_time':
                if not v:
                    continue
                new_v = str(datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ"))
                new_value = str(value.strftime('%Y-%m-%d %H:%M:%S'))
                if new_v.strip() != new_value.strip():

                    record_list.append(
                        f' 实例ID:<<{baseic["instance_id"]}>> {row_map[k]},由 << {value} >> 变更为: << {v} >>.')
                    setattr(server_obj, k, v)
                    continue
                else:
                    continue
            elif k == 'intranet_ip':
                v = ','.join(v) if v else None
            elif k == 'public_ip':
                v = ','.join(v) if v else None
            elif k == 'security_groupids':
                v = ','.join(v) if v else None

            if v != value:
                record_list.append(f' 实例ID:<<{baseic["instance_id"]}>> {row_map[k]},由 << {value} >> 变更为: << {v} >>.')
                setattr(server_obj, k, v)
        server_obj.save()
        # 判断IDC等资产信息
        asset_obj = models.Asset.objects.filter(title=server_obj.instance_name).first()
        device_status_dic = {
            0: '上线',
            1: '在线',
            2: '离线',
            3: '下架'
        }
        if content['device_status_id'] != asset_obj.device_status_id:
            old_id = asset_obj.device_status_id
            asset_obj.device_status_id = content['device_status_id']
            record_list.append(
                f' 资产状态变更:<<{baseic["instance_id"]}>> 实例状态状态,由 << {device_status_dic[old_id]} >> 变更为: << {device_status_dic[content["device_status_id"]]} >>.')
        device_category_obj = self.__check_asset_type(content['cloud_vendors'])
        idc_obj = self.__check_idc_id(content['idc'], content['zone'])
        if device_category_obj.id != asset_obj.device_type.id:
            old_device_type = asset_obj.device_type.title
            asset_obj.device_type = device_category_obj
            record_list.append(
                f' 资产信息变更:<<{baseic["instance_id"]}>> 实例信息变更类型,由 << {old_device_type} >> 变更为: <<{device_category_obj.title}>>.')
        if idc_obj.id != asset_obj.idc.id:
            old_idc = asset_obj.idc.title
            asset_obj.idc = idc_obj
            record_list.append(
                f' 资产信息变更:<<{baseic["instance_id"]}>> 机房信息变更类型,由<<{old_idc}>> 变更为: <<{idc_obj.title}>>.')
        asset_obj.save()
        # 记录日志
        if record_list:
            contents = ';  '.join(record_list)
            self.access_logging(title='实例信息变更', server_obj=server_obj, content=contents)
        self.__clent_data(content['disk'], server_obj)

    def __create_server(self, server_info, ):

        ''' 获取实例类型及IDC机房 '''
        if not 'cloud_vendors' in server_info:
            ''' 记录数据类型提交错误日志 '''
            self.error_logging(content=f'实例ID:{server_info["baseic"]["instance_id"]} 上传数据没有 <cloud_vendors> 数据.',
                               title='数据提交格式错误')
            return False
        device_category_obj = self.__check_asset_type(server_info['cloud_vendors'])

        if not device_category_obj:
            self.error_logging(
                content=f'实例ID:{server_info["baseic"]["instance_id"]} 类型错误: {server_info["cloud_vendors"]}.',
                title='类型没有定义')
            return False

        ''' 判断 idc '''
        if not 'zone' in server_info or not 'idc' in server_info:
            # 记录日志 数据格式错误
            self.error_logging(content=f'实例ID:{server_info["baseic"]["instance_id"]} 上传数据没有 <zone/idc> 数据.',
                               title='数据提交格式错误')
            return False

        idc_obj = self.__check_idc_id(server_info['idc'], server_info['zone'])
        ''' 创建资产 '''
        to_day = datetime.date.today()
        asset_obj = models.Asset.objects.create(title=server_info['baseic']['instance_name'],
                                                device_status_id=server_info['device_status_id'], idc=idc_obj,
                                                device_type=device_category_obj)
        asset_obj.save()
        cloud_server_dic = {
            'asset_obj': asset_obj,
            'instance_id': server_info['baseic']['instance_id'],
            'instance_name': server_info['baseic']['instance_name'],
            'instance_type': server_info['baseic']['instance_type'],
            'manage_ip': server_info['baseic']['manage_ip'],
            'cpu': server_info['baseic']['cpu'],
            'memory': server_info['baseic']['memory'],
            'intranet_ip': ','.join(server_info['baseic']['intranet_ip']) if server_info['baseic'][
                'intranet_ip'] else None,
            'public_ip': ','.join(server_info['baseic']['public_ip']) if server_info['baseic']['public_ip'] else None,
            'os_version': server_info['baseic']['os_version'],
            'security_groupids': ','.join(server_info['baseic']['security_groupids']) if server_info['baseic'][
                'security_groupids'] else None,
            'created_time': server_info['baseic']['created_time'],
            'expired_time': server_info['baseic']['expired_time'],
            'latest_date': str(to_day)
        }
        cloud_server_obj = models.CloudServer.objects.create(**cloud_server_dic)
        cloud_server_obj.save()
        self.access_logging(title='新增云服务器', server_obj=cloud_server_obj,
                            content=f'实例ID:{cloud_server_obj.instance_id}, 实例名称: {cloud_server_obj.instance_name} CPU: {cloud_server_obj.cpu}')
        self.__clent_data(server_info['disk'], cloud_server_obj)
        return True

    def __clent_data(self, content, cloud_server_obj):
        new_disk_dict = content
        old_disk_list = models.CloudDisk.objects.filter(server_obj=cloud_server_obj)
        # # 取到所有新数据内存的槽位
        new_disk_id_list = list(new_disk_dict.keys())
        # # 取到所有旧数据内存的槽位
        old_disk_id_list = [old_obj.disk_id for old_obj in old_disk_list]
        # # 取交集 要更新的数据
        update_disk_id_list = set(new_disk_id_list).intersection(old_disk_id_list)
        # # 差集 要创建的数据
        create_disk_id_list = set(new_disk_id_list).difference(old_disk_id_list)
        # # 差集 要删除的数据
        delete_disk_id_list = set(old_disk_id_list).difference(new_disk_id_list)
        if create_disk_id_list:
            self.__create_disk_data(create_disk_id_list, new_disk_dict, cloud_server_obj)
        if update_disk_id_list:
            self.__update_disk_data(update_disk_id_list, new_disk_dict, cloud_server_obj)
        if delete_disk_id_list:
            self.__delete_data(delete_disk_id_list, cloud_server_obj)

    # def __create_dick(self, server_obj, disk_info):
    #
    #     for disk_item in disk_info:
    #         disk_item['server_obj'] = server_obj
    #         disk_obj = models.CloudDisk.objects.create(**disk_item)
    #
    #         disk_obj.save()

    def __create_disk_data(self, create_disk_id_list, new_disk_dict, cloud_server_obj):
        record_list = []
        for disk_id in create_disk_id_list:
            # 新数据
            disk_dict = new_disk_dict[disk_id]
            disk_dict['server_obj'] = cloud_server_obj
            models.CloudDisk.objects.create(**disk_dict)
            temp = f': 磁盘ID: << {disk_id} >>, 容量: << {disk_dict["capacity"]} >>'
            record_list.append(temp)
        # 记录日志
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title='新增磁盘', server_obj=cloud_server_obj, content=content)

    def __update_disk_data(self, update_disk_id_list, new_disk_dict, cloud_server_obj):
        row_map = {'disk_id': '磁盘ID', 'capacity': '磁盘容量', 'disk_type': '磁盘类型'}
        record_list = []
        for disk_id in update_disk_id_list:
            # 新数据
            new_dict_row = new_disk_dict[disk_id]
            old_disk_row = models.CloudDisk.objects.filter(disk_id=disk_id, server_obj=cloud_server_obj).first()
            for k, v in new_dict_row.items():
                value = getattr(old_disk_row, k)
                if v != value:
                    record_list.append(f' 磁盘ID:　<< {disk_id} >> {row_map[k]},由 << {value} >> 变更为: << {v} >>.')
                    setattr(old_disk_row, k, v)
            old_disk_row.save()
        # 记录日志
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title='磁盘变更', server_obj=cloud_server_obj, content=content)

    def __delete_data(self, delete_disk_id_list, cloud_server_obj):
        record_list = []
        delete_disk_obj = models.CloudDisk.objects.filter(disk_id__in=delete_disk_id_list, server_obj=cloud_server_obj)
        for obj in delete_disk_obj:
            record_list.append(f'磁盘ID: << {obj.disk_id} >>, 容量: << {obj.capacity} >>')
        delete_disk_obj.delete()
        if record_list:
            content = ';  '.join(record_list)
            self.access_logging(title='磁盘移除', server_obj=cloud_server_obj, content=content)

    def error_logging(self, content, title, server_obj=None):
        models.AssetErrorLog.objects.create(
            content=content,
            title=title, asset_obj=server_obj)

    def access_logging(self, title, server_obj, content):
        models.AssetRecord.objects.create(title=title, asset_obj=server_obj.asset_obj, content=content)

    def __check_asset_type(self, asset_type):
        device_category = models.DeviceCategory.objects.filter(title=asset_type).first()
        return device_category

    def __check_idc_id(self, idc_title, idc_position):
        idc_obj = models.IDC.objects.filter(title=idc_title, position=idc_position).first()
        if idc_obj:
            return idc_obj
        else:
            idc_obj = models.IDC.objects.create(title=idc_title, position=idc_position)
            idc_obj.save()
            return idc_obj
