# UTOPAI Backend Deployment Guide

## Railway Deployment - Dag 1

### 1. Opret Railway Konto
1. Gå til [railway.app](https://railway.app)
2. Sign up med GitHub konto
3. Verify email

### 2. Opret Nyt Projekt
1. Klik "New Project"
2. Vælg "Deploy from GitHub repo"
3. Connect GitHub og vælg UTOPAI repository
4. Vælg `/backend` folder som root

### 3. Konfigurer Environment Variables
I Railway dashboard:
```
FLASK_ENV=production
SECRET_KEY=utopai-secret-key-2024-super-secure
OPENAI_API_KEY=your_actual_openai_api_key
```

### 4. Deploy Settings
Railway auto-detecter Python og bruger:
- `requirements.txt` for dependencies
- `Procfile` for start command
- `runtime.txt` for Python version

### 5. Test Deployment
Efter deployment, test endpoints:
- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `GET /api/islands` - API test

### 6. Få Railway URL
Railway giver dig en URL som:
`https://utopai-backend-production.up.railway.app`

## Næste Steps (Dag 2)
- Setup PostgreSQL database
- Migrate data fra SQLite
- Test database connectivity

## Troubleshooting
- Check Railway logs for errors
- Verify environment variables
- Ensure all dependencies in requirements.txt

