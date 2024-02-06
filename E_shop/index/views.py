from django.shortcuts import render, redirect
from . import forms, models
from .models import Product, Category, Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .handlers import bot


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
    return render(request, 'index.html', context)


# Вывод товаров по категории
def get_full_category(request, pk):
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(category_name=category)
    # Отправить данные на фронт
    context = {'products': products}
    return render(request, 'exact_category.html', context)


# Вывод товаров о конкретном продукте
def get_full_product(request, pk):
    product = Product.objects.get(id=pk)
    # Отправить данные на фронт
    context = {'product': product}
    return render(request, 'exact_product.html', context)


# Отображение страницы о нас
def about(request):
    return render(request, 'about.html')


# Отображение страницы с контактами
def contact(request):
    return render(request, 'contact.html')


# Поиск продуктов
def search_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')
        try:
            exact_product = Product.objects.get(pr_name__icontains=get_product)
            return redirect(f'/product/{exact_product.id}')
        except:
            return redirect('/product_not_found')


def pr_not_found(request):
    return render(request, 'not_found.html')


# Добавление товара в корзину
def add_to_cart(request, pk):
    if request.method == 'POST':
        checker = Product.objects.get(id=pk)
        if checker.pr_count >= int(request.POST.get('pr_amount')):
            Cart.objects.create(user_id=request.user.id,
                                user_product=checker,
                                user_product_quantity=int(request.POST.get('pr_amount'))).save()
            # new_pr_amount = Product.objects.get(pr)
            # new_pr_amount -= int(request.POST.get('pr_amount')).save()

            return redirect('/')


# Отображение корзины пользователя
def get_user_cart(request):
    # Вся инфа о корзине пользователя
    cart = Cart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        text = 'Новый заказ!\n\n'

        for i in cart:
            text += f'Название товара: {i.user_product}\n' \
                    f'Количество: {i.user_product_quantity}\n\n'
        bot.send_message(-4104295979, text)
        cart.delete()
        return redirect('/')

    # Отправить данные на фронт
    context = {'cart': cart}
    return render(request, 'user_cart.html', context)


# Удаления товара из корзины
def del_from_cart(request, pk):
    product_to_delete = Product.objects.get(id=pk)
    Cart.objects.filter(user_id=request.user.id,
                        user_product=product_to_delete).delete()

    return redirect('/cart')


# Регистрация
class Register(View):
    template_name = 'registration/register.html'

    # Отправка формы регистрации
    def get(self, request):
        context = {'form': UserCreationForm}
        return render(request, self.template_name, context)

        # Добавление в БД
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        context = {'form': UserCreationForm}
        return render(request, self.template_name, context)


# Функция для logout
def logout_view(request):
    logout(request)
    return redirect('/')
