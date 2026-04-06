"""
View module
"""
# pylint: disable=(ungrouped-imports, no-member, too-many-ancestors)
import random
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from faker import Faker
from django.contrib.auth import authenticate, login, logout
from toy_shop.models import (Brand, Category, Product, ProductImage,
                             SlideImage, UserProfile, Cart, CartItem,
                             Order, OrderItem)
from . import forms
from .forms import UserProfileForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .serializers import ProductSerializer


class IndexView(ListView):
    """
    Create IndexView
    """
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        """
        :return:
        """
        return Product.objects.order_by('-rating')[:15]

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        context['slides'] = SlideImage.objects.all()
        context['cart_count'] = get_cart_count(self.request)
        return context


class CategoryView(ListView):
    """
    Create CategoryView
    """
    model = Product
    template_name = 'category.html'
    context_object_name = 'products'
    paginate_by = 15
    category = None

    def get_queryset(self):
        """
        :return:
        """
        # получаем категорию по slug
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug']
        )
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        context['cart_count'] = get_cart_count(self.request)
        return context


class BrandView(ListView):
    """
    Create BrandView
    """
    template_name = 'brand.html'
    context_object_name = 'products'
    paginate_by = 15
    brand = None

    def get_queryset(self):
        """
        :return:
        """
        # сохраняем бренд в self.brand
        self.brand = get_object_or_404(Brand, slug=self.kwargs['brand_slug'])
        # возвращаем товары этого бренда
        return Product.objects.filter(brand=self.brand)

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['brand'] = self.brand
        context['categories'] = Category.objects.all()
        context['cart_count'] = get_cart_count(self.request)
        return context


class ProductView(TemplateView):
    """
    Create ProductView
    """
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        product_images = ProductImage.objects.filter(product=product)
        context['product'] = product
        context['categories'] = Category.objects.all()
        context['images'] = product_images
        context['cart_count'] = get_cart_count(self.request)
        return context


class TestView(ListView):
    """
    Create TestView
    """
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    faker = Faker()

    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        categories = list(Category.objects.all())
        brands = list(Brand.objects.all())

        for _ in range(1000):
            get_name = self.faker.sentence(nb_words=3)
            descriptions = self.faker.text(max_nb_chars=500)
            Product.objects.create(
                category=random.choice(categories),
                brand=random.choice(brands),
                name=get_name,
                slug=self.faker.slug(),
                article=self.faker.random_number(digits=5),
                description_short=descriptions[:100],
                description_full=descriptions,
                price=self.faker.random_number(digits=3),
                old_price=self.faker.random_number(digits=3),
                stock=self.faker.random_number(digits=2),
                age_min=random.choice(range(3, 18)),
                material=self.faker.text(max_nb_chars=50),
                dimensions=self.faker.random_number(digits=5),
                weight=self.faker.random_number(digits=5),
                is_active=True
            )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        return context


class LogoutView(TemplateView):
    """
    Create LogoutView
    """
    redirect_url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.redirect_url)


class RegisterView(TemplateView):
    """
    Create RegisterView
    """
    template_name = "auth/register.html"
    form = forms.StyledUserCreationForm()

    def post(self, request):
        """
        :param request:
        :return:
        """
        data = forms.StyledUserCreationForm(request.POST)
        if data.is_valid():
            user = data.save()
            login(request, user)
        else:
            return HttpResponseRedirect('/')
        return request

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = self.form
        return context


class LoginView(TemplateView):
    """
    Create LoginView
    """
    template_name = "auth/login.html"
    form_class = forms.CustomUserAuthenticationForm

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = self.form_class()
        return context

    def post(self, request):
        """
        :param request:
        :return:
        """
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
        # если невалидно — возвращаем ту же страницу с ошибками
        return self.render_to_response(self.get_context_data(form=form))


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Create ProfileDetailView
    """
    model = UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'
    login_url = '/register/'

    def get_object(self, queryset=None):
        """
        :param queryset:
        :return:
        """
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cart_count'] = get_cart_count(self.request)
        context['form'] = UserProfileForm(
            instance=self.get_object(),
            initial={
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'email': self.request.user.email,
            }
        )
        return context

    def post(self, request):
        """
        :param request:
        :return:
        """
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=self.get_object()
        )
        if form.is_valid():
            form.save()
            return redirect("/profile/")
        # если форма невалидна — рендерим шаблон с ошибками
        return render(request, self.template_name, {
            'profile': self.get_object(),
            'categories': Category.objects.all(),
            'form': form
        })


class CartItemView(View):
    """
    Create CartItemView
    """

    def get_queryset(self, request):
        """
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=request.user)

        return CartItem.objects.filter(
            cart__session_key=request.session.session_key
        )

    def post(self, request):
        """
        :param request:
        :return:
        """
        data = request.POST
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(
                user=request.user,
                defaults={'session_key': request.session.session_key}
            )
        else:
            cart, created = Cart.objects.get_or_create(
                session_key=request.session.session_key,
                defaults={'user': None}
            )

        if data.get('id'):
            cart_item = get_object_or_404(CartItem, pk=data.get('id'))
            cart_item.delete()
            return redirect(request.META.get('HTTP_REFERER', '/trash'))
        product_id = data.get('product')
        if not product_id:
            # можно вернуть ошибку или редирект
            return redirect(request.META.get('HTTP_REFERER', '/'))

        product = get_object_or_404(Product, id=product_id)
        quantity = int(data.get('quantity', 1))

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))

    def delete(self, request, **kwargs):
        """
        :param request:
        :param kwargs:
        :return:
        """
        pk = kwargs.get("pk")
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))

    def put(self, request, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk = kwargs.get("pk")
        cart_item = get_object_or_404(CartItem, pk=pk)
        quantity = request.POST.get("quantity")
        if quantity is None:
            raise ValueError("quantity is required")
        cart_item.quantity = int(quantity)
        cart_item.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class TrashView(TemplateView):
    """
    Create TrashView
    """
    template_name = "orders/trash.html"
    forms = forms.CustomOrderForm

    def get_context_data(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
        else:
            cart = Cart.objects.filter(
                session_key=self.request.session.session_key
            ).first()

        cart_items = CartItem.objects.filter(cart=cart) if cart else []
        context['categories'] = Category.objects.all()
        context['carts'] = cart_items
        context['cart_count'] = get_cart_count(self.request)
        context['forms'] = self.forms(
            initial={
                "first_name": self.request.user.first_name,
                "last_name": self.request.user.last_name,
                "email": self.request.user.email,
            }
        )

        if cart and cart_items.exists():
            context['cart_total_quantity'] = cart_items.aggregate(
                total_quantity=Sum('quantity')
            )['total_quantity']
            context['cart_total_price'] = sum(
                item.quantity * item.product.price for item in cart_items
            )
        else:
            context['cart_total_quantity'] = 0
            context['cart_total_price'] = 0
        return context


class OrderView(LoginRequiredMixin, CreateView):
    """
    Create OrderView
    """
    model = Order
    form_class = forms.CustomOrderForm
    template_name = 'index.html'  # укажите ваш шаблон

    def form_valid(self, form):
        """
        :param form:
        :return:
        """
        order = form.save(commit=False)
        order.user = self.request.user
        order.delivery_method = "New post"
        order.payment_method = "Card payment"
        order.total_amount = 0
        # Сохраняем заказ сначала, чтобы получить ID для OrderItem
        order.save()

        cart = Cart.objects.filter(user=order.user).first()
        total = 0

        if cart:
            for item in cart.items.all():
                total += item.quantity * item.product.price

                # Создаем OrderItem для каждого товара в корзине
                OrderItem.objects.create(
                    order=order,  # передаем объект order, а не item.objects
                    product=item.product,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity
                )

            cart.items.all().delete()
            cart.delete()

        order.total_amount = total
        order.save()

        return redirect(self.get_success_url())

    def get_success_url(self):
        """
        :return:
        """
        return self.request.META.get('HTTP_REFERER', '/')


def get_cart_count(request):
    """
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(
            session_key=request.session.session_key
        ).first()
    count = 0
    if cart:
        count = CartItem.objects.filter(cart=cart).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    return count


class ExportProductsView(APIView):
    """
    Create ExportProductsView
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        :param request:
        :return:
        """
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)