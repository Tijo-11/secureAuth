secureAuth
A Django and React project providing secure authentication using JWT and HTTP-only cookies. This project overrides the default JWT authentication with a custom 
authenticate.py file to enhance security by utilizing HTTP-only cookies.
Table of Contents

About
Features
Installation
Usage
Contributing
License

About
secureAuth is a web application built with Django (backend) and React + Vite (frontend). It implements a secure authentication system based on JSON Web Tokens (JWT)
with HTTP-only cookies to ensure enhanced security for user sessions.
Repository: https://github.com/Tijo-11/secureAuth
Features

Custom JWT authentication using HTTP-only cookies
Django backend with RESTful API
React + Vite frontend for a fast and modern user interface
Secure session management

Installation
Prerequisites

Python 3.8+ (for backend)
Node.js 16+ (for frontend)
Git

Backend Setup

Clone the repository:git clone https://github.com/Tijo-11/secureAuth.git


Navigate to the backend directory:cd secureAuth/backend


Create and activate a virtual environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install the required dependencies:pip install -r requirements.txt


Run the Django server:python manage.py runserver



Frontend Setup

Navigate to the frontend directory:cd secureAuth/frontend


Install the dependencies:npm install


Start the development server:npm run dev

Usage

Access the backend API at http://localhost:8000 (default Django port).
Access the frontend at the URL provided by Vite (typically http://localhost:5173).
The application provides secure login and registration endpoints with JWT-based authentication stored in HTTP-only cookies.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.
