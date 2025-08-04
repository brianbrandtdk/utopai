#!/usr/bin/env python3
"""
API Endpoint Testing Script for UTOPAI
Test all endpoints to ensure they work with PostgreSQL
"""
import requests
import json
import sys
from datetime import datetime

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, endpoint, method, status, message):
        """Log test result"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'status': 'PASS' if status else 'FAIL',
            'message': message
        }
        self.test_results.append(result)
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {method} {endpoint}: {message}")
        
    def test_health_endpoints(self):
        """Test basic health endpoints"""
        print("\n🔍 Testing Health Endpoints...")
        
        # Test root endpoint
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log_test("/", "GET", True, f"Status: {response.status_code}")
            else:
                self.log_test("/", "GET", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("/", "GET", False, f"Error: {str(e)}")
            
        # Test health check
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                self.log_test("/api/health", "GET", True, f"Service: {data.get('service', 'Unknown')}")
            else:
                self.log_test("/api/health", "GET", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("/api/health", "GET", False, f"Error: {str(e)}")
    
    def test_database_endpoints(self):
        """Test database-dependent endpoints"""
        print("\n🗄️ Testing Database Endpoints...")
        
        # Test islands endpoint
        try:
            response = self.session.get(f"{self.base_url}/api/islands")
            if response.status_code in [200, 401]:  # 401 is expected without auth
                self.log_test("/api/islands", "GET", True, f"Status: {response.status_code} (Expected)")
            else:
                self.log_test("/api/islands", "GET", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("/api/islands", "GET", False, f"Error: {str(e)}")
    
    def test_auth_endpoints(self):
        """Test authentication endpoints"""
        print("\n🔐 Testing Auth Endpoints...")
        
        # Test user registration
        test_user = {
            "name": "API Test User",
            "username": f"test_api_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "password": "testpass123",
            "user_type": "child"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=test_user,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 201:
                self.log_test("/api/auth/register", "POST", True, "User created successfully")
                
                # Test login with created user
                login_data = {
                    "username": test_user["username"],
                    "password": test_user["password"]
                }
                
                login_response = self.session.post(
                    f"{self.base_url}/api/auth/login",
                    json=login_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if login_response.status_code == 200:
                    self.log_test("/api/auth/login", "POST", True, "Login successful")
                    return True
                else:
                    self.log_test("/api/auth/login", "POST", False, f"Status: {login_response.status_code}")
                    
            else:
                self.log_test("/api/auth/register", "POST", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("/api/auth/register", "POST", False, f"Error: {str(e)}")
            
        return False
    
    def test_activity_endpoints(self):
        """Test activity endpoints"""
        print("\n🎮 Testing Activity Endpoints...")
        
        # Test activity 1 endpoints
        endpoints = [
            "/api/activity/1/start",
            "/api/activity/2/start"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.post(f"{self.base_url}{endpoint}")
                if response.status_code in [200, 401]:  # 401 expected without proper auth
                    self.log_test(endpoint, "POST", True, f"Status: {response.status_code} (Expected)")
                else:
                    self.log_test(endpoint, "POST", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, "POST", False, f"Error: {str(e)}")
    
    def test_gamification_endpoints(self):
        """Test gamification endpoints"""
        print("\n🏆 Testing Gamification Endpoints...")
        
        endpoints = [
            ("/api/gamification/badges", "GET"),
            ("/api/gamification/leaderboard", "GET")
        ]
        
        for endpoint, method in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}")
                else:
                    response = self.session.post(f"{self.base_url}{endpoint}")
                    
                if response.status_code in [200, 401]:  # 401 expected without auth
                    self.log_test(endpoint, method, True, f"Status: {response.status_code} (Expected)")
                else:
                    self.log_test(endpoint, method, False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, method, False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print(f"🧪 UTOPAI API Testing - {self.base_url}")
        print("=" * 50)
        
        self.test_health_endpoints()
        self.test_database_endpoints()
        self.test_auth_endpoints()
        self.test_activity_endpoints()
        self.test_gamification_endpoints()
        
        # Summary
        print("\n📊 Test Summary:")
        print("=" * 30)
        
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Save results
        with open('api_test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\nDetailed results saved to: api_test_results.json")
        
        return passed == total

def main():
    """Main testing function"""
    if len(sys.argv) != 2:
        print("Usage: python test_api_endpoints.py <base_url>")
        print("Example: python test_api_endpoints.py https://utopai-backend.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1]
    tester = APITester(base_url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

