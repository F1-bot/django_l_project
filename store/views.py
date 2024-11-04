from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Monkey, Category, Cart, CartItem, Order, OrderItem
from .forms import AddToCartForm, CheckoutForm
from decimal import Decimal
from django.http import JsonResponse
import json
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


class HomeView(ListView):
    model = Monkey
    template_name = 'store/home.html'
    context_object_name = 'monkeys'
    paginate_by = 12

    def get_queryset(self):
        queryset = Monkey.objects.filter(available=True)
        category = self.request.GET.get('category')
        rarity = self.request.GET.get('rarity')
        search = self.request.GET.get('search')

        if category:
            queryset = queryset.filter(category__slug=category)
        if rarity:
            queryset = queryset.filter(rarity=rarity)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_monkeys'] = Monkey.objects.filter(
            available=True,
            rarity='legendary'
        )[:4]
        return context


class MonkeyDetailView(DetailView):
    model = Monkey
    template_name = 'store/monkey_detail.html'
    context_object_name = 'monkey'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddToCartForm()
        context['related_monkeys'] = Monkey.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context


class CartView(LoginRequiredMixin, ListView):
    template_name = 'store/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.cartitem_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context['total_quantity'] = cart.get_total_quantity()
        context['subtotal'] = cart.get_subtotal()
        context['fee'] = cart.get_fee()
        context['total'] = cart.get_total()
        return context


@require_POST
@login_required
def update_cart_item(request, item_id):
    try:
        data = json.loads(request.body)
        change = int(data.get('change', 0))

        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        new_quantity = cart_item.quantity + change

        if new_quantity > 0 and new_quantity <= 10:
            cart_item.quantity = new_quantity
            cart_item.save()

            cart = cart_item.cart
            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'item_subtotal': float(cart_item.get_subtotal()),
                'total_quantity': cart.get_total_quantity(),
                'subtotal': float(cart.get_subtotal()),
                'fee': float(cart.get_fee()),
                'total': float(cart.get_total())
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Недопустима кількість'
            })

    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Товар не знайдено'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@login_required
def add_to_cart(request, slug):
    monkey = get_object_or_404(Monkey, slug=slug)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1 or quantity > 10:
        messages.error(request, 'Недопустима кількість товару')
        return redirect('monkey_detail', slug=slug)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        monkey=monkey,
        defaults={'quantity': quantity}
    )

    if not created:
        # Якщо товар вже є в кошику, додаємо нову кількість
        cart_item.quantity = min(cart_item.quantity + quantity, 10)  # Обмежуємо максимум 10
        cart_item.save()

    messages.success(request, f"{monkey.name} додано до кошика!")
    return redirect('cart')


@require_POST
@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()

        return JsonResponse({
            'success': True,
            'total_quantity': cart.get_total_quantity(),
            'subtotal': float(cart.get_subtotal()),
            'fee': float(cart.get_fee()),
            'total': float(cart.get_total())
        })
    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Товар не знайдено'
        })


class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = CheckoutForm
    template_name = 'store/checkout.html'
    success_url = reverse_lazy('order_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context['cart_items'] = cart.cartitem_set.all()
        context['total_quantity'] = cart.get_total_quantity()
        context['subtotal'] = cart.get_subtotal()
        context['fee'] = cart.get_fee()
        context['total'] = cart.get_total()
        return context

    def form_valid(self, form):
        cart = Cart.objects.get(user=self.request.user)
        if not cart.cartitem_set.exists():
            messages.error(self.request, "Ваш кошик порожній")
            return redirect('cart')

        form.instance.user = self.request.user
        form.instance.total_price = cart.get_total()
        response = super().form_valid(form)

        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=self.object,
                monkey=cart_item.monkey,
                quantity=cart_item.quantity,
                price=cart_item.monkey.price
            )

        cart.cartitem_set.all().delete()
        messages.success(self.request, "Замовлення успішно оформлено!")
        return response

def order_success(request):
    return render(request, 'store/order_success.html')

class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'store/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'store/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracking'] = self.object.ordertracker_set.all()
        return context