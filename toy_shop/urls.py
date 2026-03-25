from django.urls import path
from django.contrib.auth import logout
from toy_shop import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<slug:category_slug>/', views.CategoryView.as_view(), name='category'),
    path('brand/<slug:brand_slug>/', views.BrandView.as_view(), name='brand'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("test/", views.TestView.as_view(), name='test'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path("login/", views.LoginView.as_view(), name='login'),

]
