from django.dispatch import receiver

# from decouple import config
from django_rest_passwordreset.signals import reset_password_token_created

from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # FRONT_END_HOST = config("FRONT_END_HOST", default="http://localhost:8082")
    FRONT_END_HOST="http://localhost:8000"
    message = f"""To reset password for your {reset_password_token.user.email} Account,
    Click the link below:
    {FRONT_END_HOST}/reset-password/{reset_password_token.key}/
    If clicking the link above doesn't work, please copy and paste the URL in a new browser window instead.
    Sincerely,
    Uniladder Consultancy
    """
    send_mail(
        subject="Password Reset for {title}".format(title="Mocking Bird"),
        message=message,
        from_email="",
        recipient_list=[reset_password_token.user.email],
    )