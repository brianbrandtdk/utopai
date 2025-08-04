import React, { useState } from 'react';
import './App.css';

// Simple API service
const api = {
  async get(endpoint) {
    const response = await fetch(`http://localhost:5002/api${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'API fejl');
    }
    
    return response.json();
  },

  async post(endpoint, data) {
    const response = await fetch(`http://localhost:5002/api${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'API fejl');
    }
    
    return response.json();
  }
};

function App() {
  const [currentView, setCurrentView] = useState('login');
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  const handleLogin = async (email, password, userType) => {
    try {
      setError('');
      const response = await api.post('/auth/login', {
        email,
        password,
        user_type: userType
      });
      
      setUser(response.user);
      
      if (!response.user.chosen_theme) {
        setCurrentView('theme_select');
      } else {
        setCurrentView('dashboard');
      }
    } catch (err) {
      setError(err.message || 'Login fejlede');
    }
  };

  const handleThemeSelect = async (theme) => {
    try {
      setError('');
      const response = await api.post('/auth/select-theme', { theme });
      setUser(response.user);
      setCurrentView('dashboard');
    } catch (err) {
      setError(err.message || 'Tema-valg fejlede');
    }
  };

  // Login Screen
  if (currentView === 'login') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-purple-900 p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">UTOPAI</h1>
            <p className="text-gray-600">Log ind til dit eventyr</p>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <LoginForm onLogin={handleLogin} onSwitchToRegister={() => setCurrentView('register')} />
        </div>
      </div>
    );
  }

  // Theme Selection
  if (currentView === 'theme_select') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-purple-900 p-4">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-8">UTOPAI</h1>
          <p className="text-xl text-gray-200 mb-8">Vælg dit eventyr!</p>
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 max-w-md mx-auto">
              {error}
            </div>
          )}
          
          <div className="flex gap-8 justify-center">
            <div 
              className="bg-gradient-to-br from-blue-600 to-red-600 p-8 rounded-2xl text-white text-center cursor-pointer hover:scale-105 transition-transform"
              onClick={() => handleThemeSelect('superhelte')}
            >
              <div className="text-6xl mb-4">🦸‍♂️</div>
              <h2 className="text-2xl font-bold mb-2">Superhelte</h2>
              <p className="mb-4">Bliv en AI-superhelt og red verden!</p>
              <button className="bg-white/20 px-6 py-2 rounded-lg hover:bg-white/30 transition-colors">
                Vælg Superhelte
              </button>
            </div>
            
            <div 
              className="bg-gradient-to-br from-pink-500 to-purple-600 p-8 rounded-2xl text-white text-center cursor-pointer hover:scale-105 transition-transform"
              onClick={() => handleThemeSelect('prinsesse')}
            >
              <div className="text-6xl mb-4">👸</div>
              <h2 className="text-2xl font-bold mb-2">Prinsesse</h2>
              <p className="mb-4">Udforsk det magiske AI-kongerige!</p>
              <button className="bg-white/20 px-6 py-2 rounded-lg hover:bg-white/30 transition-colors">
                Vælg Prinsesse
              </button>
            </div>
          </div>
          
          <p className="text-gray-300 mt-6">Du kan altid ændre dit tema senere i indstillingerne</p>
        </div>
      </div>
    );
  }

  // Dashboard
  if (currentView === 'dashboard') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-purple-900 p-4">
        <div className="text-center text-white">
          <h1 className="text-4xl font-bold mb-4">
            {user?.chosen_theme === 'superhelte' ? '🦸‍♂️' : '👸'} Velkommen, {user?.username}!
          </h1>
          <p className="text-xl mb-8">Dit AI-eventyr begynder nu!</p>
          
          <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
              <div className="text-3xl mb-2">⭐</div>
              <div className="text-2xl font-bold">{user?.total_points || 0}</div>
              <div className="text-gray-300 text-sm">Total Point</div>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
              <div className="text-3xl mb-2">🏝️</div>
              <div className="text-2xl font-bold">{user?.current_island || 1}</div>
              <div className="text-gray-300 text-sm">Nuværende Ø</div>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
              <div className="text-3xl mb-2">🎯</div>
              <div className="text-2xl font-bold">0%</div>
              <div className="text-gray-300 text-sm">Gennemført</div>
            </div>
          </div>
          
          <div className="space-y-4">
            <button 
              onClick={() => setCurrentView('island_map')}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              🏝️ Gå til Øer
            </button>
            
            <br />
            
            <button 
              onClick={() => {
                setUser(null);
                setCurrentView('login');
              }}
              className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              Log ud
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Island Map (placeholder)
  if (currentView === 'island_map') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-purple-900 p-4">
        <div className="text-center text-white">
          <button
            onClick={() => setCurrentView('dashboard')}
            className="mb-4 text-white/70 hover:text-white"
          >
            ← Tilbage til dashboard
          </button>
          
          <h1 className="text-4xl font-bold mb-8">
            {user?.chosen_theme === 'superhelte' ? '🦸‍♂️ Prompt City' : '👸 Prompt Palace'}
          </h1>
          
          <div className="max-w-2xl mx-auto bg-white/10 backdrop-blur-sm rounded-xl p-8">
            <h2 className="text-2xl font-bold mb-6">Ø 1: ChatGPT & Prompting</h2>
            <p className="text-gray-200 mb-8">Lær at mestre ChatGPT og prompting!</p>
            
            <div className="text-center">
              <p className="text-lg mb-4">Øer og aktiviteter kommer snart!</p>
              <p className="text-sm text-gray-300">
                Her vil du kunne se alle aktiviteter og din fremgang
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
}

// Login Form Component
const LoginForm = ({ onLogin, onSwitchToRegister }) => {
  const [email, setEmail] = useState('test3@barn.dk'); // Pre-filled for testing
  const [password, setPassword] = useState('test123');
  const [userType, setUserType] = useState('child');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(email, password, userType);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Adgangskode</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Jeg er</label>
        <select
          value={userType}
          onChange={(e) => setUserType(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="child">Barn</option>
          <option value="parent">Forælder</option>
        </select>
      </div>
      
      <button
        type="submit"
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300"
      >
        Log ind
      </button>
      
      <button
        type="button"
        onClick={onSwitchToRegister}
        className="w-full text-blue-600 hover:text-blue-800 text-sm"
      >
        Har du ikke en konto? Opret en her
      </button>
    </form>
  );
};

export default App;

