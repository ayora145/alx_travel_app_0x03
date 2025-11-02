from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(booking_id, user_email, booking_data=None):
    subject = 'Booking Confirmation'
    message = f'Your booking (ID: {booking_id}) has been confirmed. Thank you for choosing our service!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return True
