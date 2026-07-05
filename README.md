# 🎙️ SpeakU v2.0 — Real-Time Language Exchange Platform

<div align="center">

![SpeakU Banner](https://img.shields.io/badge/SpeakU-v2.0-a855f7?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0xMiAydjEwbDkgNXYtN2wtOS04eiIvPjwvc3ZnPg==)

**Practice languages through real voice calls with native speakers worldwide — 100% Free!**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.137-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?style=flat&logo=postgresql&logoColor=white)](https://supabase.com)
[![Redis](https://img.shields.io/badge/Redis-Upstash-DC382D?style=flat&logo=redis&logoColor=white)](https://upstash.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![WebRTC](https://img.shields.io/badge/WebRTC-Enabled-333333?style=flat&logo=webrtc&logoColor=white)](https://webrtc.org)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

 · [Report Bug](https://github.com/deepakpandey2004/speaku/issues) · [Request Feature](https://github.com/deepakpandey2004/speaku/issues)

</div>

---

## 🌟 Overview

**SpeakU** is a production-grade language exchange platform inspired by Lingbe, enabling users to practice foreign languages through **real-time voice calls** with native speakers. Built on **FastAPI**, **WebRTC**, and **WebSocket**, it delivers seamless peer-to-peer voice calling without relying on any paid third-party calling infrastructure.

### ✨ Key Highlights

| | |
|---|---|
| 🎙️ **Real Voice Calls** | Peer-to-peer WebRTC audio — zero server bandwidth cost |
| 🌍 **Smart Matching** | Instant partner pairing based on complementary languages |
| ⚡ **Real-Time Signaling** | WebSocket-driven matchmaking & call setup |
| 💎 **Lingos Economy** | In-app reward currency to drive engagement |
| 🔒 **Secure Auth** | JWT-based authentication with bcrypt password hashing |
| 🐳 **Containerized** | Fully Dockerized for reproducible deployments |
| 📱 **Responsive UI** | Mobile-first design, works across all devices |

---

## 🛠️ Tech Stack

**Backend:** FastAPI · SQLAlchemy · PostgreSQL (Supabase) · Redis (Upstash) · WebSocket · JWT (python-jose) · Bcrypt · Pydantic

**Frontend:** HTML5 · CSS3 · Vanilla JavaScript · WebRTC API · WebSocket API

**DevOps:** Docker · Docker Compose · Uvicorn (ASGI) · Render (hosting)

---

## 🚀 Features

### 🔐 Authentication & Profiles
- Email-validated registration with password strength checks
- JWT-based secure authentication
- Editable profile: username, native language, learning language, bio

### 🎯 Real-Time Matchmaking
- WebSocket-based live matching engine
- Complementary language pairing (e.g. Hindi speaker learning English ↔ English speaker learning Hindi)
- Redis-powered waiting pool with 60-second timeout and retry

### 🎙️ Voice Calling (WebRTC)
- Peer-to-peer audio streaming via free Google STUN servers
- Echo cancellation and noise suppression
- Mute/unmute controls and live call duration tracking

### ⭐ Ratings & Rewards
- 5-star post-call rating with optional feedback
- Lingos currency rewards per completed call
- Leaderboard for top-rated users

---

## 📁 Project Structure

```
SpeakU-2.0/
├── app/
│   ├── api/            # Route handlers (auth, profile, match, signaling, call, rating)
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic validation schemas
│   ├── utils/           # JWT helpers, Redis client
│   ├── config.py        # App configuration
│   ├── extensions.py    # DB & Redis initialization
│   └── dependencies.py  # FastAPI dependencies
├── frontend/            # HTML/CSS/JS client
├── tests/                # Test suite
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── run.py               # Application entry point
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.11+
- Docker Desktop (recommended)
- A [Supabase](https://supabase.com) project (free tier works)
- An [Upstash](https://upstash.com) Redis instance (free tier works)

### Option 1 — Run with Docker

```bash
git clone https://github.com/deepakpandey2004/speaku.git
cd speaku

cp .env.example .env
# Fill in DATABASE_URL, REDIS_URL, REDIS_TOKEN, JWT_SECRET_KEY

docker build -t speaku-app .
docker run -p 8000:8000 --env-file .env --name speaku speaku-app
```

Visit `http://localhost:8000` 🎉

### Option 2 — Run Locally

```bash
git clone https://github.com/deepakpandey2004/speaku.git
cd speaku

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
cp .env.example .env         # then edit with your credentials

python run.py
```

Visit `http://localhost:8000` 🎉

---

## 🔑 Environment Variables

```env
# App
APP_NAME=SpeakU
APP_VERSION=2.0.0
DEBUG=True
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# Database (Supabase)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Redis (Upstash)
REDIS_URL=https://your-redis-url.upstash.io
REDIS_TOKEN=your_redis_token

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Security
BCRYPT_ROUNDS=12

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# WebRTC
STUN_SERVER=stun:stun.l.google.com:19302

# Lingos Economy
LINGOS_NEW_USER_BONUS=10
LINGOS_PER_CALL_COST=1
LINGOS_PER_CALL_REWARD=5
```

---

## ☁️ Deployment (Render)

SpeakU is deployed as a **Render Web Service**:

| Setting | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn run:app --host 0.0.0.0 --port $PORT` |
| Environment | Python 3.11 |
| Env Vars | Same as `.env.example`, set via Render Dashboard |

> WebSocket connections work out of the box on Render — no extra configuration needed. In production, use `wss://` instead of `ws://`.

---

## 📚 API Documentation

Once running, interactive docs are available at:

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login user |
| GET | `/auth/me` | Get current user info |
| GET | `/profile/me` | Get my profile |
| PUT | `/profile/update` | Update profile |
| WS | `/match/find` | Find match (WebSocket) |
| WS | `/signaling/signal/{room_id}` | WebRTC signaling |
| POST | `/call/end/{room_id}` | End active call |
| POST | `/rating/submit` | Submit rating |

---

## 🎯 How It Works

**1. User Journey**
```
Landing Page → Register → Profile Setup → Home Dashboard
     ↓
Find Match → Match Found → Voice Call → Rating → Home
```

**2. Matching Algorithm**
```
User A: Speaks Hindi, Learning English
User B: Speaks English, Learning Hindi

Redis Waiting Pool:
- Key: "waiting:English:Hindi" → User A
- Key: "waiting:Hindi:English" → User B

When A joins, checks "waiting:English:Hindi"
When B joins, checks "waiting:Hindi:English"
→ Instant match 🎯
```

**3. WebRTC Call Flow**
```
1. Both users join a signaling room via WebSocket
2. User A creates an SDP Offer → sent through signaling
3. User B receives Offer → creates Answer → sends back
4. ICE candidates exchanged for NAT traversal
5. Peer-to-peer audio connection established
6. Voice flows directly between users — no server relay
```

---

## 🧪 Testing

```bash
# With Docker
docker exec speaku pytest

# Locally
pytest tests/
```

**Manual test:** open two browser windows (one normal, one incognito), register two users with complementary languages, click "Find Match" on both, grant mic permission, and start the call.

---

## 🚧 Roadmap

- [ ] Video calling support
- [ ] Group practice rooms
- [ ] AI-powered conversation topics
- [ ] Language proficiency tests
- [ ] Mobile apps (iOS & Android)
- [ ] Friends system & chat history
- [ ] Premium features
- [ ] Multi-language UI

---

## 🐛 Known Issues

- WebRTC may require a TURN server on restrictive/corporate networks (currently STUN-only)
- iOS Safari requires HTTPS for microphone access in production

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📜 License

Licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Deepak Pandey**

- GitHub: [@deepakpandey2004](https://github.com/deepakpandey2004)
- LinkedIn: [deepakpandey12](https://linkedin.com/in/deepakpandey12)

---

## 🙏 Acknowledgments

- Inspired by [Lingbe](https://lingbe.com) — the original language exchange app
- WebRTC implementation guided by [MDN WebRTC docs](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)
- Free STUN servers by Google
- Free-tier hosting by Supabase and Upstash

---

## 💡 Learning Outcomes

This project demonstrates hands-on experience with:

✅ Backend development — FastAPI, async programming, WebSockets
✅ Database design — relational schemas, migrations, ORM
✅ Real-time systems — WebSocket, WebRTC, peer-to-peer connections
✅ Caching — Redis for high-performance matchmaking
✅ Authentication — JWT tokens, bcrypt hashing
✅ Containerization — Docker, Docker Compose
✅ API design — RESTful principles, WebSocket protocols
✅ Cloud deployment — Render Web Service configuration
✅ Full-stack integration — end-to-end feature delivery

<div align="center">

⭐ **If you found this project useful, please give it a star!**

Made with ❤️ and lots of ☕

</div>
