from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_token(user):
    token = default_token_generator.make_token(user)
    return token 

def send_verification_email(user, verification_token):
    base_url = 'https://localhost:8000'  # Replace with your application's base URL
    verification_url = f'{base_url}/verify/{verification_token}'

    subject = 'Verify your email'
    message = f'Click the following link to verify your email: {verification_url}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    send_mail(subject, message, from_email, [to_email])
