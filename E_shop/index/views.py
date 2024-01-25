from django.shortcuts import render, redirect
from . import forms, models
from .models import Product, Category, Cart


# Create your views here.
# Отображение главной страницы
def home(request):
    # Поисковая строка
    search_bar = forms.SearchForm()
    # Собираем все продукты
    product_info = Product.objects.all()
    # Собираем все категории товаров
    category_info = Category.objects.all()
    # Отправить элементы на фронт
    context = {'form': search_bar,
               'product': product_info,
               'category': category_info}
    return render(request, 'home.html', context)


# Вывод товаров по категории
def get_full_category(request, pk):
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(category_name=category)
    # Отправить данные на фронт
    context = {'products': products}
    return render(request, 'category.html', context)


# Вывод товаров о конкретном продукте
def get_full_product(request, pk):
    product = Product.objects.get(id=pk)
    # Отправить данные на фронт
    context = {'product': product}
    return render(request, 'product.html', context)


# Отображение страницы о нас
def about(request):
    return render(request, 'about.html')


# Отображение страницы с контактами
def contact(request):
    return render(request, 'contact.html')


# Поиск продуктов
def search_product(request):
    if request.method == 'POST':
        get_product = request.post.get('search_product')
        try:
            exact_product = Product.objects.get(product_name__icontains=get_product)
            return redirect(f'product/{exact_product.id}')
        except:
            return redirect('/pr-not-found')


def pr_not_found(request):
    return render(request, 'not_found.html')
