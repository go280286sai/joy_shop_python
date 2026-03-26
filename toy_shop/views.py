from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, DetailView
from faker import Faker
import random
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from toy_shop.models import Brand, Category, Product, ProductImage, SlideImage, UserProfile
from . import forms
from django.contrib.auth import PermissionDenied

from .forms import UserProfileForm


# Create your views here.
class IndexView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        # возвращаем только продукты этой категории
        return Product.objects.order_by('-rating')[:15]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        context['slides'] = SlideImage.objects.all()
        return context


class CategoryView(ListView):
    model = Product
    template_name = 'category.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        # получаем категорию по slug
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        # возвращаем только продукты этой категории
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


class BrandView(ListView):
    template_name = 'brand.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        # сохраняем бренд в self.brand
        self.brand = get_object_or_404(Brand, slug=self.kwargs['brand_slug'])
        # возвращаем товары этого бренда
        return Product.objects.filter(brand=self.brand)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = self.brand
        context['categories'] = Category.objects.all()
        return context


class ProductView(TemplateView):
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        product_images = ProductImage.objects.filter(product=product)
        context['product'] = product
        context['categories'] = Category.objects.all()
        context['images'] = product_images
        return context


class TestView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'
    faker = Faker()

    def get(self, request, *args, **kwargs):
        categories = list(Category.objects.all())
        brands = list(Brand.objects.all())

        for i in range(1000):
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
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        return context


class LogoutView(TemplateView):
    redirect_url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.redirect_url)


class RegisterView(TemplateView):
    template_name = "auth/register.html"
    form = forms.StyledUserCreationForm()

    def post(self, request):
        data = forms.StyledUserCreationForm(request.POST)
        if data.is_valid():
            user = data.save()
            login(request, user)
        else:
            return HttpResponseRedirect('/')
        return request

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = self.form
        return context


class LoginView(TemplateView):
    template_name = "auth/login.html"
    form_class = forms.CustomUserAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
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
    model = UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'
    login_url = '/register/'

    def get_object(self, queryset=None):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = UserProfileForm(
            instance=self.get_object(),
            initial={
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
                'email': self.request.user.email,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
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


