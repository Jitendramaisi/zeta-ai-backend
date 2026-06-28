# Zeta AI Backend 🚀

A complete AI chat backend with user authentication, conversation history, and Google Gemini integration.

## Features

✅ **User Authentication** - Secure signup/login with JWT tokens  
✅ **Conversation Management** - Save and retrieve chat history  
✅ **AI Chat** - Powered by Google Gemini 2.5 Flash  
✅ **Database** - SQLite with SQLAlchemy ORM  
✅ **Error Handling** - Comprehensive logging and error responses  
✅ **Docker Support** - Easy deployment with Docker & Docker Compose  
✅ **CORS Enabled** - Ready for frontend integration  

## Tech Stack

- **Framework:** Flask 3.0
- **Database:** SQLite + SQLAlchemy
- **Authentication:** JWT (Flask-JWT-Extended)
- **AI:** Google Gemini API (google-genai)
- **Container:** Docker & Docker Compose

## Setup

### 1. Clone and Install

```bash
git clone https://github.com/Jitendramaisi/zeta-ai-backend.git
cd zeta-ai-backend
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` and add:
- `GEMINI_API_KEY` - Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- `JWT_SECRET_KEY` - Any random secret string

### 3. Run Locally

```bash
python app.py
```

Server starts at `http://localhost:5000`

### 4. Run with Docker

```bash
docker-compose up -d
```

## API Endpoints

### Authentication

#### Sign Up
```bash
POST /api/auth/signup
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}

# Response:
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

#### Get Current User
```bash
GET /api/auth/me
Authorization: Bearer {access_token}
```

### Chat

#### Send Message
```bash
POST /api/chat/send
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "message": "What is machine learning?",
  "conversation_id": null  // Optional - create new if null
}

# Response:
{
  "conversation_id": 1,
  "user_message": "What is machine learning?",
  "ai_reply": "Machine learning is...",
  "messages": [...]
}
```

#### Get All Conversations
```bash
GET /api/chat/conversations
Authorization: Bearer {access_token}
```

#### Get Specific Conversation
```bash
GET /api/chat/conversations/{conversation_id}
Authorization: Bearer {access_token}
```

#### Delete Conversation
```bash
DELETE /api/chat/conversations/{conversation_id}
Authorization: Bearer {access_token}
```

### Health Check
```bash
GET /api/health
```

## Project Structure

```
.
├── app.py                 # Flask application factory & entry point
├── config.py              # Configuration for different environments
├── models.py              # Database models (User, Conversation, Message)
├── auth.py                # Authentication routes (signup, login)
├── chat.py                # Chat routes (send, history)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── logs/                  # Application logs
└── zeta_ai.db            # SQLite database (generated)
```

## Usage Example

```bash
# 1. Sign up
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"pass123"}'

# 2. Login
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}' | jq -r .access_token)

# 3. Send Chat Message
curl -X POST http://localhost:5000/api/chat/send \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello AI!"}'
```

## Deployment

### Deploy to Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key
heroku config:set JWT_SECRET_KEY=your_secret

# Deploy
git push heroku enhanced-backend:main
```

### Deploy to AWS/DigitalOcean

Use Docker to deploy:
```bash
# Build image
docker build -t zeta-ai-backend .

# Push to registry
docker push your-registry/zeta-ai-backend

# Run container
docker run -d -p 5000:5000 \
  -e GEMINI_API_KEY=your_key \
  -e JWT_SECRET_KEY=your_secret \
  zeta-ai-backend
```

## Logs

Logs are stored in `logs/zeta_ai.log`. Check them for debugging:

```bash
tail -f logs/zeta_ai.log
```

## Database

### Reset Database

```bash
rm zeta_ai.db
python app.py
```

## Troubleshooting

**Q: Getting "GEMINI_API_KEY not set" error?**  
A: Make sure you've created `.env` file and set `GEMINI_API_KEY`

**Q: Database locked error?**  
A: Restart the application. SQLite has limitations for concurrent access.

**Q: Port 5000 already in use?**  
A: Change port in `.env`: `SERVER_PORT=5001`

## Next Steps

- [ ] Add conversation titles/summaries
- [ ] Implement rate limiting
- [ ] Add message search
- [ ] Build React Native APK frontend
- [ ] Add Redis caching
- [ ] Implement WebSocket for real-time chat

## License

MIT License

## Support

For issues and questions, create an issue on GitHub.
