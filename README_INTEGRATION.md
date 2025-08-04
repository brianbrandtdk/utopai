# UTOPAI Frontend-Backend Integration Guide - Dag 5

## Complete Integration Setup

### 1. CORS Configuration

#### Backend (Railway) Setup
Set these environment variables in Railway dashboard:

```bash
# CORS Configuration
ALLOWED_ORIGINS=https://your-frontend.vercel.app
CORS_CREDENTIALS=true

# API Configuration  
OPENAI_API_KEY=sk-your-openai-key
DATABASE_URL=postgresql://... # Auto-provided by Railway
FLASK_ENV=production
SECRET_KEY=your-secret-key
```

#### Frontend (Vercel) Setup
Set these environment variables in Vercel dashboard:

```bash
# API Configuration
VITE_API_BASE_URL=https://your-backend.railway.app

# App Configuration
VITE_APP_NAME=UTOPAI
VITE_APP_VERSION=1.0.0
VITE_ENABLE_ANALYTICS=true
```

### 2. CORS Validation

#### Automatic Testing
```bash
# Test CORS configuration
python cors_setup.py https://your-backend.railway.app https://your-frontend.vercel.app

# This will:
# - Validate URL formats
# - Test CORS preflight requests
# - Test actual API requests
# - Generate configuration files
```

#### Manual Testing
```bash
# Test CORS preflight
curl -X OPTIONS https://your-backend.railway.app/api/health \
  -H "Origin: https://your-frontend.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

# Should return CORS headers:
# Access-Control-Allow-Origin: https://your-frontend.vercel.app
# Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
# Access-Control-Allow-Headers: Content-Type, Authorization
# Access-Control-Allow-Credentials: true
```

### 3. End-to-End Testing

#### Complete Integration Test
```bash
# Run full integration test
python integration_test.py https://your-backend.railway.app https://your-frontend.vercel.app

# Tests:
# - Backend health and CORS
# - Frontend loading
# - API integration (register, login, theme selection)
# - Activity flow
# - Gamification system
# - Performance metrics
```

#### Manual User Flow Test
1. **Frontend Loading:**
   - [ ] Visit frontend URL
   - [ ] Page loads without errors
   - [ ] UTOPAI branding visible

2. **Authentication Flow:**
   - [ ] Click "Log ind som Superhelt" or "Log ind som Prinsesse"
   - [ ] Login successful
   - [ ] Dashboard loads with user data

3. **Theme Selection:**
   - [ ] Theme selection works
   - [ ] UI updates with chosen theme
   - [ ] Theme persists on refresh

4. **Activity Access:**
   - [ ] Navigate to "Gå til Øer"
   - [ ] Island map loads
   - [ ] Activities are visible
   - [ ] Can start Activity 1 and 2

5. **Gamification:**
   - [ ] Points display correctly
   - [ ] Badges system works
   - [ ] Leaderboard loads

### 4. Common Integration Issues

#### CORS Errors
**Symptom:** Browser console shows CORS errors
**Solution:**
```bash
# Check ALLOWED_ORIGINS on Railway
# Ensure exact match with Vercel domain
# Include protocol (https://)
# No trailing slash
```

#### API Connection Errors
**Symptom:** Frontend can't reach backend
**Solution:**
```bash
# Verify VITE_API_BASE_URL on Vercel
# Check Railway backend is running
# Test backend health endpoint directly
curl https://your-backend.railway.app/api/health
```

#### Authentication Issues
**Symptom:** Login fails or sessions don't persist
**Solution:**
```bash
# Ensure CORS credentials enabled
# Check SECRET_KEY is set on Railway
# Verify cookie settings in browser
```

#### Database Connection Issues
**Symptom:** API returns database errors
**Solution:**
```bash
# Check DATABASE_URL on Railway
# Verify PostgreSQL service is running
# Run database initialization if needed
```

### 5. Performance Optimization

#### Backend Optimization
```python
# Enable gzip compression
from flask_compress import Compress
Compress(app)

# Add caching headers
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'public, max-age=300'
    return response
```

#### Frontend Optimization
```javascript
// Lazy load components
const Activity2 = lazy(() => import('./components/Activity2'));

// Optimize API calls
const api = useMemo(() => new ApiClient(), []);

// Add loading states
if (loading) return <LoadingSpinner />;
```

### 6. Monitoring & Analytics

#### Backend Monitoring
- Railway provides automatic logging
- Monitor response times in Railway dashboard
- Set up error alerts

#### Frontend Monitoring
- Enable Vercel Analytics
- Monitor Core Web Vitals
- Track user interactions

#### Custom Monitoring
```javascript
// Track API errors
window.addEventListener('unhandledrejection', (event) => {
  if (event.reason?.message?.includes('API')) {
    console.error('API Error:', event.reason);
    // Send to analytics
  }
});
```

### 7. Security Considerations

#### HTTPS Only
- Both frontend and backend use HTTPS
- No mixed content warnings
- Secure cookie transmission

#### Environment Variables
- Never expose API keys in frontend
- Use VITE_ prefix for public variables
- Keep sensitive data on backend only

#### CORS Security
- Use specific origins, not wildcards
- Enable credentials only when needed
- Validate all incoming requests

### 8. Deployment Checklist

#### Pre-Deployment
- [ ] Backend tests pass
- [ ] Frontend builds successfully
- [ ] Environment variables configured
- [ ] CORS setup validated

#### Post-Deployment
- [ ] Health endpoints respond
- [ ] Frontend loads correctly
- [ ] API integration works
- [ ] User flows complete successfully
- [ ] Performance is acceptable

#### Rollback Plan
- [ ] Previous versions tagged in Git
- [ ] Railway rollback procedure documented
- [ ] Vercel rollback procedure documented
- [ ] Database backup available

## Next Steps (Dag 6)
- Activity testing and validation
- User experience optimization
- Performance tuning
- Bug fixes and polish

