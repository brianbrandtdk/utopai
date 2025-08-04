import React from 'react';

const BadgeModal = ({ badge, isOpen, onClose, user }) => {
  if (!isOpen || !badge) return null;

  const getThemeColors = (theme) => {
    if (theme === 'superhelte') {
      return {
        primary: 'from-blue-600 to-red-600',
        secondary: 'from-blue-500 to-red-500',
        accent: 'border-blue-400',
        text: 'text-blue-100'
      };
    } else {
      return {
        primary: 'from-pink-500 to-purple-600',
        secondary: 'from-pink-400 to-purple-500',
        accent: 'border-pink-400',
        text: 'text-pink-100'
      };
    }
  };

  const colors = getThemeColors(user?.chosen_theme);

  const getRequirementText = (badge) => {
    switch (badge.requirement_type) {
      case 'points':
        return `Saml ${badge.requirement_value} point`;
      case 'activities':
        return `Fuldfør ${badge.requirement_value} aktiviteter`;
      case 'island':
        return `Fuldfør Ø ${badge.requirement_value}`;
      case 'streak':
        return `Oprethold en ${badge.requirement_value} dages streak`;
      default:
        return 'Ukendt krav';
    }
  };

  const getThemeText = (theme) => {
    if (!theme) return 'Universelt badge';
    return theme === 'superhelte' ? 'Superhelte badge' : 'Prinsesse badge';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-gray-800 rounded-2xl max-w-md w-full p-6 relative">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Badge Display */}
        <div className="text-center mb-6">
          <div className={`
            inline-flex items-center justify-center w-24 h-24 rounded-full mb-4
            ${badge.earned 
              ? `bg-gradient-to-br ${colors.primary} shadow-lg` 
              : 'bg-gray-600'
            }
            ${badge.earned ? 'border-4 border-yellow-400' : 'border-2 border-gray-500'}
          `}>
            <span className={`text-5xl ${badge.earned ? '' : 'grayscale opacity-50'}`}>
              {badge.icon}
            </span>
          </div>

          {/* Badge Status */}
          {badge.earned ? (
            <div className="inline-flex items-center px-3 py-1 bg-green-600 text-white text-sm rounded-full mb-2">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Optjent
            </div>
          ) : (
            <div className="inline-flex items-center px-3 py-1 bg-gray-600 text-gray-300 text-sm rounded-full mb-2">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
              </svg>
              Låst
            </div>
          )}
        </div>

        {/* Badge Info */}
        <div className="space-y-4">
          <div>
            <h3 className="text-2xl font-bold text-white text-center mb-2">
              {badge.name}
            </h3>
            <p className="text-gray-300 text-center">
              {badge.description}
            </p>
          </div>

          {/* Requirements */}
          <div className="bg-gray-700 rounded-lg p-4">
            <h4 className="text-white font-semibold mb-2 flex items-center">
              <span className="text-lg mr-2">🎯</span>
              Krav
            </h4>
            <p className="text-gray-300">
              {getRequirementText(badge)}
            </p>
          </div>

          {/* Theme Info */}
          <div className="bg-gray-700 rounded-lg p-4">
            <h4 className="text-white font-semibold mb-2 flex items-center">
              <span className="text-lg mr-2">
                {badge.theme === 'superhelte' ? '🦸‍♂️' : badge.theme === 'prinsesse' ? '👸' : '🌟'}
              </span>
              Type
            </h4>
            <p className="text-gray-300">
              {getThemeText(badge.theme)}
            </p>
          </div>

          {/* Earned Date */}
          {badge.earned && badge.earned_at && (
            <div className="bg-green-900 bg-opacity-50 rounded-lg p-4">
              <h4 className="text-white font-semibold mb-2 flex items-center">
                <span className="text-lg mr-2">📅</span>
                Optjent
              </h4>
              <p className="text-green-300">
                {new Date(badge.earned_at).toLocaleDateString('da-DK', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </p>
            </div>
          )}

          {/* Progress Hint for Locked Badges */}
          {!badge.earned && (
            <div className="bg-blue-900 bg-opacity-50 rounded-lg p-4">
              <h4 className="text-white font-semibold mb-2 flex items-center">
                <span className="text-lg mr-2">💡</span>
                Tip
              </h4>
              <p className="text-blue-300">
                {badge.requirement_type === 'points' && 'Fuldfør flere aktiviteter for at tjene point!'}
                {badge.requirement_type === 'activities' && 'Fortsæt med at løse aktiviteter på øerne!'}
                {badge.requirement_type === 'island' && 'Fuldfør alle aktiviteter på denne ø!'}
                {badge.requirement_type === 'streak' && 'Log ind og lær hver dag for at opbygge din streak!'}
              </p>
            </div>
          )}
        </div>

        {/* Action Button */}
        <div className="mt-6 text-center">
          {badge.earned ? (
            <button
              onClick={onClose}
              className={`px-6 py-3 bg-gradient-to-r ${colors.primary} text-white font-semibold rounded-lg hover:opacity-90 transition-opacity`}
            >
              Fantastisk! 🎉
            </button>
          ) : (
            <button
              onClick={onClose}
              className="px-6 py-3 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 transition-colors"
            >
              Luk
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default BadgeModal;

