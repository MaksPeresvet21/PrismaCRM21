from django.shortcuts import render, redirect
from .filters import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
import datetime
from django.http import JsonResponse
from django.urls import reverse
import re

status_codes = ['102', '103', '111', '105', '2', '3']

def home(request):
    if request.user.groups.filter(name='hometown').exists():
        return redirect('dashboard')
    else:
        return redirect('orders')

@login_required
def dashboard(request):
    orders = Order.objects.all()
    recent_orders = orders.order_by('-date_created')[:5]
    current_page = 'dashboard'
    context = {'orders': orders, 'status_codes': status_codes, 'recent_orders': recent_orders, 'current_page': current_page}
    return render(request, 'crm/dashboard.html', context)

def get_ttn(request):
    ttn_total = Order.objects.filter(status__in=['Предоплата', 'Повна Оплата']).count()
    return JsonResponse({'ttn_total': ttn_total})

@login_required
def products(request):
    current_page = "products"
    products = Product.objects.order_by("-date_created")
    pf = ProductFilter(request.GET, queryset=products)
    products = pf.qs
    return render(request,'crm/products.html',{'products':products, 'pf': pf, 'current_page': current_page})

@login_required
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def update_product(request, pk):
    from_url = reverse('update_product', args=[pk])
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    context = {'form': form, 'from_url': from_url}
    return render(request, 'crm/form_page.html', context)

@login_required
def create_product(request):
    form = ProductForm()
    from_url = reverse('create_product')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    context = {'form': form, 'from_url': from_url}
    return render(request, 'crm/form_page.html', context)


@login_required
def orders(request):
    current_page = "orders"
    if request.user.groups.filter(name='hometown').exists():
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(seller_id=request.user.id)
    orders = orders.order_by("-date_created")
    total_margin = sum([o.margin for o in orders])
    total_amount = sum([o.amount for o in orders])
    total_orders = orders.count()
    context = {'orders':orders, 'total_margin': total_margin, 'total_amount': total_amount,
                'total_orders': total_orders, 'current_page': current_page, 'status_codes': status_codes}
    return render(request, 'crm/orders.html', context)


@login_required
def create_order(request):
    form = Form()
    from_url = reverse("create_order")
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.seller = request.user
            order.save()
            form.save_m2m()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_text()
            errors = re.sub(r'\*\s*__all__\s*\*', '', errors)
            return JsonResponse({'success': False, 'errors': errors})
    context = {'form': form, 'from_url': from_url}
    return render(request, 'crm/form_page.html', context)


@login_required
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def contacts(request):
    current_page = "contacts"
    req = request.GET.get('search', None)
    if request.user.groups.filter(name='hometown').exists():
        customer = Customer.objects.all()
    else:
        customer = Customer.objects.filter(seller_id=request.user.id)
    if req is not None:
        query = request.GET.get('search')
        customer = customer.filter(Q(name__icontains=query) | Q(phone__icontains=query))
    else:
        customer = customer.all()
    customers = customer.order_by("-date_created")
    sellers = Seller.objects.order_by("-date_joined")
    context = {'customers':customers, 'sellers': sellers, 'current_page': current_page}
    return render(request,'crm/contacts.html', context)

@login_required
def customer_orders(request, pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    context = {'customer': customer, 'order': order, 'status_codes': status_codes}
    return render(request,'crm/customer_orders.html', context)


@login_required
def seller_orders(request, pk):
    current_page = "orders"
    seller = Seller.objects.get(id=pk)
    orders = Order.objects.filter(seller=seller)
    if request.method == 'POST' and 'cancel' in request.POST:
            orders = orders.filter(status_code__in=status_codes)
    if request.GET.get('refresh') == 'true':
        return redirect('seller_orders', pk=pk)
    total_margin = sum([o.margin for o in orders])
    total_amount = sum([o.amount for o in orders])
    total_orders = orders.count()
    context = {'seller': seller, 'orders': orders, 'current_page': current_page,
               'total_orders': total_orders, 'total_margin': total_margin,
               'status_codes': status_codes, 'total_amount': total_amount}
    return render(request, 'crm/orders.html', context)

@login_required
def add_seller(request):
    form = SellerForm()
    from_url = reverse('add_seller')
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_text()
            errors = re.sub(r'\*\s*(username|password2)\s*\*', '', errors)
            return JsonResponse({'success': False, 'errors': errors})
    context = {'form': form, 'from_url': from_url}
    return render(request, "crm/form_page.html", context)

def delete_seller(request, pk):
    contact = Seller.objects.get(id=pk)
    contact.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def analysis(request):
    current_page = "analysis"
    if request.method == 'POST' and 'cancel' in request.POST:
        orders = Order.objects.filter(status_code__in=status_codes)
    else:
        orders = Order.objects.all()
    orders_sum = int(sum([o.amount * o.product.cost for o in orders]))
    total_amount = sum([o.amount for o in orders])
    total_orders = orders.count()
    recent_orders = orders.order_by('-date_created')[:5]
    context = {'orders_sum': orders_sum,  'status_codes': status_codes, 'products': products,
               'recent_orders': recent_orders, 'total_amount': total_amount,
               'total_orders': total_orders, 'current_page': current_page}
    return render(request, 'crm/analysis.html', context)



#Розрахунок об'єму для ваги
def calculate_weight_volume(quantity):
    if quantity == 1:
        volume = "0.005"
    elif quantity == 2:
        volume = "0.01"
    else:
        volume = "0.02"
    return volume

def create_ttn(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        now_datetime = datetime.datetime.now().strftime('%d.%m.%Y')
        address = re.search(r'(?P<city_type>м\.|смт\.?|с\.?)?\s*(?P<city>[^,]+),?\s*(?P<region>[^,]*?)(?: р-н| міськрада)?,?\s*(?P<area>[^,]+)?\s*обл\.', order.city_client)
        url = 'https://api.novaposhta.ua/v2.0/json/'
        data = {
            "apiKey": "your APi",
            "modelName": "InternetDocument",
            "calledMethod": "save",
            "methodProperties": {
                "PayerType": "Recipient",
                "PaymentMethod": "Cash",
                "DateTime": now_datetime,
                "CargoType": "Cargo",
                "Weight": order.actual_weight,
                "VolumeGeneral": calculate_weight_volume(int(order.actual_weight)),
                "ServiceType": "WarehouseWarehouse",
                "SeatsAmount": "1",
                "Description": "Одяг",
                "Cost": "",
                "CitySender": "e71f8e8f-4b33-11e4-ab6d-005056801329",
                "Sender": "1c95f620-f648-11e8-8b24-005056881c6b",
                "SenderAddress": "1b77ddbc-cc01-11ea-b39d-b8830365bd14",
                "ContactSender": "061bfc58-f6ca-11e8-8b24-005056881c6b",
                "SendersPhone": "380986337369",
                "RecipientsPhone": order.phone_client,
                "NewAddress": "1",
                "RecipientCityName": address.group('city'),
                "RecipientArea": address.group('area'),
                "RecipientAreaRegions": address.group('region'),
                "RecipientAddressName": re.search(r'№(\d+)', order.dep_np).group(1),
                "RecipientHouse": "",
                "RecipientFlat": "",
                "RecipientName": order.name_client,
                "RecipientType": "PrivatePerson",
                "SettlementType": address.group('city_type'),
                "EDRPOU": ""
            },
        }
        if order.status == 'Предоплата':
            backward_delivery = {
                "PayerType": "Recipient",
                "CargoType": "Money",
                "RedeliveryString": str(int(order.sum) - 150)
            }
            data["methodProperties"]["BackwardDeliveryData"] = [backward_delivery]
        response = requests.post(url, json=data)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['success']:
                order.number_ttn = response_json['data'][0]['IntDocNumber']
                order.save()
                return JsonResponse({'success': True, 'data': order.number_ttn})
            else:
                errors = response_json.get('errors', [])
                return JsonResponse({'success': False, 'errors': errors}, status=400)

        else:
            return JsonResponse({'success': False, 'errors': ["Ошибка соединения"]}, status=500)


def update_status(request):
    if request.method == 'POST':
        orders = Order.objects.order_by('-id')[:100]
        numbers_ttn = [order.number_ttn for order in orders if order.number_ttn and order.status_code not in ['2', '9', '10', '106']]

        if numbers_ttn:
            url = 'https://api.novaposhta.ua/v2.0/json/'
            data = {
                "apiKey": "your APi",
                "modelName": "TrackingDocument",
                "calledMethod": "getStatusDocuments",
                "methodProperties": {
                    "Documents": [{"DocumentNumber": number} for number in numbers_ttn]
                }
            }
            response = requests.post(url, json=data)

            if response.status_code == 200:
                response_json = response.json()
                if response_json['success']:
                    for i, order in enumerate(orders):
                        if order.number_ttn:
                            status = response_json['data'][i]['Status']
                            status_code = response_json['data'][i]['StatusCode']
                            order.status = status
                            order.status_code = status_code
                            order.save()
                    return JsonResponse({'success': True})

        return JsonResponse({'success': False})


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"Нікнейм або пароль не вірний.")
    return render(request, 'crm/signin.html', {})

def signout(request):
    logout(request)
    return redirect('signin')






