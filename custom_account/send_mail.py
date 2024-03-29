from django.core.mail import send_mail


def send_confirmation_email(code, email):
    """
    function for send message
    """
    full_link = f"http://localhost:8000/custom_account/activate/{code}"

    send_mail(
        'Activation code for Tutorial_v2',
        full_link,
        'info@codingsolutionedu.com',
        [email]
    )