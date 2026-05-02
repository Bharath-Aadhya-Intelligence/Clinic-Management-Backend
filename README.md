# Homeopathy Hospital Management System - Backend

This is the FastAPI-based backend for the Homeopathy Hospital Management System.

## Tech Stack
- **FastAPI**: Web framework
- **MongoDB (Motor)**: Async database driver
- **Pillow**: Image compression
- **JWT**: Authentication
- **Pydantic v2**: Data validation

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file (one has been created for you) and update the `MONGODB_URL`.

3. **Seed Admin User**:
   Ensure MongoDB is running, then run:
   ```bash
   python seed_admin.py
   ```
   *Default credentials: admin / adminpassword123*

4. **Run the Server**:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation
Once the server is running, visit:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure
- `app/api/`: Route handlers
- `app/core/`: Configuration, Security, DB connection
- `app/models/`: Pydantic schemas and DB models
- `app/services/`: Business logic and DB operations
- `app/utils/`: Utility functions (image compression)
- `app/static/`: Static files (medicine images)
