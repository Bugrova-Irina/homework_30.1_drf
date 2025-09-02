from decimal import Decimal

import stripe

from config.settings import STRIPE_API_KEY
from forex_python.converter import CurrencyRates

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_usd(amount):
    """ Конвертируем рубли в доллары """

    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return Decimal(float(amount) * rate)


def create_stripe_product(name="Product"):
    """ Создаем продукт в страйпе """

    return stripe.Product.create(name=name)


def create_stripe_price(amount, product):
    """ Создаем цену в страйпе """

    return stripe.Price.create(
        currency="usd",
        unit_amount=int(amount * 100),
        product = product.id,
    )


def create_stripe_session(price):
    """ Создаем сессию на оплату в страйпе """

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment"
    )
    return session.id, session.url
