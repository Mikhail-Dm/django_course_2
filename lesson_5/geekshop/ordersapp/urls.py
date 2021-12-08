from django.urls import path

from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='list'),
    path('create/', ordersapp.OrderCreateView.as_view(), name='create'),
    path('read/<pk>/', ordersapp.OrderReadView.as_view(), name='read'),
    path('update/<pk>/', ordersapp.OrderUpdateView.as_view(), name='update'),
    path('delete/<pk>/', ordersapp.OrderDeleteView.as_view(), name='delete'),
    path('cancel/forming/<pk>/', ordersapp.order_forming_complete, name='forming_cancel'),
    path('product/price/<int:pk>/', ordersapp.get_product_price, name='get_product_price'),
]