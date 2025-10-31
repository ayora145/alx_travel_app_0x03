# ALX Travel App 0x02 - Chapa Payment Integration

This project integrates the Chapa Payment Gateway into a Django travel booking system.

## Features
- Secure payment initiation using Chapa API
- Verification of payment status
- Payment tracking model
- Asynchronous email confirmation via Celery
- Sandbox testing environment

## Setup
1. Create a `.env` file with:
```
CHAPA_SECRET_KEY=your_key_here
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start Celery:
```bash
celery -A alx_travel_app worker --loglevel=info
```

5. Start Django server and test:
```bash
python manage.py runserver
```

## API Endpoints
- `GET /api/listings/` - List all listings
- `POST /api/listings/` - Create new listing
- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create new booking
- `POST /api/initiate-payment/` - Initiate payment
- `GET /api/verify-payment/` - Verify payment

## Testing
Use Postman to test endpoints at `http://127.0.0.1:8000/api/`
## Celery + RabbitMQ Configuration (Milestone 5)

Files added/modified:
- alx_travel_app/celery.py
- alx_travel_app/__init__.py
- alx_travel_app/settings.py (added CELERY_ and EMAIL_ settings)
- listings/tasks.py (send_booking_confirmation_email task)
- listings/views.py (BookingViewSet triggers task)

To run locally:
1. Install RabbitMQ: `sudo apt install rabbitmq-server`
2. Start RabbitMQ: `sudo systemctl start rabbitmq-server`
3. Start Django server: `python manage.py runserver`
4. Start Celery worker: `celery -A alx_travel_app worker --loglevel=info`
5. Create a booking via POST /api/bookings/ - email task will be processed asynchronously

Repository: alx_travel_app_0x03
