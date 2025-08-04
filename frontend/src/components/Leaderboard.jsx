import React, { useState, useEffect } from 'react';

const Leaderboard = ({ user, isVisible, onClose }) => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [userRank, setUserRank] = useState(null);

  useEffect(() => {
    if (isVisible) {
      fetchLeaderboard();
    }
  }, [isVisible]);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5002/api/gamification/leaderboard', {
        method: 'GET',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch leaderboard');
      }

      const data = await response.json();
      setLeaderboard(data.leaderboard || []);
      
      // Find current user's rank
      const currentUserRank = data.leaderboard.findIndex(
        player => player.username === user?.username
      ) + 1;
      setUserRank(currentUserRank > 0 ? currentUserRank : null);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getThemeColors = (theme) => {
    if (theme === 'superhelte') {
      return {
        primary: 'from-blue-600 to-red-600',
        secondary: 'from-blue-500 to-red-500',
        accent: 'border-blue-400',
        text: 'text-blue-100',
        bg: 'bg-blue-900/20'
      };
    } else {
      return {
        primary: 'from-pink-500 to-purple-600',
        secondary: 'from-pink-400 to-purple-500',
        accent: 'border-pink-400',
        text: 'text-pink-100',
        bg: 'bg-pink-900/20'
      };
    }
  };

  const colors = getThemeColors(user?.chosen_theme);

  const getRankIcon = (rank) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return `#${rank}`;
    }
  };

  const getThemeIcon = (theme) => {
    return theme === 'superhelte' ? '🦸‍♂️' : '👸';
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className={`bg-gradient-to-r ${colors.primary} p-6 relative`}>
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-white hover:text-gray-200 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <div className="text-center">
            <h2 className="text-3xl font-bold text-white mb-2 flex items-center justify-center">
              <span className="text-4xl mr-3">🏆</span>
              Leaderboard
            </h2>
            <p className="text-gray-200">
              Top 5 AI-helte i UTOPAI universet
            </p>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 max-h-96 overflow-y-auto">
          {loading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto"></div>
              <p className="text-white mt-4">Indlæser leaderboard...</p>
            </div>
          )}

          {error && (
            <div className="text-center py-8">
              <p className="text-red-300">Fejl: {error}</p>
              <button 
                onClick={fetchLeaderboard}
                className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Prøv igen
              </button>
            </div>
          )}

          {!loading && !error && (
            <div className="space-y-4">
              {/* Current User Rank (if not in top 5) */}
              {userRank && userRank > 5 && (
                <div className={`${colors.bg} rounded-xl p-4 border-2 ${colors.accent}`}>
                  <div className="text-center">
                    <p className="text-white font-semibold mb-2">Din placering</p>
                    <div className="flex items-center justify-center space-x-4">
                      <span className="text-2xl">{getRankIcon(userRank)}</span>
                      <div>
                        <p className="text-white font-bold">{user?.username}</p>
                        <p className="text-gray-300 text-sm">{user?.total_points || 0} point</p>
                      </div>
                      <span className="text-2xl">{getThemeIcon(user?.chosen_theme)}</span>
                    </div>
                  </div>
                </div>
              )}

              {/* Top 5 List */}
              {leaderboard.length > 0 ? (
                <div className="space-y-3">
                  {leaderboard.map((player, index) => (
                    <LeaderboardItem
                      key={player.username}
                      player={player}
                      rank={index + 1}
                      isCurrentUser={player.username === user?.username}
                      colors={colors}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-gray-400">Ingen spillere på leaderboard endnu</p>
                  <p className="text-gray-500 text-sm mt-2">
                    Vær den første til at tjene point!
                  </p>
                </div>
              )}

              {/* Stats Summary */}
              {leaderboard.length > 0 && (
                <div className="mt-6 pt-6 border-t border-gray-700">
                  <div className="grid grid-cols-2 gap-4 text-center">
                    <div className={`${colors.bg} rounded-lg p-3`}>
                      <div className="text-2xl font-bold text-white">
                        {leaderboard.length}
                      </div>
                      <div className="text-sm text-gray-300">Aktive spillere</div>
                    </div>
                    <div className={`${colors.bg} rounded-lg p-3`}>
                      <div className="text-2xl font-bold text-white">
                        {leaderboard[0]?.total_points || 0}
                      </div>
                      <div className="text-sm text-gray-300">Højeste score</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 bg-gray-700 border-t border-gray-600">
          <div className="text-center">
            <p className="text-gray-300 text-sm mb-3">
              Leaderboard opdateres i real-time
            </p>
            <button
              onClick={onClose}
              className={`px-6 py-3 bg-gradient-to-r ${colors.primary} text-white font-semibold rounded-lg hover:opacity-90 transition-opacity`}
            >
              Luk
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const LeaderboardItem = ({ player, rank, isCurrentUser, colors }) => {
  const getRankIcon = (rank) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return `#${rank}`;
    }
  };

  const getThemeIcon = (theme) => {
    return theme === 'superhelte' ? '🦸‍♂️' : '👸';
  };

  return (
    <div className={`
      rounded-xl p-4 transition-all duration-300
      ${isCurrentUser 
        ? `bg-gradient-to-r ${colors.primary} shadow-lg border-2 border-yellow-400` 
        : 'bg-gray-700 hover:bg-gray-600'
      }
      ${rank <= 3 ? 'ring-2 ring-yellow-400 ring-opacity-50' : ''}
    `}>
      <div className="flex items-center justify-between">
        {/* Rank and User Info */}
        <div className="flex items-center space-x-4">
          <div className={`
            text-2xl font-bold
            ${rank <= 3 ? 'animate-pulse' : ''}
          `}>
            {getRankIcon(rank)}
          </div>
          
          <div className="flex items-center space-x-3">
            <div className="text-2xl">
              {getThemeIcon(player.theme)}
            </div>
            
            <div>
              <div className={`font-bold ${isCurrentUser ? 'text-white' : 'text-white'}`}>
                {player.username}
                {isCurrentUser && (
                  <span className="ml-2 text-xs bg-yellow-500 text-black px-2 py-1 rounded-full">
                    DIG
                  </span>
                )}
              </div>
              <div className={`text-sm ${isCurrentUser ? 'text-gray-200' : 'text-gray-400'}`}>
                Ø {player.current_island} • {player.badge_count} badges
              </div>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="text-right">
          <div className={`text-xl font-bold ${isCurrentUser ? 'text-white' : 'text-white'}`}>
            {player.total_points.toLocaleString('da-DK')}
          </div>
          <div className={`text-sm ${isCurrentUser ? 'text-gray-200' : 'text-gray-400'}`}>
            {player.completion_percentage}% færdig
          </div>
        </div>
      </div>

      {/* Progress Bar for Top 3 */}
      {rank <= 3 && (
        <div className="mt-3">
          <div className="w-full bg-gray-600 rounded-full h-2">
            <div 
              className={`h-2 rounded-full bg-gradient-to-r ${colors.secondary} transition-all duration-1000`}
              style={{ width: `${player.completion_percentage}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Crown for #1 */}
      {rank === 1 && (
        <div className="absolute -top-2 left-1/2 transform -translate-x-1/2">
          <div className="text-3xl animate-bounce">
            👑
          </div>
        </div>
      )}
    </div>
  );
};

export default Leaderboard;

