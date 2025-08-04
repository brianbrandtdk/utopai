#!/usr/bin/env python3
"""
User Experience Validator for UTOPAI
Tests user flows and experience quality
"""
import requests
import json
import sys
import time
from datetime import datetime

class UXValidator:
    def __init__(self, backend_url, frontend_url):
        self.backend_url = backend_url.rstrip('/')
        self.frontend_url = frontend_url.rstrip('/')
        self.session = requests.Session()
        self.ux_results = []
        
    def log_ux(self, test_name, status, message, score=None):
        """Log UX test result"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'test': test_name,
            'status': 'PASS' if status else 'FAIL',
            'message': message,
            'score': score
        }
        self.ux_results.append(result)
        status_icon = "✅" if status else "❌"
        score_text = f" (Score: {score}/10)" if score else ""
        print(f"{status_icon} {test_name}: {message}{score_text}")
    
    def test_onboarding_flow(self):
        """Test user onboarding experience"""
        print("\n👋 Testing Onboarding Flow...")
        
        # Test registration flow
        test_user = {
            "name": "UX Test User",
            "username": f"ux_test_{int(time.time())}",
            "password": "testpass123",
            "user_type": "child"
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.backend_url}/api/auth/register",
                json=test_user,
                headers={'Content-Type': 'application/json'}
            )
            registration_time = (time.time() - start_time) * 1000
            
            if response.status_code == 201:
                if registration_time < 2000:  # Less than 2 seconds
                    self.log_ux("Registration Speed", True, f"Fast registration ({registration_time:.0f}ms)", 9)
                elif registration_time < 5000:  # Less than 5 seconds
                    self.log_ux("Registration Speed", True, f"Acceptable registration ({registration_time:.0f}ms)", 7)
                else:
                    self.log_ux("Registration Speed", False, f"Slow registration ({registration_time:.0f}ms)", 4)
                    
                # Test immediate login after registration
                login_response = self.session.post(
                    f"{self.backend_url}/api/auth/login",
                    json={
                        "username": test_user["username"],
                        "password": test_user["password"]
                    },
                    headers={'Content-Type': 'application/json'}
                )
                
                if login_response.status_code == 200:
                    self.log_ux("Post-Registration Login", True, "Seamless login after registration", 10)
                else:
                    self.log_ux("Post-Registration Login", False, "Login failed after registration", 2)
                    
            else:
                self.log_ux("Registration Flow", False, f"Registration failed: {response.status_code}", 1)
                
        except Exception as e:
            self.log_ux("Onboarding Flow", False, f"Error: {str(e)}", 1)
    
    def test_theme_selection_ux(self):
        """Test theme selection user experience"""
        print("\n🎨 Testing Theme Selection UX...")
        
        themes = ["superhelte", "prinsesse"]
        
        for theme in themes:
            try:
                start_time = time.time()
                response = self.session.post(
                    f"{self.backend_url}/api/auth/select-theme",
                    json={"theme": theme},
                    headers={'Content-Type': 'application/json'}
                )
                theme_time = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    if theme_time < 1000:  # Less than 1 second
                        self.log_ux(f"Theme {theme.capitalize()} Speed", True, f"Instant theme change ({theme_time:.0f}ms)", 10)
                    elif theme_time < 3000:  # Less than 3 seconds
                        self.log_ux(f"Theme {theme.capitalize()} Speed", True, f"Fast theme change ({theme_time:.0f}ms)", 8)
                    else:
                        self.log_ux(f"Theme {theme.capitalize()} Speed", False, f"Slow theme change ({theme_time:.0f}ms)", 5)
                        
                    # Test theme persistence
                    verify_response = self.session.get(f"{self.backend_url}/api/auth/me")
                    if verify_response.status_code == 200:
                        user_data = verify_response.json()
                        if user_data.get('theme') == theme:
                            self.log_ux(f"Theme {theme.capitalize()} Persistence", True, "Theme saved correctly", 10)
                        else:
                            self.log_ux(f"Theme {theme.capitalize()} Persistence", False, "Theme not saved", 3)
                else:
                    self.log_ux(f"Theme {theme.capitalize()} Selection", False, f"Failed: {response.status_code}", 2)
                    
            except Exception as e:
                self.log_ux(f"Theme {theme.capitalize()} UX", False, f"Error: {str(e)}", 1)
    
    def test_activity_navigation_ux(self):
        """Test activity navigation user experience"""
        print("\n🗺️ Testing Activity Navigation UX...")
        
        try:
            # Test islands loading
            start_time = time.time()
            islands_response = self.session.get(f"{self.backend_url}/api/islands")
            islands_time = (time.time() - start_time) * 1000
            
            if islands_response.status_code == 200:
                islands = islands_response.json()
                
                if islands_time < 1000:  # Less than 1 second
                    self.log_ux("Islands Loading", True, f"Fast islands load ({islands_time:.0f}ms)", 9)
                elif islands_time < 3000:  # Less than 3 seconds
                    self.log_ux("Islands Loading", True, f"Acceptable islands load ({islands_time:.0f}ms)", 7)
                else:
                    self.log_ux("Islands Loading", False, f"Slow islands load ({islands_time:.0f}ms)", 4)
                
                # Test activity starting
                for activity_id in [1, 2]:
                    start_time = time.time()
                    activity_response = self.session.post(f"{self.backend_url}/api/activity/{activity_id}/start")
                    activity_time = (time.time() - start_time) * 1000
                    
                    if activity_response.status_code == 200:
                        if activity_time < 2000:  # Less than 2 seconds
                            self.log_ux(f"Activity {activity_id} Start", True, f"Quick start ({activity_time:.0f}ms)", 9)
                        elif activity_time < 5000:  # Less than 5 seconds
                            self.log_ux(f"Activity {activity_id} Start", True, f"Acceptable start ({activity_time:.0f}ms)", 7)
                        else:
                            self.log_ux(f"Activity {activity_id} Start", False, f"Slow start ({activity_time:.0f}ms)", 4)
                    else:
                        self.log_ux(f"Activity {activity_id} Start", False, f"Failed: {activity_response.status_code}", 2)
                        
            else:
                self.log_ux("Islands Loading", False, f"Failed: {islands_response.status_code}", 1)
                
        except Exception as e:
            self.log_ux("Activity Navigation", False, f"Error: {str(e)}", 1)
    
    def test_ai_interaction_ux(self):
        """Test AI interaction user experience"""
        print("\n🤖 Testing AI Interaction UX...")
        
        # Test Activity 1 AI responses
        try:
            start_time = time.time()
            ai_response = self.session.get(f"{self.backend_url}/api/activity/1/step/1")
            ai_time = (time.time() - start_time) * 1000
            
            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                
                # Test response time
                if ai_time < 3000:  # Less than 3 seconds
                    self.log_ux("AI Response Time", True, f"Fast AI response ({ai_time:.0f}ms)", 9)
                elif ai_time < 8000:  # Less than 8 seconds
                    self.log_ux("AI Response Time", True, f"Acceptable AI response ({ai_time:.0f}ms)", 7)
                else:
                    self.log_ux("AI Response Time", False, f"Slow AI response ({ai_time:.0f}ms)", 4)
                
                # Test content quality (basic checks)
                content = str(ai_data).lower()
                if len(content) > 100:  # Substantial content
                    self.log_ux("AI Content Quality", True, "Rich AI content provided", 8)
                elif len(content) > 50:  # Minimal content
                    self.log_ux("AI Content Quality", True, "Basic AI content provided", 6)
                else:
                    self.log_ux("AI Content Quality", False, "Insufficient AI content", 3)
                    
            else:
                self.log_ux("AI Interaction", False, f"AI request failed: {ai_response.status_code}", 1)
                
        except Exception as e:
            self.log_ux("AI Interaction", False, f"Error: {str(e)}", 1)
    
    def test_gamification_feedback_ux(self):
        """Test gamification feedback user experience"""
        print("\n🏆 Testing Gamification Feedback UX...")
        
        try:
            # Test point awarding
            start_time = time.time()
            points_response = self.session.post(
                f"{self.backend_url}/api/gamification/points/award",
                json={
                    "activity_id": 1,
                    "points": 50
                },
                headers={'Content-Type': 'application/json'}
            )
            points_time = (time.time() - start_time) * 1000
            
            if points_response.status_code == 200:
                if points_time < 1000:  # Less than 1 second
                    self.log_ux("Point Feedback Speed", True, f"Instant feedback ({points_time:.0f}ms)", 10)
                elif points_time < 3000:  # Less than 3 seconds
                    self.log_ux("Point Feedback Speed", True, f"Fast feedback ({points_time:.0f}ms)", 8)
                else:
                    self.log_ux("Point Feedback Speed", False, f"Slow feedback ({points_time:.0f}ms)", 5)
                    
                # Test badge checking
                badges_response = self.session.get(f"{self.backend_url}/api/gamification/user/badges")
                if badges_response.status_code == 200:
                    badges_data = badges_response.json()
                    if isinstance(badges_data, list) and len(badges_data) > 0:
                        self.log_ux("Badge System UX", True, "Badge system provides feedback", 9)
                    else:
                        self.log_ux("Badge System UX", True, "Badge system accessible", 7)
                else:
                    self.log_ux("Badge System UX", False, f"Badge system failed: {badges_response.status_code}", 3)
                    
            else:
                self.log_ux("Gamification Feedback", False, f"Points failed: {points_response.status_code}", 2)
                
        except Exception as e:
            self.log_ux("Gamification UX", False, f"Error: {str(e)}", 1)
    
    def test_error_handling_ux(self):
        """Test error handling user experience"""
        print("\n🚨 Testing Error Handling UX...")
        
        # Test invalid login
        try:
            error_response = self.session.post(
                f"{self.backend_url}/api/auth/login",
                json={
                    "username": "nonexistent_user",
                    "password": "wrong_password"
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if error_response.status_code == 401:
                error_data = error_response.json()
                if 'error' in error_data and len(error_data['error']) > 10:
                    self.log_ux("Error Messages", True, "Clear error messages provided", 8)
                else:
                    self.log_ux("Error Messages", False, "Unclear error messages", 4)
            else:
                self.log_ux("Error Handling", False, f"Unexpected error response: {error_response.status_code}", 3)
                
        except Exception as e:
            self.log_ux("Error Handling", False, f"Error handling failed: {str(e)}", 1)
    
    def run_ux_validation(self):
        """Run complete UX validation"""
        print("🎯 UTOPAI User Experience Validation")
        print("=" * 40)
        print(f"Backend: {self.backend_url}")
        print(f"Frontend: {self.frontend_url}")
        
        # Run UX tests
        self.test_onboarding_flow()
        self.test_theme_selection_ux()
        self.test_activity_navigation_ux()
        self.test_ai_interaction_ux()
        self.test_gamification_feedback_ux()
        self.test_error_handling_ux()
        
        # Calculate overall UX score
        scores = [r['score'] for r in self.ux_results if r['score'] is not None]
        if scores:
            avg_score = sum(scores) / len(scores)
            
            print(f"\n📊 UX Validation Summary:")
            print("=" * 25)
            
            passed = len([r for r in self.ux_results if r['status'] == 'PASS'])
            total = len(self.ux_results)
            
            print(f"Total Tests: {total}")
            print(f"Passed: {passed}")
            print(f"Failed: {total - passed}")
            print(f"Success Rate: {(passed/total)*100:.1f}%")
            print(f"Average UX Score: {avg_score:.1f}/10")
            
            # UX Grade
            if avg_score >= 9:
                grade = "A+ (Excellent UX)"
            elif avg_score >= 8:
                grade = "A (Great UX)"
            elif avg_score >= 7:
                grade = "B (Good UX)"
            elif avg_score >= 6:
                grade = "C (Acceptable UX)"
            else:
                grade = "D (Poor UX - Needs Improvement)"
                
            print(f"UX Grade: {grade}")
            
            # Save results
            with open('ux_validation_results.json', 'w') as f:
                json.dump({
                    'summary': {
                        'total_tests': total,
                        'passed': passed,
                        'failed': total - passed,
                        'success_rate': (passed/total)*100,
                        'average_score': avg_score,
                        'grade': grade
                    },
                    'results': self.ux_results
                }, f, indent=2)
            
            print(f"\nDetailed results saved to: ux_validation_results.json")
            
            if avg_score >= 7 and passed >= total * 0.8:
                print("\n🎉 UX validation passed!")
                print("✅ User experience ready for production!")
                return True
            else:
                print("\n⚠️  UX validation needs improvement")
                print("🔧 Address issues before production deployment")
                return False
        else:
            print("\n❌ No UX scores available")
            return False

def main():
    """Main validation function"""
    if len(sys.argv) != 3:
        print("Usage: python user_experience_validator.py <backend_url> <frontend_url>")
        print("Example: python user_experience_validator.py https://utopai-backend.railway.app https://utopai-frontend.vercel.app")
        sys.exit(1)
    
    backend_url = sys.argv[1]
    frontend_url = sys.argv[2]
    
    validator = UXValidator(backend_url, frontend_url)
    success = validator.run_ux_validation()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

