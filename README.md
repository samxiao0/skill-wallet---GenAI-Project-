# Personalized Networking Assistant

## Features
- Event Analysis
- Topic Detection
- Conversation Starter Generation
- Fact Checking
- History Tracking
- Feedback System
- PDF Export

## Tech Stack
- FastAPI
- Streamlit
- Transformers
- Wikipedia API
- ReportLab

## Installation

pip install -r requirements.txt

## Run Backend

python -m uvicorn app.main:app --reload

## Run Frontend

streamlit run frontend/streamlit_app.py

## Run Tests

pytest -v