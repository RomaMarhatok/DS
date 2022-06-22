from rest_framework.routers import DefaultRouter
from shop.views.product_views import ProductViewSet

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")

urlpatterns = router.urls
