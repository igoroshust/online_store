from django.urls import path, include
from rest_framework import routers

from .views import (ProductViewset, CategoryViewset, ProductsList, ProductDetail, ProductCreate, ProductUpdate,
                    ProductDelete, subscriptions, UserViewSet)  # импортируем созданное нами представление
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # path('', cache_page(100)(ProductsList.as_view()), name='product_list'),
    path('', ProductsList.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('create/', ProductCreate.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('api/', include(router.urls)),
    # path('swagger-ui/', TemplateView.as_view(
    #     template_name='swagger-ui.html',
    #     extra_context={'schema_url': 'openapi-schema'}),
    #      name='swagger-ui'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('index/', Index.as_view()), # тест локализации
]

# <int:pk:> - мы хотим получить целочисленный идентификатор нашего продукта.