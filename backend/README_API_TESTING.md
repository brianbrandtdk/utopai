# UTOPAI API Testing Guide - Dag 3

## API Testing & Environment Validation

### 1. Environment Validation
Før deployment, valider environment setup:

```bash
# Validate all environment variables
python environment_setup.py

# Check output for errors and warnings
# Fix any issues before proceeding
```

**Expected Environment Variables:**
```bash
DATABASE_URL=postgresql://...     # Railway provides this
OPENAI_API_KEY=sk-...            # Your OpenAI API key
FLASK_ENV=production
SECRET_KEY=your-secret-key
PORT=5000                        # Railway provides this
```

### 2. OpenAI Integration Testing
Test AI functionality before deployment:

```bash
# Test OpenAI API connectivity
python openai_test.py

# Should test:
# - Basic API connection
# - Activity 1 AI functions
# - Activity 2 AI functions  
# - Theme personalization
```

### 3. API Endpoints Testing
After deployment, test all endpoints:

```bash
# Test deployed API
python test_api_endpoints.py https://your-app.railway.app

# Tests all endpoints:
# - Health checks (/, /api/health)
# - Database endpoints (/api/islands)
# - Auth endpoints (/api/auth/register, /api/auth/login)
# - Activity endpoints (/api/activity/1/start, /api/activity/2/start)
# - Gamification endpoints (/api/gamification/badges)
```

### 4. Manual Testing Checklist

#### Health Endpoints
- [ ] `GET /` - Root endpoint returns service info
- [ ] `GET /api/health` - Health check returns status

#### Database Endpoints
- [ ] `GET /api/islands` - Returns 401 (auth required) or island data
- [ ] Database tables created automatically
- [ ] Seed data populated (islands, activities, badges)

#### Authentication
- [ ] `POST /api/auth/register` - User registration works
- [ ] `POST /api/auth/login` - User login works
- [ ] `POST /api/auth/select-theme` - Theme selection works

#### Activities
- [ ] `POST /api/activity/1/start` - Activity 1 starts
- [ ] `POST /api/activity/2/start` - Activity 2 starts
- [ ] AI integration works with valid OpenAI key

#### Gamification
- [ ] `GET /api/gamification/badges` - Returns badge list
- [ ] `GET /api/gamification/leaderboard` - Returns leaderboard
- [ ] Point system works correctly

### 5. Common Issues & Solutions

#### Database Issues
```bash
# If tables missing
python src/database_init.py

# If connection fails
# Check DATABASE_URL in Railway dashboard
# Ensure PostgreSQL service is running
```

#### OpenAI Issues
```bash
# If AI features fail
# Verify OPENAI_API_KEY is set correctly
# Check API key has sufficient credits
# Test with openai_test.py
```

#### CORS Issues
```bash
# If frontend can't connect
# Set ALLOWED_ORIGINS environment variable
# Format: https://your-frontend.vercel.app
```

### 6. Performance Testing

#### Load Testing
```bash
# Test with multiple concurrent requests
curl -X POST https://your-app.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","username":"test1","password":"test123","user_type":"child"}' &

curl -X POST https://your-app.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","username":"test2","password":"test123","user_type":"child"}' &
```

#### Response Time Testing
```bash
# Measure response times
time curl https://your-app.railway.app/api/health
time curl https://your-app.railway.app/api/islands
```

### 7. Monitoring & Logs

#### Railway Logs
- Check Railway dashboard for deployment logs
- Monitor for errors during startup
- Watch for database connection issues

#### API Monitoring
- Monitor response times
- Check error rates
- Verify OpenAI API usage

## Next Steps (Dag 4)
- Frontend deployment to Vercel
- Frontend-backend integration
- CORS configuration
- End-to-end testing

