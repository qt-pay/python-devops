from utils.rest_framework.base_response import new_response
from utils.rest_framework.base_view import NewModelViewSet
from ..serializers import AssetSerializer
from ..models import Asset, Server, NetworkDevice
from django.forms.models import model_to_dict


class TestViewSet(NewModelViewSet):
    queryset = Asset.objects.all().order_by('id')
    serializer_class = AssetSerializer


    def list(self, request):
        try:
            dic = {}
            queryset = Asset.objects.all()
            for obj in queryset:
                new_idc = model_to_dict(obj)
                print(new_idc)
                # print(new_idc)
                server = Server.objects.filter(asset=obj.id).first()
                network = NetworkDevice.objects.filter(asset_obj=obj.id).first()

                if server:
                    print(server.hostname)
                    new_idc['manage_ip'] = server.manage_ip
                    new_idc['hostname'] = server.hostname
                    dic.update(new_idc)
                if network:
                    print(network.hostname)
                    new_idc['manage_ip'] = network.manage_ip
                    new_idc['hostname'] = network.hostname
                    dic.update(new_idc)
            return new_response(data=dic)
        except Exception as e:
            return new_response(code=10200, message=str(e), data='error')