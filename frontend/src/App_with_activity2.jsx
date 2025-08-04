import React, { useState, useEffect } from 'react';
import './App.css';

// Import components
import BadgeDisplay from './components/BadgeDisplay';
import BadgeModal from './components/BadgeModal';
import PointCounter from './components/PointCounter';
import { PointNotification } from './components/PointCounter';
import Leaderboard from './components/Leaderboard';
import AchievementNotification from './components/AchievementNotification';
import Activity2 from './components/Activity2';

// Simple API service
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://utopai-production.up.railway.app';

const api = {
  async get(endpoint) {
    const response = await fetch(`${API_BASE_URL}/api${endpoint}`, {
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
    const response = await fetch(`${API_BASE_URL}/api${endpoint}`, {
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
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('login');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [selectedBadge, setSelectedBadge] = useState(null);
  const [achievementNotification, setAchievementNotification] = useState({
    visible: false,
    badges: [],
    points: 0
  });
  const [pointNotification, setPointNotification] = useState({
    visible: false,
    points: 0
  });

  // Login function
  const handleLogin = async (email, password) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await api.post('/auth/login', {
        email,
        password,
        user_type: 'child'
      });
      
      setUser(response.user);
      setCurrentView('dashboard');
    } catch (err) {
      setError(err.message || 'Login fejlede');
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const handleRegister = async (userData) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await api.post('/auth/register', userData);
      
      setUser(response.user);
      setCurrentView('theme_selection');
    } catch (err) {
      setError(err.message || 'Registrering fejlede');
    } finally {
      setLoading(false);
    }
  };

  // Theme selection
  const handleThemeSelection = async (theme) => {
    try {
      setLoading(true);
      
      const response = await api.post('/auth/select-theme', { theme });
      
      setUser(prev => ({
        ...prev,
        chosen_theme: theme
      }));
      
      setCurrentView('dashboard');
    } catch (err) {
      setError(err.message || 'Tema-valg fejlede');
    } finally {
      setLoading(false);
    }
  };

  // Activity completion handler
  const handleActivityComplete = (activityData) => {
    // Update user points
    setUser(prev => ({
      ...prev,
      total_points: activityData.user_points
    }));

    // Show achievement notification if there are new badges
    if (activityData.new_badges && activityData.new_badges.length > 0) {
      setAchievementNotification({
        visible: true,
        badges: activityData.new_badges,
        points: activityData.points_earned
      });
    } else {
      // Show just point notification
      setPointNotification({
        visible: true,
        points: activityData.points_earned
      });
    }

    // Return to island map after completion
    setTimeout(() => {
      setCurrentView('island_map');
    }, 3000);
  };

  // Login Screen
  if (currentView === 'login') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 to-purple-900 p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">🚀 UTOPAI</h1>
            <p className="text-gray-600">Lær AI gennem eventyr!</p>
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <button
              onClick={() => handleLogin('superhelt@utopai.dk', 'password123')}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 disabled:opacity-50"
            >
              {loading ? 'Logger ind...' : '🦸‍♂️ Log ind som Superhelt'}
            </button>
            
            <button
              onClick={() => handleLogin('prinsesse@utopai.dk', 'password123')}
              disabled={loading}
              className="w-full bg-gradient-to-r from-pink-500 to-purple-600 text-white font-bold py-3 px-6 rounded-lg hover:from-pink-600 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 disabled:opacity-50"
            >
              {loading ? 'Logger ind...' : '👸 Log ind som Prinsesse'}
            </button>
          </div>

          <div className="mt-6 text-center text-sm text-gray-600">
            <p>Test brugere til demonstration</p>
          </div>
        </div>
      </div>
    );
  }

  // Theme Selection Screen
  if (currentView === 'theme_selection') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 to-pink-900 p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Vælg Dit Tema</h1>
            <p className="text-gray-600">Hvilket eventyr vil du opleve?</p>
          </div>

          <div className="space-y-4">
            <button
              onClick={() => handleThemeSelection('superhelte')}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 to-red-600 text-white font-bold py-6 px-6 rounded-lg hover:from-blue-700 hover:to-red-700 transition-all duration-300 transform hover:scale-105 disabled:opacity-50"
            >
              <div className="text-4xl mb-2">🦸‍♂️</div>
              <div className="text-xl">Superhelte</div>
              <div className="text-sm opacity-90">Bliv en AI-superhelt!</div>
            </button>
            
            <button
              onClick={() => handleThemeSelection('prinsesse')}
              disabled={loading}
              className="w-full bg-gradient-to-r from-pink-500 to-purple-600 text-white font-bold py-6 px-6 rounded-lg hover:from-pink-600 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 disabled:opacity-50"
            >
              <div className="text-4xl mb-2">👸</div>
              <div className="text-xl">Prinsesse</div>
              <div className="text-sm opacity-90">Udforsk magiske AI-eventyr!</div>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Dashboard Screen
  if (currentView === 'dashboard') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-pink-900 p-4">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  Velkommen, {user?.name}! {user?.chosen_theme === 'superhelte' ? '🦸‍♂️' : '👸'}
                </h1>
                <p className="text-white/80">Klar til dit næste AI-eventyr?</p>
              </div>
              
              <PointCounter 
                points={user?.total_points || 0} 
                theme={user?.chosen_theme || 'superhelte'}
              />
            </div>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
              <div className="text-3xl mb-2">🏝️</div>
              <div className="text-2xl font-bold text-white">{user?.current_island || 1}</div>
              <div className="text-white/80">Nuværende Ø</div>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
              <div className="text-3xl mb-2">⭐</div>
              <div className="text-2xl font-bold text-white">{user?.completed_activities || 0}</div>
              <div className="text-white/80">Aktiviteter Færdige</div>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
              <div className="text-3xl mb-2">🏆</div>
              <div className="text-2xl font-bold text-white">{user?.badges?.length || 0}</div>
              <div className="text-white/80">Badges Optjent</div>
            </div>
          </div>

          {/* Badges Display */}
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 mb-8">
            <h2 className="text-2xl font-bold text-white mb-4">🏆 Mine Badges</h2>
            <BadgeDisplay 
              badges={user?.badges || []} 
              theme={user?.chosen_theme || 'superhelte'}
              onBadgeClick={setSelectedBadge}
            />
          </div>
          
          {/* Action Buttons */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <button 
              onClick={() => setCurrentView('island_map')}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              🏝️ Gå til Øer
            </button>
            
            <button 
              onClick={() => setCurrentView('activity_2')}
              className="bg-gradient-to-r from-green-500 to-teal-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-green-600 hover:to-teal-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              ✏️ Test Aktivitet 2
            </button>
            
            <button 
              onClick={() => setShowLeaderboard(true)}
              className="bg-gradient-to-r from-yellow-500 to-orange-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-yellow-600 hover:to-orange-700 transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              📊 Leaderboard
            </button>
          </div>
          
          {/* Logout Button */}
          <div className="text-center">
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

  // Activity 2 Screen
  if (currentView === 'activity_2') {
    return (
      <Activity2
        userTheme={user?.chosen_theme || 'superhelte'}
        onComplete={handleActivityComplete}
        onBack={() => setCurrentView('dashboard')}
      />
    );
  }

  // Island Map Screen (simplified for now)
  if (currentView === 'island_map') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-pink-900 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 mb-6">
            <div className="flex items-center justify-between">
              <h1 className="text-3xl font-bold text-white">
                🏝️ Prompt City - Ø 1
              </h1>
              <button
                onClick={() => setCurrentView('dashboard')}
                className="bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30 transition-colors"
              >
                ← Tilbage til Dashboard
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Activity 1 */}
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
              <div className="text-4xl mb-4">📚</div>
              <h3 className="text-xl font-bold text-white mb-2">Aktivitet 1</h3>
              <p className="text-white/80 mb-4">Hvad er ChatGPT?</p>
              <div className="bg-green-500 text-white px-3 py-1 rounded-full text-sm mb-4">
                ✅ Færdig
              </div>
              <button className="bg-gray-500 text-white px-4 py-2 rounded-lg cursor-not-allowed">
                Allerede færdig
              </button>
            </div>

            {/* Activity 2 */}
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
              <div className="text-4xl mb-4">✏️</div>
              <h3 className="text-xl font-bold text-white mb-2">Aktivitet 2</h3>
              <p className="text-white/80 mb-4">Dit første prompt</p>
              <div className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm mb-4">
                🚀 Tilgængelig
              </div>
              <button 
                onClick={() => setCurrentView('activity_2')}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105"
              >
                Start Aktivitet
              </button>
            </div>

            {/* Activity 3-5 (locked) */}
            {[3, 4, 5].map(num => (
              <div key={num} className="bg-white/5 backdrop-blur-sm rounded-xl p-6 text-center opacity-50">
                <div className="text-4xl mb-4">🔒</div>
                <h3 className="text-xl font-bold text-white mb-2">Aktivitet {num}</h3>
                <p className="text-white/80 mb-4">Låst</p>
                <div className="bg-gray-500 text-white px-3 py-1 rounded-full text-sm mb-4">
                  🔒 Ikke tilgængelig
                </div>
                <button className="bg-gray-500 text-white px-4 py-2 rounded-lg cursor-not-allowed">
                  Færdiggør forrige aktiviteter
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      {/* Leaderboard Modal */}
      {showLeaderboard && (
        <Leaderboard 
          isOpen={showLeaderboard}
          onClose={() => setShowLeaderboard(false)}
          currentUser={user}
        />
      )}

      {/* Badge Modal */}
      {selectedBadge && (
        <BadgeModal 
          badge={selectedBadge}
          onClose={() => setSelectedBadge(null)}
          theme={user?.chosen_theme || 'superhelte'}
        />
      )}

      {/* Achievement Notification */}
      <AchievementNotification 
        isVisible={achievementNotification.visible}
        badges={achievementNotification.badges}
        points={achievementNotification.points}
        onClose={() => setAchievementNotification({ visible: false, badges: [], points: 0 })}
        theme={user?.chosen_theme || 'superhelte'}
      />

      {/* Point Notification */}
      <PointNotification 
        isVisible={pointNotification.visible}
        points={pointNotification.points}
        onClose={() => setPointNotification({ visible: false, points: 0 })}
        theme={user?.chosen_theme || 'superhelte'}
      />
    </>
  );
}

export default App;

