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
    rating = models.PositiveIntegerField(default=0) # Рейтинг
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
