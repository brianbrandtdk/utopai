#!/usr/bin/env python3
"""
CORS Setup and Validation Script for UTOPAI
Helps configure and test CORS between frontend and backend
"""
import requests
import sys
import json
from urllib.parse import urlparse

class CORSValidator:
    def __init__(self, backend_url, frontend_url):
        self.backend_url = backend_url.rstrip('/')
        self.frontend_url = frontend_url.rstrip('/')
        
    def log(self, message, type='info'):
        """Log message with appropriate icon"""
        icons = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️ ',
            'info': 'ℹ️ '
        }
        print(f"{icons.get(type, 'ℹ️ ')} {message}")
    
    def validate_urls(self):
        """Validate URL formats"""
        self.log("Validating URLs...", 'info')
        
        try:
            backend_parsed = urlparse(self.backend_url)
            frontend_parsed = urlparse(self.frontend_url)
            
            if not backend_parsed.scheme or not backend_parsed.netloc:
                self.log(f"Invalid backend URL: {self.backend_url}", 'error')
                return False
                
            if not frontend_parsed.scheme or not frontend_parsed.netloc:
                self.log(f"Invalid frontend URL: {self.frontend_url}", 'error')
                return False
                
            self.log(f"Backend URL valid: {self.backend_url}", 'success')
            self.log(f"Frontend URL valid: {self.frontend_url}", 'success')
            
            return True
            
        except Exception as e:
            self.log(f"URL validation error: {str(e)}", 'error')
            return False
    
    def test_cors_preflight(self):
        """Test CORS preflight request"""
        self.log("Testing CORS preflight...", 'info')
        
        try:
            # Send OPTIONS request (preflight)
            response = requests.options(
                f"{self.backend_url}/api/health",
                headers={
                    'Origin': self.frontend_url,
                    'Access-Control-Request-Method': 'POST',
                    'Access-Control-Request-Headers': 'Content-Type'
                }
            )
            
            # Check CORS headers
            cors_origin = response.headers.get('Access-Control-Allow-Origin')
            cors_methods = response.headers.get('Access-Control-Allow-Methods')
            cors_headers = response.headers.get('Access-Control-Allow-Headers')
            cors_credentials = response.headers.get('Access-Control-Allow-Credentials')
            
            if cors_origin:
                if cors_origin == '*' or cors_origin == self.frontend_url:
                    self.log(f"CORS Origin allowed: {cors_origin}", 'success')
                else:
                    self.log(f"CORS Origin mismatch: {cors_origin} (expected: {self.frontend_url})", 'error')
                    return False
            else:
                self.log("No CORS Origin header found", 'error')
                return False
                
            if cors_methods:
                self.log(f"CORS Methods: {cors_methods}", 'success')
            else:
                self.log("No CORS Methods header found", 'warning')
                
            if cors_headers:
                self.log(f"CORS Headers: {cors_headers}", 'success')
            else:
                self.log("No CORS Headers header found", 'warning')
                
            if cors_credentials:
                self.log(f"CORS Credentials: {cors_credentials}", 'success')
            else:
                self.log("No CORS Credentials header found", 'warning')
                
            return True
            
        except Exception as e:
            self.log(f"CORS preflight test failed: {str(e)}", 'error')
            return False
    
    def test_actual_request(self):
        """Test actual CORS request"""
        self.log("Testing actual CORS request...", 'info')
        
        try:
            # Send actual request with Origin header
            response = requests.get(
                f"{self.backend_url}/api/health",
                headers={'Origin': self.frontend_url}
            )
            
            if response.status_code == 200:
                self.log("API request successful", 'success')
                
                # Check response CORS headers
                cors_origin = response.headers.get('Access-Control-Allow-Origin')
                if cors_origin:
                    self.log(f"Response CORS Origin: {cors_origin}", 'success')
                else:
                    self.log("No CORS Origin in response", 'warning')
                    
                return True
            else:
                self.log(f"API request failed: {response.status_code}", 'error')
                return False
                
        except Exception as e:
            self.log(f"Actual CORS request failed: {str(e)}", 'error')
            return False
    
    def generate_cors_config(self):
        """Generate CORS configuration for Railway"""
        self.log("Generating CORS configuration...", 'info')
        
        frontend_domain = urlparse(self.frontend_url).netloc
        
        config = {
            'railway_env_vars': {
                'ALLOWED_ORIGINS': self.frontend_url,
                'CORS_CREDENTIALS': 'true'
            },
            'vercel_env_vars': {
                'VITE_API_BASE_URL': self.backend_url
            },
            'cors_settings': {
                'origins': [self.frontend_url],
                'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
                'headers': ['Content-Type', 'Authorization'],
                'credentials': True
            }
        }
        
        # Save configuration
        with open('cors_config.json', 'w') as f:
            json.dump(config, f, indent=2)
            
        self.log("CORS configuration saved to cors_config.json", 'success')
        
        # Print Railway setup instructions
        print("\n📋 Railway Environment Variables:")
        print("=" * 35)
        print(f"ALLOWED_ORIGINS = {self.frontend_url}")
        print("CORS_CREDENTIALS = true")
        
        print("\n📋 Vercel Environment Variables:")
        print("=" * 35)
        print(f"VITE_API_BASE_URL = {self.backend_url}")
        
        return config
    
    def run_validation(self):
        """Run complete CORS validation"""
        print("🔗 UTOPAI CORS Validation")
        print("=" * 30)
        print(f"Backend: {self.backend_url}")
        print(f"Frontend: {self.frontend_url}")
        
        # Validate URLs
        if not self.validate_urls():
            return False
            
        # Test CORS
        preflight_ok = self.test_cors_preflight()
        request_ok = self.test_actual_request()
        
        # Generate configuration
        self.generate_cors_config()
        
        # Summary
        print("\n📊 CORS Validation Summary:")
        print("=" * 25)
        
        if preflight_ok and request_ok:
            print("✅ CORS configuration working correctly!")
            print("🎉 Frontend-Backend integration ready!")
            return True
        elif preflight_ok:
            print("⚠️  CORS preflight working, but actual requests failing")
            print("🔧 Check API endpoints and authentication")
            return False
        else:
            print("❌ CORS configuration not working")
            print("🔧 Update Railway ALLOWED_ORIGINS environment variable")
            print(f"   Set to: {self.frontend_url}")
            return False

def main():
    """Main validation function"""
    if len(sys.argv) != 3:
        print("Usage: python cors_setup.py <backend_url> <frontend_url>")
        print("Example: python cors_setup.py https://utopai-backend.railway.app https://utopai-frontend.vercel.app")
        sys.exit(1)
    
    backend_url = sys.argv[1]
    frontend_url = sys.argv[2]
    
    validator = CORSValidator(backend_url, frontend_url)
    success = validator.run_validation()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

