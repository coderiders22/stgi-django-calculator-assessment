# CalculatorPro – STGI Technical Assessment of Full-Stack Django Calculator Application

**A professional, full-stack calculator application built with Django REST Framework and Vue.js**, designed to demonstrate authentication, session management, REST APIs, guest access, and admin control — as required in the Django assessment.

---

## Assessment Overview

This project was developed as part of a **Django Technical Assessment** consisting of **four progressive phases**:

1. Basic calculator functionality
2. User authentication & REST APIs
3. Guest session support
4. Admin interface & testing readiness

The application evolves from a simple calculator into a **production-grade, role-aware system** supporting **guest users, authenticated users, session isolation, and administrative oversight**.

---

## 🔗 Deployment Details

- **Live App (Integrated):** [https://basictaskmanager.vercel.app/](https://basictaskmanager.vercel.app/)

## 🔗 Frontend and Backend Deployed Link
- **Vercel (Frontend):** `https://basictaskmanager.vercel.app/` 
- Render (Backend): `https://basic-task-manager-9f0x.onrender.com` 

---

## Application Overview

**CalculatorPro** allows users to perform mathematical operations while maintaining a detailed calculation history.

### Key Highlights

* Guest & Premium access modes
* Session-based guest history (isolated per user)
* Secure authentication for registered users
* RESTful API architecture
* Smart calculation notes
* Weekly analytics
* Admin dashboard with read-only data control

---

## 🧩 Project Phases & Implementation

---

## Phase 1 – Basic Calculator Functionality 

### Features Implemented

* Two numeric input fields
* Operator selection:

  * Addition (+)
  * Subtraction (−)
  * Multiplication (×)
  * Division (÷)
* Real-time validation (division by zero handled)
* Calculation result storage in database
* History page displaying calculations

### Technologies Used

* Django Models
* Django Views
* SQLite Database
* Django ORM

---

## Phase 2 – Authentication & REST API 

### Authentication

* User registration
* Login & logout
* Session-based authentication
* Secure CSRF handling

### REST API (Django REST Framework)

| Endpoint          | Method | Description                    |
| ----------------- | ------ | ------------------------------ |
| `/calculate/`     | POST   | Perform calculation            |
| `/history/`       | GET    | Fetch calculation history      |
| `/history/{id}/`  | DELETE | Delete calculation (auth only) |
| `/history/clear/` | DELETE | Clear history (auth only)      |
| `/auth/register/` | POST   | Register user                  |
| `/auth/login/`    | POST   | Login                          |
| `/auth/logout/`   | POST   | Logout                         |
| `/auth/me/`       | GET    | Current user info              |
| `/auth/csrf/`     | GET    | CSRF token                     |

### Permissions

* **Authenticated users:** Full access
* **Guests:** Limited access (session-based)

---

## Phase 3 – Guest Session Support 

### Guest Capabilities

* Use calculator **without login**
* Session-based history storage
* Session isolation:

  * Guest A sees only Guest A’s history
  * Guest B sees only Guest B’s history
* Parallel guest sessions supported
* Cookies + Django sessions used

### Guest Limitations

* Maximum **10 calculations**
* Can view history (read-only)
* Cannot:

  * Delete individual items
  * Clear full history
  * Permanently save data

---

## Phase 4 – Admin Interface & Testing Readiness ✅

### Django Admin Panel

* Admin login enabled
* View:

  * Registered users
  * All calculation histories
* **Read-only CalculationHistory model**

  * No delete or modify allowed from admin
* Clean admin UI

### Logging & Error Handling

* Input validation
* API error responses
* Graceful UI error messages

> Unit tests can be added using `Django TestCase` (structure prepared).

---

## Access Modes

### Guest Mode

✔ Basic calculator
✔ View last 10 calculations
✔ Add notes to **2 calculations**
✔ Weekly analytics
✖ Cannot delete history
✖ Cannot clear history
✖ Session data not permanent

### Premium (Authenticated) Mode

✔ Unlimited calculations
✔ Complete history access
✔ Unlimited notes
✔ Weekly analytics
✔ Delete individual history items
✔ Clear entire history
✔ Persistent database storage

---

## 📝 Smart Notes System

* Attach notes to calculations
* Useful for:

  * Business calculations
  * Financial planning
  * Learning & tracking
* Guest: limited notes
* Premium: unlimited notes

---

## Weekly Analytics

* Track number of calculations
* Weekly usage insights
* Available to both guest & premium users

---

## Tech Stack

| Layer    | Technology                     |
| -------- | ------------------------------ |
| Backend  | Django + Django REST Framework |
| Frontend | Vue.js 3                       |
| Database | SQLite                         |
| Auth     | Django Session Authentication  |
| API      | REST (JSON)                    |
| UI Icons | Lucide Icons                   |
| State    | Cookies + Sessions             |

---

##  Project Setup

### Clone Repository

```bash
git clone https://github.com/coderiders22/stgi-django-calculator-assessment.git

```

---

### Backend Setup (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### Frontend Setup (Vue)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

##  Running Tests

```bash
python manage.py test
```

---

##  Database Schema (Core)

### `CalculationHistory`

| Field       | Type                  |
| ----------- | --------------------- |
| user        | ForeignKey (nullable) |
| session_key | CharField             |
| operand1    | Float                 |
| operand2    | Float                 |
| operator    | Char                  |
| result      | Float                 |
| created_at  | DateTime              |

---

## Security Considerations

* CSRF protection enabled
* Session-based authentication
* Permission-controlled endpoints
* Guest session isolation
* Admin access restricted

---

## Folder Structure (Simplified)

## 📁 Project Structure

The project is organized into two main parts: a Django REST backend and a Vue.js frontend.

### Frontend (Vue.js)

``` frontend/vue-calculator-ui/
├── public/
│   └── index.html
│
├── src/
│   ├── assets/
│   │   ├── gradient.css      # Global gradient & theme styles
│   │   └── logo.svg
│   │
│   ├── components/
│   │   ├── Calculator.vue    # Core calculator UI + guest/premium logic
│   │   ├── History.vue       # Calculation history with access control
│   │   ├── Modal.vue         # Reusable modal (errors, warnings, success)
│   │   ├── Navbar.vue        # Auth-aware navigation bar
│   │   ├── Footer.vue        # Application footer
│   │   └── Logo.vue
│   │
│   ├── views/
│   │   ├── Welcome.vue       # Landing page (Guest vs Premium comparison)
│   │   ├── Dashboard.vue     # Calculator + History combined view
│   │   ├── Login.vue         # Login screen
│   │   ├── Register.vue      # Registration screen
│   │   └── NotFound.vue      # 404 page
│   │
│   ├── router/
│   │   └── index.js          # Vue Router configuration
│   │
│   ├── services/
│   │   └── api.js            # Axios instance (CSRF + session support)
│   │
│   ├── App.vue               # Root Vue component
│   └── main.js               # App bootstrap + CSRF initialization
│
├── package.json
├── vite.config.js
└── node_modules/ 
```

### Backend (Django)

``` backend/
├── calculator/
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py              # Admin configuration for CalculationHistory
│   ├── apps.py               # App configuration
│   ├── auth_views.py         # Session-based auth (login, register, logout, me, csrf)
│   ├── models.py             # CalculationHistory model
│   ├── serializers.py        # DRF serializers
│   ├── tests.py              # Test placeholders
│   ├── urls.py               # Calculator + Auth API routes
│   └── views.py              # Calculate, history, delete, clear logic
│
├── config/
│   ├── __init__.py
│   ├── asgi.py               # ASGI entry point
│   ├── settings.py           # Django settings (CORS, sessions, installed apps)
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI entry point
│
├── manage.py                 # Django management script
├── requirements.txt          # Backend dependencies
└── venv/                   # Python virtual environment (local)


```
---

## Screenshots (Demo)

| Screen | Preview |
|------|--------|
| Welcome Screen | ![Welcome](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/welcome.png) |
| Guest Mode Dashboard | ![Guest Dashboard](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/guest%20dashboard.png) |
| Guest History (Limited) | ![Guest History Limit](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/guest%20history.png) |
| Guest Limit Reached     | ![Guest Limit](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/guest%20limit.png) |
| Authentication Screen   | ![Login](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/login.png) |
| Authentication Screen   | ![Register](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/register.png) |
| Access Modes            | ![Guest vs Premium Access](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/Guest%20vs%20Premium%20Access.png) |
| Premium User Dashboard | ![Premium Dashboard](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/premium%20user.png) |
| Delete Single History Item | ![Premium user deleting an individual calculation](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/delete%20single%20history.png)|
| Clear Entire History | ![Premium user clearing all calculation history at once](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/clear%20all%20history.png)| 
| Premium Unlimited History Management | ![Premium Unlimited History](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/939dca14a05bb75676c150dd7f74dfdef593dbbe/Screenshots/Premium%20Unlimited%20History.png) |
| Add Notes | ![Adding notes to a calculation (Premium feature)](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/add%20notes.png) |
| Calculation Notes | ![Notes](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/calculation%20notes..png) |
| Weekly Analytics | ![Analytics](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/analytics.png) |
| Django Admin Panel | ![Admin](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/admin%20portal.png) |
| Django Admin Panel | ![Users List](https://github.com/coderiders22/stgi-django-calculator-assessment/blob/30584f196411d2ebfc2792932bdad04dffb757d7/Screenshots/users%20admin.png) |

---

## Author

**Manav Rai**
Punjab Engineering College, Chandigarh
Email: [manavrai454@gmail.com](mailto:manavrai454@gmail.com)
GitHub: [https://github.com/coderiders22](https://github.com/coderiders22)

---

## License

© 2026 **Manav Rai**
All rights reserved.

---
