# 🛠️ API Documentation

## 📌 Introduction  
This project is the **backend** for the **Cyna** project, an application that manages users via a **secure REST API** with **JWT authentication**. The backend is built using **Django Ninja** and uses **MySQL** as the database.

---

## 🚀 Installation & Setup

### 1️⃣ Prerequisites  
- **Python 3.9+**  
- **Django 4+**  
- **MySQL**  
- **Docker (optional)**  

### 2️⃣ Install the project  
Clone the repository and install dependencies:  

```bash
git clone https://github.com/Tiffany-Dby/mes-dev
cd mes-dev
pip install -r requirements.txt
```

### 3️⃣ Configure the environment  
Create a `.env` file at the project root:

```env
SECRET_KEY="your_secret_key"
DEBUG=True
DATABASE_URL="mysql://mesdev:mesdev@127.0.0.1:3306/mesdev_db"
```

### 4️⃣ Apply migrations and run the server  
```bash
python manage.py migrate
python manage.py runserver
```
The API will be available at **http://127.0.0.1:8000**

---

## 🔐 Authentication  
The API uses **JWT** to secure routes.  
- 🔑 **Access Token**: Generated during `login` or `register`.  
- 🔄 **Refresh Token**: Used to renew the access token.  

The token must be sent in the **Authorization** header in the following format:

```
Authorization: Bearer <your_access_token>
```

---

## 📡 **API Routes Documentation**

### 🔹 **Auth Routes**
#### ➤ **📌 Register**
- **Method:** `POST`
- **Endpoint:** `/api/auth/register`
- **Description:** Creates a new user.
- **Request Body:**
  ```json
  {
    "firstName": "string",
    "lastName": "string",
    "email": "string",
    "password": "string",
    "confirmPassword": "string"
  }
  ```
- **Response:**
  ```json
  {
    "code": 200,
    "message": "User successfully created"
  }
  ```

#### ➤ **📌 Login**
- **Method:** `POST`
- **Endpoint:** `/api/auth/login`
- **Description:** Logs in a user and returns JWT tokens.
- **Request Body:**
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Response:**
  ```json
  {
    "access": "eyJhbGciOiJIUzI1NiIs...",
    "refresh": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": int,
      "firstName": "string",
      "lastName": "string",
      "email": "string"
    }
  }
  ```

---

### 🔹 **User Routes**
#### ➤ **📌 Get User by ID**
- **Method:** `GET`
- **Endpoint:** `/api/users/get/{id}`
- **Description:** Retrieves user information by ID.
- **Example Response:**
  ```json
  {
    "id": 1,
    "firstName": "string",
    "lastName": "string",
    "email": "string"
  }
  ```

#### ➤ **📌 Get User by Email**
- **Method:** `POST`
- **Endpoint:** `/api/users/getByEmail/{email}`
- **Description:** Retrieves a user by email address.
- **Example Response:**
  ```json
  {
    "id": 1,
    "firstName": "string",
    "lastName": "string",
    "email": "string"
  }
  ```

#### ➤ **📌 Update User Information**
- **Method:** `PUT`
- **Endpoint:** `/api/users/update`
- **Description:** Updates user details.
- **Request Body:**
  ```json
  {
    "id": int,
    "firstName": "string",
    "lastName": "string",
    "email": "string"
  }
  ```
- **Example Response:**
  ```json
  {
    "id": int,
    "firstName": "string",
    "lastName": "string",
    "email": "string"
  }
  ```

#### ➤ **📌 Update Password**
- **Method:** `PUT`
- **Endpoint:** `/api/users/updatePassword`
- **Description:** Updates the user’s password.
- **Request Body:**
  ```json
  {
    "id": int,
    "password": "string"
  }
  ```

#### ➤ **📌 Delete a User**
- **Method:** `DELETE`
- **Endpoint:** `/api/users/delete/{id}`
- **Description:** Deletes a user by ID.
- **Response:**
  ```json
  true  // If the user has been successfully deleted
  ```

---

## 🛠️ **Technologies Used**
- **Backend:** Django, Django Ninja  
- **Authentication:** JWT  
- **Database:** MySQL  
- **Containerization:** Docker  
- **Linting & Formatting:** Black  
- **CI/CD:** SonarQube for static code analysis  

