#!/usr/bin/env node
/**
 * Frontend Build Test Script for UTOPAI
 * Tests build process and validates output
 */

import { execSync } from 'child_process';
import { existsSync, readFileSync, statSync } from 'fs';
import { join } from 'path';

class FrontendTester {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.buildDir = 'dist';
  }

  log(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const prefix = {
      'error': '❌',
      'warning': '⚠️ ',
      'success': '✅',
      'info': 'ℹ️ '
    }[type] || 'ℹ️ ';
    
    console.log(`${prefix} ${message}`);
    
    if (type === 'error') this.errors.push(message);
    if (type === 'warning') this.warnings.push(message);
  }

  testEnvironmentVariables() {
    this.log('Testing Environment Variables...', 'info');
    
    const envFiles = ['.env.example', '.env.production', '.env.development'];
    
    for (const envFile of envFiles) {
      if (existsSync(envFile)) {
        this.log(`Found ${envFile}`, 'success');
        
        const content = readFileSync(envFile, 'utf8');
        if (content.includes('VITE_API_BASE_URL')) {
          this.log(`${envFile} contains required VITE_API_BASE_URL`, 'success');
        } else {
          this.log(`${envFile} missing VITE_API_BASE_URL`, 'error');
        }
      } else {
        this.log(`Missing ${envFile}`, 'warning');
      }
    }
  }

  testBuildProcess() {
    this.log('Testing Build Process...', 'info');
    
    try {
      // Clean previous build
      if (existsSync(this.buildDir)) {
        this.log('Cleaning previous build...', 'info');
        execSync(`rm -rf ${this.buildDir}`, { stdio: 'pipe' });
      }
      
      // Test production build
      this.log('Running production build...', 'info');
      const buildOutput = execSync('npm run build:production', { 
        encoding: 'utf8',
        stdio: 'pipe'
      });
      
      this.log('Production build completed successfully', 'success');
      
      // Check if build directory exists
      if (existsSync(this.buildDir)) {
        this.log(`Build directory ${this.buildDir} created`, 'success');
      } else {
        this.log(`Build directory ${this.buildDir} not found`, 'error');
        return false;
      }
      
      return true;
      
    } catch (error) {
      this.log(`Build failed: ${error.message}`, 'error');
      return false;
    }
  }

  testBuildOutput() {
    this.log('Testing Build Output...', 'info');
    
    const requiredFiles = [
      'index.html',
      'assets'
    ];
    
    for (const file of requiredFiles) {
      const filePath = join(this.buildDir, file);
      if (existsSync(filePath)) {
        this.log(`Found required file: ${file}`, 'success');
      } else {
        this.log(`Missing required file: ${file}`, 'error');
      }
    }
    
    // Check index.html content
    const indexPath = join(this.buildDir, 'index.html');
    if (existsSync(indexPath)) {
      const indexContent = readFileSync(indexPath, 'utf8');
      
      if (indexContent.includes('<div id="root">')) {
        this.log('index.html contains React root element', 'success');
      } else {
        this.log('index.html missing React root element', 'error');
      }
      
      if (indexContent.includes('UTOPAI')) {
        this.log('index.html contains app title', 'success');
      } else {
        this.log('index.html missing app title', 'warning');
      }
    }
    
    // Check assets directory
    const assetsPath = join(this.buildDir, 'assets');
    if (existsSync(assetsPath)) {
      const files = execSync(`ls ${assetsPath}`, { encoding: 'utf8' }).split('\n').filter(f => f);
      
      const hasJS = files.some(f => f.endsWith('.js'));
      const hasCSS = files.some(f => f.endsWith('.css'));
      
      if (hasJS) {
        this.log('Found JavaScript assets', 'success');
      } else {
        this.log('No JavaScript assets found', 'error');
      }
      
      if (hasCSS) {
        this.log('Found CSS assets', 'success');
      } else {
        this.log('No CSS assets found', 'warning');
      }
      
      this.log(`Total assets: ${files.length}`, 'info');
    }
  }

  testBuildSize() {
    this.log('Testing Build Size...', 'info');
    
    if (!existsSync(this.buildDir)) {
      this.log('Build directory not found for size test', 'error');
      return;
    }
    
    try {
      const sizeOutput = execSync(`du -sh ${this.buildDir}`, { encoding: 'utf8' });
      const size = sizeOutput.split('\t')[0];
      
      this.log(`Total build size: ${size}`, 'info');
      
      // Parse size for warnings
      const sizeNum = parseFloat(size);
      const unit = size.replace(sizeNum.toString(), '').trim();
      
      if (unit === 'M' && sizeNum > 10) {
        this.log(`Build size ${size} is quite large (>10MB)`, 'warning');
      } else if (unit === 'G') {
        this.log(`Build size ${size} is very large (>1GB)`, 'error');
      } else {
        this.log(`Build size ${size} is reasonable`, 'success');
      }
      
    } catch (error) {
      this.log(`Could not determine build size: ${error.message}`, 'warning');
    }
  }

  testPreview() {
    this.log('Testing Preview Server...', 'info');
    
    try {
      // Start preview server in background
      this.log('Starting preview server...', 'info');
      
      // Note: This would normally start a server, but for testing we just check if the command exists
      execSync('npm run preview --help', { stdio: 'pipe' });
      this.log('Preview command available', 'success');
      
      this.log('Preview server test completed (manual verification required)', 'info');
      
    } catch (error) {
      this.log(`Preview test failed: ${error.message}`, 'error');
    }
  }

  runAllTests() {
    console.log('🧪 UTOPAI Frontend Build Test');
    console.log('=' * 40);
    
    this.testEnvironmentVariables();
    
    const buildSuccess = this.testBuildProcess();
    if (buildSuccess) {
      this.testBuildOutput();
      this.testBuildSize();
      this.testPreview();
    }
    
    // Summary
    console.log('\n📊 Test Summary:');
    console.log('=' * 20);
    
    if (this.errors.length > 0) {
      console.log(`❌ Errors: ${this.errors.length}`);
      this.errors.forEach(error => console.log(`   • ${error}`));
    }
    
    if (this.warnings.length > 0) {
      console.log(`⚠️  Warnings: ${this.warnings.length}`);
      this.warnings.forEach(warning => console.log(`   • ${warning}`));
    }
    
    if (this.errors.length === 0 && this.warnings.length === 0) {
      console.log('✅ All tests passed!');
      console.log('🚀 Frontend ready for Vercel deployment!');
    } else if (this.errors.length === 0) {
      console.log('✅ Build successful with warnings');
      console.log('🚀 Frontend ready for deployment (check warnings)');
    } else {
      console.log('❌ Build failed - fix errors before deployment');
    }
    
    return this.errors.length === 0;
  }
}

// Run tests
const tester = new FrontendTester();
const success = tester.runAllTests();

process.exit(success ? 0 : 1);

