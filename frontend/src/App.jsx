import React, { useState, useEffect } from 'react';
import './App.css';
import { api } from './lib/api';
import ThemeSelector from './components/ThemeSelector';
import IslandMap from './components/IslandMap';
import Dashboard from './components/Dashboard';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentView, setCurrentView] = useState('login'); // login, register, theme_select, dashboard, island_map, activity
  const [selectedActivity, setSelectedActivity] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await api.get('/auth/me');
      setUser(response.user);
      
      if (!response.user.chosen_theme) {
        setCurrentView('theme_select');
      } else {
        setCurrentView('dashboard');
      }
    } catch (err) {
      setCurrentView('login');
    } finally {
      setLoading(false);
    }
  };

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

  const handleRegister = async (formData) => {
    try {
      setError('');
      const response = await api.post('/auth/register', formData);
      setUser(response.child);
      setCurrentView('theme_select');
    } catch (err) {
      setError(err.message || 'Registrering fejlede');
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

  const handleLogout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setUser(null);
      setCurrentView('login');
    }
  };

  const handleActivitySelect = (activity) => {
    setSelectedActivity(activity);
    setCurrentView('activity');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-purple-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-white">Indlæser UTOPAI...</p>
        </div>
      </div>
    );
  }

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

  // Register Screen
  if (currentView === 'register') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-purple-900 p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-lg">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">UTOPAI</h1>
            <p className="text-gray-600">Opret ny konto</p>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <RegisterForm onRegister={handleRegister} onSwitchToLogin={() => setCurrentView('login')} />
        </div>
      </div>
    );
  }

  // Theme Selection
  if (currentView === 'theme_select') {
    return <ThemeSelector onThemeSelect={handleThemeSelect} error={error} />;
  }

  // Dashboard
  if (currentView === 'dashboard') {
    return (
      <div>
        <Dashboard user={user} onLogout={handleLogout} />
        
        {/* Navigation */}
        <div className="fixed bottom-0 left-0 right-0 bg-white/10 backdrop-blur-sm border-t border-white/20">
          <div className="flex justify-around py-4">
            <button
              onClick={() => setCurrentView('dashboard')}
              className={`flex flex-col items-center space-y-1 px-4 py-2 rounded-lg transition-colors ${
                currentView === 'dashboard' ? 'bg-white/20 text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              <span className="text-xl">🏠</span>
              <span className="text-xs">Hjem</span>
            </button>
            
            <button
              onClick={() => setCurrentView('island_map')}
              className={`flex flex-col items-center space-y-1 px-4 py-2 rounded-lg transition-colors ${
                currentView === 'island_map' ? 'bg-white/20 text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              <span className="text-xl">🏝️</span>
              <span className="text-xs">Øer</span>
            </button>
            
            <button
              onClick={() => setCurrentView('leaderboard')}
              className={`flex flex-col items-center space-y-1 px-4 py-2 rounded-lg transition-colors ${
                currentView === 'leaderboard' ? 'bg-white/20 text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              <span className="text-xl">🏆</span>
              <span className="text-xs">Toplist</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Island Map
  if (currentView === 'island_map') {
    return (
      <div>
        <IslandMap user={user} onActivitySelect={handleActivitySelect} />
        
        {/* Navigation */}
        <div className="fixed bottom-0 left-0 right-0 bg-white/10 backdrop-blur-sm border-t border-white/20">
          <div className="flex justify-around py-4">
            <button
              onClick={() => setCurrentView('dashboard')}
              className={`flex flex-col items-center space-y-1 px-4 py-2 rounded-lg transition-colors ${
                currentView === 'dashboard' ? 'bg-white/20 text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              <span className="text-xl">🏠</span>
              <span className="text-xs">Hjem</span>
            </button>
            
            <button
              onClick={() => setCurrentView('island_map')}
              className={`flex flex-col items-center space-y-1 px-4 py-2 rounded-lg transition-colors ${
                currentView === 'island_map' ? 'bg-white/20 text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              <span className="text-xl">🏝️</span>
              <span className="text-xs">Øer</span>
            </button>
            
            <button
              onClick={() => setCurrentView('leaderboard')}
              className={`flex flex-col items-center space-y-1 px-4 py-2 rounded-lg transition-colors ${
                currentView === 'leaderboard' ? 'bg-white/20 text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              <span className="text-xl">🏆</span>
              <span className="text-xs">Toplist</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Activity View (placeholder for now)
  if (currentView === 'activity' && selectedActivity) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-purple-900 p-4">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-white">
            <button
              onClick={() => setCurrentView('island_map')}
              className="mb-4 text-white/70 hover:text-white"
            >
              ← Tilbage til øer
            </button>
            
            <h1 className="text-2xl font-bold mb-4">{selectedActivity.name}</h1>
            <p className="text-gray-200 mb-6">{selectedActivity.description}</p>
            
            <div className="text-center">
              <p className="text-lg mb-4">Aktivitet kommer snart!</p>
              <p className="text-sm text-gray-300">
                Type: {selectedActivity.activity_type} | 
                Niveau: {selectedActivity.difficulty_level} | 
                Point: {selectedActivity.points_reward}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Leaderboard placeholder
  if (currentView === 'leaderboard') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 to-purple-900 p-4">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-white text-center">
            <h1 className="text-2xl font-bold mb-4">🏆 Toplist</h1>
            <p className="text-gray-200 mb-6">Se hvem der er bedst til AI!</p>
            <p className="text-lg">Toplist kommer snart!</p>
          </div>
        </div>
        
        {/* Navigation */}
        <div className="fixed bottom-0 left-0 right-0 bg-white/10 backdrop-blur-sm border-t border-white/20">
          <div className="flex justify-around py-4">
            <button
              onClick={() => setCurrentView('dashboard')}
              className={`flex flex-col items-center space-y-1 px-4 py-2 rounded-lg transition-colors ${
                currentView === 'dashboard' ? 'bg-white/20 text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              <span className="text-xl">🏠</span>
              <span className="text-xs">Hjem</span>
            </button>
            
            <button
              onClick={() => setCurrentView('island_map')}
              className={`flex flex-col items-center space-y-1 px-4 py-2 rounded-lg transition-colors ${
                currentView === 'island_map' ? 'bg-white/20 text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              <span className="text-xl">🏝️</span>
              <span className="text-xs">Øer</span>
            </button>
            
            <button
              onClick={() => setCurrentView('leaderboard')}
              className={`flex flex-col items-center space-y-1 px-4 py-2 rounded-lg transition-colors ${
                currentView === 'leaderboard' ? 'bg-white/20 text-white' : 'text-white/70 hover:text-white'
              }`}
            >
              <span className="text-xl">🏆</span>
              <span className="text-xs">Toplist</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
}

// Login Form Component
const LoginForm = ({ onLogin, onSwitchToRegister }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
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

// Register Form Component  
const RegisterForm = ({ onRegister, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    child_username: '',
    child_email: '',
    child_password: '',
    child_date_of_birth: '',
    parent_first_name: '',
    parent_last_name: '',
    parent_email: '',
    parent_password: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onRegister(formData);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="border-b pb-4 mb-4">
        <h3 className="font-semibold text-gray-800 mb-3">Barnets oplysninger</h3>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Brugernavn</label>
            <input
              type="text"
              name="child_username"
              value={formData.child_username}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              name="child_email"
              value={formData.child_email}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Adgangskode</label>
            <input
              type="password"
              name="child_password"
              value={formData.child_password}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fødselsdato</label>
            <input
              type="date"
              name="child_date_of_birth"
              value={formData.child_date_of_birth}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>
      
      <div>
        <h3 className="font-semibold text-gray-800 mb-3">Forælders oplysninger</h3>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Fornavn</label>
            <input
              type="text"
              name="parent_first_name"
              value={formData.parent_first_name}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Efternavn</label>
            <input
              type="text"
              name="parent_last_name"
              value={formData.parent_last_name}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              name="parent_email"
              value={formData.parent_email}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Adgangskode</label>
            <input
              type="password"
              name="parent_password"
              value={formData.parent_password}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>
      
      <button
        type="submit"
        className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all duration-300"
      >
        Opret konto
      </button>
      
      <button
        type="button"
        onClick={onSwitchToLogin}
        className="w-full text-purple-600 hover:text-purple-800 text-sm"
      >
        Har du allerede en konto? Log ind her
      </button>
    </form>
  );
};

export default App;

