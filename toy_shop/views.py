from django.shortcuts import render

from toy_shop.models import Brand


# Create your views here.
def index(request):
    brands = Brand.objects.all()
    print(brands)
    return render(request, 'index.html', {'brands': brands})
