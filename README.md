# ☕ Kafe - Coffee Shop Management System

A comprehensive full-stack application for managing a modern coffee shop with inventory, POS, employee management, analytics, customer relationships, menu management, and online reservations with payment integration.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database Schema](#database-schema)

## ✨ Features

### Core Features
- **☕ Inventory Management** - Track coffee, supplies, stock levels with alerts
- **💰 POS/Sales System** - Modern point-of-sale with payment processing
- **👥 Employee Management** - Staff scheduling and performance tracking
- **📦 Order Management** - Customer orders and order history
- **📊 Analytics & Reports** - Sales reports and business insights
- **🛎️ Customer Management** - Customer profiles and loyalty programs
- **📋 Menu Management** - Create and manage menu items
- **📅 Reservation System** - Online booking with payment (cash/online)
- **📸 Day-to-Day Features** - Customer photos and testimonials
- **🔐 OAuth Authentication** - Google, GitHub OAuth 2.0

## 🛠️ Tech Stack

**Frontend:** React 18, React Router, Axios, Tailwind CSS, Redux Toolkit, Vite  
**Backend:** Python 3.9+, Flask, SQLAlchemy, Flask-JWT-Extended  
**Database:** MySQL 8.0 (IONOS)  
**Authentication:** OAuth 2.0 + JWT  
**Payments:** Stripe/PayPal Integration  

## 📁 Project Structure

```
kafe/
├── frontend/              # React application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── App.jsx
│   └── package.json
├── backend/               # Python Flask application
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── middleware/
│   │   └── config.py
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
├── database/
│   ├── schema.sql
│   └── migrations/
└── docker-compose.yml
```

## 🚀 Prerequisites

- Node.js 16+
- Python 3.9+
- MySQL 8.0+
- Docker (optional)

## 📦 Quick Start

### 1. Create Repository
Go to https://github.com/new and create a repository named "kafe"

### 2. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### 4. Database
Connect to your IONOS MySQL 8.0 database and run the schema.sql file

## 📊 Day-to-Day Features

The application includes:
- **Customer Photo Feature** - Capture and display photos of customers buying coffee
- **Daily Reports** - See daily coffee sales and customer interactions
- **Social Engagement** - Share customer testimonials and stories
- **Real-time Analytics** - Track daily trends and popular items

## 🔐 Authentication

OAuth 2.0 integration with:
- Google Sign-in
- GitHub Sign-in
- JWT token-based session management

## 💳 Payment Integration

Support for:
- **Online Payments** - Stripe/PayPal for reservations and online orders
- **Cash Payments** - POS integration for cash transactions
- **Payment Tracking** - Full payment history and reconciliation

## 📄 License

MIT License - see LICENSE file

---

**Ready to brew! ☕**
