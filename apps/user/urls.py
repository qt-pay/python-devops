from rest_framework import routers
from .views import userprofile
from .views import department
from django.urls import path, include
router = routers.DefaultRouter()

router.register(r'department', department.DepartmentViewSet, )





router.register(r'user-profile', userprofile.UserProfileViewSet, )
router.register(r'user-manager', userprofile.UserManagerViewSet, )
# router.register(r'login', userprofile.LoginViewSet, )
# router.register(r'logout', userprofile.LogoutViewSet, )
urlpatterns = [

    path('login', userprofile.LoginViewSet.as_view()),
    path('logout', userprofile.LogoutViewSet.as_view()),
    # path('userinfo', userprofile.UserInfoViewSet.as_view()),
]
urlpatterns += router.urls
