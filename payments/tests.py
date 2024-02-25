# import os
# import stripe

# stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
# stripe.PaymentIntent.create(
#   amount=5000,
#   currency="usd",
#   automatic_payment_methods={"enabled": True},
# )

#
# stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
# a = stripe.PaymentIntent.list(limit=3)
# print(a)