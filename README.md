# 📚 Capstone Library API

A Django REST Framework API for managing a library system, allowing users to browse books, borrow/return them, and track borrowing history.  
Includes token-based authentication, filtering, and admin controls.

---

## 🚀 Features
- **User Authentication** (Token-based)
- **Book Management** (CRUD)
- **Borrowing & Returning Books**
- **Borrow History Tracking**
- **Filtering & Search** (by title, author, ISBN)
- **Admin Dashboard**
- **Pagination** for large datasets
- **Deployed to Heroku**

---

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** SQLite (local), PostgreSQL (Heroku)
- **Deployment:** Heroku
- **Auth:** DRF Token Authentication
- **Environment Management:** python-decouple, dotenv
- **Static Files:** WhiteNoise

---

## 📂 Project Structure
```
capstone-library-api/
│
├── library/                  # Main app
│   ├── models.py              # Database models
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # API views & ViewSets
│   ├── urls.py                 # App URLs
│
├── capstone-library-api/      # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/your-username/capstone-library-api.git
cd capstone-library-api
```

### 2️⃣ Create a virtual environment & activate it
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` file
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url-if-using-postgres
```

### 5️⃣ Run migrations & create superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6️⃣ Start development server
```bash
python manage.py runserver
```
API will be available at:  
```
http://127.0.0.1:8000/
```

---

## ☁️ Heroku Deployment

### 1️⃣ Login to Heroku
```bash
heroku login
```

### 2️⃣ Create a new Heroku app
```bash
heroku create capstone-library-api
```

### 3️⃣ Add Postgres
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 4️⃣ Set environment variables
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
```

### 5️⃣ Push code to Heroku
```bash
git push heroku main
```

### 6️⃣ Run migrations & create superuser
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 7️⃣ Open the app
```bash
heroku open
```

---

## 🔗 API Endpoints

### Authentication
- **POST** `/api-token-auth/` → Get token

### Users
- **GET** `/users/` → List users (admin)
- **POST** `/users/` → Create user (admin)

### Books
- **GET** `/books/` → List books
- **POST** `/books/` → Create book (admin)
- **PUT/PATCH** `/books/{id}/` → Update book (admin)
- **DELETE** `/books/{id}/` → Delete book (admin)

### Borrowing
- **POST** `/books/{id}/borrow/` → Borrow book
- **POST** `/books/{id}/return/` → Return book

### Borrow Records
- **GET** `/borrow-records/` → List borrow records

---

## 🔒 Permissions
- **Admin:** Full CRUD for users & books
- **Authenticated Users:** Borrow/return books, view own borrow history
- **Public:** View available books

---

## 📜 License
This project is licensed under the MIT License.
