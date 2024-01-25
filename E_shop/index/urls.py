from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about-us', views.about),
    path('contact-us', views.contact),
    path('search', views.search_product),
    path('category/<int:pk>', views.get_full_category),
    path('product/<int:pk>', views.get_full_product),
    path('product_not_found', views.pr_not_found),
]
