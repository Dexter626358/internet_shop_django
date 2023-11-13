from django.http import HttpResponse
import logging
from django.shortcuts import render, get_object_or_404
from .models import Client, ClientRegistrationForm
from .models import Order, OrderProduct
from .models import Product
from django.shortcuts import HttpResponse
from faker import Faker
from .models import Product
from django.shortcuts import render, redirect
from django import forms
from .models import Client

logger = logging.getLogger(__name__)


def welcome_view(request):
    logger.info('Welcome page accessed')
    content = {
        "greetings": "Добро пожаловать в наш интренет-магазин!"
    }
    return render(request, 'store/base.html', context=content)


def contacts(request):
    contact = {
        'name': 'Виртуальный магазинчик',
        'Email': 'hello@virtualmart.com',
        'adress': 'Ул. Виртуальная, д. 456, Город, Страна',
    }
    return render(request, 'store/contacts.html', context=contact)


def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            content = {
                "success": "Вы успешно прошли регистрацию на сайте"
            }
            return render(request, 'store/success_registration.html',
                          context=content)  # Перенаправление на страницу успешной регистрации
    else:
        form = ClientRegistrationForm()
    return render(request, 'store/register_client.html', {'form': form})


# Создание клиента
def create_client(name, email, phone_number, address):
    client = Client.objects.create(
        name=name,
        email=email,
        phone_number=phone_number,
        address=address
    )
    return client


# Получение всех клиентов
def get_all_clients(request):
    clients = Client.objects.all()
    return render(request, 'store/all_clients.html', {'clients': clients})


# Получение клиента по ID

def search_client_by_id(request, client_id):
    if request.method == 'GET':
        try:
            client = Client.objects.get(id=client_id)
            return render(request, 'store/client_details.html', {'client': client})
        except Client.DoesNotExist:
            error_message = f"Клиент с ID {client_id} не найден."
            return render(request, 'store/error.html', {'store/error_message': error_message})
    return render(request, 'store/search_client.html')


# Удаление клиента
def delete_client(request, client_id):
    if request.method == 'GET':
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            content = {
                "greetings": "Клиент успешно удален"
            }
            return render(request, 'store/delete_client.html', context=content)
        except Client.DoesNotExist:
            error_message = f"Клиент с ID {client_id} не найден."
            return render(request, 'store/error.html', {'store/error_message': error_message})
    return render(request, 'store/search_client.html')


# Создание заказа
def create_order(client, products, total_amount):
    order = Order.objects.create(client=client, total_amount=total_amount)
    for product in products:
        OrderProduct.objects.create(order=order, product=product['product'], quantity=product['quantity'])
    return order


# Получение всех заказов
def get_all_orders():
    return Order.objects.all()


# Получение заказа по ID
def get_order_by_id(order_id):
    return Order.objects.get(id=order_id)


# Обновление информации о заказе
def update_order_info(order_id, client=None, products=None, total_amount=None):
    order = get_order_by_id(order_id)
    if client:
        order.client = client
    if total_amount:
        order.total_amount = total_amount
    if products:
        OrderProduct.objects.filter(order=order).delete()
        for product in products:
            OrderProduct.objects.create(order=order, product=product['product'], quantity=product['quantity'])
    order.save()
    return order


# Удаление заказа
def delete_order(order_id):
    order = get_order_by_id(order_id)
    order.delete()


# Создание товара
def create_product(name, description, price, quantity):
    product = Product.objects.create(
        name=name,
        description=description,
        price=price,
        quantity=quantity
    )
    return product


# Получение всех товаров
def get_all_products(request):
    products = Product.objects.all()
    return render(request, 'store/all_products.html', {'products': products})


# Получение товара по ID
def get_product_by_id(product_id):
    return Product.objects.get(id=product_id)


# Обновление информации о товаре
def update_product_info(product_id, name=None, description=None, price=None, quantity=None):
    product = get_product_by_id(product_id)
    if name:
        product.name = name
    if description:
        product.description = description
    if price:
        product.price = price
    if quantity:
        product.quantity = quantity
    product.save()
    return product


# Удаление товара
def delete_product(product_id):
    product = get_product_by_id(product_id)
    product.delete()


def generate_fake_products(request):
    fake = Faker()

    for _ in range(10):  # Создание 10 фейковых товаров
        name = fake.word()
        description = fake.text()
        price = fake.random_number(4, True)  # Случайная цена от 0 до 9999
        quantity = fake.random_int(0, 100)
        added_date = fake.date_this_decade()  # Дата в пределах последнего 10-летия

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            added_date=added_date
        )
        product.save()
    content = {
        "greetings": "Фейковые товары были добавлены в базу данных."
    }
    return render(request, 'store/fake_products.html', context=content)


def generate_fake_clients(request):
    fake = Faker()

    for _ in range(10):  # Создание 10 фейковых клиентов
        name = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()
        address = fake.address()
        registration_date = fake.date_this_decade()

        client = Client.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            registration_date=registration_date
        )
        client.save()
    content = {
        "greetings": "Фейковые клиенты были добавлены в базу данных."
    }

    return render(request, 'store/fake_clients.html', context=content)
