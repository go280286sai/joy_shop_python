"""
Models module
"""
# pylint: disable=too-few-public-methods
from django.contrib.auth.models import User
from django.db import models


class Brand(models.Model):
    """
    Register Brand model
    """
    name: models.CharField = models.CharField(max_length=100)
    slug: models.SlugField = models.SlugField(unique=True)
    logo: models.ImageField = models.ImageField(upload_to='brands/')
    description: models.TextField = models.TextField(blank=True)
    website: models.URLField = models.URLField(blank=True)
    is_active: models.BooleanField = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        """
        Register Brand model
        """
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class Category(models.Model):
    """
    Register Category model
    """
    name: models.CharField = models.CharField(max_length=100)
    slug: models.SlugField = models.SlugField(unique=True)
    parent: models.ForeignKey = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    description: models.TextField = models.TextField(blank=True)
    image: models.ImageField = models.ImageField(upload_to='categories/')
    is_active: models.BooleanField = models.BooleanField(default=True)
    order: models.PositiveIntegerField = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        """
        Register Category model
        """
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']


class Product(models.Model):
    """
    Register Product model
    """
    category: models.ForeignKey = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True
    )
    brand: models.ForeignKey = models.ForeignKey(
        "Brand", on_delete=models.SET_NULL, null=True
    )
    name: models.CharField = models.CharField(max_length=200)
    slug: models.SlugField = models.SlugField(unique=True)
    article: models.CharField = models.CharField(max_length=50, unique=True)
    description_short: models.CharField = models.CharField(max_length=300)
    description_full: models.TextField = models.TextField()
    price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    old_price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    stock: models.PositiveIntegerField = models.PositiveIntegerField(default=0)
    age_min: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0
    )
    age_max: models.PositiveIntegerField = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    material: models.CharField = models.CharField(max_length=100, blank=True)
    dimensions: models.CharField = models.CharField(max_length=100, blank=True)
    weight: models.DecimalField = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True
    )
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_featured: models.BooleanField = models.BooleanField(default=False)
    is_new: models.BooleanField = models.BooleanField(default=False)
    rating: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        """
        Register Product model
        """
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']


class ProductImage(models.Model):
    """
    Register ProductImage model
    """
    product: models.ForeignKey = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )
    image: models.ImageField = models.ImageField(upload_to='products/')
    alt_text: models.CharField = models.CharField(max_length=200, blank=True)
    order: models.PositiveIntegerField = models.PositiveIntegerField(default=0)
    is_main: models.BooleanField = models.BooleanField(default=False)


class SlideImage(models.Model):
    """
    Register SlideImage model
    """
    name: models.CharField = models.CharField(max_length=200)
    image: models.ImageField = models.ImageField(upload_to='slides/')
    alt_text: models.CharField = models.CharField(max_length=200, blank=True)
    order: models.PositiveIntegerField = models.PositiveIntegerField(default=0)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        """
        Register SlideImage model
        """
        verbose_name = 'Slide Image'
        verbose_name_plural = 'Slide Images'


class Address(models.Model):
    """
    Register Address model
    """
    user: models.ForeignKey = models.ForeignKey(User, related_name='addresses',
                                                on_delete=models.CASCADE)
    first_name: models.CharField = models.CharField(max_length=100)
    last_name: models.CharField = models.CharField(max_length=100)
    phone: models.CharField = models.CharField(max_length=20)
    address: models.TextField = models.TextField()
    city: models.CharField = models.CharField(max_length=100)
    postal_code: models.CharField = models.CharField(max_length=10)
    is_default: models.BooleanField = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        """
        Register Address model
        """
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Favorite(models.Model):
    """
    Register Favorite model
    """
    user: models.ForeignKey = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    product: models.ForeignKey = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        """
        Register Favorite model
        """
        unique_together = ['user', 'product']
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'


class PromoCode(models.Model):
    """
    Register Favorite model
    """
    code: models.CharField = models.CharField(max_length=50, unique=True)
    discount_type: models.CharField = models.CharField(
        max_length=10,
        choices=[('percent', 'Процент'), ('fixed', 'Фикс. сумма')]
    )
    discount_value: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    min_order_amount: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    max_uses: models.PositiveIntegerField = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    used_count: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0
    )
    valid_from: models.DateTimeField = models.DateTimeField()
    valid_until: models.DateTimeField = models.DateTimeField()
    is_active: models.BooleanField = models.BooleanField(default=True)

    def __str__(self):
        return str(self.code)

    class Meta:
        """
        Register Favorite model
        """
        verbose_name = 'Promo Code'
        verbose_name_plural = 'Promo Codes'


class UserProfile(models.Model):
    """
    Register UserProfile model
    """
    user: models.OneToOneField = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone: models.CharField = models.CharField(max_length=20, blank=True)
    date_of_birth: models.DateField = models.DateField(null=True, blank=True)
    avatar: models.ImageField = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    bonus_points: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0
    )
    newsletter_subscribed: models.BooleanField = models.BooleanField(
        default=False
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        """
        Register UserProfile model
        """
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class Review(models.Model):
    """
    Register Review model
    """
    product: models.ForeignKey = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    user: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    rating: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    text: models.TextField = models.TextField()
    images: models.ImageField = models.ImageField(upload_to='reviews/')
    is_approved: models.BooleanField = models.BooleanField(default=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        """
        Register Review model
        """
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Cart(models.Model):
    """
    Register Cart model
    """
    user: models.ForeignKey = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    session_key: models.CharField = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.session_key if self.session_key else "null")

    class Meta:
        """
        Register Cart model
        """
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'


class CartItem(models.Model):
    """
    Register CartItem model
    """
    cart: models.ForeignKey = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )
    product: models.ForeignKey = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity: models.PositiveIntegerField = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return self.product.name

    class Meta:
        """
        Register CartItem model
        """
        unique_together = ['cart', 'product']
        verbose_name = 'CartItem'
        verbose_name_plural = 'CartItems'


class Order(models.Model):
    """
    Register Order model
    """
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user: models.ForeignKey = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    status: models.CharField = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    first_name: models.CharField = models.CharField(max_length=100)
    last_name: models.CharField = models.CharField(max_length=100)
    email: models.EmailField = models.EmailField()
    phone: models.CharField = models.CharField(max_length=20)
    address: models.TextField = models.TextField()
    city: models.CharField = models.CharField(max_length=100)
    postal_code: models.CharField = models.CharField(max_length=10)
    delivery_method: models.CharField = models.CharField(max_length=50)
    payment_method: models.CharField = models.CharField(max_length=50)
    total_amount: models.DecimalField = models.DecimalField(max_digits=10,
                                                            decimal_places=2)
    discount_amount: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    delivery_cost: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    promo_code: models.CharField = models.CharField(max_length=50, blank=True)
    notes: models.TextField = models.TextField(blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        """
        Register Order model
        """
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    """
    Register OrderItem model
    """
    order: models.ForeignKey = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product: models.ForeignKey = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    product_name: models.CharField = models.CharField(max_length=200)
    product_price: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity: models.PositiveIntegerField = models.PositiveIntegerField()

    def __str__(self):
        return str(self.product_name)

    class Meta:
        """
        Register OrderItem model
        """
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'
