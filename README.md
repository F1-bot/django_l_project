# 🚀 Космічні Мавпочки - NFT Маркетплейс

Веб-додаток для купівлі та колекціонування унікальних NFT космічних мавпочок з використанням Django.

## 📋 Опис проєкту

Космічні Мавпочки - це маркетплейс NFT, де користувачі можуть:
- Переглядати колекції унікальних NFT мавпочок
- Фільтрувати за категоріями та рідкістю
- Додавати товари до кошика
- Оформлювати замовлення
- Відстежувати статус замовлень
- Оплачувати криптовалютою або банківською картою

## 🛠 Технології

- Python 3.10+
- Django 5.1.2
- Bootstrap 5
- SQLite
- Crispy Forms
- Font Awesome
- JavaScript

## 🚀 Встановлення та запуск

1. Клонуйте репозиторій:
```bash
git clone https://github.com/username/space-monkeys.git
cd space-monkeys
```

2. Створіть та активуйте віртуальне середовище:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/MacOS
python -m venv venv
source venv/bin/activate
```

3. Встановіть залежності:
```bash
pip install -r requirements.txt
```

4. Виконайте міграції:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Створіть суперкористувача:
```bash
python manage.py createsuperuser
```

6. Запустіть сервер:
```bash
python manage.py runserver
```

7. Відкрийте http://127.0.0.1:8000/ у браузері

## 📁 Структура проєкту

```
space_monkeys/
├── monkey_store/          # Основний проєкт Django
│   ├── settings.py        # Налаштування проєкту
│   ├── urls.py           # Головні URL-патерни
│   └── wsgi.py           # WSGI конфігурація
├── store/                 # Додаток магазину
│   ├── models.py         # Моделі даних
│   ├── views.py          # Представлення
│   ├── urls.py           # URL-патерни магазину
│   ├── forms.py          # Форми
│   └── admin.py          # Налаштування адмін-панелі
├── templates/            # HTML шаблони
├── static/               # Статичні файли
│   ├── css/             # CSS стилі
│   ├── js/              # JavaScript файли
│   └── images/          # Зображення
├── media/               # Завантажені файли
├── requirements.txt     # Залежності проєкту
└── manage.py           # Утиліта керування Django
```

## 🌟 Основні функції

- Перегляд каталогу NFT мавпочок
- Фільтрація за категоріями та рідкістю
- Система кошика
- Оформлення замовлень
- Система відстеження статусу замовлень
- Адмін-панель для керування товарами
- Підтримка різних способів оплати
- Адаптивний дизайн
