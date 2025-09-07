from django.contrib import admin
from .models import Category, Item, Cart, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "category", "stock")
    list_filter = ("category",)
    search_fields = ("title", "description")

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "updated_at")
    inlines = [CartItemInline]
