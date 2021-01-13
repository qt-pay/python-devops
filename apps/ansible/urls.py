from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'history', HistoryViewSet, )
router.register(r'project', ProjectViewSet, )
router.register(r'job', JobViewSet, )
router.register(r'extravars', ExtravarsViewSet, )

urlpatterns = [
    path('task-submit', Task_SubmitView.as_view()),
]

urlpatterns = urlpatterns + router.urls
