# 🌍 StalkerApp — Real-Time Location Sharing & Chat

**StalkApp** — это веб-приложение, позволяющее пользователям делиться своей геолокацией в реальном времени, видеть друзей на интерактивной карте, обмениваться сообщениями и договариваться о встречах. Идеально подходит для встреч в городе, поиска друзей на фестивалях, конференциях или просто для совместных прогулок.

---

## 🚀 Основные возможности

- 📍 **Реальное время**: ваши друзья видят ваше местоположение на карте с обновлением каждые 15 секунд  
- 👥 **Система дружбы**: только добавленные вами пользователи могут видеть вашу геопозицию  
- 💬 **Чат 1:1**: встроенный мессенджер для общения с друзьями  
- 🔒 **Приватность**: геолокация передаётся только с вашего разрешения и только друзьям  
- 🗺️ **Интерактивная карта**: современный UI на базе Mapbox GL JS  

---

## 🛠️ Технологии

### Frontend (Next.js)
- **Next.js 14** (App Router)
- **React 18**
- **TypeScript**
- **Mapbox GL JS** — интерактивная карта
- **Socket.IO Client** — WebSocket-соединение
- **Tailwind CSS** — стилизация
- **NextAuth.js** — аутентификация

### Backend (FastAPI)
- **FastAPI** — высокопроизводительный Python-фреймворк
- **WebSocket** — реалтайм-обмен геоданными
- **PostgreSQL** — хранение пользователей, дружбы, сообщений
- **Redis** — кэширование онлайн-статусов и координат
- **JWT** — безопасная авторизация
- **SQLAlchemy** — ORM для работы с БД

### Инфраструктура
- **Docker & Docker Compose** — локальная разработка
- **Nginx** — проксирование WebSocket
- **Vercel** (frontend) + **Render / Railway** (backend) — деплой

---

## 📦 Установка и запуск (локально)

### Требования
- Docker и Docker Compose
- Node.js ≥ 18
- Python ≥ 3.10

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/your-username/meetnear.git
cd meetnear
```

### 2. Настройка переменных окружения

Создайте файлы `.env.local` (в `frontend/`) и `.env` (в `backend/`):

**`frontend/.env.local`**
```env
NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN=ваш_mapbox_токен
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=секретный_ключ
```

**`backend/.env`**
```env
DATABASE_URL=postgresql://user:password@db:5432/meetnear
REDIS_URL=redis://redis:6379/0
JWT_SECRET_KEY=секретный_jwt_ключ
MAPBOX_ACCESS_TOKEN=ваш_mapbox_токен
```

> 💡 Получите бесплатный [Mapbox Access Token](https://account.mapbox.com/access-tokens/)

### 3. Запуск через Docker Compose
```bash
docker-compose up --build
```

Приложение будет доступно по адресу:
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)

### 4. (Опционально) Запуск без Docker

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
# или venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

---

> ⚠️ **Важно**: Геолокация — чувствительные данные. Приложение **никогда** не хранит историю перемещений. Координаты хранятся только в памяти (Redis) и удаляются при отключении пользователя.