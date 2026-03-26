from django.contrib.auth.models import User
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='brands/')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)  # Категория
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)  # Бренд
    name = models.CharField(max_length=200)  # Название
    slug = models.SlugField(unique=True)  # URL-якорь
    article = models.CharField(max_length=50, unique=True)  # Артикул
    description_short = models.CharField(max_length=300)  # Краткое описание
    description_full = models.TextField()  # Полное описание (HTML)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Старая цена
    stock = models.PositiveIntegerField(default=0)  # Остаток на складе
    age_min = models.PositiveIntegerField(default=0)  # Минимальный возраст (мес.)
    age_max = models.PositiveIntegerField(null=True, blank=True)  # Максимальный возраст (мес.)
    material = models.CharField(max_length=100, blank=True)  # Материал
    dimensions = models.CharField(max_length=100, blank=True)  # Габариты
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # Вес (кг)
    is_active = models.BooleanField(default=True)  # Активен
    is_featured = models.BooleanField(default=False)  # Рекомендуемый
    is_new = models.BooleanField(default=False)  # Новинка
    rating = models.PositiveIntegerField(default=0)  # Рейтинг
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_main = models.BooleanField(default=False)  # Основное изображение


class SlideImage(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='slides/')
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Slide Image'
        verbose_name_plural = 'Slide Images'


class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    class Meta:
        unique_together = ['user', 'product']
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=[('percent', 'Процент'), ('fixed', 'Фикс. сумма')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Promo Code'
        verbose_name_plural = 'Promo Codes'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bonus_points = models.PositiveIntegerField(default=0)
    newsletter_subscribed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
