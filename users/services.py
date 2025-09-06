from decimal import Decimal

import stripe
from django.urls import reverse_lazy
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_usd(amount):
    """Конвертируем рубли в доллары"""

    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return Decimal(float(amount) * rate)


def create_stripe_product(name="Product"):
    """Создаем продукт в страйпе"""

    return stripe.Product.create(name=name)


def create_stripe_price(amount, product):
    """Создаем цену в страйпе"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=int(amount * 100),
        product=product.id,
    )


def create_stripe_session(price):
    """Создаем сессию на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url=reverse_lazy("materials:courses"),
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
