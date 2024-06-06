from django.urls import path
from .views import (ProductsList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete, subscriptions, index) # импортируем созданное нами представление
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('', cache_page(100)(ProductsList.as_view()), name='product_list'),
    path('', ProductsList.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('create/', ProductCreate.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('index/', index),
]

# <int:pk:> - мы хотим получить целочисленный идентификатор нашего продукта.