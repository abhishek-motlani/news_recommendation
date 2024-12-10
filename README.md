# News Recommendation System

This project implements a news article recommendation system. The system consists of both a backend and frontend, which work together to provide personalized news article suggestions to users.

## Prerequisites

Before you begin, ensure that you have the following installed:

- Python 3.x
- Node.js (for frontend)

## Installation

### 1. Backend Setup

1. Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use .\env\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Frontend Setup

1. Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2. Install the required dependencies:
    ```bash
    npm install
    ```

## Running the Application

### 1. Start the Backend

Ensure your virtual environment is activated, then run the backend server using `uvicorn`:
```bash
uvicorn main_point:app --reload
```

## 2. Start the frontend

Ensure you are in frontend directory:
```bash
npm start
```
