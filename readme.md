
# Mini Project (Semester 4)

## Overview
This is a Django-based web application that includes a chat module. The project is designed for real-time communication and database management.

## Features
- User authentication
- Real-time chat functionality
- SQLite database integration

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip
- Virtual environment (optional but recommended)

### Setup Instructions
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd miniprojectsem4-main
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```

5. Run the development server:
   ```sh
   python manage.py runserver
   ```

6. Open your browser and visit:
   ```
   http://127.0.0.1:8000/
   ```

## Project Structure
```
miniprojectsem4-main/
│── chat/               # Chat application module
│── db.sqlite3          # Database file
│── manage.py           # Django project management script
│── requirements.txt    # Project dependencies (if available)
│── static/             # Static files (CSS, JS, images)
│── templates/          # HTML templates
└── other Django app files
```

## Contribution
If you'd like to contribute, fork the repository and create a pull request.

## License
This project is for educational purposes and does not have a specific license.