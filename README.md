# AI-Powered HCP Interaction CRM

An AI-assisted Customer Relationship Management (CRM) application for Life Science Sales Representatives to efficiently capture, review, and manage Healthcare Professional (HCP) interactions.

The application uses **Groq Llama 3.3-70B-Versatile**, **LangGraph**, and **FastAPI** to automatically extract structured information from natural language conversation notes, populate the interaction form, allow manual review before saving, retrieve interaction history, edit existing interactions, and generate intelligent follow-up recommendations.

---

# Features

## AI Assistant

- Extracts interaction details from natural language
- Automatically populates the interaction form
- Identifies HCP sentiment (Positive, Neutral, Negative)
- Normalizes extracted dates and times
- Prevents duplicate values between Outcomes and Follow-up Actions
- Returns structured JSON to the frontend
- Supports editing existing interactions
- Retrieves previous HCP interactions
- Generates AI-powered follow-up recommendations

---

## Interaction Management

- Create new HCP interactions
- Review extracted data before saving
- Save interactions into MySQL
- Edit existing interactions
- Retrieve previous interaction history
- AI-assisted data entry with manual confirmation

---

## AI Entity Extraction

The AI automatically extracts:

- HCP Name
- Interaction Type
- Interaction Date
- Interaction Time
- Attendees
- Topics Discussed
- Materials Shared
- Samples Distributed
- Sentiment
- Outcomes
- Follow-up Actions

---

# Tech Stack

## Frontend

- React.js
- Redux Toolkit
- Axios
- Lucide React
- CSS

## Backend

- FastAPI
- LangGraph
- LangChain
- Groq API
- Llama-3.3-70B-Versatile
- SQLAlchemy
- MySQL
- Pydantic

---

# Project Structure

```text
AIVOA-FullStack-AI-Assignment/

├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   ├── styles/
│   │   └── App.jsx
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── graph/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── tools/
│   ├── main.py
│   └── requirements.txt
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd AIVOA-FullStack-AI-Assignment
```

---

# Backend Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
uvicorn main:app --reload
```

Backend URL

```
http://localhost:8000
```

---

# Frontend Setup

Navigate to frontend

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Run application

```bash
npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

# Environment Variables

Create a `.env` file inside the backend folder.

```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.3-70b-versatile

DB_HOST=localhost
DB_PORT=3308
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=your_database
```

---

# LangGraph AI Workflow

```text
User Message
      │
      ▼
 process_chat()
      │
      ▼
 LangGraph
      │
      ▼
 chatbot()
      │
      ▼
 AI selects appropriate tool
      │
      ▼
 ToolNode executes tool
      │
      ▼
 Normalize extracted data
      │
      ▼
 Return JSON response
      │
      ▼
 Redux updates Interaction Form
      │
      ▼
 User reviews data
      │
      ▼
 Save Interaction
      │
      ▼
 MySQL Database
```

---

# Available AI Tools

## 1. extract_entities

Extracts structured information from natural language.

Fields extracted:

- HCP Name
- Interaction Type
- Date
- Time
- Attendees
- Topics Discussed
- Materials Shared
- Samples Distributed
- Sentiment
- Outcomes
- Follow-up Actions

---

## 2. fetch_past_interactions

Retrieves previous interactions for a Healthcare Professional from the database.

---

## 3. edit_interaction

Updates editable fields of an existing interaction.

Supports updates for:

- Topics Discussed
- Materials Shared
- Samples Distributed
- Sentiment
- Outcomes
- Follow-up Actions
- Attendees

Includes validation that converts string Interaction IDs into integers before updating the database.

---

## 4. suggest_follow_up

Uses the Groq LLM to generate intelligent follow-up recommendations based on:

- Topics Discussed
- Meeting Outcomes

Returns 1–2 professional actionable follow-up tasks.

---

## 5. log_interaction

Stores interactions into the MySQL database.

In this application, saving is performed only after the user reviews the extracted information and clicks **Save Interaction**.

---

# Example Input

```text
I met Dr. Wilson today at 10 AM.

We discussed Product X.

I shared a brochure.

I distributed 3 sample packs.

Dr. Wilson agreed to evaluate the product.

I will send the clinical trial data tomorrow.
```

---

# Example AI Extraction

```text
HCP Name:
Dr. Wilson

Interaction Type:
Meeting

Date:
2026-07-09

Time:
10:00

Topics Discussed:
Product X

Materials Shared:
Brochure

Samples Distributed:
3 sample packs

Sentiment:
Positive

Outcomes:
Agreed to evaluate the product

Follow-up Actions:
Send clinical trial data tomorrow
```

---

# API Endpoints

## AI Chat

```http
POST /api/chat
```

Processes natural language interaction notes.

---

## Create Interaction

```http
POST /api/interactions
```

Stores interaction into MySQL.

---

## Update Interaction

```http
PUT /api/interactions/{id}
```

Updates an existing interaction.

---

## Retrieve Interactions

```http
GET /api/interactions
```

Returns stored interaction history.

---

# Backend Highlights

- LangGraph-based AI workflow
- Automatic tool selection
- Tool execution logging
- Structured entity extraction
- Response normalization
- Date & time conversion
- Improved error handling
- AI tool validation
- Manual confirmation before database save

---

# Dependencies

## Backend

- FastAPI
- Uvicorn
- SQLAlchemy
- MySQL Connector
- Pydantic
- LangGraph
- LangChain
- LangChain Groq
- Python Dotenv
- Alembic

## Frontend

- React
- Redux Toolkit
- Axios
- Lucide React

---

# Future Enhancements

- Authentication & Authorization
- Dashboard Analytics
- Advanced Search & Filtering
- File Upload Support
- Export Interactions
- Email Notifications
- Multi-user Support
- Role-based Access Control

---

# Author

**Vasuki T**

MERN Stack Developer

GitHub

https://github.com/Vasuki-84

LinkedIn

https://www.linkedin.com/in/vasuki-fullstackdeveloper

---

# License

Developed as part of the **AiVOA Full Stack AI Assignment** for learning and evaluation purposes.