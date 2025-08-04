#!/usr/bin/env python3
"""
Environment Setup and Validation Script for UTOPAI
Validates all required environment variables and configurations
"""
import os
import sys
from urllib.parse import urlparse

class EnvironmentValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def log_error(self, message):
        """Log an error"""
        self.errors.append(message)
        print(f"❌ ERROR: {message}")
        
    def log_warning(self, message):
        """Log a warning"""
        self.warnings.append(message)
        print(f"⚠️  WARNING: {message}")
        
    def log_success(self, message):
        """Log a success"""
        print(f"✅ {message}")
    
    def validate_database_url(self):
        """Validate database URL configuration"""
        print("\n🗄️ Validating Database Configuration...")
        
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            self.log_warning("DATABASE_URL not set - will use SQLite for development")
            return
            
        try:
            parsed = urlparse(database_url)
            
            if parsed.scheme not in ['postgresql', 'postgres']:
                self.log_error(f"Invalid database scheme: {parsed.scheme}. Expected 'postgresql' or 'postgres'")
                return
                
            if not parsed.hostname:
                self.log_error("Database hostname missing in DATABASE_URL")
                return
                
            if not parsed.username:
                self.log_error("Database username missing in DATABASE_URL")
                return
                
            if not parsed.password:
                self.log_error("Database password missing in DATABASE_URL")
                return
                
            self.log_success(f"Database URL valid: {parsed.scheme}://{parsed.hostname}:{parsed.port or 5432}")
            
        except Exception as e:
            self.log_error(f"Invalid DATABASE_URL format: {str(e)}")
    
    def validate_openai_config(self):
        """Validate OpenAI configuration"""
        print("\n🤖 Validating OpenAI Configuration...")
        
        api_key = os.environ.get('OPENAI_API_KEY')
        api_base = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1')
        
        if not api_key:
            self.log_error("OPENAI_API_KEY not set - AI features will not work")
            return
            
        if not api_key.startswith('sk-'):
            self.log_error("OPENAI_API_KEY format invalid - should start with 'sk-'")
            return
            
        if len(api_key) < 20:
            self.log_error("OPENAI_API_KEY too short - check if complete")
            return
            
        self.log_success("OpenAI API key format valid")
        
        # Validate API base URL
        try:
            parsed = urlparse(api_base)
            if not parsed.scheme or not parsed.netloc:
                self.log_error(f"Invalid OPENAI_API_BASE URL: {api_base}")
            else:
                self.log_success(f"OpenAI API base URL valid: {api_base}")
        except Exception as e:
            self.log_error(f"Invalid OPENAI_API_BASE: {str(e)}")
    
    def validate_flask_config(self):
        """Validate Flask configuration"""
        print("\n🌶️ Validating Flask Configuration...")
        
        secret_key = os.environ.get('SECRET_KEY')
        flask_env = os.environ.get('FLASK_ENV', 'development')
        port = os.environ.get('PORT', '5000')
        
        if not secret_key:
            self.log_warning("SECRET_KEY not set - using default (not secure for production)")
        elif len(secret_key) < 16:
            self.log_warning("SECRET_KEY too short - should be at least 16 characters")
        else:
            self.log_success("SECRET_KEY configured")
            
        if flask_env not in ['development', 'production']:
            self.log_warning(f"FLASK_ENV '{flask_env}' not standard - use 'development' or 'production'")
        else:
            self.log_success(f"Flask environment: {flask_env}")
            
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                self.log_error(f"Invalid PORT number: {port}")
            else:
                self.log_success(f"Port configured: {port}")
        except ValueError:
            self.log_error(f"PORT must be a number: {port}")
    
    def validate_cors_config(self):
        """Validate CORS configuration"""
        print("\n🌐 Validating CORS Configuration...")
        
        allowed_origins = os.environ.get('ALLOWED_ORIGINS')
        
        if not allowed_origins:
            self.log_warning("ALLOWED_ORIGINS not set - allowing all origins (not secure for production)")
        else:
            origins = [origin.strip() for origin in allowed_origins.split(',')]
            for origin in origins:
                try:
                    parsed = urlparse(origin)
                    if not parsed.scheme or not parsed.netloc:
                        self.log_error(f"Invalid origin URL: {origin}")
                    else:
                        self.log_success(f"Valid origin: {origin}")
                except Exception as e:
                    self.log_error(f"Invalid origin '{origin}': {str(e)}")
    
    def test_database_connection(self):
        """Test database connection"""
        print("\n🔗 Testing Database Connection...")
        
        try:
            # Import here to avoid issues if dependencies not installed
            sys.path.insert(0, os.path.dirname(__file__))
            from src.main import app
            from src.models.user import db
            
            with app.app_context():
                # Try to connect to database
                db.engine.execute('SELECT 1')
                self.log_success("Database connection successful")
                
                # Check if tables exist
                from sqlalchemy import inspect
                inspector = inspect(db.engine)
                tables = inspector.get_table_names()
                
                expected_tables = ['users', 'islands', 'activities', 'badges', 'user_progress', 'user_badges']
                missing_tables = [table for table in expected_tables if table not in tables]
                
                if missing_tables:
                    self.log_warning(f"Missing tables: {', '.join(missing_tables)} - run database initialization")
                else:
                    self.log_success("All database tables present")
                    
        except ImportError as e:
            self.log_error(f"Cannot import application modules: {str(e)}")
        except Exception as e:
            self.log_error(f"Database connection failed: {str(e)}")
    
    def run_validation(self):
        """Run all validations"""
        print("🔍 UTOPAI Environment Validation")
        print("=" * 40)
        
        self.validate_database_url()
        self.validate_openai_config()
        self.validate_flask_config()
        self.validate_cors_config()
        self.test_database_connection()
        
        # Summary
        print("\n📊 Validation Summary:")
        print("=" * 25)
        
        if self.errors:
            print(f"❌ Errors: {len(self.errors)}")
            for error in self.errors:
                print(f"   • {error}")
                
        if self.warnings:
            print(f"⚠️  Warnings: {len(self.warnings)}")
            for warning in self.warnings:
                print(f"   • {warning}")
                
        if not self.errors and not self.warnings:
            print("✅ All validations passed!")
            
        return len(self.errors) == 0

def main():
    """Main validation function"""
    validator = EnvironmentValidator()
    success = validator.run_validation()
    
    if success:
        print("\n🎉 Environment is ready for deployment!")
    else:
        print("\n🚨 Please fix errors before deployment!")
        
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

