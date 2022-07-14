from django.core.mail import send_mail


def send_confirmation_email(code, email):
    full_link = f"http://localhost:8000/account/activate/{code}"

    send_mail(
        'Активационный код для Tutorial_v2',
        full_link,
        'bekbol.2019@gmail.com',
        [email]
    )