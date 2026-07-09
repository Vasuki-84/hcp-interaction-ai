# AI-Powered HCP Interaction CRM

An AI-assisted Customer Relationship Management (CRM) application for Life Science Sales Representatives to efficiently capture, review, and manage Healthcare Professional (HCP) interactions.

The application uses **Groq Llama 3.3-70B**, **LangGraph**, and **FastAPI** to automatically extract structured information from natural language conversation notes and populate an interaction form for user review before saving.

---

## Features

### AI Assistant

- Extracts interaction details from natural language
- Auto-populates the interaction form
- Identifies HCP sentiment (Positive, Neutral, Negative)
- Generates structured interaction data
- Supports editing existing interactions
- Fetches past HCP interactions
- Suggests follow-up actions

### Interaction Management

- Create new HCP interactions
- Edit existing interactions
- Store interactions in MySQL
- AI-assisted data entry
- Manual review before saving

### AI Entity Extraction

The AI automatically extracts:

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

## Tech Stack

### Frontend

- React.js
- Redux Toolkit
- Axios
- Lucide React
- CSS

### Backend

- FastAPI
- LangGraph
- LangChain
- Groq API
- Llama 3.3 70B Versatile
- SQLAlchemy
- MySQL
- Pydantic

---

## Project Structure

```
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

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd AIVOA-FullStack-AI-Assignment
```

---

## Backend Setup

Create a virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run backend

```bash
uvicorn main:app --reload
```

Backend runs at

```
http://localhost:8000
```

---

## Frontend Setup

Navigate to frontend

```bash
cd frontend
```

Install packages

```bash
npm install
```

Run application

```bash
npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

## Environment Variables

Create a `.env` file inside the backend folder.

Example:

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

## AI Workflow

1. User describes an HCP interaction in natural language.
2. AI processes the conversation.
3. LangGraph invokes the `extract_entities` tool.
4. Structured data is returned.
5. Redux updates the interaction form.
6. User reviews the extracted information.
7. User clicks **Save Interaction**.
8. FastAPI stores the interaction in MySQL.

---

## Example Input

```
I met Dr. Wilson today.

We discussed Product X.

I shared a Product X brochure and clinical trial data.

I distributed 3 sample packs.

Dr. Wilson agreed to evaluate the product.

I will send additional clinical trial data tomorrow.
```

---

## Example AI Extraction

```
HCP Name:
Dr. Wilson

Interaction Type:
Meeting

Date:
2026-07-09

Topics Discussed:
Product X

Materials Shared:
Product X brochure, clinical trial data

Samples Distributed:
3 sample packs

Sentiment:
Positive

Outcomes:
Dr. Wilson agreed to evaluate the product

Follow-up Actions:
Send additional clinical trial data tomorrow
```

---

## API Endpoints

### AI Chat

```
POST /api/chat
```

Processes natural language interaction notes.

---

### Create Interaction

```
POST /api/interactions
```

Stores interaction in the database.

---

### Update Interaction

```
PUT /api/interactions/{id}
```

Updates an existing interaction.

---

### Fetch Interaction History

```
GET /api/interactions
```

Returns stored interactions.

---

## Dependencies

Backend

- FastAPI
- Uvicorn
- SQLAlchemy
- mysql-connector-python
- Pydantic
- LangGraph
- LangChain
- LangChain Groq
- Python Dotenv
- Alembic

Frontend

- React
- Redux Toolkit
- Axios
- Lucide React

---

## Future Enhancements

- Authentication & Authorization
- Dashboard Analytics
- Advanced Search & Filtering
- File Upload Support
- Export Interactions
- Email Notifications
- Multi-user Support

---

## Author

**Vasuki T**

MERN Stack Developer

GitHub:
https://github.com/Vasuki-84

LinkedIn:
https://www.linkedin.com/in/vasuki-fullstackdeveloper

---

## License

This project was developed as part of the **AiVOA Full Stack AI Assignment** for learning and evaluation purposes.
