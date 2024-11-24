import stripe
from config.settings import STRIPE_API_KEY
from materials.models import Course
from users.models import Payment

stripe.api_key = STRIPE_API_KEY


def create_product(course_id):
    product = Course.objects.get(id=course_id)
    return stripe.Product.create(name=product.name)


def create_stripe_price(amount, product_name):

    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": product_name},
    )

    return price


def create_stripe_session(price_id):

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )

    return session.get('id'), session.get("url")

# доп. задание
def retrieve_stripe_session(session_id):
    return stripe.checkout.Session.retrieve(
      session_id,
    )




