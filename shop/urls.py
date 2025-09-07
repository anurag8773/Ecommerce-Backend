from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CategoryViewSet, ItemViewSet, CartView, CartAddView, CartItemDetail

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"items", ItemViewSet, basename="item")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", CartAddView.as_view(), name="cart-add"),
    path("cart/items/<int:pk>/", CartItemDetail.as_view(), name="cart-item-detail"),
]
