# SetupFX — USDT Investment & Wallet Platform

A professional-grade USDT investment and wallet management platform built with Django REST Framework (backend) and Next.js (frontend).

## Tech Stack

### Backend
- **Framework**: Django 5.x + Django REST Framework
- **Database**: PostgreSQL
- **Cache/Broker**: Redis
- **Task Queue**: Celery + Celery Beat
- **Auth**: JWT (djangorestframework-simplejwt)
- **Blockchain**: tronpy (TRC-20), web3.py (ERC-20/BEP-20)

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: Zustand
- **HTTP**: Axios
- **Auth**: NextAuth.js (Auth.js v5)

## Project Structure

```
currency_list/
├── backend/          # Django + DRF API
├── frontend/         # Next.js Application
├── docker-compose.yml
└── README.md
```

## Getting Started

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker (Full Stack)
```bash
docker-compose up --build
```

## Environment Variables
Copy `.env.example` to `.env` in both `backend/` and `frontend/` directories and fill in the values.
