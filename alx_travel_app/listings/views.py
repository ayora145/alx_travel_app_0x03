from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation_email
import requests
import uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        
        # Get user email - use a default if not available
        user_email = 'test@example.com'
        if hasattr(request.user, 'email') and request.user.email:
            user_email = request.user.email
        elif 'email' in request.data:
            user_email = request.data['email']
            
        # Trigger background email task
        send_booking_confirmation_email.delay(booking.id, user_email)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        data = request.POST
        amount = data.get('amount')
        email = data.get('email')

        if not amount or not email:
            return JsonResponse({"error": "Amount and email are required"}, status=400)

        booking_reference = str(uuid.uuid4())
        Payment.objects.create(
            booking_reference=booking_reference,
            amount=amount,
            email=email,
            transaction_id=booking_reference,
            status='Pending'
        )
        return JsonResponse({
            "checkout_url": f"http://127.0.0.1:8000/mock-payment/{booking_reference}/",
            "booking_reference": booking_reference
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def verify_payment(request):
    if request.method == 'GET':
        tx_ref = request.GET.get('tx_ref')
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            payment.status = 'Completed'
            payment.save()
            return JsonResponse({"message": "Payment verified successfully"})
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Transaction not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)
