# UTOPAI Database Setup Guide - Dag 2

## PostgreSQL på Railway

### 1. Tilføj PostgreSQL til Railway Projekt
1. Gå til dit Railway projekt dashboard
2. Klik "New Service" → "Database" → "PostgreSQL"
3. Railway opretter automatisk database og sætter `DATABASE_URL` environment variable

### 2. Verificer Database Connection
Railway sætter automatisk:
```
DATABASE_URL=postgresql://postgres:password@host:port/database
```

### 3. Database Migration Options

#### Option A: Fresh Start (Anbefalet)
Hvis du ikke har vigtig data i SQLite:
```bash
# Railway vil automatisk køre database initialization
# når appen starter første gang
```

#### Option B: Migrate Existing Data
Hvis du har data i SQLite du vil beholde:

**Lokalt:**
```bash
# Export data fra SQLite
python migrate_to_postgresql.py export

# Upload export fil til Railway (via GitHub)
```

**På Railway:**
```bash
# Import data til PostgreSQL
python migrate_to_postgresql.py import
```

### 4. Database Initialization
Backend kører automatisk `database_init.py` første gang:
- Opretter alle tabeller
- Seeder øer og aktiviteter
- Opretter badges
- Opretter test brugere

### 5. Test Database
Efter deployment, test endpoints:
```bash
# Test database connectivity
curl https://your-app.railway.app/api/islands

# Test user creation
curl -X POST https://your-app.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","username":"test","password":"test123","user_type":"child"}'
```

### 6. Database Schema
**Tabeller:**
- `users` - Bruger information
- `islands` - Øer (Ø 1, Ø 2, etc.)
- `activities` - Aktiviteter på hver ø
- `badges` - Tilgængelige badges
- `user_progress` - Bruger fremskridt
- `user_badges` - Optjente badges

### 7. Troubleshooting

**Connection Issues:**
- Verificer `DATABASE_URL` er sat korrekt
- Check Railway logs for database errors
- Ensure PostgreSQL service er running

**Migration Issues:**
- Check file permissions på migration scripts
- Verify SQLite database exists før export
- Check PostgreSQL connection før import

## Næste Steps (Dag 3)
- Test alle API endpoints
- Verificer OpenAI integration
- Test gamification system
- Debug eventuelle fejl

