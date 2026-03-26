from django.contrib import admin

from toy_shop.models import Brand, Category, Product, ProductImage, SlideImage, UserProfile


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