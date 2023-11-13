from django.urls import path
from .views import welcome_view, get_all_clients, delete_client, \
    create_order, get_all_orders, get_order_by_id, update_order_info, delete_order, create_product, get_all_products, \
    get_product_by_id, update_product_info, delete_product, contacts, generate_fake_products, generate_fake_clients, \
    register_client, search_client_by_id

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('contacts/', contacts, name='get_contacts'),
    path('fake/product', generate_fake_products, name='fake_products'),
    path('fake/client', generate_fake_clients, name='fake_clients'),
    path('registr/', register_client, name='create_client'),
    path('clients/', get_all_clients, name='get_all_clients'),
    path('client/<int:client_id>/', search_client_by_id, name='get_client_by_id'),
    path('client/delete/<int:client_id>/', delete_client, name='delete_client'),

    # path('order/create/', create_order, name='create_order'),
    # path('orders/', get_all_orders, name='get_all_orders'),
    # path('order/<int:order_id>/', get_order_by_id, name='get_order_by_id'),
    # path('order/update/<int:order_id>/', update_order_info, name='update_order_info'),
    # path('order/delete/<int:order_id>/', delete_order, name='delete_order'),

    # path('product/create/', create_product, name='create_product'),
    path('products/', get_all_products, name='get_all_products'),
    # path('product/<int:product_id>/', get_product_by_id, name='get_product_by_id'),
    # path('product/update/<int:product_id>/', update_product_info, name='update_product_info'),
    # path('product/delete/<int:product_id>/', delete_product, name='delete_product'),
    # другие URL-маршруты и представления
]
