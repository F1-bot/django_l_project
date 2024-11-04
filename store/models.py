from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Опис", blank=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Monkey(models.Model):
    RARITY_CHOICES = [
        ('common', 'Звичайна'),
        ('rare', 'Рідкісна'),
        ('epic', 'Епічна'),
        ('legendary', 'Легендарна'),
    ]

    name = models.CharField(max_length=200, verbose_name="Ім'я")
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='monkeys/', verbose_name="Зображення")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, verbose_name="Рідкісність")
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True, verbose_name="В наявності")

    class Meta:
        verbose_name = "Мавпочка"
        verbose_name_plural = "Мавпочки"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('monkey_detail', kwargs={'slug': self.slug})


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('crypto', 'Криптовалюта'),
        ('card', 'Банківська карта'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Очікує підтвердження'),
        ('processing', 'В обробці'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    first_name = models.CharField(max_length=100, verbose_name="Ім'я")
    last_name = models.CharField(max_length=100, verbose_name="Прізвище")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адреса")
    city = models.CharField(max_length=100, verbose_name="Місто")
    postal_code = models.CharField(max_length=10, verbose_name="Поштовий індекс")
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='crypto',
        verbose_name="Спосіб оплати"
    )
    items = models.ManyToManyField('Monkey', through='OrderItem', verbose_name="Товари")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Загальна сума"
    )

    @property
    def fee(self):
        return self.total_price * Decimal('0.01')  # 1% комісія

    def __str__(self):
        return f'Замовлення #{self.id} від {self.user.username}'

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def get_status_color(self):
        status_colors = {
            'pending': 'warning',  # жовтий
            'processing': 'info',  # синій
            'completed': 'success',  # зелений
            'cancelled': 'danger',  # червоний
            'shipped': 'primary'  # голубий
        }
        return status_colors.get(self.status, 'secondary')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    monkey = models.ForeignKey(Monkey, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.monkey.name} в замовленні {self.order.id}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Monkey', through='CartItem')
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_quantity(self):
        return sum(item.quantity for item in self.cartitem_set.all())

    def get_subtotal(self):
        return sum(item.get_subtotal() for item in self.cartitem_set.all())

    def get_fee(self):
        return Decimal('0.01') * self.get_subtotal()  # 1% комісія

    def get_total(self):
        return self.get_subtotal() + self.get_fee()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    monkey = models.ForeignKey(Monkey, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_subtotal(self):
        return self.monkey.price * self.quantity

class OrderTracker(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує обробки'),
        ('processing', 'Обробляється'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано')
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']