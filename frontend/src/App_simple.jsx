import React from 'react';
import './App.css';

function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-purple-900">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-white mb-4">UTOPAI</h1>
        <p className="text-xl text-gray-200 mb-8">Lær AI gennem eventyr!</p>
        
        <div className="space-y-4">
          <button 
            onClick={() => alert('Test knap virker! 🚀')}
            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            Test Knap 🚀
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;

