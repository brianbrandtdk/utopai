import React, { useState, useEffect } from 'react';

const PointCounter = ({ currentPoints, targetPoints, duration = 1000, user }) => {
  const [displayPoints, setDisplayPoints] = useState(currentPoints || 0);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (targetPoints !== undefined && targetPoints !== displayPoints) {
      animatePoints(displayPoints, targetPoints, duration);
    }
  }, [targetPoints]);

  const animatePoints = (start, end, duration) => {
    setIsAnimating(true);
    const startTime = Date.now();
    const difference = end - start;

    const updatePoints = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function for smooth animation
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      const currentValue = Math.floor(start + (difference * easeOutQuart));
      
      setDisplayPoints(currentValue);

      if (progress < 1) {
        requestAnimationFrame(updatePoints);
      } else {
        setDisplayPoints(end);
        setIsAnimating(false);
      }
    };

    requestAnimationFrame(updatePoints);
  };

  const getThemeColors = (theme) => {
    if (theme === 'superhelte') {
      return {
        primary: 'from-blue-600 to-red-600',
        secondary: 'from-blue-500 to-red-500',
        accent: 'text-blue-300',
        glow: 'shadow-blue-500/50'
      };
    } else {
      return {
        primary: 'from-pink-500 to-purple-600',
        secondary: 'from-pink-400 to-purple-500',
        accent: 'text-pink-300',
        glow: 'shadow-pink-500/50'
      };
    }
  };

  const colors = getThemeColors(user?.chosen_theme);

  return (
    <div className={`
      relative inline-flex items-center px-6 py-3 rounded-xl
      bg-gradient-to-r ${colors.primary}
      shadow-lg ${isAnimating ? colors.glow + ' shadow-xl' : ''}
      transition-all duration-300
      ${isAnimating ? 'scale-110' : 'scale-100'}
    `}>
      {/* Star Icon */}
      <div className={`text-2xl mr-3 ${isAnimating ? 'animate-spin' : ''}`}>
        ⭐
      </div>

      {/* Points Display */}
      <div className="flex flex-col">
        <div className="flex items-baseline">
          <span className={`
            text-3xl font-bold text-white
            ${isAnimating ? 'animate-pulse' : ''}
          `}>
            {displayPoints.toLocaleString('da-DK')}
          </span>
          <span className="text-sm text-gray-200 ml-1">
            point
          </span>
        </div>
        
        {/* Label */}
        <span className={`text-xs ${colors.accent} font-medium`}>
          Total Point
        </span>
      </div>

      {/* Animation Effects */}
      {isAnimating && (
        <>
          {/* Pulse Effect */}
          <div className={`
            absolute inset-0 rounded-xl
            bg-gradient-to-r ${colors.secondary}
            animate-ping opacity-75
          `}></div>
          
          {/* Sparkle Effects */}
          <div className="absolute -top-1 -right-1 text-yellow-300 animate-bounce">
            ✨
          </div>
          <div className="absolute -bottom-1 -left-1 text-yellow-300 animate-bounce delay-100">
            ✨
          </div>
        </>
      )}
    </div>
  );
};

const PointNotification = ({ points, isVisible, onComplete, user }) => {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onComplete && onComplete();
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [isVisible, onComplete]);

  const getThemeColors = (theme) => {
    if (theme === 'superhelte') {
      return {
        primary: 'from-blue-600 to-red-600',
        text: 'text-blue-100'
      };
    } else {
      return {
        primary: 'from-pink-500 to-purple-600',
        text: 'text-pink-100'
      };
    }
  };

  const colors = getThemeColors(user?.chosen_theme);

  if (!isVisible) return null;

  return (
    <div className="fixed top-20 right-4 z-50 animate-slide-in-right">
      <div className={`
        px-6 py-4 rounded-xl shadow-2xl
        bg-gradient-to-r ${colors.primary}
        border border-yellow-400
        transform transition-all duration-500
      `}>
        <div className="flex items-center">
          <div className="text-3xl mr-3 animate-bounce">
            🎉
          </div>
          <div>
            <div className="text-white font-bold text-lg">
              +{points} Point!
            </div>
            <div className={`text-sm ${colors.text}`}>
              Godt klaret!
            </div>
          </div>
        </div>
        
        {/* Progress bar */}
        <div className="mt-2 w-full bg-white/20 rounded-full h-1">
          <div className="bg-yellow-400 h-1 rounded-full animate-shrink-width"></div>
        </div>
      </div>
    </div>
  );
};

const ProgressBar = ({ current, target, label, user }) => {
  const percentage = target > 0 ? Math.min((current / target) * 100, 100) : 0;
  
  const getThemeColors = (theme) => {
    if (theme === 'superhelte') {
      return {
        primary: 'from-blue-600 to-red-600',
        secondary: 'bg-blue-900/30'
      };
    } else {
      return {
        primary: 'from-pink-500 to-purple-600',
        secondary: 'bg-pink-900/30'
      };
    }
  };

  const colors = getThemeColors(user?.chosen_theme);

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm text-gray-300">
        <span>{label}</span>
        <span>{current} / {target}</span>
      </div>
      
      <div className={`w-full ${colors.secondary} rounded-full h-3 overflow-hidden`}>
        <div 
          className={`h-full bg-gradient-to-r ${colors.primary} transition-all duration-1000 ease-out relative`}
          style={{ width: `${percentage}%` }}
        >
          {/* Shine effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer"></div>
        </div>
      </div>
      
      <div className="text-xs text-gray-400 text-center">
        {percentage.toFixed(1)}% fuldført
      </div>
    </div>
  );
};

// Custom CSS animations (add to your CSS file)
const styles = `
@keyframes slide-in-right {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes shrink-width {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.animate-slide-in-right {
  animation: slide-in-right 0.5s ease-out;
}

.animate-shrink-width {
  animation: shrink-width 3s linear;
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}
`;

export { PointCounter, PointNotification, ProgressBar, styles };
export default PointCounter;

