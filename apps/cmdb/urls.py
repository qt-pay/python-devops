from rest_framework import routers
from .views import tag, device_category, idc, contacts, asset, test, asset_record, asset_errorLog, server, network, memory, disk, networkdevice, business_unit, cloud_server,cloud_disk
router = routers.DefaultRouter()
router.register(r'tag', tag.TagViewSet, )
router.register(r'idc', idc.IDCViewSet, )
router.register(r'device-category', device_category.DeviceCategoryViewSet, )
router.register(r'user', contacts.UserViewSet, )
router.register(r'user-group', contacts.UserGroupViewSet, )
router.register(r'asset', asset.AssetViewSet, )
router.register(r'server', server.ServerViewSet, )



router.register(r'asset-record', asset_record.AssetRecordViewSet, )
router.register(r'asset-error', asset_errorLog.AssetErrorLogViewSet )
router.register(r'asset-error', asset_errorLog.AssetErrorLogViewSet )


router.register(r'server-network', network.NetworkViewSet )
router.register(r'server-disk', disk.DiskViewSet )
router.register(r'server-memory', memory.MemoryViewSet )

router.register(r'network-device', networkdevice.NetworkDeviceViewSet )
router.register(r'business-unit', business_unit.BusinessUnitViewSet)


router.register(r'cloud-server', cloud_server.CloudServerViewSet)
router.register(r'cloud-disk', cloud_disk.CloudDiskViewSet)


router.register(r'test', test.TestViewSet, )



urlpatterns = router.urls
