# HeyBuddy — Mental Health & Diary Assistant

A full-stack mental health companion application that combines AI-powered chat, personal diary management, and RAG-based diary query capabilities. HeyBuddy helps users express their feelings, track daily thoughts, and reflect on past entries through intelligent Q&A.

## Features

### 🎯 Core Functionality
- **Chat Interface**: Talk to an AI assistant for mental health support and mood tracking
- **Diary Management**: Write, edit, and view personal diary entries organized by date
- **Chat with Your Diary**: Ask questions about your diary entries using RAG (Retrieval-Augmented Generation)
- **Vector Search**: Local embeddings-based semantic search across diary entries
- **User Authentication**: Secure login and role-based access (User/Admin)

### 🔒 Security
- JWT-based authentication
- Password hashing with bcrypt
- Session management via access/refresh tokens
- Environment-based configuration

### 🎨 UI/UX
- Modern, futuristic dark theme with high-contrast cyan/mint accents
- Responsive two-panel layout (sidebar navigation + content area)
- Real-time message display and streaming responses
- No unnecessary page scrolling — optimized viewport management
- Active tab highlighting in sidebar

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **ORM**: SQLAlchemy
- **Authentication**: PyJWT + python-jose
- **Embeddings**: Sentence-Transformers (local, free)
- **LLM**: OpenAI GPT-3.5-turbo (for chat responses)
- **API Server**: Uvicorn

### Frontend
- **Framework**: Angular 17+ (standalone components)
- **Styling**: CSS with CSS variables for theming
- **Routing**: Angular Router with child routes
- **HTTP**: Native fetch API
- **Storage**: localStorage for session tokens & user info

### Database Schema
- **users**: User accounts with roles
- **diary_entries**: User diary entries with content and dates
- **diary_vectors**: Embeddings for diary entries (RAG index)

## Project Structure

```
HeyBuddy/
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI app initialization
│   │   ├── db.py                        # SQLAlchemy setup
│   │   ├── models.py                    # Database models (User, Diary, DiaryVector)
│   │   ├── schemas.py                   # Pydantic request/response schemas
│   │   ├── routes.py                    # Route registration
│   │   ├── controllers/                 # API endpoint handlers
│   │   │   ├── auth_controller.py
│   │   │   ├── user_controller.py
│   │   │   ├── chat_controller.py
│   │   │   ├── diary_controller.py
│   │   │   └── rag_controller.py
│   │   ├── services/                    # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── diary_service.py
│   │   │   └── rag_service.py
│   │   ├── core/                        # Core utilities
│   │   │   ├── config.py
│   │   │   ├── jwt_manager.py
│   │   │   └── security.py
│   │   └── utils/                       # Utility helpers
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── main.ts
│   │   ├── styles.css                   # Global CSS variables & theming
│   │   ├── index.html
│   │   ├── assets/
│   │   │   └── logo.svg                 # HeyBuddy logo
│   │   └── app/
│   │       ├── app.routes.ts            # Root routing
│   │       ├── app.component.ts
│   │       ├── services/
│   │       │   ├── auth.service.ts
│   │       │   └── user.service.ts
│   │       └── pages/
│   │           ├── login/
│   │           ├── chat/
│   │           ├── admin-dashboard/
│   │           └── user-dashboard/
│   │               ├── diary-management/
│   │               └── chat-with-diary/
│   ├── package.json
│   ├── angular.json
│   └── tsconfig.json
└── README.md
```

## Installation & Setup

### Prerequisites
- **Node.js 18+** (for frontend)
- **Python 3.9+** (for backend)
- **Git**

### Backend Setup

1. **Clone and navigate**:
```bash
cd c:\Users\neelo\codes\HeyBuddy\backend
```

2. **Create virtual environment**:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set environment variables** (PowerShell):
```powershell
$env:OPENAI_API_KEY = "<your_openai_api_key>"
$env:DATABASE_URL = "sqlite:///./test.db"  # or PostgreSQL URL
```

5. **Run migrations** (if applicable):
```bash
# Alembic migrations can be set up, or just start the app to auto-create tables
```

6. **Start the server**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will run at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**:
```bash
cd c:\Users\neelo\codes\HeyBuddy\frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start the dev server**:
```bash
npm start
```

Frontend will run at `http://localhost:4200`

## API Endpoints

### Authentication
- `POST /auth/login` — Redirect to SSO/OpenID flow
- `GET /auth/callback` — Handle OAuth callback
- `GET /auth/me` — Get current authenticated user
- `POST /auth/debug/token/{user_id}` — DEV: Create test token

### User Management
- `POST /users/register` — Register new user
- `POST /users/login` — Login with email/password
- `GET /users/{user_id}` — Get user details
- `GET /users` — List users (paginated)
- `PUT /users/{user_id}` — Update user
- `DELETE /users/{user_id}` — Delete user
- `POST /users/{user_id}/change-password` — Change password

### Diary
- `POST /diary` — Create diary entry
- `PUT /diary/{entry_id}` — Update diary entry
- `GET /diary/dates/{user_id}` — Get dates with diary entries
- `GET /diary/{user_id}/{date}` — Get diary entry by date (YYYY-MM-DD)

### RAG (Chat with Your Diary)
- `POST /rag/index/{user_id}` — Index/embed user's diary entries
- `POST /rag/chat` — Query diary entries with RAG

Request body for `/rag/chat`:
```json
{
  "user_id": 1,
  "question": "How was I feeling last week?",
  "top_k": 5
}
```

Response:
```json
{
  "answer": "Based on your diary entries...",
  "contexts": [
    {
      "date": "2025-12-11",
      "content": "...",
      "score": 0.85
    }
  ]
}
```

### Chat
- `POST /chat/chat` — Chat with mental health assistant (streaming)

### Jokes
- `GET /jokes/random` — Get a random joke for mood boost

### Health
- `GET /health` — Health check endpoint

## Usage

### User Workflow

1. **Login**: Open the app at `http://localhost:4200`, log in with credentials.
2. **Dashboard**: You land on the User Dashboard with a left sidebar showing navigation.
3. **Diary**: Write/edit diary entries, browse past entries by date.
4. **Chat**: Talk to the AI assistant for support and mood tracking.
5. **Chat with Diary**: Ask questions about your diary using RAG (e.g., "Was I happy last month?").
6. **Logout**: Click the Logout button in the top-right header.

### Example Queries (Chat with Your Diary)
- "Summarize my emotions this week"
- "What were the main themes in my entries last month?"
- "How has my mood changed over time?"

## Configuration

### Environment Variables

**Backend** (`.env` or shell):
```
OPENAI_API_KEY=<your-key>
DATABASE_URL=sqlite:///./test.db
JWT_SECRET=<your-secret>
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Frontend** (hardcoded in services):
- API URL: `http://localhost:8000` (update in `services/auth.service.ts` for production)

### Color Palette (CSS Variables)
Located in `frontend/src/styles.css`:
- `--bg`: #041022 (very dark navy)
- `--accent`: #6ec8ff (electric cyan)
- `--accent-2`: #7fffd4 (mint)
- `--text`: #e6f7ff (light cyan)
- `--muted`: #9bb9c9 (muted cyan)

## Security Considerations

⚠️ **Current Status**: Open endpoints without full JWT protection on diary/RAG routes.

### Recommended Enhancements
1. **Secure Diary Endpoints**: Add `Depends(validate_access_token)` to diary routes.
2. **Derive user_id from JWT**: Extract user_id from token payload server-side (don't accept from client).
3. **Rate Limiting**: Add rate limits to prevent abuse.
4. **CORS**: Configure CORS for production domains.
5. **Audit Logging**: Log sensitive operations (reads, updates, deletes).
6. **Data Encryption**: Encrypt diary content at rest (optional).

## Performance & Scaling

### Current Limitations
- **Vector Search**: In-memory cosine similarity computation. For 1000+ embeddings, consider Faiss or Milvus.
- **Embeddings**: Uses local sentence-transformers (fast, free). No external API.
- **LLM**: OpenAI API calls for chat. Consider caching common responses or using open models.

### Optimization Tips
1. **Batch Indexing**: Index multiple diaries at once using vectorized operations.
2. **Caching**: Cache LLM responses for frequently asked questions.
3. **Database Indexing**: Ensure indexes on `diary.user_id`, `diary.date`, `diary_vectors.user_id`.
4. **Model Serving**: Use async embeddings if processing many entries.

## Testing

### Manual Testing

**Create a test user**:
```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123"}'
```

**Login**:
```bash
curl -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Create diary entry**:
```bash
curl -X POST http://localhost:8000/diary \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"date":"2025-12-12","content":"Today was a good day!"}'
```

**Index and query**:
```bash
# Index user's diary
curl -X POST http://localhost:8000/rag/index/1

# Ask a question
curl -X POST http://localhost:8000/rag/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"question":"How was my mood?","top_k":5}'
```

## Troubleshooting

### OpenAI Quota Error
- **Issue**: `insufficient_quota` error from OpenAI API.
- **Solution**: Embeddings now use local sentence-transformers (free). Only LLM responses use OpenAI — ensure you have API credit and the key is valid.

### Port Already in Use
- **Backend**: Change port with `--port 8001` in uvicorn command.
- **Frontend**: Change port in `angular.json` or run `ng serve --port 4201`.

### CORS Errors
- Ensure `allow_origins=["*"]` in FastAPI CORS middleware or restrict to frontend domain.

### Missing Embeddings
- If RAG queries fail, run `POST /rag/index/{user_id}` to compute embeddings.
- Ensure sentence-transformers is installed: `pip install sentence-transformers`.

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -m "Add my feature"`
3. Push: `git push origin feature/my-feature`
4. Open a Pull Request

## License

This project is licensed under the MIT License — see LICENSE file for details.

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

---

**HeyBuddy** — Taking care of your mental health, one diary entry at a time. 💙
