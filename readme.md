
# Mini Project (Semester 4)

## Overview
This is a Django-based web application featuring a real-time chat system implemented with Django Channels and WebSocket protocol. The project demonstrates modern web technologies for real-time communication and efficient database management.

## Key Features
- User Authentication and Authorization
- Real-time Chat with WebSocket Support
- Profile Management
- Donation System
- Responsive UI Design
- SQLite Database Integration

## Technical Stack
- **Backend Framework**: Django 4.x
- **WebSocket Server**: Daphne (ASGI Server)
- **Channel Layer**: Redis (for production) / In-Memory Channel Layer (for development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite3
- **Real-time Protocol**: WebSocket

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- Redis (for production deployment)
- Virtual environment (recommended)

### Development Setup
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd miniprojectsem4
   ```

2. Create and activate virtual environment:
   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```sh
   python manage.py createsuperuser
   ```

6. Run development server:
   ```sh
   python manage.py runserver
   ```

7. Access the application:
   ```
   http://127.0.0.1:8000/
   ```

## Production Deployment

### Daphne Server Configuration
1. Install Daphne:
   ```sh
   pip install daphne
   ```

2. Configure ASGI application in `asgi.py`:
   ```python
   import os
   from django.core.asgi import get_asgi_application
   from channels.routing import ProtocolTypeRouter, URLRouter
   from channels.auth import AuthMiddlewareStack
   from chat.routing import websocket_urlpatterns

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatproject.settings')

   application = ProtocolTypeRouter({
       'http': get_asgi_application(),
       'websocket': AuthMiddlewareStack(
           URLRouter(websocket_urlpatterns)
       ),
   })
   ```

3. Run with Daphne:
   ```sh
   daphne -b 0.0.0.0 -p 8000 chatproject.asgi:application
   ```

### Redis Configuration (Production)
1. Install Redis server
2. Update `settings.py` channel layer:
   ```python
   CHANNEL_LAYERS = {
       'default': {
           'BACKEND': 'channels_redis.core.RedisChannelLayer',
           'CONFIG': {
               'hosts': [('127.0.0.1', 6379)],
           },
       },
   }
   ```

## Project Structure
```
miniprojectsem4/
├── chat/                # Chat application module
│   ├── consumers.py     # WebSocket consumer
│   ├── routing.py       # WebSocket URL routing
│   └── views/           # View modules
├── chatproject/         # Project configuration
│   ├── asgi.py         # ASGI configuration
│   └── settings.py     # Project settings
├── static/             # Static assets
├── templates/          # HTML templates
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```

## WebSocket Implementation
- WebSocket connections are handled by Django Channels
- Real-time chat messages are broadcasted through channel layers
- Authentication is required for WebSocket connections
- Connection status is monitored for reliability

## Security Considerations
- CSRF protection enabled for all POST requests
- WebSocket connections are authenticated
- Database queries are protected against SQL injection
- Static files are served securely

## Contributing
To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is developed for educational purposes as part of semester 4 coursework.