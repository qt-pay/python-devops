from apps.cmdb.models import AssetRecord
from apps.rbac.auth.jwt_auth import analysis_token
from base.views import BaseModelViewSet
from base.response import json_ok_response, json_error_response


class Base(BaseModelViewSet):
    def asset_record(self, request, title, content, asset_obj):
        user_info = analysis_token(request)
        name = user_info['user_info']['username']
        record = AssetRecord.objects.create(title=title, creator=name, content=content, asset_obj_id=asset_obj)
        record.save()


