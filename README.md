<div align="center">

# 🎙️ SpeakU

### Real-time language exchange platform — practice languages through voice calls with native speakers worldwide

100% free, peer-to-peer voice calls · Smart language matching · WebRTC-powered · Lingos reward economy

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-4169E1?style=flat&logo=postgresql&logoColor=white)](https://supabase.com/)
[![Redis](https://img.shields.io/badge/Redis-Upstash-DC382D?style=flat&logo=redis&logoColor=white)](https://upstash.com/)
[![WebRTC](https://img.shields.io/badge/WebRTC-Peer%20to%20Peer-333333?style=flat&logo=webrtc&logoColor=white)](https://webrtc.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[🌐 Live Demo](https://speaku-2-o.onrender.com)** · **[📖 API Docs](https://speaku-2-o.onrender.com/docs)** · **[🐛 Report Bug](https://github.com/deepakpandey2004/SpeakU-2.O/issues)** · **[💡 Request Feature](https://github.com/deepakpandey2004/SpeakU-2.O/issues)**

</div>

---

## 📸 Preview

<div align="center">

<table>
  <tr>
    <td align="center"><b>Landing / Sign Up</b></td>
    <td align="center"><b>Home Dashboard</b></td>
  </tr>
  <tr>
    <td><img src="docs/screenshots/landing.png" alt="Landing page" width="450"/></td>
    <td><img src="docs/screenshots/home.png" alt="Home dashboard" width="450"/></td>
  </tr>
  <tr>
    <td align="center"><b>Finding a Match</b></td>
    <td align="center"><b>Live Voice Call</b></td>
  </tr>
  <tr>
    <td><img src="docs/screenshots/call.png" alt="Match finding" width="450"/></td>
    <td><img src="docs/screenshots/call.jpeg" alt="Voice call" width="450"/></td>
  </tr>
</table>

</div>

> 📌 Screenshots coming soon. See the [**Live Demo**](https://speaku-2-o.onrender.com) for the full experience.

---

## 🌟 Overview

**SpeakU** is a production-grade language exchange platform inspired by [Lingbe](https://www.lingbe.com/), enabling users to practice foreign languages through **real-time voice calls with native speakers**. Built on **FastAPI**, **WebRTC**, and **WebSocket**, it delivers seamless peer-to-peer voice calling **without relying on any paid third-party calling infrastructure**.

---

## ✨ Features

### 🔐 Authentication & Profiles
- **Email-validated registration** with password strength checks
- **JWT-based secure authentication** with bcrypt password hashing
- **Editable user profile** — username, native language, learning language, bio
- **Lingos welcome bonus** on signup

### 🎯 Real-Time Matchmaking
- **WebSocket-based live matching engine** — instant partner discovery
- **Complementary language pairing** (e.g., Hindi speaker learning English ↔ English speaker learning Hindi)
- **Redis-powered waiting pool** with 60-second timeout and retry logic
- **Fair-queue algorithm** — first-come, first-served matching

### 🎙️ Peer-to-Peer Voice Calling (WebRTC)
- **Direct P2P audio streaming** via free Google STUN servers
- **Zero server bandwidth cost** — audio never touches our servers
- **Echo cancellation** and **noise suppression** built-in
- **Mute/unmute controls** with live call duration tracking
- **Automatic reconnection** on temporary network drops

### ⭐ Ratings & Rewards
- **5-star post-call rating** with optional written feedback
- **Lingos currency rewards** per completed call (encourages engagement)
- **Leaderboard** highlighting top-rated users
- **Call history** with rating stats

### 🎨 Responsive UI
- **Mobile-first design** — works flawlessly on phones, tablets, desktops
- **Clean vanilla JS frontend** — no framework overhead
- **Smooth transitions** between match / call / rating flows
- **Real-time UI updates** driven by WebSocket events

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       CLIENT (Browser)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  HTML/CSS    │  │  Vanilla JS  │  │  WebRTC + WS     │  │
│  │  Responsive  │  │  Async APIs  │  │  Media Devices   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────┬───────────────────────────────────┬───────────────┘
          │ HTTPS + WSS                       │ Peer-to-Peer
          ▼                                   ▼ (WebRTC audio)
┌───────────────────────────────────┐  ┌──────────────────┐
│         FASTAPI BACKEND           │  │   Other User's   │
│  ┌───────┐ ┌───────┐ ┌─────────┐  │  │     Browser      │
│  │ Auth  │ │Profile│ │ Match   │  │  └──────────────────┘
│  │  API  │ │  API  │ │  (WS)   │  │
│  └───────┘ └───────┘ └─────────┘  │
│  ┌────────────┐ ┌──────────────┐  │
│  │ Signaling  │ │  Call/Rating │  │
│  │   (WS)     │ │     API      │  │
│  └────────────┘ └──────────────┘  │
└──────┬─────────────────────┬──────┘
       │                     │
       ▼                     ▼
┌──────────────┐    ┌──────────────────┐
│  PostgreSQL  │    │      Redis       │
│  (Supabase)  │    │    (Upstash)     │
│              │    │  Match queue +   │
│  Users, Calls│    │  Active sessions │
└──────────────┘    └──────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (async Python web framework)
- **Database:** PostgreSQL via [Supabase](https://supabase.com/) (serverless)
- **Cache & Queue:** Redis via [Upstash](https://upstash.com/) (serverless)
- **ORM:** SQLAlchemy 2.0
- **Real-time:** WebSocket (matchmaking + WebRTC signaling)
- **Auth:** JWT (python-jose) + bcrypt password hashing
- **Validation:** Pydantic v2
- **ASGI Server:** Uvicorn

### Frontend
- **Markup:** HTML5, CSS3
- **Interactivity:** Vanilla JavaScript (ES6+)
- **Voice:** WebRTC API (getUserMedia + RTCPeerConnection)
- **Real-time:** WebSocket API
- **Design:** Mobile-first responsive layout

### DevOps
- **Containerization:** Docker + Docker Compose
- **Cloud Hosting:** Render (auto-deploy from GitHub)
- **Database Hosting:** Supabase (managed PostgreSQL)
- **Cache Hosting:** Upstash (serverless Redis)
- **STUN Server:** Google (`stun:stun.l.google.com:19302`) — free

---

## 📂 Project Structure

```
speaku-2.0/
├── app/                          # FastAPI application
│   ├── api/                      # Route handlers
│   │   ├── auth.py               # /auth/* — register, login, me
│   │   ├── profile.py            # /profile/* — get, update profile
│   │   ├── match.py              # /match/find — WebSocket matchmaking
│   │   ├── signaling.py          # /signaling/* — WebRTC SDP/ICE exchange
│   │   ├── call.py               # /call/* — call lifecycle (end, timeout)
│   │   └── rating.py             # /rating/* — submit + fetch ratings
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── call.py
│   │   └── rating.py
│   ├── schemas/                  # Pydantic request/response schemas
│   ├── utils/                    # Helpers
│   │   ├── jwt_helper.py         # Token creation + verification
│   │   ├── redis_client.py       # Upstash Redis wrapper
│   │   └── security.py           # bcrypt hashing
│   ├── config.py                 # Environment settings
│   ├── extensions.py             # DB + Redis initialization
│   └── dependencies.py           # FastAPI dependency injection
├── frontend/                     # Static client
│   ├── index.html                # Landing / register / login
│   ├── home.html                 # Dashboard after login
│   ├── match.html                # Match-finding screen
│   ├── call.html                 # Live voice call UI
│   ├── profile.html              # Profile editor
│   ├── css/                      # Stylesheets
│   └── js/
│       ├── auth.js               # Login/register logic
│       ├── match.js              # Match WebSocket client
│       ├── webrtc.js             # WebRTC peer connection
│       └── call.js               # Call controls (mute, end, rating)
├── tests/                        # Pytest test suite
├── docs/screenshots/             # UI screenshots for README
├── Dockerfile                    # Production Docker image
├── docker-compose.yml            # Local dev (app + optional local Redis)
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── run.py                        # Application entry point
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Docker Desktop** (recommended for easy setup)
- **Supabase account** — free-tier PostgreSQL ([signup](https://supabase.com/))
- **Upstash account** — free-tier Redis ([signup](https://upstash.com/))
- **Git**

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/deepakpandey2004/SpeakU-2.O.git
cd SpeakU-2.O

# Copy and fill environment variables
cp .env.example .env
# Edit .env — add DATABASE_URL, REDIS_URL, REDIS_TOKEN, JWT_SECRET_KEY

# Build and run
docker build -t speaku:latest .
docker run -p 8000:8000 --env-file .env --name speaku speaku:latest

# App runs at:
# → http://localhost:8000
```

### Option 2: Local Python Setup

```bash
# Clone and enter directory
git clone https://github.com/deepakpandey2004/SpeakU-2.O.git
cd SpeakU-2.O

# Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Supabase + Upstash credentials

# Start the server
python run.py

# Visit in browser:
# → http://localhost:8000
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
# App
APP_NAME=SpeakU
APP_VERSION=2.0.0
DEBUG=True
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# Database (Supabase PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Redis (Upstash)
REDIS_URL=https://your-redis-url.upstash.io
REDIS_TOKEN=your_redis_token

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
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

> 💡 **Tip:** Generate a strong `JWT_SECRET_KEY` with `python -c "import secrets; print(secrets.token_urlsafe(48))"`

---

## 📖 API Documentation

Interactive API docs are auto-generated by FastAPI:

- **Swagger UI:** [/docs](https://speaku-2-o.onrender.com/docs)
- **ReDoc:** [/redoc](https://speaku-2-o.onrender.com/redoc)

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register a new user account |
| `POST` | `/auth/login` | Login and receive JWT token |
| `GET`  | `/auth/me` | Get current authenticated user |
| `GET`  | `/profile/me` | Get my profile |
| `PUT`  | `/profile/update` | Update profile (languages, bio) |
| `WS`   | `/match/find` | WebSocket for real-time matchmaking |
| `WS`   | `/signaling/signal/{room_id}` | WebRTC SDP/ICE signaling |
| `POST` | `/call/end/{room_id}` | End an active call |
| `POST` | `/rating/submit` | Submit post-call rating |
| `GET`  | `/rating/leaderboard` | Top-rated users |

---

## 🎯 How It Works

### 1. User Journey

```
Landing → Register → Profile Setup → Home Dashboard
                                          ↓
              Find Match → Match Found → Voice Call → Rating → Home
```

### 2. Matching Algorithm

```
User A: Speaks Hindi, Learning English
User B: Speaks English, Learning Hindi

Redis Waiting Pool:
  Key: "waiting:English:Hindi" → User A queued
  Key: "waiting:Hindi:English" → User B queued

When B joins, algorithm checks "waiting:Hindi:English"
  → finds User A → instant match ✅

Both users receive room_id via WebSocket → proceed to call.
```

### 3. WebRTC Call Flow

```
1. Both users join a signaling room via WebSocket
2. User A creates an SDP Offer → sent through signaling channel
3. User B receives Offer → creates SDP Answer → sends back
4. ICE candidates exchanged for NAT traversal
5. Peer-to-peer audio connection established directly
6. Voice flows browser-to-browser — server bandwidth = 0
```

---

## 🧪 Testing

```bash
# With Docker
docker exec speaku pytest

# Locally
pytest tests/ -v
```

**Manual end-to-end test:**
1. Open two browser windows (one normal, one incognito)
2. Register two users with complementary languages
3. Click **"Find Match"** on both
4. Grant microphone permission when prompted
5. Voice call establishes automatically 🎉

---

## 🔒 Security Highlights

- ✅ **Passwords hashed** with bcrypt (12 rounds)
- ✅ **JWT tokens** with configurable expiry
- ✅ **Pydantic validation** on every request body
- ✅ **SQL injection prevention** via SQLAlchemy ORM
- ✅ **Environment secrets** — never committed to repo
- ✅ **CORS restrictions** in production
- ✅ **HTTPS + WSS** enforced on Render (production)

---

## ☁️ Deployment (Render)

SpeakU is deployed as a Render **Web Service**:

| Setting | Value |
|---------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn run:app --host 0.0.0.0 --port $PORT` |
| **Environment** | Python 3.11 |
| **Env Vars** | Same as `.env.example`, set via Render Dashboard |

WebSocket connections work out of the box on Render — no extra configuration needed. In production, browser automatically uses `wss://` (secure WebSocket) instead of `ws://`.

---

## 🚧 Roadmap

- [ ] Video calling support
- [ ] Group practice rooms (3-5 users)
- [ ] AI-powered conversation topics & prompts
- [ ] Language proficiency tests
- [ ] Native mobile apps (iOS + Android)
- [ ] Friends system & persistent chat history
- [ ] Premium features (unlimited calls, priority matching)
- [ ] Multi-language UI (i18n)
- [ ] TURN server integration for restrictive networks

---

## 🐛 Known Issues

- WebRTC may fail on **restrictive/corporate networks** — currently STUN-only. TURN server integration planned.
- **iOS Safari** requires HTTPS for microphone access in production (works fine on Render).
- **Free-tier Render** cold-starts after 15 min inactivity — first request may take 30-60 sec.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## 👨‍💻 Author

**Deepak Pandey**

- 🌐 **GitHub:** [@deepakpandey2004](https://github.com/deepakpandey2004)
- 💼 **LinkedIn:** [@deepakpandey12](https://www.linkedin.com/in/deepakpandey12)
- 📧 **Email:** deepakpandey4002@gmail.com

---

## 🙏 Acknowledgments

- Inspired by **[Lingbe](https://www.lingbe.com/)** — the original language exchange app
- **WebRTC** implementation guided by [MDN WebRTC docs](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API)
- **Free STUN servers** by Google
- **Free-tier hosting** by [Render](https://render.com/), [Supabase](https://supabase.com/), and [Upstash](https://upstash.com/)

---

## 💡 What This Project Demonstrates

Hands-on production experience with:

- ✅ **Async backend development** — FastAPI, Python asyncio, WebSockets
- ✅ **Real-time systems** — WebRTC peer-to-peer, WebSocket signaling
- ✅ **Database design** — relational schemas, migrations, SQLAlchemy ORM
- ✅ **Caching & queuing** — Redis for high-performance matchmaking
- ✅ **Authentication** — JWT tokens, bcrypt hashing, secure session flow
- ✅ **Containerization** — Docker, environment isolation
- ✅ **API design** — RESTful endpoints + WebSocket protocols
- ✅ **Cloud deployment** — Render + Supabase + Upstash integration
- ✅ **Full-stack integration** — end-to-end feature delivery

---

<div align="center">

**⭐ If you found this project useful, please give it a star!**

Made with ❤️ and lots of ☕ by [Deepak Pandey](https://github.com/deepakpandey2004)

**🔗 [Try SpeakU Live →](https://speaku-2-o.onrender.com)**

</div>
