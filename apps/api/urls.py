from django.urls import path, include
from .views import client_asset, cloud_server

urlpatterns = [
    path('client-asset.store', client_asset.ClentAsset.as_view({
        'get': 'list',
        'post': 'create'})
         ),
    path('cloud-server.store', cloud_server.CloudServerView.as_view())
]