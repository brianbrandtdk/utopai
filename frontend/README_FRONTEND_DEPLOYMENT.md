# UTOPAI Frontend Deployment Guide - Dag 4

## Vercel Deployment Setup

### 1. Forbered Frontend til Deployment
Alle nødvendige filer er nu klar:
- `vercel.json` - Vercel konfiguration
- `.env.production` - Production environment variables
- `.env.development` - Development environment variables
- Opdateret `package.json` med build scripts
- Opdateret `src/lib/api.js` med environment variable support

### 2. Opret Vercel Konto
1. Gå til [vercel.com](https://vercel.com)
2. Sign up med GitHub konto
3. Connect GitHub repository

### 3. Deploy til Vercel

#### Option A: GitHub Integration (Anbefalet)
1. Push frontend kode til GitHub repository
2. Gå til Vercel dashboard
3. Klik "New Project"
4. Import UTOPAI repository
5. Set root directory til `/frontend`
6. Vercel auto-detecter React/Vite setup

#### Option B: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login til Vercel
vercel login

# Deploy fra frontend directory
cd frontend
vercel

# Follow prompts for configuration
```

### 4. Konfigurer Environment Variables
I Vercel dashboard under "Settings" → "Environment Variables":

**Production Variables:**
```
VITE_API_BASE_URL = https://your-railway-backend-url.railway.app
VITE_APP_NAME = UTOPAI
VITE_APP_VERSION = 1.0.0
VITE_ENABLE_ANALYTICS = true
VITE_ENABLE_DEBUG = false
```

**Preview/Development Variables:**
```
VITE_API_BASE_URL = http://localhost:5002
VITE_APP_NAME = UTOPAI (Dev)
VITE_ENABLE_DEBUG = true
```

### 5. Build Settings
Vercel auto-detecter disse settings:
- **Framework Preset:** Vite
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm install`

### 6. Custom Domain (Optional)
1. Gå til "Settings" → "Domains"
2. Add custom domain (f.eks. utopai.dk)
3. Configure DNS records
4. SSL certificate auto-genereres

### 7. Test Deployment

#### Automatic Tests
```bash
# Test build locally først
npm run build:production
npm run preview

# Check for build errors
# Verify environment variables work
```

#### Manual Testing
Efter deployment, test:
- [ ] Frontend loader korrekt
- [ ] API calls til Railway backend virker
- [ ] Login/register flow fungerer
- [ ] Tema-valg virker
- [ ] Aktivitet 1 og 2 kan startes
- [ ] Responsive design på mobil/tablet

### 8. Performance Optimering

#### Vite Build Optimering
```javascript
// vite.config.js optimering
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['lucide-react', '@radix-ui/react-dialog']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
})
```

#### Vercel Optimering
- Enable "Speed Insights" i Vercel dashboard
- Configure "Web Analytics"
- Setup "Edge Functions" hvis nødvendigt

### 9. Monitoring & Analytics

#### Vercel Analytics
- Real User Monitoring (RUM)
- Core Web Vitals tracking
- Performance insights

#### Error Tracking
```javascript
// Add error boundary for production
if (import.meta.env.PROD) {
  window.addEventListener('error', (event) => {
    console.error('Production error:', event.error);
    // Send to analytics service
  });
}
```

### 10. Troubleshooting

#### Build Errors
```bash
# Common issues:
# - Missing environment variables
# - Import path errors
# - TypeScript errors (if using TS)

# Debug build locally:
npm run build:production
```

#### API Connection Issues
```bash
# Check environment variables
console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL);

# Test API connectivity
curl https://your-frontend.vercel.app/api/health
```

#### CORS Issues
- Ensure Railway backend has correct CORS setup
- Add Vercel domain to ALLOWED_ORIGINS
- Check browser network tab for CORS errors

## Next Steps (Dag 5)
- Frontend-Backend Integration
- CORS konfiguration
- End-to-end testing
- Performance optimering

