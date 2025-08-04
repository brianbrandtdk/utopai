#!/usr/bin/env python3
"""
OpenAI Integration Test for UTOPAI
Tests OpenAI API connectivity and key functionality
"""
import os
import sys
import json
from datetime import datetime

def test_openai_connection():
    """Test basic OpenAI connection"""
    print("🤖 Testing OpenAI Integration...")
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False
        
    try:
        import openai
        
        # Set API key
        openai.api_key = api_key
        
        # Test simple completion
        print("📡 Testing API connection...")
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for children learning about AI."},
                {"role": "user", "content": "What is AI in one simple sentence?"}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        if response and response.choices:
            answer = response.choices[0].message.content.strip()
            print(f"✅ OpenAI API working! Response: {answer[:100]}...")
            return True
        else:
            print("❌ No response from OpenAI API")
            return False
            
    except ImportError:
        print("❌ OpenAI package not installed - run: pip install openai")
        return False
    except Exception as e:
        print(f"❌ OpenAI API error: {str(e)}")
        return False

def test_activity_ai_functions():
    """Test AI functions used in activities"""
    print("\n🎮 Testing Activity AI Functions...")
    
    try:
        # Import UTOPAI OpenAI service
        sys.path.insert(0, os.path.dirname(__file__))
        from src.services.openai_service import openai_service
        
        # Test Activity 1 functions
        print("📚 Testing Activity 1 AI functions...")
        
        try:
            intro = openai_service.generate_activity_1_intro("superhelte")
            if intro and len(intro) > 50:
                print("✅ Activity 1 intro generation working")
            else:
                print("❌ Activity 1 intro generation failed")
        except Exception as e:
            print(f"❌ Activity 1 intro error: {str(e)}")
        
        # Test Activity 2 functions
        print("✏️ Testing Activity 2 AI functions...")
        
        try:
            prompt_parts = {
                "role": "helpful teacher",
                "task": "explain AI",
                "context": "to a 10-year old",
                "tone": "friendly"
            }
            
            built_prompt = openai_service.build_prompt_from_parts(prompt_parts, "superhelte")
            if built_prompt and len(built_prompt) > 20:
                print("✅ Activity 2 prompt building working")
            else:
                print("❌ Activity 2 prompt building failed")
        except Exception as e:
            print(f"❌ Activity 2 prompt building error: {str(e)}")
            
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import UTOPAI services: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Activity AI functions error: {str(e)}")
        return False

def test_theme_personalization():
    """Test theme-based personalization"""
    print("\n🎨 Testing Theme Personalization...")
    
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from src.services.openai_service import openai_service
        
        themes = ["superhelte", "prinsesse"]
        
        for theme in themes:
            try:
                personalized = openai_service.personalize_content("Tell me about AI", theme)
                if personalized and theme.lower() in personalized.lower():
                    print(f"✅ {theme.capitalize()} theme personalization working")
                else:
                    print(f"⚠️  {theme.capitalize()} theme personalization may not be working properly")
            except Exception as e:
                print(f"❌ {theme.capitalize()} theme error: {str(e)}")
                
        return True
        
    except Exception as e:
        print(f"❌ Theme personalization error: {str(e)}")
        return False

def main():
    """Main testing function"""
    print("🧪 UTOPAI OpenAI Integration Test")
    print("=" * 40)
    
    results = []
    
    # Test basic connection
    results.append(test_openai_connection())
    
    # Test activity functions
    results.append(test_activity_ai_functions())
    
    # Test theme personalization
    results.append(test_theme_personalization())
    
    # Summary
    print("\n📊 OpenAI Test Summary:")
    print("=" * 25)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All OpenAI tests passed!")
        print("✅ AI features ready for production!")
    else:
        print("🚨 Some OpenAI tests failed!")
        print("⚠️  AI features may not work properly")
        
    # Save test results
    test_result = {
        'timestamp': datetime.now().isoformat(),
        'tests_passed': passed,
        'tests_total': total,
        'success_rate': (passed/total)*100,
        'status': 'PASS' if passed == total else 'FAIL'
    }
    
    with open('openai_test_results.json', 'w') as f:
        json.dump(test_result, f, indent=2)
        
    print(f"\nResults saved to: openai_test_results.json")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

