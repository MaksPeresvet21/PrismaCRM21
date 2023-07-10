from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('products/', views.products, name="products"),
    path('create_product/', views.create_product, name="create_product"),
    path('update_product/<str:pk>/', views.update_product, name="update_product"),
    path('delete_product/<str:pk>/', views.delete_product, name="delete_product"),
    path('orders/', views.orders, name="orders"),
    path('create_order/', views.create_order, name="create_order"),
    path('delete_order/<str:pk>', views.delete_order, name="delete_order"),
    path('contacts/', views.contacts, name="contacts"),
    path('customer_orders/<str:pk>/', views.customer_orders, name="customer_orders"),
    path('seller_orders/<str:pk>/', views.seller_orders, name="seller_orders"),
    path('add_seller/', views.add_seller, name='add_seller'),
    path('delete_seller/<str:pk>/', views.delete_seller, name="delete_seller"),
    path('create_ttn/', views.create_ttn, name='create_ttn'),
    path('get_ttn/', views.get_ttn, name='get_ttn'),
    path('update_status/', views.update_status, name="update_status"),
    path('analysis/', views.analysis, name='analysis'),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),

]
