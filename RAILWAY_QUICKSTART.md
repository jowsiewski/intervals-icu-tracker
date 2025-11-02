# 🚀 Szybki Deploy na Railway.app

## Krok po kroku (5 minut)

### 1. Przygotuj kod
```bash
# Uruchom skrypt setup (jeśli jeszcze nie masz repo Git)
./git-setup.sh

# Lub ręcznie:
git init
git add .
git commit -m "Initial commit"
```

### 2. Utwórz repozytorium na GitHub
1. Idź na https://github.com/new
2. Nazwa: `intervals-icu-tracker`
3. **NIE** dodawaj README, .gitignore, ani licencji
4. Kliknij "Create repository"

### 3. Wypchnij kod na GitHub
```bash
# Dodaj remote (zamień YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/intervals-icu-tracker.git

git branch -M main
git push -u origin main
```

### 4. Deploy na Railway
1. Idź na https://railway.app
2. Zaloguj się przez GitHub
3. Kliknij **"New Project"**
4. Wybierz **"Deploy from GitHub repo"**
5. Wybierz `intervals-icu-tracker`
6. Railway automatycznie wykryje Dockerfile i zacznie budować!

### 5. Dodaj zmienne środowiskowe
Po zbudowaniu, kliknij na swój projekt → **Variables** → **+ New Variable**

Dodaj:
```
INTERVALS_ICU_API_KEY=3m1tci9dv5zh1yk7v364w3ch4
INTERVALS_ICU_ATHLETE_ID=i36307
DATABASE_URL=sqlite:///./data/activities.db
INTERVALS_ICU_BASE_URL=https://intervals.icu/api/v1
FETCH_INTERVAL_MINUTES=60
```

### 6. Dodaj wolumen dla bazy danych (opcjonalne, ale zalecane)
1. W projekcie Railway kliknij **Settings**
2. Przewiń do **Volumes**
3. Kliknij **+ New Volume**
4. Mount Path: `/app/data`
5. Kliknij **Add**

### 7. Redeploy
1. Kliknij **Deployments**
2. Kliknij **... (menu)** obok ostatniego deployu
3. Wybierz **Redeploy**

### 8. Gotowe! 🎉
1. Kliknij **Settings** → **Networking**
2. Kliknij **Generate Domain**
3. Skopiuj swój URL (np. `your-app.up.railway.app`)
4. Otwórz w przeglądarce!

---

## 🔧 Troubleshooting

**Problem: Build fails**
- Sprawdź logi w Railway Dashboard
- Upewnij się, że wszystkie pliki są w repo (git push)

**Problem: App crashes**
- Sprawdź czy wszystkie zmienne środowiskowe są ustawione
- Zobacz logi: Railway Dashboard → Deployments → View Logs

**Problem: Baza danych się resetuje**
- Dodaj Volume (krok 6 powyżej)
- Lub użyj PostgreSQL (lepsze dla produkcji)

**Problem: 404 Not Found**
- Upewnij się, że PORT nie jest ustawiony ręcznie w zmiennych
- Railway automatycznie ustawia PORT

---

## 💡 Pro Tips

1. **Automatyczny deploy**: Każdy `git push` automatycznie deployuje na Railway!

2. **Monitoring**: Railway pokazuje:
   - CPU usage
   - Memory usage
   - Network traffic
   - Logi w czasie rzeczywistym

3. **Custom domain**: W Settings → Networking możesz dodać własną domenę

4. **PostgreSQL**: Dla produkcji, dodaj PostgreSQL:
   - W Railway: New → Database → PostgreSQL
   - Railway automatycznie ustawi DATABASE_URL
   - Dodaj do requirements.txt: `psycopg2-binary==2.9.9`

---

## 📊 Free Tier Limity

Railway Free Tier:
- ✅ $5 credit miesięcznie
- ✅ ~500 godzin działania
- ✅ Więcej niż wystarczające dla osobistego użytku!

Dla 24/7 uptime: ~$5/miesiąc

---

## 🎯 Twój URL będzie wyglądał tak:

```
https://intervals-icu-tracker-production.up.railway.app
```

Gotowe do użycia z telefonu, komputera, wszędzie! 🌍
