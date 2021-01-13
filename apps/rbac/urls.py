from rest_framework import routers
from .views import menus
from .views import roles
from .views import permissions
router = routers.DefaultRouter()
router.register(r'roles', roles.RolesViewSet, )
router.register(r'menus', menus.MenusViewSet, )
router.register(r'permissions', permissions.PermissionsViewSet, )

urlpatterns = router.urls
