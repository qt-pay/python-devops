
from rest_framework import  serializers
from .models import *




class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SSHSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=32, write_only=True)
    class Meta:
        model = SSH
        fields = 'name, port, password'

class DeviceCategorySerializer(serializers.ModelSerializer):
    hasChildren = serializers.SerializerMethodField(read_only=True)
    def get_hasChildren(self,  obj):
        if obj.pid == 0:
            return True
        else:
            return False
    class Meta:
        model = DeviceCategory
        fields = '__all__'


class IDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDC
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    method_name = serializers.CharField(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserGropSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGrop
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_name'] = [ user.name for user in instance.users.all() ]
        representation['user_list'] =  UserProfileSerializer(instance.users.all(), many=True).data
        return representation

class AssetSerializer(serializers.ModelSerializer):
    hostname = serializers.SerializerMethodField(read_only=True)
    # manage_ip = serializers.SerializerMethodField(read_only=True)
    def get_hostname(self, obj):
        server = Server.objects.filter(asset_obj=obj.id).first()
        network = NetworkDevice.objects.filter(asset_obj=obj.id).first()
        if server:
            return server.hostname
        if network:
            return network.hostname
        else:
            return 'Null'
    # def get_manage_ip(self, obj):
    #     server = Server.objects.filter(asset_obj=obj.id).first()
    #     network = NetworkDevice.objects.filter(asset_obj=obj.id).first()
    #     cloud_server = CloudServer.objects.filter(asset_obj=obj.id).first()
    #     if server:
    #         return server.manage_ip
    #     elif network:
    #         return network.manage_ip
    #     elif cloud_server:
    #         return cloud_server.manage_ip
    #     else:
    #         return None
    class Meta:
        model = Asset
        fields ='__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['devices_type'] = instance.device_type.title if instance.device_type  else None
        representation['devices_father_type'] = DeviceCategorySerializer(DeviceCategory.objects.filter(id=instance.device_type.pid).first()).data['title'] if instance.device_type  else 'Null'
        representation['device_status'] = instance.get_device_status_id_display()
        representation['idc_title'] = instance.idc.title if instance.idc else None
        representation['tag_list'] = [tag.title for tag in instance.tag.all()] if instance.tag else []
        representation['business_unit_title'] = instance.business_unit.title if instance.business_unit else None
        # representation['group_obj'] = UserGropSerializer(UserGrop.objects.filter(id=instance.maintain_groups.id).first()).data if instance.maintain_groups else None
        return representation

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'

class AssetRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetRecord
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['creator'] =  instance.creator if instance.creator else '自动采集'
        return representation

class AssetErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetErrorLog
        fields = '__all__'

class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk
        fields = '__all__'

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = '__all__'

class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'


class NetworkDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDevice
        fields = '__all__'
class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['contact_title'] =  instance.contact.title if instance.contact else 'Null'
        representation['asset_num'] =  instance.asset.all().count()
        representation['group_obj'] =  UserGropSerializer(UserGrop.objects.filter(id=instance.contact.id).first()).data if instance.contact else None
        return representation


class CloudServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudServer
        fields = '__all__'

class CloudDiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudDisk
        fields = '__all__'