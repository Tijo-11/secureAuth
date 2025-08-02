# secureAuth

A Django and React project providing **secure authentication** using JWT and HTTP-only cookies.  
This project overrides the default JWT authentication with a custom `authenticate.py` file to enhance security.

---

##  Table of Contents

- About
- Features
- Installation
  - Backend Setup
  - Frontend Setup
- Usage
- Contributing

---

##  About

**secureAuth** is a web application built with:
- Django (backend)
- React + Vite (frontend)

It implements a secure authentication system using **JSON Web Tokens (JWT)** stored in **HTTP-only cookies**, ensuring enhanced session security.

 Repository: https://github.com/Tijo-11/secureAuth

---

##  Features

- Custom JWT authentication via HTTP-only cookies  
- Django backend with RESTful API  
- React + Vite frontend for a fast UI  
- Secure session management

---

## ⚙ Installation

###  Prerequisites

- Python 3.8+ (backend)  
- Node.js 16+ (frontend)  
- Git

---

###  Backend Setup

1. Clone the repository:  
   git clone https://github.com/Tijo-11/secureAuth.git

2. Navigate to the backend directory:  
   cd secureAuth/backend

3. Create and activate a virtual environment:  
   python -m venv venv  
   source venv/bin/activate      (On Windows: venv\Scripts\activate)

4. Install dependencies:  
   pip install -r requirements.txt

5. Run the server:  
   python manage.py runserver

---

###  Frontend Setup

1. Navigate to the frontend directory:  
   cd secureAuth/frontend

2. Install dependencies:  
   npm install

3. Start the development server:  
   npm run dev

---

##  Usage

- Backend API: http://localhost:8000  
- Frontend (via Vite): http://localhost:5173

This application supports secure **login** and **registration** using JWT stored in **HTTP-only cookies**.

---

##  Contributing

We welcome contributions!

1. Fork the repository  
2. Create a new branch  
   git checkout -b feature/your-feature

3. Make your changes and commit  
   git commit -m 'Add your feature'

4. Push to GitHub  
   git push origin feature/your-feature

5. Open a Pull Request

---

##  License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
