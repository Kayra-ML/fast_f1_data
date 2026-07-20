# F1 Data Analysis

## Project Overview

This project is a web-based Formula 1 analytics platform built using OpenF1 data. It collects race data, processes and stores it in a PostgreSQL database, then provides analytics through a FastAPI backend and a Node.js frontend.

---

## System Architecture

```
OpenF1 API
     │
     ▼
Worker (Data Collection)
     │
     ▼
Data Processing
(Cleaning & Validation)
     │
     ▼
PostgreSQL
     │
     ▼
FastAPI Backend
     │
     ▼
Node.js Frontend
     │
     ▼
User Dashboard
```

---

## Data Flow

1. Worker requests data from the OpenF1 API.
2. The raw JSON data is cleaned and validated.
3. Processed data is stored in PostgreSQL.
4. FastAPI retrieves data from the database.
5. The frontend requests data from FastAPI.
6. Users view analytics through the dashboard.

---

## Tech Stack

- Frontend: Node.js
- Backend: FastAPI
- Database: PostgreSQL
- Data Source: OpenF1 API
- Language: Python & JavaScript
