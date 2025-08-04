import React, { useState, useEffect } from 'react';

const BadgeDisplay = ({ user, onBadgeClick }) => {
  const [badges, setBadges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchBadges();
  }, []);

  const fetchBadges = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5002/api/gamification/badges', {
        method: 'GET',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch badges');
      }

      const data = await response.json();
      setBadges(data.badges || []);
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
        earned: 'bg-gradient-to-br from-blue-500 to-red-500',
        locked: 'bg-gray-600'
      };
    } else {
      return {
        primary: 'from-pink-500 to-purple-600',
        secondary: 'from-pink-400 to-purple-500',
        accent: 'border-pink-400',
        text: 'text-pink-100',
        earned: 'bg-gradient-to-br from-pink-500 to-purple-600',
        locked: 'bg-gray-600'
      };
    }
  };

  const colors = getThemeColors(user?.chosen_theme);

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto"></div>
        <p className="text-white mt-4">Indlæser badges...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-300">Fejl: {error}</p>
        <button 
          onClick={fetchBadges}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Prøv igen
        </button>
      </div>
    );
  }

  const earnedBadges = badges.filter(badge => badge.earned);
  const lockedBadges = badges.filter(badge => !badge.earned);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-white mb-2">
          {user?.chosen_theme === 'superhelte' ? '🦸‍♂️ Superhelt Badges' : '👸 Prinsesse Badges'}
        </h2>
        <p className="text-gray-300">
          {earnedBadges.length} af {badges.length} badges optjent
        </p>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-700 rounded-full h-3">
        <div 
          className={`h-3 rounded-full bg-gradient-to-r ${colors.primary} transition-all duration-500`}
          style={{ width: `${badges.length > 0 ? (earnedBadges.length / badges.length) * 100 : 0}%` }}
        ></div>
      </div>

      {/* Earned Badges Section */}
      {earnedBadges.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <span className="text-2xl mr-2">🏆</span>
            Optjente Badges ({earnedBadges.length})
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {earnedBadges.map((badge) => (
              <BadgeCard 
                key={badge.id} 
                badge={badge} 
                earned={true} 
                colors={colors}
                onClick={() => onBadgeClick && onBadgeClick(badge)}
              />
            ))}
          </div>
        </div>
      )}

      {/* Locked Badges Section */}
      {lockedBadges.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <span className="text-2xl mr-2">🔒</span>
            Låste Badges ({lockedBadges.length})
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {lockedBadges.map((badge) => (
              <BadgeCard 
                key={badge.id} 
                badge={badge} 
                earned={false} 
                colors={colors}
                onClick={() => onBadgeClick && onBadgeClick(badge)}
              />
            ))}
          </div>
        </div>
      )}

      {badges.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-400">Ingen badges fundet</p>
        </div>
      )}
    </div>
  );
};

const BadgeCard = ({ badge, earned, colors, onClick }) => {
  return (
    <div 
      className={`
        relative p-4 rounded-xl cursor-pointer transition-all duration-300 transform hover:scale-105
        ${earned 
          ? `bg-gradient-to-br ${colors.primary} shadow-lg hover:shadow-xl` 
          : 'bg-gray-700 hover:bg-gray-600'
        }
        ${earned ? 'border-2 border-yellow-400' : 'border border-gray-600'}
      `}
      onClick={onClick}
    >
      {/* Badge Icon */}
      <div className="text-center mb-2">
        <div className={`text-4xl mb-2 ${earned ? '' : 'grayscale opacity-50'}`}>
          {badge.icon}
        </div>
        
        {/* Earned Indicator */}
        {earned && (
          <div className="absolute -top-2 -right-2 bg-yellow-500 rounded-full p-1">
            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
            </svg>
          </div>
        )}

        {/* Lock Icon for locked badges */}
        {!earned && (
          <div className="absolute -top-2 -right-2 bg-gray-500 rounded-full p-1">
            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </div>

      {/* Badge Name */}
      <h4 className={`font-semibold text-center text-sm mb-1 ${earned ? 'text-white' : 'text-gray-400'}`}>
        {badge.name}
      </h4>

      {/* Badge Description */}
      <p className={`text-xs text-center ${earned ? 'text-gray-100' : 'text-gray-500'}`}>
        {badge.description}
      </p>

      {/* Requirement Info */}
      <div className={`mt-2 text-xs text-center ${earned ? 'text-gray-200' : 'text-gray-500'}`}>
        {badge.requirement_type === 'points' && `${badge.requirement_value} point`}
        {badge.requirement_type === 'activities' && `${badge.requirement_value} aktiviteter`}
        {badge.requirement_type === 'island' && `Fuldfør Ø ${badge.requirement_value}`}
        {badge.requirement_type === 'streak' && `${badge.requirement_value} dages streak`}
      </div>

      {/* Earned Date */}
      {earned && badge.earned_at && (
        <div className="mt-2 text-xs text-center text-gray-300">
          Optjent: {new Date(badge.earned_at).toLocaleDateString('da-DK')}
        </div>
      )}

      {/* Shine Effect for Earned Badges */}
      {earned && (
        <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-transparent via-white to-transparent opacity-20 transform -skew-x-12 -translate-x-full animate-pulse"></div>
      )}
    </div>
  );
};

export default BadgeDisplay;

