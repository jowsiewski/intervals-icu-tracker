# Intervals.icu Activity Tracker

Aplikacja FastAPI do pobierania i zarządzania aktywnościami z serwisu Intervals.icu.

## Funkcjonalności

- 🚴‍♀️ **Pobieranie aktywności** z Intervals.icu API
- 📊 **Przechowywanie danych** w lokalnej bazie SQLite
- 🔄 **Automatyczna synchronizacja** w tle
- 🛠️ **REST API** do zarządzania danymi
- 📱 **Przygotowane do integracji** z aplikacją mobilną
- 📝 **Automatyczna dokumentacja** API (Swagger/OpenAPI)

## Szybki start

### 1. Instalacja

```bash
# Klonuj repozytorium
git clone <repo-url>
cd appka

# Stwórz środowisko wirtualne
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# lub
venv\Scripts\activate  # Windows

# Zainstaluj zależności
pip install -r requirements.txt
```

### 2. Konfiguracja

Skopiuj plik `.env.example` do `.env` i skonfiguruj:

```bash
cp .env.example .env
```

Edytuj `.env` i wprowadź swoje dane:

```env
# Twoje dane dostępowe do Intervals.icu
INTERVALS_ICU_API_KEY=your_api_key_here
INTERVALS_ICU_ATHLETE_ID=your_athlete_id_here

# Pozostałe ustawienia można zostawić domyślne
DATABASE_URL=sqlite:///./activities.db
FETCH_INTERVAL_MINUTES=60
```

### 3. Uruchomienie

```bash
# Aktywuj środowisko wirtualne
source venv/bin/activate

# Uruchom serwer
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Aplikacja będzie dostępna pod adresem: http://localhost:8000

## API Endpoints

### Dokumentacja API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Główne endpointy

#### Health Check
- `GET /api/v1/health` - Status aplikacji
- `GET /api/v1/health/intervals` - Test połączenia z Intervals.icu

#### Aktywności
- `GET /api/v1/activities` - Lista aktywności
  - Query params: `skip`, `limit`, `activity_type`, `start_date`, `end_date`
- `GET /api/v1/activities/{id}` - Szczegóły aktywności
- `PUT /api/v1/activities/{id}` - Aktualizacja aktywności
- `DELETE /api/v1/activities/{id}` - Usunięcie aktywności
- `GET /api/v1/activities/summary` - Statystyki aktywności
- `POST /api/v1/activities/sync` - Ręczna synchronizacja

## Struktura projektu

```
appka/
├── app/
│   ├── __init__.py
│   ├── main.py              # Główna aplikacja FastAPI
│   ├── config.py            # Konfiguracja
│   ├── database.py          # Modele bazy danych
│   ├── scheduler.py         # Zadania w tle
│   ├── routers/             # Endpointy API
│   │   ├── activities.py
│   │   └── health.py
│   ├── schemas/             # Schematy Pydantic
│   │   └── activity.py
│   └── services/            # Logika biznesowa
│       ├── activity_service.py
│       └── intervals_client.py
├── requirements.txt         # Zależności Python
├── .env.example            # Przykład konfiguracji
├── .gitignore              # Ignorowane pliki
└── README.md               # Ten plik
```

## Rozwój

### Testowanie
```bash
pytest
```

### Dodawanie nowych funkcji
1. Dodaj modele w `app/database.py`
2. Stwórz schematy w `app/schemas/`
3. Zaimplementuj logikę w `app/services/`
4. Dodaj endpointy w `app/routers/`
5. Zaktualizuj testy

### Migracje bazy danych
Projekt używa Alembic do zarządzania migracjami:

```bash
# Stwórz nową migrację
alembic revision --autogenerate -m "Description"

# Zastosuj migracje
alembic upgrade head
```

## Integracja z aplikacją mobilną

API zostało zaprojektowane z myślą o łatwej integracji z aplikacjami mobilnymi:

- **RESTful API** ze standardowymi metodami HTTP
- **JSON** jako format wymiany danych
- **Paginacja** dla dużych zbiorów danych
- **Filtrowanie** po typie aktywności i datach
- **CORS** skonfigurowany dla cross-origin requests

### Przykład użycia w aplikacji mobilnej

```javascript
// Pobierz ostatnie 10 aktywności
const response = await fetch('http://localhost:8000/api/v1/activities?limit=10');
const activities = await response.json();

// Pobierz statystyki
const summary = await fetch('http://localhost:8000/api/v1/activities/summary');
const stats = await summary.json();
```

## 🚀 Deployment do Chmury

Aplikacja jest gotowa do wdrożenia w chmurze! Sprawdź [DEPLOYMENT.md](DEPLOYMENT.md) dla szczegółowych instrukcji.

### Szybkie linki:
- 🌟 **Railway.app** (zalecane) - [railway.app](https://railway.app)
- 🎨 **Render.com** - [render.com](https://render.com)
- ✈️ **Fly.io** - [fly.io](https://fly.io)

### Przygotowane pliki:
- ✅ `Dockerfile` - Gotowy obraz Docker
- ✅ `Procfile` - Dla platform PaaS
- ✅ `railway.json` - Konfiguracja Railway
- ✅ `fly.toml` - Konfiguracja Fly.io

## Licencja

MIT License