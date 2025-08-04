import { useState } from 'react';
import { useAuth } from '../hooks/useAuth.jsx';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';

const themes = [
  {
    id: 'superhelte',
    name: 'Superhelte',
    description: 'Bliv en AI-superhelt og red verden!',
    colors: ['#1e40af', '#dc2626', '#fbbf24'],
    emoji: '🦸‍♂️',
    background: 'linear-gradient(135deg, #1e40af, #dc2626)',
  },
  {
    id: 'prinsesse',
    name: 'Prinsesse',
    description: 'Udforsk det magiske AI-kongerige!',
    colors: ['#ec4899', '#8b5cf6', '#06b6d4'],
    emoji: '👸',
    background: 'linear-gradient(135deg, #ec4899, #8b5cf6)',
  },
];

export const ThemeSelector = ({ onThemeSelected }) => {
  const { selectTheme } = useAuth();
  const [selectedTheme, setSelectedTheme] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleThemeSelect = async (themeId) => {
    try {
      setIsLoading(true);
      setSelectedTheme(themeId);
      
      await selectTheme(themeId);
      
      if (onThemeSelected) {
        onThemeSelected(themeId);
      }
    } catch (error) {
      console.error('Theme selection failed:', error);
      setSelectedTheme(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-800 mb-4">
            UTOPAI
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            Vælg dit eventyr!
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-3xl mx-auto">
          {themes.map((theme) => (
            <Card
              key={theme.id}
              className={`cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-2xl ${
                selectedTheme === theme.id ? 'ring-4 ring-blue-500' : ''
              }`}
              onClick={() => handleThemeSelect(theme.id)}
            >
              <CardContent className="p-0">
                <div
                  className="h-48 rounded-t-lg flex items-center justify-center text-white relative overflow-hidden"
                  style={{ background: theme.background }}
                >
                  <div className="text-center z-10">
                    <div className="text-6xl mb-4">{theme.emoji}</div>
                    <h2 className="text-3xl font-bold mb-2">{theme.name}</h2>
                  </div>
                  
                  {/* Decorative elements */}
                  <div className="absolute inset-0 opacity-20">
                    {theme.id === 'superhelte' && (
                      <>
                        <div className="absolute top-4 left-4 text-4xl">⚡</div>
                        <div className="absolute top-8 right-8 text-3xl">🏢</div>
                        <div className="absolute bottom-4 left-8 text-2xl">🚀</div>
                        <div className="absolute bottom-8 right-4 text-3xl">💪</div>
                      </>
                    )}
                    {theme.id === 'prinsesse' && (
                      <>
                        <div className="absolute top-4 left-4 text-4xl">✨</div>
                        <div className="absolute top-8 right-8 text-3xl">🏰</div>
                        <div className="absolute bottom-4 left-8 text-2xl">🦄</div>
                        <div className="absolute bottom-8 right-4 text-3xl">👑</div>
                      </>
                    )}
                  </div>
                </div>
                
                <div className="p-6">
                  <p className="text-gray-600 text-center mb-6">
                    {theme.description}
                  </p>
                  
                  <div className="flex justify-center space-x-2 mb-4">
                    {theme.colors.map((color, index) => (
                      <div
                        key={index}
                        className="w-6 h-6 rounded-full border-2 border-white shadow-sm"
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                  
                  <Button
                    className="w-full text-lg py-3"
                    style={{ background: theme.background }}
                    disabled={isLoading}
                  >
                    {isLoading && selectedTheme === theme.id ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Vælger...
                      </div>
                    ) : (
                      `Vælg ${theme.name}`
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="text-center mt-12">
          <p className="text-gray-500">
            Du kan altid ændre dit tema senere i indstillingerne
          </p>
        </div>
      </div>
    </div>
  );
};

