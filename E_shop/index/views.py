from django.shortcuts import render
from . import forms


# Create your views here.
# Отображение главной страницы
def home(request):
    search_bar = forms.SearchForm()
    # Отправить элементы на фронт
    context = {'form': search_bar}
    return render(request, 'home.html', context)


# Отображение страницы о нас
def about(request):
    return render(request, 'about.html')


# Отображение страницы с контактами
def contact(request):
    return render(request, 'contact.html')


# Поиск продуктов
def search_product(request):
    if request.method == 'POST':
        pass
