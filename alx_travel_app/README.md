# ALX Travel App 0x03 - Background Jobs with Celery

This project integrates Celery with RabbitMQ for background task processing in a Django travel booking system.

## Features
- Secure payment initiation using Chapa API
- Verification of payment status
- Payment tracking model
- Asynchronous email confirmation via Celery
- RabbitMQ message broker integration
- Background task processing

## Setup
1. Install RabbitMQ:
```bash
sudo apt install rabbitmq-server
```

2. Start RabbitMQ:
```bash
sudo systemctl start rabbitmq-server
```

3. Create a `.env` file with:
```
CHAPA_SECRET_KEY=your_key_here
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start Celery worker:
```bash
celery -A alx_travel_app worker --loglevel=info
```

7. Start Django server:
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
## Background Task Processing

This project implements asynchronous email notifications using Celery with RabbitMQ as the message broker.

### Key Components:
- **alx_travel_app/celery.py** - Celery configuration
- **alx_travel_app/__init__.py** - Celery app initialization
- **alx_travel_app/settings.py** - Celery and email settings
- **listings/tasks.py** - Background email task
- **listings/views.py** - Task triggering in BookingViewSet

### Testing:
Create a booking via `POST /api/bookings/` and the email confirmation will be processed asynchronously in the background.

**Repository:** alx_travel_app_0x03
