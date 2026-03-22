from django.urls import path

from toy_shop import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]