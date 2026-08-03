# Enterprise AI Solution Architect Platform

An enterprise-grade, full-stack AI Solution Architect system built with **FastAPI**, **React.js**, **PostgreSQL / SQLAlchemy 2.0 ORM**, **JWT Authentication**, **Google Gemini API**, and **ReportLab PDF Engine**.

---

## 🏛️ System Architecture

```
                                +-------------------+
                                |   React Frontend  |
                                |  (Vite + Tailwind)|
                                +---------+---------+
                                          |
                                    HTTP / REST API
                                          |
                                +---------v---------+
                                |  FastAPI Backend  |
                                +----+---------+----+
                                     |         |
                  +------------------+         +-------------------+
                  |                                                |
        +---------v---------+                            +---------v---------+
        | PostgreSQL Database|                            |  Google Gemini    |
        |  (SQLAlchemy 2.0) |                            |  AI Service SDK   |
        +-------------------+                            +-------------------+
```

---

## 📁 Repository Directory Structure

```
AI-SOLUTION-ARCHITECTURE/
├── backend/                  # FastAPI Application Core
│   ├── .venv/                # Python Virtual Environment
│   └── requirements.txt      # Python Backend Dependencies
├── frontend/                 # React SPA Frontend
│   ├── node_modules/         # Node Dependencies
│   └── package.json          # React & Vite Dependencies
├── database/                 # PostgreSQL & SQLAlchemy Session / Engine Setup
├── models/                   # Pydantic Schemas & SQLAlchemy ORM Models
├── routes/                   # REST API Controller Handlers (Clean MVC)
├── services/                 # Core Business Logic & AI Orchestration Services
├── utils/                    # Common Utilities (JWT, Hashing, Formatting)
├── prompts/                  # Enterprise System Prompts for Gemini AI
├── reports/                  # PDF Generation Engine & Storage
├── .env.example              # Master Environment Variables Template
├── .env                      # Local Environment Variables (Git Ignored)
├── .gitignore                # Repository Git Ignore Rules
└── README.md                 # System Documentation & Architecture Guide
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ / npm
- PostgreSQL (or local SQLite for lightweight testing)

### 2. Backend Setup
```powershell
# Navigate to repository root
python -m venv backend\.venv

# Activate environment and install dependencies
.\backend\.venv\Scripts\pip.exe install -r backend\requirements.txt
```

### 3. Frontend Setup
```cmd
cmd.exe /c "npm install --prefix frontend"
```

### 4. Environment Variables
Copy `.env.example` to `.env` and populate your secrets:
```powershell
Copy-Item .env.example .env
```
Ensure your `GEMINI_API_KEY` and `DATABASE_URL` are configured inside `.env`.

---

## 📋 12-Phase Roadmap Status

- [x] **Phase 1: Project Setup & Environment** (Root Setup, `.gitignore`, Dependencies, `.env`, Structure)
- [ ] **Phase 2: FastAPI Backend & PostgreSQL Auth** (FastAPI Core, DB Engine, JWT Auth, CORS)
- [ ] **Phase 3: React Frontend & Dashboard** (React Shell, Auth Provider, Dashboard, Project Requirement Form)
- [ ] **Phase 4: Gemini API Integration Core** (Google GenAI SDK Integration, Async Prompt Service)
- [ ] **Phase 5: AI Recommendation Engine** (Structured Architecture Generation)
- [ ] **Phase 6: Architecture Comparison** (Multi-Option Trade-off Matrix)
- [ ] **Phase 7: Cloud Cost Estimator** (Cloud Provider Cost Analysis Engine)
- [ ] **Phase 8: Timeline & WBS Generator** (Work Breakdown Structure & Milestone Timeline)
- [ ] **Phase 9: Agile Sprint Planner** (Backlog Generation & Sprint Scheduling)
- [ ] **Phase 10: Enterprise Risk Analysis** (Risk Register & Mitigation Matrix)
- [ ] **Phase 11: Executive PDF Report Exporter** (ReportLab PDF Generation Service)
- [ ] **Phase 12: Architecture History & Versioning** (Project Persistence & Version Tracking)

---

## 🔐 Security & Best Practices
- **Strict Separation of Concerns**: Routes handle HTTP protocols only; business logic resides strictly inside `services/`.
- **JWT Protection**: Secure RS256/HS256 token verification with standard bearer headers.
- **Structured AI Generation**: Pydantic v2 validation enforced on all Gemini AI outputs.
