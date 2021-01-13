from django.db import models
#
__all__ = ['SSH','CloudDisk','CloudServer', 'UserProfile', 'UserGrop', 'BusinessUnit', 'IDC', 'DeviceCategory', 'Tag', 'Asset', 'Server', 'NetworkDevice', 'Disk','Network', 'Memory', 'AssetRecord', 'AssetErrorLog']
# 联系人表
class UserProfile(models.Model):
    name = models.CharField(verbose_name='联系人姓名', max_length=32)
    email = models.EmailField(verbose_name='联系人邮箱')
    phone = models.CharField(verbose_name='联系人座机', max_length=32)
    mobile = models.CharField(verbose_name='联系人手机号', max_length=32)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cmdb_user'
        verbose_name = '设备联系人表'
        verbose_name_plural = '设备联系人表'



class UserGrop(models.Model):
    '''
    用户组
    '''
    title = models.CharField(verbose_name='联系人组',max_length=32, unique=True )
    remark = models.CharField(verbose_name='联系人组备注', max_length=128, blank=True, null=True)
    users = models.ManyToManyField('UserProfile')
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'cmdb_user_group'
        verbose_name = '联系人组'
        verbose_name_plural = '联系人表'


class BusinessUnit(models.Model):
    """
    业务线
    """
    title = models.CharField(verbose_name='业务线', max_length=64, unique=True)
    contact = models.ForeignKey(to='UserGrop', verbose_name='业务联系人', related_name='c', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'cmdb_businessUnit'
        verbose_name = '业务线'
        verbose_name_plural = '业务线'


class IDC(models.Model):
    """
    机房信息
    """
    title = models.CharField(verbose_name='IDC名称', max_length=32)
    position = models.CharField(verbose_name='设备位置', max_length=32)
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'cmdb_idc'
        verbose_name = '业务线'
        verbose_name_plural = "机房表"

class DeviceCategory(models.Model):
    ''' 设备类型 '''
    title = models.CharField(verbose_name='设备种类', unique=True, max_length=32)
    pid = models.IntegerField(verbose_name='是否为主菜单', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'cmdb_device_category'
        verbose_name = '设备种类'
        verbose_name_plural = "设备种类"

class Tag(models.Model):
    ''' 资产标签 '''
    title = models.CharField(verbose_name='标签', max_length=32, unique=True)
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'cmdb_tag'
        verbose_name = '标签表'
        verbose_name_plural = "标签表"
# ssh 用户表
class SSH(models.Model):
    user = models.CharField(verbose_name='ssh用户名', max_length=32)
    password = models.CharField(verbose_name='ssh用户密码', max_length=32)
    port = models.IntegerField(verbose_name='ssh端口')
    class Meta:
        db_table = 'cmdb_ssh'
        verbose_name = 'ssh表'
        verbose_name_plural = 'ssh表'
# 资产表
class Asset(models.Model):
    ''' 资产信息表 存放公共信息 '''
    device_status_choices = (
        (1, '上线'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架')
    )
    title = models.CharField(max_length=32, )
    manage_ip = models.GenericIPAddressField(verbose_name='管理IP', blank=True, null=True)
    device_type = models.ForeignKey(to='DeviceCategory', verbose_name='资产类型', on_delete=models.CASCADE, blank=True, null=True)
    device_status_id = models.IntegerField(verbose_name='设备状态', choices=device_status_choices, default=1)
    maintain_groups = models.ForeignKey(to='UserGrop', verbose_name='资产维护组', related_name='m', on_delete=models.CASCADE, blank=True, null=True)
    cabinet_num = models.CharField(verbose_name='机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField(verbose_name='机柜中序号', max_length=30, null=True, blank=True)
    idc = models.ForeignKey(to='IDC', verbose_name='IDC机房', null=True, blank=True, on_delete=models.CASCADE)
    business_unit = models.ForeignKey(to='BusinessUnit', verbose_name='所属的业务线', null=True, blank=True, on_delete=models.CASCADE, related_name='asset')
    tag = models.ManyToManyField(to='Tag', verbose_name='资产标签',  blank=True)
    ssh = models.ForeignKey(verbose_name='绑定的ssh账户信息', to='SSH', on_delete=models.SET_NULL, blank=True, null=True)
    latest_date =  models.DateTimeField( verbose_name='最近同步日期', auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    def __str__(self):
        return f'{self.title}-'
    class Meta:
        db_table = 'cmdb_asset'
        verbose_name = '资产表'
        verbose_name_plural = "资产表"

# 资产变更记录表
class AssetRecord(models.Model):
    """
    资产变更记录,creator为空时，表示是资产汇报的数据。
    """
    title = models.CharField(verbose_name='更新标题', max_length=32)

    asset_obj = models.ForeignKey(verbose_name='所属资产', to='Asset', related_name='ar', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='变更内容', null=True)
    creator = models.CharField(verbose_name='变更人', max_length=32, null=True, blank=True, )
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return f'{self.asset_obj.title}---{self.title}'

    class Meta:
        db_table = 'cmdb_asset_record'
        verbose_name = '资产更新记录'
        verbose_name_plural = "资产更新记录"



# 错误日志表
class AssetErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset_obj = models.ForeignKey(verbose_name='所属资产', to='Asset', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='错误名称', max_length=32)
    content = models.TextField(verbose_name='错误内容')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'cmdb_asset_errorLog'
        verbose_name = '资产错误日志'
        verbose_name_plural = "资产错误日志"

class Server(models.Model):
    """
    服务器信息
    """
    asset_obj = models.OneToOneField(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE, related_name='server')
    # 基本信息 + 主板信息 + CPU信息
    hostname = models.CharField(verbose_name='主机名', max_length=128, unique=True)
    # manage_ip = models.GenericIPAddressField(verbose_name='管理ip', null=True, blank=True)

    os_platform = models.CharField(verbose_name='操作系统', max_length=16, null=True, blank=True)
    os_version = models.CharField(verbose_name='操作系统版本', max_length=16, null=True, blank=True)

    sn = models.CharField(verbose_name='SN号', max_length=64, db_index=True, null=True, blank=True)
    manufacturer = models.CharField(verbose_name='制造商', max_length=128, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=128, null=True, blank=True)

    cpu_count = models.IntegerField(verbose_name='CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField(verbose_name='CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField(verbose_name='CPU型号', max_length=256, null=True, blank=True)

    latest_date = models.DateField(verbose_name='更新时间', blank=True, null=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True)

    def __str__(self):
        return self.hostname

    class Meta:
        db_table = 'cmdb_server'
        verbose_name = '服务器表'
        verbose_name_plural = "服务器表"



class Disk(models.Model):
    """
    硬盘信息
    """
    slot = models.CharField(verbose_name='插槽位', max_length=8, null=True, blank=True)
    model = models.CharField(verbose_name='磁盘型号', max_length=128, null=True, blank=True)
    capacity = models.CharField(verbose_name='磁盘容量GB',  max_length=32, null=True, blank=True)
    pd_type = models.CharField(verbose_name='磁盘类型', max_length=32, null=True, blank=True)
    server_obj = models.ForeignKey(verbose_name='所属服务器', to='Server', related_name='disk', on_delete=models.CASCADE)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True)
    def __str__(self):
        return f'{self.server_obj.hostname}---{self.slot}'

    class Meta:
        db_table = 'cmdb_disk'
        verbose_name = '硬盘表'
        verbose_name_plural = "硬盘表"



# 网卡信息
class Network(models.Model):
    """
    网卡信息
    """
    title = models.CharField(verbose_name='网卡名称', max_length=128)
    hwaddr = models.CharField(verbose_name='网卡mac地址', max_length=64, null=True, blank=True)
    netmask = models.GenericIPAddressField(verbose_name='子网掩码', null=True, blank=True )
    ipaddress = models.GenericIPAddressField(verbose_name='ip地址', null=True, blank=True)
    broadcast = models.GenericIPAddressField(verbose_name='广播地址', null=True, blank=True)
    up = models.BooleanField(verbose_name='网卡状态', default=False)
    server_obj = models.ForeignKey(verbose_name='所属服务器', to='Server', related_name='nic_list', on_delete=models.CASCADE)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True)
    def __str__(self):
        return f'{self.server_obj.hostname}---{self.title}'

    class Meta:
        db_table = 'cmdb_network'
        verbose_name = '网卡表'
        verbose_name_plural = "网卡表"




class Memory(models.Model):
    """
    内存信息
    """
    slot = models.CharField(verbose_name='插槽位', max_length=32)
    manufacturer = models.CharField(verbose_name='制造商', max_length=32, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=128)
    capacity = models.FloatField(verbose_name='容量', null=True, blank=True)
    sn = models.CharField(verbose_name='内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField(verbose_name='速度', max_length=16, null=True, blank=True)
    server_obj = models.ForeignKey(verbose_name='所属服务器', to='Server', related_name='memory', on_delete=models.CASCADE)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True)
    def __str__(self):
        return f'{self.server_obj.hostname}---{self.slot}'

    class Meta:
        db_table = 'cmdb_memory'
        verbose_name = '内存表'
        verbose_name_plural = "内存表"





class NetworkDevice(models.Model):
    '''
    网络设备表
    '''
    asset_obj = models.OneToOneField(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE, )
    hostname = models.CharField(verbose_name='名称', max_length=64, blank=True, null=True)
    # manage_ip = models.GenericIPAddressField(verbose_name='管理IP', blank=True, null=True)
    vlan_ip = models.GenericIPAddressField(verbose_name='VlanIp',  blank=True, null=True)
    intranet_ip = models.GenericIPAddressField(verbose_name='内网ip', blank=True, null=True)
    sn = models.CharField(verbose_name='SN号', max_length=64, unique=True)
    manufacture = models.CharField(verbose_name='制造商', max_length=128, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField(verbose_name='端口个数', null=True, blank=True)
    device_detail = models.TextField(verbose_name='设置详细配置',  null=True, blank=True)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True)
    def __str__(self):
        return self.hostname

    class Meta:
        db_table = 'cmdb_network_device'
        verbose_name = '网络设备表'
        verbose_name_plural = "网络设备表"

class CloudServer(models.Model):
    instance_id = models.CharField(verbose_name='实例ID', max_length=64, blank=True, null=True)
    instance_name = models.CharField(verbose_name='实例名称', max_length=64, blank=True, null=True)
    instance_type = models.CharField(verbose_name='实例类型', max_length=64, blank=True, null=True)
    manage_ip = models.GenericIPAddressField(verbose_name='管理IP', blank=True, null=True)
    cpu = models.IntegerField(verbose_name='CPU',  blank=True, null=True)
    memory = models.IntegerField(verbose_name='内存',  blank=True, null=True)
    intranet_ip = models.CharField(verbose_name='内网IP', max_length=1024, blank=True, null=True)
    public_ip = models.CharField(verbose_name='内网IP', max_length=1024, blank=True, null=True)
    os_version = models.CharField(verbose_name='系统版本', max_length=64, blank=True, null=True)
    security_groupids = models.CharField(verbose_name='安全组', max_length=1024, blank=True, null=True)
    created_time = models.DateTimeField(verbose_name='创建时间', blank=True, null=True)
    expired_time = models.DateTimeField(verbose_name='到期时间',  blank=True, null=True)
    latest_date = models.DateField(verbose_name='更新时间', blank=True, null=True)
    create_at = models.DateTimeField(verbose_name='信息创建时间', auto_now_add=True, blank=True)
    asset_obj = models.OneToOneField(verbose_name='所属资产', to='Asset', on_delete=models.CASCADE, related_name='cloudserver')

    def __str__(self):
        return self.instance_name

    class Meta:
        db_table = 'cmdb_cloud_server'
        verbose_name = '云服务器表'
        verbose_name_plural = "云服务器表"
class CloudDisk(models.Model):
    """
    硬盘信息
    """

    disk_type = models.CharField(verbose_name='磁盘类型', max_length=128, null=True, blank=True)
    disk_id = models.CharField(verbose_name='磁盘ID',  max_length=32, null=True, blank=True)
    capacity = models.IntegerField(verbose_name='磁盘容量',  null=True, blank=True)
    server_obj = models.ForeignKey(verbose_name='所属云服务器', to='CloudServer', related_name='clouddisk', on_delete=models.CASCADE)
    latest_date = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True)
    def __str__(self):
        return self.disk_id
    class Meta:
        db_table = 'cmdb_cloud_disk'
        verbose_name = '云磁盘'
        verbose_name_plural = "云磁盘"