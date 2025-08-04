import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';

const Dashboard = ({ user, onLogout }) => {
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUserProgress();
  }, []);

  const loadUserProgress = async () => {
    try {
      const response = await api.get('/user/progress');
      setProgress(response);
      setLoading(false);
    } catch (err) {
      console.error('Failed to load progress:', err);
      setLoading(false);
    }
  };

  const getThemeColors = () => {
    if (user.chosen_theme === 'superhelte') {
      return {
        primary: 'from-blue-600 to-red-600',
        secondary: 'from-blue-500 to-purple-600',
        accent: 'text-yellow-400',
        bg: 'bg-gradient-to-br from-blue-900 via-purple-900 to-red-900'
      };
    } else {
      return {
        primary: 'from-pink-500 to-purple-600',
        secondary: 'from-purple-500 to-blue-500',
        accent: 'text-pink-300',
        bg: 'bg-gradient-to-br from-pink-900 via-purple-900 to-blue-900'
      };
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Indlæser dit dashboard...</p>
        </div>
      </div>
    );
  }

  const colors = getThemeColors();

  return (
    <div className={`min-h-screen ${colors.bg} p-4`}>
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">
            {user.chosen_theme === 'superhelte' ? '🦸‍♂️' : '👸'} Hej, {user.username}!
          </h1>
          <p className="text-gray-200">Velkommen tilbage til dit AI-eventyr</p>
        </div>
        <button
          onClick={onLogout}
          className="bg-white/20 backdrop-blur-sm text-white px-4 py-2 rounded-lg hover:bg-white/30 transition-colors"
        >
          Log ud
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
          <div className="text-3xl mb-2">⭐</div>
          <div className="text-2xl font-bold text-white">{user.total_points}</div>
          <div className="text-gray-300 text-sm">Total Point</div>
        </div>
        
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
          <div className="text-3xl mb-2">✅</div>
          <div className="text-2xl font-bold text-white">
            {progress?.statistics?.completed_activities || 0}
          </div>
          <div className="text-gray-300 text-sm">Færdige Aktiviteter</div>
        </div>
        
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
          <div className="text-3xl mb-2">🏝️</div>
          <div className="text-2xl font-bold text-white">{user.current_island}</div>
          <div className="text-gray-300 text-sm">Nuværende Ø</div>
        </div>
        
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center">
          <div className="text-3xl mb-2">📊</div>
          <div className="text-2xl font-bold text-white">
            {Math.round(progress?.statistics?.completion_percentage || 0)}%
          </div>
          <div className="text-gray-300 text-sm">Gennemført</div>
        </div>
      </div>

      {/* Recent Progress */}
      {progress?.recent_progress && progress.recent_progress.length > 0 && (
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 mb-8">
          <h2 className="text-xl font-bold text-white mb-4">📈 Seneste Fremskridt</h2>
          <div className="space-y-3">
            {progress.recent_progress.slice(-3).map((item, index) => (
              <div key={index} className="flex items-center justify-between bg-white/10 rounded-lg p-3">
                <div>
                  <div className="text-white font-medium">Aktivitet #{item.activity_id}</div>
                  <div className="text-gray-300 text-sm">
                    Status: {item.status === 'completed' ? 'Færdig' : 'I gang'}
                  </div>
                </div>
                <div className="text-right">
                  {item.score && (
                    <div className="text-yellow-400 font-bold">{item.score} point</div>
                  )}
                  <div className="text-gray-400 text-xs">
                    {item.attempts} forsøg
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Island Progress */}
      {progress?.island_progress && (
        <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
          <h2 className="text-xl font-bold text-white mb-4">🏝️ Ø Fremskridt</h2>
          <div className="space-y-4">
            {Object.entries(progress.island_progress).map(([islandId, islandProgress]) => (
              <div key={islandId} className="bg-white/10 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-white font-medium">
                    Ø {islandId}: {islandId === '1' ? 'ChatGPT & Prompting' : 'Kommende Ø'}
                  </span>
                  <span className="text-gray-300 text-sm">
                    {islandProgress.completed}/{islandProgress.total}
                  </span>
                </div>
                <div className="bg-gray-700 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full transition-all duration-1000 bg-gradient-to-r ${colors.primary}`}
                    style={{ width: `${islandProgress.percentage}%` }}
                  />
                </div>
                <div className="text-gray-400 text-xs mt-1">
                  {Math.round(islandProgress.percentage)}% gennemført
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

