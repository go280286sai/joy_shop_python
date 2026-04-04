from django.contrib import admin
from django.contrib.auth.models import User

from toy_shop.models import (Brand, Category, Product, ProductImage, SlideImage, UserProfile,
                             Address, Favorite, PromoCode, Review, Order, OrderItem, Cart, CartItem)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    class Meta:
        model = Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent',)
    search_fields = ('name',)

    class Meta:
        model = Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category',)
    search_fields = ('name',)

    class Meta:
        model = Product


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image',)
    search_fields = ('image',)

    class Meta:
        model = ProductImage


@admin.register(SlideImage)
class SlideImagesAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    class Meta:
        model = SlideImage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user",)

    class Meta:
        model = UserProfile


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone", "city")
    search_fields = ("first_name", "last_name", "phone", "city")
    list_filter = ("city",)

    class Meta:
        model = Address


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    search_fields = ("user",)

    class Meta:
        model = Favorite


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "is_active")
    search_fields = ("code",)

    class Meta:
        model = PromoCode

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    list_filter = ("product",)
    class Meta:
        model = Review

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone", "city", "status")
    search_fields = ("last_name", "phone", "city", "status")
    class Meta:
        model = Order

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product_name", "product_price")
    search_fields = ("product_name", "product_price")
    class Meta:
        model = OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "session_key",)
    search_fields = ("user", "session_key",)
    class Meta:
        model = Cart

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity",)
    search_fields = ("cart", "product",)
    class Meta:
        model = CartItem
