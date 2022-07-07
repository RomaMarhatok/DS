from rest_framework.routers import DefaultRouter
from shop.views.product_views import ProductViewSet
from shop.views.inventory_views import IventoryViewSet
from shop.views.autherization_views import AuthenticationView
from django.urls import path

router = DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"inventory", IventoryViewSet, basename="inventory")
urlpatterns = router.urls
urlpatterns += [
    path(
        "auth/sign-in",
        AuthenticationView.as_view({"post": "sign_in_user"}),
        name="user-sign-in",
    ),
    path(
        "auth/login",
        AuthenticationView.as_view({"post": "login_user"}),
        name="user-login",
    ),
    path(
        "auth/logout",
        AuthenticationView.as_view(
            {"post": "logout_user"},
        ),
        name="user-logout",
    ),
]
