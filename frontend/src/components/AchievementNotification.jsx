import React, { useState, useEffect } from 'react';

const AchievementNotification = ({ 
  badges = [], 
  points = 0, 
  isVisible, 
  onComplete, 
  user 
}) => {
  const [currentBadgeIndex, setCurrentBadgeIndex] = useState(0);
  const [showBadges, setShowBadges] = useState(false);
  const [showPoints, setShowPoints] = useState(false);

  useEffect(() => {
    if (isVisible) {
      // Show points first
      if (points > 0) {
        setShowPoints(true);
        setTimeout(() => {
          setShowPoints(false);
          if (badges.length > 0) {
            setShowBadges(true);
          } else {
            onComplete && onComplete();
          }
        }, 2000);
      } else if (badges.length > 0) {
        setShowBadges(true);
      }
    } else {
      reset();
    }
  }, [isVisible, points, badges.length]);

  useEffect(() => {
    if (showBadges && badges.length > 0) {
      const timer = setTimeout(() => {
        if (currentBadgeIndex < badges.length - 1) {
          setCurrentBadgeIndex(currentBadgeIndex + 1);
        } else {
          setShowBadges(false);
          onComplete && onComplete();
        }
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [showBadges, currentBadgeIndex, badges.length]);

  const reset = () => {
    setCurrentBadgeIndex(0);
    setShowBadges(false);
    setShowPoints(false);
  };

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

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 z-50 pointer-events-none">
      {/* Points Notification */}
      {showPoints && (
        <PointsAchievement 
          points={points} 
          colors={colors}
          user={user}
        />
      )}

      {/* Badge Notifications */}
      {showBadges && badges.length > 0 && (
        <BadgeAchievement 
          badge={badges[currentBadgeIndex]} 
          colors={colors}
          user={user}
          badgeNumber={currentBadgeIndex + 1}
          totalBadges={badges.length}
        />
      )}
    </div>
  );
};

const PointsAchievement = ({ points, colors, user }) => {
  return (
    <div className="fixed inset-0 flex items-center justify-center">
      {/* Background Overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-70 animate-fade-in"></div>
      
      {/* Content */}
      <div className="relative z-10 text-center animate-scale-in">
        {/* Confetti Effect */}
        <div className="absolute inset-0 pointer-events-none">
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute animate-confetti"
              style={{
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 2}s`,
                fontSize: `${Math.random() * 20 + 10}px`
              }}
            >
              {['🎉', '⭐', '✨', '🎊', '💫'][Math.floor(Math.random() * 5)]}
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div className={`
          bg-gradient-to-r ${colors.primary} 
          rounded-3xl p-8 shadow-2xl border-4 border-yellow-400
          transform animate-bounce-in
        `}>
          <div className="text-6xl mb-4 animate-spin-slow">
            ⭐
          </div>
          
          <h2 className="text-4xl font-bold text-white mb-2">
            +{points} Point!
          </h2>
          
          <p className="text-xl text-gray-200 mb-4">
            Fantastisk arbejde!
          </p>
          
          <div className="text-6xl animate-pulse">
            🎉
          </div>
        </div>
      </div>
    </div>
  );
};

const BadgeAchievement = ({ badge, colors, user, badgeNumber, totalBadges }) => {
  return (
    <div className="fixed inset-0 flex items-center justify-center">
      {/* Background Overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-80 animate-fade-in"></div>
      
      {/* Content */}
      <div className="relative z-10 text-center animate-scale-in max-w-md mx-4">
        {/* Sparkle Effects */}
        <div className="absolute inset-0 pointer-events-none">
          {[...Array(15)].map((_, i) => (
            <div
              key={i}
              className="absolute animate-sparkle"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`,
                fontSize: `${Math.random() * 15 + 10}px`
              }}
            >
              ✨
            </div>
          ))}
        </div>

        {/* Badge Card */}
        <div className={`
          bg-gray-800 rounded-3xl p-8 shadow-2xl border-4 border-yellow-400
          transform animate-bounce-in
        `}>
          {/* Header */}
          <div className="mb-6">
            <h2 className="text-3xl font-bold text-white mb-2">
              🏆 Nyt Badge!
            </h2>
            {totalBadges > 1 && (
              <p className="text-gray-300 text-sm">
                {badgeNumber} af {totalBadges} nye badges
              </p>
            )}
          </div>

          {/* Badge Display */}
          <div className="mb-6">
            <div className={`
              inline-flex items-center justify-center w-32 h-32 rounded-full mb-4
              bg-gradient-to-br ${colors.primary} shadow-2xl
              border-4 border-yellow-400
              animate-glow
            `}>
              <span className="text-6xl animate-bounce-slow">
                {badge.icon}
              </span>
            </div>
            
            {/* Shine Effect */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-transparent via-white to-transparent opacity-30 transform -skew-x-12 animate-shine"></div>
          </div>

          {/* Badge Info */}
          <div className="space-y-3">
            <h3 className="text-2xl font-bold text-white">
              {badge.name}
            </h3>
            
            <p className="text-gray-300">
              {badge.description}
            </p>
            
            {/* Theme Badge */}
            <div className="inline-flex items-center px-3 py-1 bg-yellow-500 text-black text-sm rounded-full font-semibold">
              <span className="mr-1">
                {badge.theme === 'superhelte' ? '🦸‍♂️' : badge.theme === 'prinsesse' ? '👸' : '🌟'}
              </span>
              {badge.theme === 'superhelte' ? 'Superhelte Badge' : 
               badge.theme === 'prinsesse' ? 'Prinsesse Badge' : 
               'Universelt Badge'}
            </div>
          </div>

          {/* Celebration Text */}
          <div className="mt-6">
            <p className="text-lg text-yellow-300 font-semibold animate-pulse">
              Tillykke, {user?.username}! 🎉
            </p>
          </div>
        </div>

        {/* Progress Indicator */}
        {totalBadges > 1 && (
          <div className="mt-4 flex justify-center space-x-2">
            {[...Array(totalBadges)].map((_, i) => (
              <div
                key={i}
                className={`
                  w-3 h-3 rounded-full transition-all duration-300
                  ${i <= badgeNumber - 1 ? 'bg-yellow-400' : 'bg-gray-600'}
                `}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// CSS Animations (add to your global CSS)
const achievementStyles = `
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scale-in {
  from { 
    transform: scale(0.5) rotate(-10deg);
    opacity: 0;
  }
  to { 
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

@keyframes bounce-in {
  0% {
    transform: scale(0.3) translateY(-100px);
    opacity: 0;
  }
  50% {
    transform: scale(1.1) translateY(0);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes confetti {
  0% {
    transform: translateY(-100vh) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(720deg);
    opacity: 0;
  }
}

@keyframes sparkle {
  0%, 100% {
    opacity: 0;
    transform: scale(0);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
  }
  50% {
    box-shadow: 0 0 40px rgba(255, 215, 0, 0.8);
  }
}

@keyframes shine {
  0% {
    transform: translateX(-100%) skewX(-12deg);
  }
  100% {
    transform: translateX(200%) skewX(-12deg);
  }
}

@keyframes spin-slow {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out;
}

.animate-scale-in {
  animation: scale-in 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.animate-bounce-in {
  animation: bounce-in 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.animate-confetti {
  animation: confetti 3s linear infinite;
}

.animate-sparkle {
  animation: sparkle 2s ease-in-out infinite;
}

.animate-glow {
  animation: glow 2s ease-in-out infinite;
}

.animate-shine {
  animation: shine 2s ease-in-out infinite;
}

.animate-spin-slow {
  animation: spin-slow 3s linear infinite;
}

.animate-bounce-slow {
  animation: bounce-slow 2s ease-in-out infinite;
}
`;

export { AchievementNotification, achievementStyles };
export default AchievementNotification;

