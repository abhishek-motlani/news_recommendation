# News Recommendation System

This project implements a news article recommendation system. The system consists of both a backend and frontend, which work together to provide personalized news article suggestions to users.

## Prerequisites

Before you begin, ensure that you have the following installed:

- Python 3.x
- Node.js (for frontend)
- OpenAi API key(please change it in the code)

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
### 3. Database Setup
 1. Note on MongoDB Data
    Due to the size of the database, the actual MongoDB data has not been included in this repository. However, in the Database/ folder, I have provided a Python file that can be used to extract 
    data via an API call and save it into a MongoDB database.

 2. Navigate to the Database/ folder in the project directory.
   Open the Python script in the folder.
   Use a different API key (you can replace it in the script) to fetch the data and insert it into your MongoDB database.
Once the data is inserted into MongoDB, you can run the rest of the code.
After you've set up your MongoDB with the data, the rest of the project should run as expected
## Running the Application

### 1. Start the Backend

Ensure your virtual environment is activated, then run the backend server using `uvicorn`:
```bash
uvicorn main_points:app --reload
```

## 2. Start the frontend

Ensure you are in frontend directory:
```bash
npm start
```

## 3. Video link to how it will look
https://www.loom.com/share/4626bed92a304a7284066a661fc9cb0f?sid=53128682-134a-452e-9fe1-01a21400335c
