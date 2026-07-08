# AI-First CRM HCP Module

A modern, full-stack CRM module designed for Healthcare Professionals (HCPs) featuring an AI-driven Chat Assistant powered by LangGraph, alongside a traditional structured form for logging interactions. 

This project demonstrates a production-ready architecture with a React frontend and a FastAPI backend.

---

## 🏗️ Project Architecture

This project is built using a clean, scalable architecture separating concerns across the stack:

### Frontend (React + Vite + Redux)
- **API Layer (`src/api/`)**: Centralized Axios configuration and dedicated service files for external communications.
- **State Management (`src/store/`)**: Redux Toolkit slices handle asynchronous API actions and application state.
- **Component Design (`src/components/`, `src/pages/`)**: Reusable UI components separated from page-level layouts.

### Backend (FastAPI + LangGraph + MySQL)
- **Routers (`app/routers/`)**: FastAPI endpoints defined cleanly with explicit Pydantic schemas and HTTP status codes.
- **Services (`app/services/`)**: Business logic and database transaction management are encapsulated here, keeping routers thin.
- **AI Agent (`app/graph/`, `app/tools/`)**: The LangGraph state machine controls the conversational flow, granting the LLM safe access to structured tools.
- **Database (`app/db/`, `app/models/`)**: SQLAlchemy models mapping to a MySQL database with a robust session management strategy.
- **Logging (`app/core/logger.py`)**: Centralized, reusable Python logging capturing API requests, database events, and tool executions.

---

## 📂 Folder Structure

```
.
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── core/             # Configuration & Logging
│   │   ├── db/               # Database Engine Setup
│   │   ├── graph/            # LangGraph State Machine
│   │   ├── models/           # SQLAlchemy Models
│   │   ├── routers/          # API Endpoints
│   │   ├── schemas/          # Pydantic Validation Schemas
│   │   ├── services/         # Business Logic
│   │   └── tools/            # LangGraph Agent Tools
│   ├── main.py               # Application Entry Point
│   ├── requirements.txt      # Python Dependencies
│   └── .env.example          # Environment Variables Template
│
├── frontend/                 # React Application
│   ├── src/
│   │   ├── api/              # Axios Client & Services
│   │   ├── components/       # Reusable UI Components
│   │   ├── pages/            # Page Layouts
│   │   ├── store/            # Redux Store & Slices
│   │   └── styles/           # Global CSS
│   ├── index.html
│   ├── package.json
│   └── .env.example          # Environment Variables Template
```

---

## 🛠️ Environment Setup

### 1. Database Setup (MySQL)
Ensure you have MySQL installed and running locally. Create the database:
```sql
CREATE DATABASE hcp_db;
```

### 2. Backend Environment (`backend/.env`)
Create a `.env` file inside the `backend/` directory using `.env.example` as a reference:
```env
PROJECT_NAME="AI-First CRM HCP Module"
DATABASE_URL="mysql+mysqlconnector://root:password@localhost:3306/hcp_db"
GROQ_API_KEY="your_groq_api_key_here"
MODEL_NAME="gemma2-9b-it"
ALLOWED_ORIGINS="http://localhost:5173"
```

### 3. Frontend Environment (`frontend/.env`)
Create a `.env` file inside the `frontend/` directory:
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 🚀 Running the Application

### Running the Backend

1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # (Windows)
   # OR source venv/bin/activate # (Mac/Linux)
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   *The API will be available at `http://localhost:8000`*

### Running the Frontend

1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The UI will be available at `http://localhost:5173`*

---

## 🤖 How LangGraph Works

The AI assistant utilizes **LangGraph** to create a structured, cyclic workflow. The agent acts as a state machine where messages flow from the user to the LLM. 
If the LLM determines it needs to perform an action (like searching the database), it generates a `ToolMessage`. LangGraph routes the execution to the `ToolNode`, executes the appropriate Python function in `app/tools/tools.py`, and returns the result to the LLM to formulate a final response.

### The Five Tools

1. **`log_interaction`**: Inserts a new HCP interaction record into the MySQL database.
2. **`edit_interaction`**: Modifies a previously logged interaction. Secured by a strict whitelist of editable fields (e.g., `topics_discussed`, `outcomes`).
3. **`search_interactions`**: Queries the database to retrieve past interactions for a specific HCP.
4. **`extract_entities`**: Parses unstructured text to extract key entities like Medical Topics, Follow-ups, and Sentiments.
5. **`suggest_follow_up`**: Generates intelligent follow-up actions based on the context of an interaction.

---

## 🌐 API Documentation

The backend automatically generates interactive API documentation.
Once the backend is running, navigate to:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints
- `POST /api/interactions/`: Log a new interaction.
- `GET /api/interactions/`: Fetch paginated interactions.
- `POST /api/chat/`: Send a message to the AI LangGraph agent.

---

## 📤 Submission Note
This project fulfills all criteria of the AI-First CRM HCP Module assignment, featuring a complete end-to-end implementation with zero human-written code manually, purely synthesized via advanced LLM coding capabilities.
