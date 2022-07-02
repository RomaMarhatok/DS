from rest_framework.routers import DefaultRouter
from shop.views.product_views import ProductViewSet
from shop.views.inventory_views import IventoryViewSet

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"inventory", IventoryViewSet, basename="inventory")
urlpatterns = router.urls
