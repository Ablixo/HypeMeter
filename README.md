# HypeMeter · Trailer Hype Voting (MVP)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)


Small FastAPI backend where users vote **HYPED** or **NAH** on trailers and view a leaderboard.  
Data is in-memory (resets on restart) to keep the MVP simple.

👉 Swagger docs: **http://localhost:8000/docs**

---

## ✨ Features
- Create trailers (id, title, platform)
- Cast one vote per user per trailer (HYPED/NAH)
- Leaderboard sorted by `(hypedCount - nahCount)`
- Health check & OpenAPI docs

---

## ⚡ Quickstart Guide

```bash
# 1) Create & activate a venv (optional but recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# 2) Install dependencies
pip install fastapi uvicorn pydantic

# 3) Run the API (dev)
uvicorn api.app:app --reload
