#!/usr/bin/env python3
"""
End-to-End Integration Test for UTOPAI
Tests complete frontend-backend integration
"""
import requests
import json
import sys
import time
from datetime import datetime

class IntegrationTester:
    def __init__(self, backend_url, frontend_url):
        self.backend_url = backend_url.rstrip('/')
        self.frontend_url = frontend_url.rstrip('/')
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, status, message, details=None):
        """Log test result"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'test': test_name,
            'status': 'PASS' if status else 'FAIL',
            'message': message,
            'details': details
        }
        self.test_results.append(result)
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {test_name}: {message}")
        if details and not status:
            print(f"   Details: {details}")
    
    def test_backend_health(self):
        """Test backend health and CORS"""
        print("\n🔍 Testing Backend Health & CORS...")
        
        try:
            # Test health endpoint
            response = self.session.get(f"{self.backend_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Backend Health", True, f"Service: {data.get('service', 'Unknown')}")
            else:
                self.log_test("Backend Health", False, f"Status: {response.status_code}")
                return False
                
            # Test CORS headers
            cors_headers = response.headers.get('Access-Control-Allow-Origin')
            if cors_headers:
                self.log_test("CORS Headers", True, f"CORS configured: {cors_headers}")
            else:
                self.log_test("CORS Headers", False, "No CORS headers found")
                
            return True
            
        except Exception as e:
            self.log_test("Backend Health", False, f"Connection failed: {str(e)}")
            return False
    
    def test_frontend_loading(self):
        """Test frontend loading"""
        print("\n🌐 Testing Frontend Loading...")
        
        try:
            response = self.session.get(self.frontend_url)
            if response.status_code == 200:
                content = response.text
                
                # Check for React app
                if '<div id="root">' in content:
                    self.log_test("Frontend Loading", True, "React app structure found")
                else:
                    self.log_test("Frontend Loading", False, "React app structure missing")
                    return False
                    
                # Check for UTOPAI title
                if 'UTOPAI' in content:
                    self.log_test("App Title", True, "UTOPAI title found")
                else:
                    self.log_test("App Title", False, "UTOPAI title missing")
                    
                return True
            else:
                self.log_test("Frontend Loading", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Frontend Loading", False, f"Connection failed: {str(e)}")
            return False
    
    def test_api_integration(self):
        """Test frontend-backend API integration"""
        print("\n🔗 Testing API Integration...")
        
        # Create test user
        test_user = {
            "name": "Integration Test User",
            "username": f"integration_test_{int(time.time())}",
            "password": "testpass123",
            "user_type": "child"
        }
        
        try:
            # Test user registration
            response = self.session.post(
                f"{self.backend_url}/api/auth/register",
                json=test_user,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                self.log_test("User Registration", True, "User created successfully")
                
                # Test login
                login_response = self.session.post(
                    f"{self.backend_url}/api/auth/login",
                    json={
                        "username": test_user["username"],
                        "password": test_user["password"]
                    },
                    headers={'Content-Type': 'application/json'}
                )
                
                if login_response.status_code == 200:
                    self.log_test("User Login", True, "Login successful")
                    
                    # Test theme selection
                    theme_response = self.session.post(
                        f"{self.backend_url}/api/auth/select-theme",
                        json={"theme": "superhelte"},
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if theme_response.status_code == 200:
                        self.log_test("Theme Selection", True, "Theme selected successfully")
                    else:
                        self.log_test("Theme Selection", False, f"Status: {theme_response.status_code}")
                        
                    return True
                else:
                    self.log_test("User Login", False, f"Status: {login_response.status_code}")
                    
            else:
                self.log_test("User Registration", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("API Integration", False, f"Error: {str(e)}")
            
        return False
    
    def test_activity_flow(self):
        """Test activity flow"""
        print("\n🎮 Testing Activity Flow...")
        
        try:
            # Test islands endpoint
            response = self.session.get(f"{self.backend_url}/api/islands")
            if response.status_code == 200:
                islands = response.json()
                self.log_test("Islands API", True, f"Found {len(islands)} islands")
                
                # Test activity endpoints
                activity_endpoints = [
                    "/api/activity/1/start",
                    "/api/activity/2/start"
                ]
                
                for endpoint in activity_endpoints:
                    try:
                        activity_response = self.session.post(f"{self.backend_url}{endpoint}")
                        if activity_response.status_code in [200, 401]:  # 401 is expected for some endpoints
                            self.log_test(f"Activity {endpoint}", True, f"Status: {activity_response.status_code}")
                        else:
                            self.log_test(f"Activity {endpoint}", False, f"Status: {activity_response.status_code}")
                    except Exception as e:
                        self.log_test(f"Activity {endpoint}", False, f"Error: {str(e)}")
                        
                return True
            else:
                self.log_test("Islands API", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Activity Flow", False, f"Error: {str(e)}")
            
        return False
    
    def test_gamification(self):
        """Test gamification system"""
        print("\n🏆 Testing Gamification System...")
        
        try:
            # Test badges endpoint
            response = self.session.get(f"{self.backend_url}/api/gamification/badges")
            if response.status_code in [200, 401]:
                self.log_test("Badges API", True, f"Status: {response.status_code}")
            else:
                self.log_test("Badges API", False, f"Status: {response.status_code}")
                
            # Test leaderboard endpoint
            leaderboard_response = self.session.get(f"{self.backend_url}/api/gamification/leaderboard")
            if leaderboard_response.status_code in [200, 401]:
                self.log_test("Leaderboard API", True, f"Status: {leaderboard_response.status_code}")
            else:
                self.log_test("Leaderboard API", False, f"Status: {leaderboard_response.status_code}")
                
            return True
            
        except Exception as e:
            self.log_test("Gamification System", False, f"Error: {str(e)}")
            return False
    
    def test_performance(self):
        """Test basic performance metrics"""
        print("\n⚡ Testing Performance...")
        
        endpoints = [
            "/api/health",
            "/api/islands",
            "/api/gamification/badges"
        ]
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.backend_url}{endpoint}")
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                if response_time < 1000:  # Less than 1 second
                    self.log_test(f"Performance {endpoint}", True, f"{response_time:.0f}ms")
                elif response_time < 3000:  # Less than 3 seconds
                    self.log_test(f"Performance {endpoint}", True, f"{response_time:.0f}ms (slow)")
                else:
                    self.log_test(f"Performance {endpoint}", False, f"{response_time:.0f}ms (too slow)")
                    
            except Exception as e:
                self.log_test(f"Performance {endpoint}", False, f"Error: {str(e)}")
    
    def run_integration_tests(self):
        """Run all integration tests"""
        print("🧪 UTOPAI Integration Test")
        print("=" * 40)
        print(f"Backend: {self.backend_url}")
        print(f"Frontend: {self.frontend_url}")
        
        # Run tests
        backend_ok = self.test_backend_health()
        frontend_ok = self.test_frontend_loading()
        
        if backend_ok:
            self.test_api_integration()
            self.test_activity_flow()
            self.test_gamification()
            self.test_performance()
        
        # Summary
        print("\n📊 Integration Test Summary:")
        print("=" * 30)
        
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Save results
        with open('integration_test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\nDetailed results saved to: integration_test_results.json")
        
        if passed == total:
            print("\n🎉 All integration tests passed!")
            print("✅ Frontend-Backend integration working perfectly!")
        else:
            print(f"\n🚨 {total - passed} integration tests failed!")
            print("⚠️  Check configuration and try again")
        
        return passed == total

def main():
    """Main testing function"""
    if len(sys.argv) != 3:
        print("Usage: python integration_test.py <backend_url> <frontend_url>")
        print("Example: python integration_test.py https://utopai-backend.railway.app https://utopai-frontend.vercel.app")
        sys.exit(1)
    
    backend_url = sys.argv[1]
    frontend_url = sys.argv[2]
    
    tester = IntegrationTester(backend_url, frontend_url)
    success = tester.run_integration_tests()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

