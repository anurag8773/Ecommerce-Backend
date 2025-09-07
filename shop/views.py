from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Item, Cart, CartItem
from .serializers import (
    RegisterSerializer, CategorySerializer, ItemSerializer,
    CartSerializer, CartItemSerializer
)
from .permissions import IsAdminOrReadOnly
from .filters import ItemFilter

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.select_related("category").all().order_by("-created_at")
    serializer_class = ItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ItemFilter
    search_fields = ["title", "description"]
    ordering_fields = ["price", "created_at"]

class CartView(APIView):
    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self.get_cart(request.user)
        return Response(CartSerializer(cart).data)

class CartAddView(APIView):
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data["item"]
        qty = serializer.validated_data.get("quantity", 1)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item, defaults={"quantity": qty})
        if not created:
            cart_item.quantity += qty
            cart_item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

class CartItemDetail(APIView):
    def patch(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        new_qty = request.data.get("quantity")
        if new_qty is None or int(new_qty) < 1:
            return Response({"detail": "quantity must be >= 1"}, status=400)
        cart_item.quantity = int(new_qty)
        cart_item.save()
        return Response(CartSerializer(cart).data)

    def delete(self, request, pk):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        cart_item.delete()
        return Response(CartSerializer(cart).data)
