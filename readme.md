
# Mini Project (Semester 4)

## Overview
This is a Django-based web application featuring a real-time chat system implemented with Django Channels and WebSocket protocol. The project demonstrates modern web technologies for real-time communication and efficient database management.

## Key Features
- User Authentication and Authorization
- Real-time Chat with WebSocket Support
- Profile Management
- Donation System with In-Database Image Storage
- Responsive UI Design
- MySQL Database Integration

## Technical Stack
- **Backend Framework**: Django 4.x
- **WebSocket Server**: Daphne (ASGI Server)
- **Channel Layer**: Redis (for production) / In-Memory Channel Layer (for development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MySQL
- **Real-time Protocol**: WebSocket

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- MySQL Server
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

4. Configure MySQL Database:
   - Create a MySQL database named 'donateshare_db'
   - Update database settings in settings.py if needed

5. Run migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start the development server:
   ```sh
   python manage.py runserver
   ```

## Features
- **User Management**: Complete authentication system with registration, login, and profile management
- **Real-time Chat**: WebSocket-based chat system for instant communication
- **Donation System**: Platform for managing donations with image storage in database
- **Responsive Design**: Mobile-friendly interface with modern UI/UX

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## References & Documentation

### Django & Channels
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Channels Documentation](https://channels.readthedocs.io/)
- [Django Authentication System](https://docs.djangoproject.com/en/stable/topics/auth/)
- [WebSocket Protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

### Database & Storage
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Django Database API](https://docs.djangoproject.com/en/stable/topics/db/)
- [Django File Uploads](https://docs.djangoproject.com/en/stable/topics/http/file-uploads/)

### Frontend Development
- [HTML5 Guide](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS3 Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [JavaScript Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

### Deployment & Infrastructure
- [Daphne ASGI Server](https://github.com/django/daphne)
- [Redis Documentation](https://redis.io/documentation)
- [Django Deployment Guide](https://docs.djangoproject.com/en/stable/howto/deployment/)

## License
This project is licensed under the MIT License - see the LICENSE file for details.