#!/usr/bin/env python3
"""
Activity Test Suite for UTOPAI
Comprehensive testing of Activity 1 and Activity 2 functionality
"""
import requests
import json
import sys
import time
from datetime import datetime

class ActivityTester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.test_results = []
        self.user_token = None
        
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
    
    def setup_test_user(self):
        """Create and login test user"""
        print("\n👤 Setting up test user...")
        
        test_user = {
            "name": "Activity Test User",
            "username": f"activity_test_{int(time.time())}",
            "password": "testpass123",
            "user_type": "child"
        }
        
        try:
            # Register user
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=test_user,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                self.log_test("User Registration", True, "Test user created")
                
                # Login user
                login_response = self.session.post(
                    f"{self.base_url}/api/auth/login",
                    json={
                        "username": test_user["username"],
                        "password": test_user["password"]
                    },
                    headers={'Content-Type': 'application/json'}
                )
                
                if login_response.status_code == 200:
                    self.log_test("User Login", True, "Test user logged in")
                    
                    # Select theme
                    theme_response = self.session.post(
                        f"{self.base_url}/api/auth/select-theme",
                        json={"theme": "superhelte"},
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if theme_response.status_code == 200:
                        self.log_test("Theme Selection", True, "Superhelte theme selected")
                        return True
                    else:
                        self.log_test("Theme Selection", False, f"Status: {theme_response.status_code}")
                else:
                    self.log_test("User Login", False, f"Status: {login_response.status_code}")
            else:
                self.log_test("User Registration", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("User Setup", False, f"Error: {str(e)}")
            
        return False
    
    def test_activity_1_flow(self):
        """Test complete Activity 1 flow"""
        print("\n📚 Testing Activity 1: Hvad er ChatGPT?...")
        
        try:
            # Start Activity 1
            start_response = self.session.post(f"{self.base_url}/api/activity/1/start")
            if start_response.status_code == 200:
                self.log_test("Activity 1 Start", True, "Activity started successfully")
                start_data = start_response.json()
                
                # Test step 1
                step1_response = self.session.get(f"{self.base_url}/api/activity/1/step/1")
                if step1_response.status_code == 200:
                    self.log_test("Activity 1 Step 1", True, "Step 1 loaded")
                    
                    # Test step 2
                    step2_response = self.session.get(f"{self.base_url}/api/activity/1/step/2")
                    if step2_response.status_code == 200:
                        self.log_test("Activity 1 Step 2", True, "Step 2 loaded")
                        
                        # Test step 3
                        step3_response = self.session.get(f"{self.base_url}/api/activity/1/step/3")
                        if step3_response.status_code == 200:
                            self.log_test("Activity 1 Step 3", True, "Step 3 loaded")
                            
                            # Test hint system
                            hint_response = self.session.post(
                                f"{self.base_url}/api/activity/1/hint",
                                json={
                                    "step_id": 1,
                                    "question": "Jeg har brug for hjælp",
                                    "attempt_number": 1
                                },
                                headers={'Content-Type': 'application/json'}
                            )
                            
                            if hint_response.status_code == 200:
                                self.log_test("Activity 1 Hints", True, "Hint system working")
                            else:
                                self.log_test("Activity 1 Hints", False, f"Status: {hint_response.status_code}")
                                
                            # Test step submission
                            submit_response = self.session.post(
                                f"{self.base_url}/api/activity/1/step/1/submit",
                                json={"answer": "ChatGPT er en AI assistent"},
                                headers={'Content-Type': 'application/json'}
                            )
                            
                            if submit_response.status_code == 200:
                                self.log_test("Activity 1 Submit", True, "Step submission working")
                                return True
                            else:
                                self.log_test("Activity 1 Submit", False, f"Status: {submit_response.status_code}")
                        else:
                            self.log_test("Activity 1 Step 3", False, f"Status: {step3_response.status_code}")
                    else:
                        self.log_test("Activity 1 Step 2", False, f"Status: {step2_response.status_code}")
                else:
                    self.log_test("Activity 1 Step 1", False, f"Status: {step1_response.status_code}")
            else:
                self.log_test("Activity 1 Start", False, f"Status: {start_response.status_code}")
                
        except Exception as e:
            self.log_test("Activity 1 Flow", False, f"Error: {str(e)}")
            
        return False
    
    def test_activity_2_flow(self):
        """Test complete Activity 2 flow"""
        print("\n✏️ Testing Activity 2: Dit første prompt...")
        
        try:
            # Start Activity 2
            start_response = self.session.post(f"{self.base_url}/api/activity/2/start")
            if start_response.status_code == 200:
                self.log_test("Activity 2 Start", True, "Activity started successfully")
                
                # Test prompt building
                prompt_parts = {
                    "role": "helpful teacher",
                    "task": "explain AI",
                    "context": "to a 10-year old",
                    "tone": "friendly"
                }
                
                build_response = self.session.post(
                    f"{self.base_url}/api/activity/2/build-prompt",
                    json={
                        "prompt_parts": prompt_parts,
                        "step_id": 1
                    },
                    headers={'Content-Type': 'application/json'}
                )
                
                if build_response.status_code == 200:
                    self.log_test("Activity 2 Prompt Building", True, "Prompt builder working")
                    build_data = build_response.json()
                    
                    # Test prompt testing
                    test_response = self.session.post(
                        f"{self.base_url}/api/activity/2/test-prompt",
                        json={
                            "prompt": build_data.get('built_prompt', 'Test prompt'),
                            "step_id": 1
                        },
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if test_response.status_code == 200:
                        self.log_test("Activity 2 Prompt Testing", True, "Prompt testing working")
                        
                        # Test step 2 (politeness training)
                        step2_response = self.session.get(f"{self.base_url}/api/activity/2/step/2")
                        if step2_response.status_code == 200:
                            self.log_test("Activity 2 Step 2", True, "Politeness training loaded")
                            
                            # Test step 3 (personalized exercise)
                            step3_response = self.session.get(f"{self.base_url}/api/activity/2/step/3")
                            if step3_response.status_code == 200:
                                self.log_test("Activity 2 Step 3", True, "Personalized exercise loaded")
                                return True
                            else:
                                self.log_test("Activity 2 Step 3", False, f"Status: {step3_response.status_code}")
                        else:
                            self.log_test("Activity 2 Step 2", False, f"Status: {step2_response.status_code}")
                    else:
                        self.log_test("Activity 2 Prompt Testing", False, f"Status: {test_response.status_code}")
                else:
                    self.log_test("Activity 2 Prompt Building", False, f"Status: {build_response.status_code}")
            else:
                self.log_test("Activity 2 Start", False, f"Status: {start_response.status_code}")
                
        except Exception as e:
            self.log_test("Activity 2 Flow", False, f"Error: {str(e)}")
            
        return False
    
    def test_gamification_integration(self):
        """Test gamification integration with activities"""
        print("\n🏆 Testing Gamification Integration...")
        
        try:
            # Test point awarding
            points_response = self.session.post(
                f"{self.base_url}/api/gamification/points/award",
                json={
                    "activity_id": 1,
                    "points": 50
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if points_response.status_code == 200:
                self.log_test("Point Awarding", True, "Points awarded successfully")
                points_data = points_response.json()
                
                # Test badge checking
                badges_response = self.session.get(f"{self.base_url}/api/gamification/user/badges")
                if badges_response.status_code == 200:
                    self.log_test("Badge System", True, "Badge system working")
                    
                    # Test leaderboard
                    leaderboard_response = self.session.get(f"{self.base_url}/api/gamification/leaderboard")
                    if leaderboard_response.status_code == 200:
                        self.log_test("Leaderboard", True, "Leaderboard working")
                        return True
                    else:
                        self.log_test("Leaderboard", False, f"Status: {leaderboard_response.status_code}")
                else:
                    self.log_test("Badge System", False, f"Status: {badges_response.status_code}")
            else:
                self.log_test("Point Awarding", False, f"Status: {points_response.status_code}")
                
        except Exception as e:
            self.log_test("Gamification Integration", False, f"Error: {str(e)}")
            
        return False
    
    def test_theme_personalization(self):
        """Test theme personalization across activities"""
        print("\n🎨 Testing Theme Personalization...")
        
        themes = ["superhelte", "prinsesse"]
        
        for theme in themes:
            try:
                # Set theme
                theme_response = self.session.post(
                    f"{self.base_url}/api/auth/select-theme",
                    json={"theme": theme},
                    headers={'Content-Type': 'application/json'}
                )
                
                if theme_response.status_code == 200:
                    # Test personalized content
                    content_response = self.session.get(f"{self.base_url}/api/activity/1/step/1")
                    if content_response.status_code == 200:
                        content_data = content_response.json()
                        content_text = str(content_data).lower()
                        
                        if theme == "superhelte" and ("superhelt" in content_text or "hero" in content_text):
                            self.log_test(f"Theme {theme.capitalize()}", True, "Theme personalization working")
                        elif theme == "prinsesse" and ("prinsesse" in content_text or "princess" in content_text):
                            self.log_test(f"Theme {theme.capitalize()}", True, "Theme personalization working")
                        else:
                            self.log_test(f"Theme {theme.capitalize()}", False, "Theme not reflected in content")
                    else:
                        self.log_test(f"Theme {theme.capitalize()}", False, f"Content load failed: {content_response.status_code}")
                else:
                    self.log_test(f"Theme {theme.capitalize()}", False, f"Theme selection failed: {theme_response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Theme {theme.capitalize()}", False, f"Error: {str(e)}")
    
    def run_activity_tests(self):
        """Run all activity tests"""
        print("🧪 UTOPAI Activity Test Suite")
        print("=" * 35)
        print(f"Backend: {self.base_url}")
        
        # Setup test user
        if not self.setup_test_user():
            print("❌ Failed to setup test user - aborting tests")
            return False
        
        # Run activity tests
        activity1_ok = self.test_activity_1_flow()
        activity2_ok = self.test_activity_2_flow()
        gamification_ok = self.test_gamification_integration()
        
        # Test theme personalization
        self.test_theme_personalization()
        
        # Summary
        print("\n📊 Activity Test Summary:")
        print("=" * 25)
        
        passed = len([r for r in self.test_results if r['status'] == 'PASS'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Save results
        with open('activity_test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\nDetailed results saved to: activity_test_results.json")
        
        if passed == total:
            print("\n🎉 All activity tests passed!")
            print("✅ Activities ready for production!")
        else:
            print(f"\n🚨 {total - passed} activity tests failed!")
            print("⚠️  Fix issues before production deployment")
        
        return passed == total

def main():
    """Main testing function"""
    if len(sys.argv) != 2:
        print("Usage: python activity_test_suite.py <backend_url>")
        print("Example: python activity_test_suite.py https://utopai-backend.railway.app")
        sys.exit(1)
    
    backend_url = sys.argv[1]
    tester = ActivityTester(backend_url)
    success = tester.run_activity_tests()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

