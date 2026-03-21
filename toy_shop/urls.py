from django.urls import path

from toy_shop import views

urlpatterns = [
    path('', views.index, name='index'),
]