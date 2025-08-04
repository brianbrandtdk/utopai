import React from 'react';
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-400 via-purple-500 to-pink-500">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-6xl font-bold text-white mb-4">
            🚀 UTOPAI
          </h1>
          <p className="text-xl text-white/90 mb-8">
            Lær AI gennem eventyr og spændende udfordringer!
          </p>
        </div>

        <div className="max-w-md mx-auto bg-white rounded-2xl shadow-2xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
            Velkommen til UTOPAI! 🎉
          </h2>
          
          <div className="space-y-4">
            <div className="p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
              <h3 className="font-bold text-blue-800 mb-2">🔧 Backend Status</h3>
              <p className="text-sm text-blue-700">Kører på port 5003</p>
            </div>
            
            <div className="p-4 bg-green-50 rounded-lg border-2 border-green-200">
              <h3 className="font-bold text-green-800 mb-2">⚛️ Frontend Status</h3>
              <p className="text-sm text-green-700">React app loader korrekt!</p>
            </div>
            
            <div className="p-4 bg-yellow-50 rounded-lg border-2 border-yellow-200">
              <h3 className="font-bold text-yellow-800 mb-2">🎮 Aktivitet 1</h3>
              <p className="text-sm text-yellow-700">Implementeret og klar til test</p>
            </div>
            
            <div className="p-4 bg-purple-50 rounded-lg border-2 border-purple-200">
              <h3 className="font-bold text-purple-800 mb-2">🏆 Gamification</h3>
              <p className="text-sm text-purple-700">Point, badges og leaderboard</p>
            </div>
          </div>

          <div className="mt-8 text-center">
            <button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105">
              🚀 Start Test (Kommer snart)
            </button>
          </div>

          <div className="mt-6 text-center text-sm text-gray-600">
            <p>✅ Backend: Kører</p>
            <p>✅ Frontend: Kører</p>
            <p>⏳ API Integration: Under test</p>
          </div>
        </div>

        <div className="mt-8 text-center">
          <div className="inline-flex space-x-4">
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
              <span className="text-white font-medium">🦸‍♂️ Superhelte Tema</span>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
              <span className="text-white font-medium">👸 Prinsesse Tema</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

