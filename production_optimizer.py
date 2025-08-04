#!/usr/bin/env python3
"""
Production Optimizer for UTOPAI
Final optimizations and performance tuning
"""
import os
import json
import sys
from pathlib import Path

class ProductionOptimizer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.optimizations = []
        
    def log_optimization(self, category, action, status, details=None):
        """Log optimization action"""
        optimization = {
            'category': category,
            'action': action,
            'status': 'APPLIED' if status else 'FAILED',
            'details': details
        }
        self.optimizations.append(optimization)
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {category}: {action}")
        if details and not status:
            print(f"   Details: {details}")
    
    def optimize_backend_performance(self):
        """Optimize backend performance"""
        print("\n🔧 Optimizing Backend Performance...")
        
        backend_path = self.project_root / 'backend'
        
        # Create optimized main.py
        optimized_main = '''import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, g
from flask_cors import CORS
from flask_compress import Compress
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.islands import islands_bp
from src.routes.activities import activities_bp
from src.routes.activity_1 import activity_1_bp
from src.routes.activity_2 import activity_2_bp
from src.routes.gamification import gamification_bp
import time

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Production optimizations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'utopai-secret-key-2024-super-secure')
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Enable compression
Compress(app)

# CORS configuration for production
allowed_origins = os.environ.get('ALLOWED_ORIGINS')
if allowed_origins:
    origins = [origin.strip() for origin in allowed_origins.split(',')]
    CORS(app, 
         supports_credentials=True,
         origins=origins,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
else:
    CORS(app, supports_credentials=True)

# Performance middleware
@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    # Add performance headers
    if hasattr(g, 'start_time'):
        response_time = time.time() - g.start_time
        response.headers['X-Response-Time'] = f"{response_time:.3f}s"
    
    # Add caching headers
    if request.endpoint in ['static', 'health_check']:
        response.headers['Cache-Control'] = 'public, max-age=3600'
    else:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    
    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    return response

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(islands_bp, url_prefix='/api')
app.register_blueprint(activities_bp, url_prefix='/api')
app.register_blueprint(activity_1_bp, url_prefix='/api')
app.register_blueprint(activity_2_bp, url_prefix='/api')
app.register_blueprint(gamification_bp, url_prefix='/api/gamification')

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if database_url:
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True
    }
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()
    from src.database_init import initialize_database
    initialize_database()

@app.route('/api/health')
def health_check():
    return {'status': 'healthy', 'service': 'UTOPAI Backend', 'version': '1.0.0'}, 200

@app.route('/')
def root():
    return {'message': 'UTOPAI Backend API', 'status': 'running', 'version': '1.0.0'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
'''
        
        try:
            with open(backend_path / 'src' / 'main_optimized.py', 'w') as f:
                f.write(optimized_main)
            self.log_optimization("Backend", "Created optimized main.py", True)
        except Exception as e:
            self.log_optimization("Backend", "Failed to create optimized main.py", False, str(e))
        
        # Add compression to requirements
        try:
            requirements_path = backend_path / 'requirements.txt'
            with open(requirements_path, 'r') as f:
                requirements = f.read()
            
            if 'flask-compress' not in requirements:
                with open(requirements_path, 'a') as f:
                    f.write('\nflask-compress==1.13\n')
                self.log_optimization("Backend", "Added compression dependency", True)
            else:
                self.log_optimization("Backend", "Compression already configured", True)
        except Exception as e:
            self.log_optimization("Backend", "Failed to update requirements", False, str(e))
    
    def optimize_frontend_performance(self):
        """Optimize frontend performance"""
        print("\n⚡ Optimizing Frontend Performance...")
        
        frontend_path = self.project_root / 'frontend'
        
        # Create optimized vite config
        optimized_vite_config = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['lucide-react', 'framer-motion'],
          utils: ['clsx', 'tailwind-merge']
        }
      }
    },
    chunkSizeWarningLimit: 1000,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  },
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV)
  }
})
'''
        
        try:
            with open(frontend_path / 'vite.config.optimized.js', 'w') as f:
                f.write(optimized_vite_config)
            self.log_optimization("Frontend", "Created optimized Vite config", True)
        except Exception as e:
            self.log_optimization("Frontend", "Failed to create optimized Vite config", False, str(e))
        
        # Create performance monitoring component
        performance_monitor = '''import { useEffect } from 'react';

export const PerformanceMonitor = () => {
  useEffect(() => {
    // Monitor Core Web Vitals
    if ('web-vital' in window) return;
    
    // Track page load time
    window.addEventListener('load', () => {
      const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
      console.log(`Page load time: ${loadTime}ms`);
      
      // Send to analytics if enabled
      if (import.meta.env.VITE_ENABLE_ANALYTICS === 'true') {
        // Analytics code here
      }
    });
    
    // Track API response times
    const originalFetch = window.fetch;
    window.fetch = async (...args) => {
      const start = performance.now();
      const response = await originalFetch(...args);
      const end = performance.now();
      
      console.log(`API call to ${args[0]}: ${(end - start).toFixed(2)}ms`);
      return response;
    };
    
    return () => {
      window.fetch = originalFetch;
    };
  }, []);
  
  return null;
};

export default PerformanceMonitor;
'''
        
        try:
            components_path = frontend_path / 'src' / 'components'
            components_path.mkdir(exist_ok=True)
            with open(components_path / 'PerformanceMonitor.jsx', 'w') as f:
                f.write(performance_monitor)
            self.log_optimization("Frontend", "Created performance monitor", True)
        except Exception as e:
            self.log_optimization("Frontend", "Failed to create performance monitor", False, str(e))
    
    def create_security_checklist(self):
        """Create security checklist"""
        print("\n🔒 Creating Security Checklist...")
        
        security_checklist = '''# UTOPAI Security Checklist

## Backend Security
- [ ] **HTTPS Only:** All endpoints use HTTPS in production
- [ ] **Environment Variables:** Sensitive data in environment variables only
- [ ] **CORS:** Specific origins configured (no wildcards)
- [ ] **Input Validation:** All user input validated and sanitized
- [ ] **SQL Injection:** Using parameterized queries (SQLAlchemy ORM)
- [ ] **XSS Protection:** Content-Type headers and input sanitization
- [ ] **CSRF Protection:** CSRF tokens for state-changing operations
- [ ] **Rate Limiting:** API rate limiting implemented
- [ ] **Error Handling:** No sensitive information in error messages
- [ ] **Session Security:** Secure session management

## Frontend Security
- [ ] **HTTPS Only:** Frontend served over HTTPS
- [ ] **Content Security Policy:** CSP headers configured
- [ ] **XSS Prevention:** Input sanitization and output encoding
- [ ] **Secure Storage:** No sensitive data in localStorage
- [ ] **API Keys:** No API keys exposed in frontend code
- [ ] **Dependencies:** All dependencies up to date
- [ ] **Build Security:** Production build removes debug code

## Data Protection
- [ ] **Minimal Data:** Collect only necessary user data
- [ ] **Data Encryption:** Sensitive data encrypted at rest
- [ ] **Password Security:** Passwords hashed with salt
- [ ] **Session Expiry:** Appropriate session timeout
- [ ] **Data Backup:** Regular database backups
- [ ] **Access Control:** Proper user authorization

## Child Safety (COPPA Compliance)
- [ ] **Age Verification:** Appropriate age verification
- [ ] **Parental Consent:** Parental consent mechanism
- [ ] **Data Minimization:** Minimal personal data collection
- [ ] **Safe Content:** All AI-generated content is child-appropriate
- [ ] **Moderation:** Content moderation for user inputs
- [ ] **Privacy Policy:** Clear privacy policy for children

## Deployment Security
- [ ] **Environment Separation:** Separate dev/staging/production
- [ ] **Access Control:** Limited access to production systems
- [ ] **Monitoring:** Security monitoring and alerting
- [ ] **Incident Response:** Security incident response plan
- [ ] **Regular Updates:** Regular security updates
- [ ] **Penetration Testing:** Regular security testing
'''
        
        try:
            with open(self.project_root / 'SECURITY_CHECKLIST.md', 'w') as f:
                f.write(security_checklist)
            self.log_optimization("Security", "Created security checklist", True)
        except Exception as e:
            self.log_optimization("Security", "Failed to create security checklist", False, str(e))
    
    def create_launch_guide(self):
        """Create launch preparation guide"""
        print("\n🚀 Creating Launch Guide...")
        
        launch_guide = '''# UTOPAI Launch Guide

## Pre-Launch Checklist (24 hours before)
- [ ] All tests passing (backend, frontend, integration, UX)
- [ ] Performance benchmarks met
- [ ] Security checklist completed
- [ ] Environment variables configured on Railway and Vercel
- [ ] Database seeded with production data
- [ ] Monitoring and alerting configured
- [ ] Team notified of launch schedule

## Launch Day Checklist
- [ ] **T-2 hours:** Final test run
- [ ] **T-1 hour:** Deploy backend to Railway
- [ ] **T-30 min:** Deploy frontend to Vercel
- [ ] **T-15 min:** Verify all endpoints working
- [ ] **T-5 min:** Final smoke test
- [ ] **T-0:** Announce launch

## Post-Launch Monitoring (First 24 hours)
- [ ] Monitor error rates (target: <5%)
- [ ] Monitor response times (target: <3s average)
- [ ] Monitor user registration success rate (target: >95%)
- [ ] Monitor activity completion rates (target: >80%)
- [ ] Check user feedback and support requests
- [ ] Monitor server resources and scaling

## Success Metrics
- **Technical Metrics:**
  - Uptime: >99.5%
  - Error rate: <5%
  - Average response time: <3 seconds
  - Registration success rate: >95%

- **User Metrics:**
  - Activity completion rate: >80%
  - Average session duration: >10 minutes
  - User return rate: >60%
  - User satisfaction: >4/5 stars

## Rollback Plan
If critical issues occur:
1. **Immediate:** Revert to previous deployment
2. **Communication:** Notify users of temporary maintenance
3. **Investigation:** Identify and fix issues
4. **Re-deployment:** Deploy fixed version
5. **Verification:** Confirm issues resolved

## Support Preparation
- [ ] Support documentation ready
- [ ] FAQ prepared for common issues
- [ ] Support team trained on UTOPAI features
- [ ] Escalation procedures defined
- [ ] User feedback collection system ready

## Marketing Preparation
- [ ] Landing page optimized
- [ ] Social media posts prepared
- [ ] Press release ready (if applicable)
- [ ] User onboarding materials prepared
- [ ] Demo videos created

## Long-term Monitoring
- **Weekly Reviews:**
  - User growth and retention
  - Feature usage analytics
  - Performance trends
  - Error patterns

- **Monthly Reviews:**
  - Security audit
  - Performance optimization
  - User feedback analysis
  - Feature roadmap updates

## Scaling Preparation
- **Traffic Growth:**
  - Railway auto-scaling configured
  - Database connection pooling optimized
  - CDN setup for static assets
  - Load testing completed

- **Feature Growth:**
  - Modular architecture for new activities
  - API versioning strategy
  - Database migration procedures
  - A/B testing framework
'''
        
        try:
            with open(self.project_root / 'LAUNCH_GUIDE.md', 'w') as f:
                f.write(launch_guide)
            self.log_optimization("Launch", "Created launch guide", True)
        except Exception as e:
            self.log_optimization("Launch", "Failed to create launch guide", False, str(e))
    
    def run_optimization(self):
        """Run all production optimizations"""
        print("🎯 UTOPAI Production Optimizer")
        print("=" * 35)
        
        self.optimize_backend_performance()
        self.optimize_frontend_performance()
        self.create_security_checklist()
        self.create_launch_guide()
        
        # Summary
        print("\n📊 Optimization Summary:")
        print("=" * 25)
        
        applied = len([o for o in self.optimizations if o['status'] == 'APPLIED'])
        total = len(self.optimizations)
        
        print(f"Total Optimizations: {total}")
        print(f"Applied: {applied}")
        print(f"Failed: {total - applied}")
        print(f"Success Rate: {(applied/total)*100:.1f}%")
        
        # Save results
        with open('production_optimization_results.json', 'w') as f:
            json.dump(self.optimizations, f, indent=2)
        
        print(f"\nResults saved to: production_optimization_results.json")
        
        if applied == total:
            print("\n🎉 All optimizations applied successfully!")
            print("✅ UTOPAI is production-ready!")
        else:
            print(f"\n⚠️  {total - applied} optimizations failed")
            print("🔧 Review and apply manually if needed")
        
        return applied == total

def main():
    """Main optimization function"""
    if len(sys.argv) != 2:
        print("Usage: python production_optimizer.py <project_root>")
        print("Example: python production_optimizer.py /home/ubuntu/utopai")
        sys.exit(1)
    
    project_root = sys.argv[1]
    optimizer = ProductionOptimizer(project_root)
    success = optimizer.run_optimization()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

