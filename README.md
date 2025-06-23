## ⚙️ Installation

### Prerequisites

Ensure the following are installed on your machine:

- Python 3.10+
- pip (Python package manager)
- [MySQL](https://dev.mysql.com/) (running via Docker, see below)
- `virtualenv` (recommended)

---

### 1. Clone the repository

```bash
git clone https://github.com/Kant1-18/cyna-backend.git
cd cyna-backend
```

---

### 2. Start the MySQL database (via Docker)

If you're using Docker only for MySQL, start the database service:

```bash
docker compose up -d
```

This will spin up a MySQL container accessible from your local Django server.

---

### 3. Set up the Python environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Update it with your secret key and database access details (must match the Docker MySQL config):

---

### 5. Apply database migrations

```bash
cd server/
python manage.py migrate
```

---

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

---

### 7. Run the development server

```bash
python manage.py runserver
```

Visit:

- **API**: http://localhost:8000/api/
- **swagger**: http://localhost:8000/api/docs#/
