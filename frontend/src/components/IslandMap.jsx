import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';

const IslandMap = ({ user, onActivitySelect }) => {
  const [islands, setIslands] = useState([]);
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadIslandData();
  }, []);

  const loadIslandData = async () => {
    try {
      setLoading(true);
      
      // Load activities for current island (Ø 1)
      const activitiesResponse = await api.get(`/islands/${user.current_island}/activities`);
      setActivities(activitiesResponse.activities);
      
      setLoading(false);
    } catch (err) {
      setError('Kunne ikke indlæse øer og aktiviteter');
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

  const getActivityIcon = (activityType) => {
    const icons = {
      intro: '📚',
      prompt_builder: '✏️',
      quiz: '🧩',
      chat: '💬',
      creative: '🎨'
    };
    return icons[activityType] || '⭐';
  };

  const getActivityStatus = (progress) => {
    if (!progress) return 'not_started';
    return progress.status;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500 text-white';
      case 'in_progress':
        return 'bg-yellow-500 text-white';
      default:
        return 'bg-gray-300 text-gray-700';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Indlæser dit eventyr...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-red-600">
          <p className="text-xl mb-4">⚠️ {error}</p>
          <button 
            onClick={loadIslandData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Prøv igen
          </button>
        </div>
      </div>
    );
  }

  const colors = getThemeColors();

  return (
    <div className={`min-h-screen ${colors.bg} p-4`}>
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">
          {user.chosen_theme === 'superhelte' ? '🦸‍♂️ Prompt City' : '👸 Prompt Palace'}
        </h1>
        <p className="text-lg text-gray-200">
          Velkommen til dit AI-eventyr, {user.username}!
        </p>
        <div className="mt-4 flex justify-center items-center space-x-4">
          <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
            <span className="text-white font-semibold">⭐ {user.total_points} point</span>
          </div>
          <div className="bg-white/20 backdrop-blur-sm rounded-lg px-4 py-2">
            <span className="text-white font-semibold">🏝️ Ø {user.current_island}</span>
          </div>
        </div>
      </div>

      {/* Island Map */}
      <div className="max-w-4xl mx-auto">
        <div className="relative">
          {/* Island Background */}
          <div className={`bg-gradient-to-r ${colors.primary} rounded-3xl p-8 shadow-2xl`}>
            <h2 className="text-2xl font-bold text-white mb-6 text-center">
              {user.chosen_theme === 'superhelte' ? '🏙️ Prompt City' : '🏰 Prompt Palace'}
            </h2>
            
            {/* Activities Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {activities.map((activity, index) => {
                const status = getActivityStatus(activity.progress);
                const isLocked = index > 0 && activities[index - 1] && getActivityStatus(activities[index - 1].progress) !== 'completed';
                
                return (
                  <div
                    key={activity.id}
                    className={`relative transform transition-all duration-300 hover:scale-105 ${
                      isLocked ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
                    }`}
                    onClick={() => !isLocked && onActivitySelect(activity)}
                  >
                    {/* Activity Card */}
                    <div className="bg-white/90 backdrop-blur-sm rounded-xl p-6 shadow-lg border-2 border-white/20">
                      {/* Activity Icon */}
                      <div className="text-center mb-4">
                        <div className="text-4xl mb-2">
                          {isLocked ? '🔒' : getActivityIcon(activity.activity_type)}
                        </div>
                        <div className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(status)}`}>
                          {status === 'completed' ? 'Færdig' : 
                           status === 'in_progress' ? 'I gang' : 
                           isLocked ? 'Låst' : 'Start'}
                        </div>
                      </div>
                      
                      {/* Activity Info */}
                      <h3 className="font-bold text-gray-800 text-center mb-2">
                        {activity.name}
                      </h3>
                      <p className="text-sm text-gray-600 text-center mb-4">
                        {activity.description}
                      </p>
                      
                      {/* Progress and Points */}
                      <div className="flex justify-between items-center text-xs">
                        <span className="text-gray-500">
                          Niveau {activity.difficulty_level}
                        </span>
                        <span className="font-semibold text-yellow-600">
                          ⭐ {activity.points_reward}
                        </span>
                      </div>
                      
                      {/* Progress Bar */}
                      {activity.progress && (
                        <div className="mt-3">
                          <div className="bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full transition-all duration-500 ${
                                status === 'completed' ? 'bg-green-500 w-full' :
                                status === 'in_progress' ? 'bg-yellow-500 w-1/2' : 'w-0'
                              }`}
                            />
                          </div>
                        </div>
                      )}
                    </div>
                    
                    {/* Connection Line to Next Activity */}
                    {index < activities.length - 1 && (
                      <div className="absolute -bottom-3 left-1/2 transform -translate-x-1/2 w-1 h-6 bg-white/50 rounded-full" />
                    )}
                  </div>
                );
              })}
            </div>
            
            {/* Island Progress */}
            <div className="mt-8 text-center">
              <div className="bg-white/20 backdrop-blur-sm rounded-lg p-4">
                <h3 className="text-white font-semibold mb-2">Ø Fremskridt</h3>
                <div className="bg-white/30 rounded-full h-4 mb-2">
                  <div 
                    className="bg-white rounded-full h-4 transition-all duration-1000"
                    style={{ 
                      width: `${(activities.filter(a => getActivityStatus(a.progress) === 'completed').length / activities.length) * 100}%` 
                    }}
                  />
                </div>
                <p className="text-white/80 text-sm">
                  {activities.filter(a => getActivityStatus(a.progress) === 'completed').length} af {activities.length} aktiviteter færdige
                </p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Next Island Preview (Locked) */}
        <div className="mt-8 text-center">
          <div className="bg-gray-600/50 backdrop-blur-sm rounded-xl p-6 opacity-50">
            <div className="text-4xl mb-2">🔒</div>
            <h3 className="text-white font-bold mb-2">Næste Ø: AI Billeder</h3>
            <p className="text-gray-300 text-sm">
              Fuldfør alle aktiviteter på denne ø for at låse op
            </p>
          </div>
        </div>
      </div>
      
      {/* Floating Action Button */}
      <div className="fixed bottom-6 right-6">
        <button 
          onClick={loadIslandData}
          className={`bg-gradient-to-r ${colors.primary} text-white p-4 rounded-full shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-300`}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default IslandMap;

