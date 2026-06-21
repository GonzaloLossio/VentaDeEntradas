import stripe
from app.core.config import settings

stripe.api_key = settings.stripe_secret_key

async def create_payment_intent(amount: float , currency : str = "usd") -> dict:
    payment_intent = stripe.PaymentIntent.create(
        amount = int(amount*100),
        currency = currency,
        payment_method_types=["card"]
    )
    return {
        "payment_intent_id": payment_intent.id,
        "client_secret": payment_intent.client_secret
    }