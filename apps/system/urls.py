from django.urls import path, include
from .views import EditConf

urlpatterns = [
    path('edit-conf', EditConf.as_view({
        'get': 'list',
        'put': 'update'})
         ),
]