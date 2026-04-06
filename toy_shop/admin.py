"""
Admin module
"""
# pylint: disable=too-few-public-methods
from django.contrib import admin
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import path

from toy_shop.models import (Brand, Category, Product, ProductImage,
                             SlideImage, UserProfile,
                             Address, Favorite, PromoCode, Review,
                             Order, OrderItem, Cart, CartItem)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Register Brand model
    """
    list_display = ('name',)
    search_fields = ('name',)

    class Meta:
        """
        Register Brand model
        """
        model = Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Register Category model
    """
    list_display = ('name', 'parent',)
    search_fields = ('name',)

    class Meta:
        """
        Register Category model
        """
        model = Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Register Product model
    """
    list_display = ('name', 'brand', 'category',)
    search_fields = ('name',)

    class Meta:
        """
        Register Product model
        """
        model = Product


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Register ProductImage model
    """
    list_display = ('product', 'image',)
    search_fields = ('image',)

    class Meta:
        """
        Register ProductImage model
        """
        model = ProductImage


@admin.register(SlideImage)
class SlideImagesAdmin(admin.ModelAdmin):
    """
    Register SlideImage model
    """
    list_display = ("name",)
    search_fields = ("name",)

    class Meta:
        """
        Register SlideImage model
        """
        model = SlideImage


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Register UserProfile model
    """
    list_display = ("user",)
    search_fields = ("user",)

    class Meta:
        """
        Register UserProfile model
        """
        model = UserProfile


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Register Address model
    """
    list_display = ("first_name", "last_name", "phone", "city")
    search_fields = ("first_name", "last_name", "phone", "city")
    list_filter = ("city",)

    class Meta:
        """
        Register Address model
        """
        model = Address


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Register Favorite model
    """
    list_display = ("user", "product")
    search_fields = ("user",)

    class Meta:
        """
        Register Favorite model
        """
        model = Favorite


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    """
    Register PromoCode model
    """
    list_display = ("code", "is_active")
    search_fields = ("code",)

    class Meta:
        """
        Register PromoCode model
        """
        model = PromoCode


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Register Review model
    """
    list_display = ("user", "product")
    list_filter = ("product",)

    class Meta:
        """
        Register Review model
        """
        model = Review


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Register Order model
    """
    list_display = ("first_name", "last_name", "phone", "city", "status")
    search_fields = ("last_name", "phone", "city", "status")

    class Meta:
        """
        Register Order model
        """
        model = Order


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Register OrderItem model
    """
    list_display = ("product_name", "product_price")
    search_fields = ("product_name", "product_price")

    class Meta:
        """
        Register OrderItem model
        """
        model = OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Register CartAdmin model
    """
    list_display = ("user", "session_key",)
    search_fields = ("user", "session_key",)

    class Meta:
        """
        Register CartAdmin model
        """
        model = Cart


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Register CartItem model
    """
    list_display = ("cart", "product", "quantity",)
    search_fields = ("cart", "product",)

    class Meta:
        """
        Register CartItem model
        """
        model = CartItem

class ActionAdmin(admin.AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"
    index_title = "Добро пожаловать"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "export/products/",
                self.admin_view(self.export_products),
                name="export-products"
            ),
        ]
        return custom_urls + urls

    def export_products(self, request):
        if not request.user.is_staff:
            return HttpResponseForbidden()

        data = list(Product.objects.values("id", "name", "price"))
        return JsonResponse(data, safe=False)


action_admin = ActionAdmin(name="action_admin")
action_admin.register(Product)