from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.db.models import F

from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
            else:
                # formset = OrderFormSet()
                formset = OrderFormSet(instance=self.object)
                for form in formset.forms:
                    if form.instance.pk:
                        form.initial['price'] = form.instance.product.price

        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():  # Применяется, когда есть 2 save, чтобы избежать ошибок. Проходит проверка на
            # выполнение двух save, если выполняется только один save то, вообще ничего не сохраняется
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():  # применяется, когда есть 2 save, чтобы избежать ошибок
            Basket.objects.filter(user=self.request.user).delete()
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                print(orderitems)
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderReadView(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderReadView, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order:list')


def order_forming_complete(request, pk):
    order = Order.objects.get(pk=pk)
    order.status = Order.STATUS_SEND_TO_PROCEED
    Basket.objects.filter(user=request.user)
    order.save()
    return HttpResponseRedirect(reverse('order:list'))


# Ниже описан такой инструмент оптимизации как Сигналы
@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - instance.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
#


def get_product_price(request, pk):
    if request.is_ajax():
        product_item = Product.objects.filter(pk=pk).first()
        if product_item:
            return JsonResponse({'price': product_item.price})
        return JsonResponse({'price': 0})
