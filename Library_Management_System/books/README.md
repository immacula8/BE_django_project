📚 Library Management System

A Django + Django REST Framework based Library Management System (LMS) that allows users to register, login, and interact with books and authors. The project includes role-based access, authentication with tokens, and CRUD operations for managing library resources.

🚀 Features

✅ User Authentication & Registration (custom user model)

✅ Token-Based Authentication (DRF tokens)

✅ Role-Based Access (admin vs. ordinary users)

✅ Book Management (create, read, update, delete)

✅ Author Management

✅ Permissions (only admins can create/edit/delete books, ordinary users can view)

✅ Secure APIs with DRF

✅ Browsable API

⚙️ Tech Stack

Backend: Django, Django REST Framework

Authentication: DRF Token Authentication

Database: SQLite (default, can switch to PostgreSQL/MySQL)

Tools: Postman for API testing

📂 Project Structure
Library_Management_System/
│── accounts/          # Custom user model, registration, login
│── books/             # Book and Author apps with models, views, serializers
│── Library_Management_System/   # Main project settings
│── requirements.txt   # Python dependencies
│── README.md          # Project documentation

🔑 Authentication

Register: POST /accounts/register/

Login: POST /api/token/ (returns token)

Use Token: Include in header → Authorization: Token <your_token>

📖 API Endpoints
Users

POST /accounts/register/ → Register a new user

POST /accounts/login/ → Login and get token

Books

GET /api/books/ → List all books

POST /api/books/ → Add a book (admin only)

PUT /api/books/<id>/ → Update book (admin only)

DELETE /api/books/<id>/ → Delete book (admin only)

Authors

GET /api/authors/ → List authors

POST /api/authors/ → Add author (admin only)

PUT /api/authors/<id>/ → Update author (admin only)

DELETE /api/authors/<id>/ → Delete author (admin only)