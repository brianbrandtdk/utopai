import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';

const Activity1 = ({ onComplete }) => {
  const { user } = useAuth();
  const [currentStep, setCurrentStep] = useState(0);
  const [activityData, setActivityData] = useState(null);
  const [stepContent, setStepContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [userAnswers, setUserAnswers] = useState({});
  const [showHint, setShowHint] = useState(false);
  const [hint, setHint] = useState('');
  const [attemptCount, setAttemptCount] = useState(0);

  useEffect(() => {
    startActivity();
  }, []);

  const startActivity = async () => {
    try {
      const response = await fetch('/api/activity/1/start', {
        method: 'POST',
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        setActivityData(data);
        loadStep(1);
      }
    } catch (error) {
      console.error('Error starting activity:', error);
    }
  };

  const loadStep = async (stepId) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/activity/1/step/${stepId}`, {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        setStepContent(data.step);
        setCurrentStep(stepId);
        setShowHint(false);
        setAttemptCount(0);
      }
    } catch (error) {
      console.error('Error loading step:', error);
    } finally {
      setLoading(false);
    }
  };

  const submitStep = async (stepId, answers) => {
    try {
      setAttemptCount(prev => prev + 1);
      
      const response = await fetch(`/api/activity/1/step/${stepId}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(answers)
      });
      
      if (response.ok) {
        const result = await response.json();
        
        if (result.activity_completed) {
          onComplete && onComplete(result);
        } else {
          // Move to next step
          if (stepId < 3) {
            loadStep(stepId + 1);
          }
        }
        
        return result;
      }
    } catch (error) {
      console.error('Error submitting step:', error);
    }
  };

  const getHint = async () => {
    try {
      const response = await fetch('/api/activity/1/hint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          step_id: currentStep,
          question: stepContent?.title || '',
          attempt_number: attemptCount
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setHint(data.hint);
        setShowHint(true);
      }
    } catch (error) {
      console.error('Error getting hint:', error);
    }
  };

  const renderStep1 = () => {
    if (!stepContent?.content) return null;

    const { story_intro, choices, story_conclusion, learning_point } = stepContent.content;

    return (
      <div className="space-y-6">
        <div className={`p-6 rounded-lg ${user?.chosen_theme === 'superhelte' ? 'bg-blue-50 border-blue-200' : 'bg-pink-50 border-pink-200'} border-2`}>
          <h3 className="text-xl font-bold mb-4">
            {user?.chosen_theme === 'superhelte' ? '🤖 Mød PROMPT-BOT!' : '✨ Mød PROMPT-FE!'}
          </h3>
          <p className="text-lg mb-4">{story_intro}</p>
        </div>

        {choices && (
          <div className="space-y-3">
            <h4 className="font-semibold text-lg">Hvad vil du gøre?</h4>
            {choices.map((choice, index) => (
              <button
                key={choice.id}
                onClick={() => {
                  const selectedChoices = [...(userAnswers.choices || []), choice.id];
                  setUserAnswers({ ...userAnswers, choices: selectedChoices });
                  
                  // Show consequence
                  setTimeout(() => {
                    if (selectedChoices.length >= choices.length) {
                      submitStep(1, { choices: selectedChoices });
                    }
                  }, 1000);
                }}
                disabled={userAnswers.choices?.includes(choice.id)}
                className={`w-full p-4 text-left rounded-lg border-2 transition-all ${
                  userAnswers.choices?.includes(choice.id)
                    ? user?.chosen_theme === 'superhelte' 
                      ? 'bg-blue-100 border-blue-300' 
                      : 'bg-pink-100 border-pink-300'
                    : 'bg-white border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium">{choice.text}</div>
                {userAnswers.choices?.includes(choice.id) && (
                  <div className="mt-2 text-sm text-gray-600">{choice.consequence}</div>
                )}
              </button>
            ))}
          </div>
        )}

        {userAnswers.choices?.length >= (choices?.length || 0) && (
          <div className={`p-4 rounded-lg ${user?.chosen_theme === 'superhelte' ? 'bg-green-50 border-green-200' : 'bg-purple-50 border-purple-200'} border-2`}>
            <p className="font-medium">{story_conclusion}</p>
            <p className="mt-2 text-sm">{learning_point}</p>
          </div>
        )}
      </div>
    );
  };

  const renderStep2 = () => {
    if (!stepContent?.content) return null;

    const { explanation, word_chain_game, comparison } = stepContent.content;

    return (
      <div className="space-y-6">
        <div className={`p-6 rounded-lg ${user?.chosen_theme === 'superhelte' ? 'bg-blue-50 border-blue-200' : 'bg-pink-50 border-pink-200'} border-2`}>
          <h3 className="text-xl font-bold mb-4">Sådan "tænker" ChatGPT</h3>
          <p className="text-lg mb-4">{explanation.simple_explanation}</p>
          <div className="bg-white p-4 rounded border">
            <strong>Metafor:</strong> {explanation.metaphor}
          </div>
          <div className="bg-white p-4 rounded border mt-2">
            <strong>Eksempel:</strong> {explanation.example}
          </div>
        </div>

        {word_chain_game && (
          <div className="space-y-4">
            <h4 className="font-semibold text-lg">🔗 Ordkæde-spil</h4>
            <p>Start med ordet: <strong>{word_chain_game.start_word}</strong></p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {word_chain_game.word_chain?.map((item, index) => (
                <div key={index} className="p-4 bg-white rounded border">
                  <div className="font-medium text-lg">{item.word}</div>
                  <div className="text-sm text-gray-600">{item.connection}</div>
                </div>
              ))}
            </div>

            <div className="mt-4">
              <label className="block font-medium mb-2">
                Kan du tilføje et ord til kæden?
              </label>
              <input
                type="text"
                placeholder="Skriv dit ord her..."
                className="w-full p-3 border rounded-lg"
                onChange={(e) => setUserAnswers({
                  ...userAnswers,
                  word_chain: [...(userAnswers.word_chain || []), e.target.value]
                })}
              />
            </div>
          </div>
        )}

        {comparison && (
          <div className="space-y-4">
            <h4 className="font-semibold text-lg">🆚 ChatGPT vs Google</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-blue-50 rounded border">
                <h5 className="font-bold text-blue-800">ChatGPT</h5>
                <p className="text-sm">{comparison.chatgpt?.description}</p>
                <div className="mt-2 text-xs bg-blue-100 p-2 rounded">
                  <strong>Eksempel:</strong> {comparison.chatgpt?.example}
                </div>
              </div>
              
              <div className="p-4 bg-green-50 rounded border">
                <h5 className="font-bold text-green-800">Google</h5>
                <p className="text-sm">{comparison.google?.description}</p>
                <div className="mt-2 text-xs bg-green-100 p-2 rounded">
                  <strong>Eksempel:</strong> {comparison.google?.example}
                </div>
              </div>
            </div>

            <div className="p-4 bg-yellow-50 rounded border">
              <strong>Hovedforskel:</strong> {comparison.key_difference}
            </div>

            <div className="mt-4">
              <label className="block font-medium mb-2">
                Forklar forskellen med dine egne ord:
              </label>
              <textarea
                placeholder="Skriv din forklaring her..."
                className="w-full p-3 border rounded-lg h-24"
                onChange={(e) => setUserAnswers({
                  ...userAnswers,
                  comparison: e.target.value
                })}
              />
            </div>
          </div>
        )}

        <button
          onClick={() => submitStep(2, {
            word_chain: userAnswers.word_chain || [],
            comparison: userAnswers.comparison || ''
          })}
          disabled={!userAnswers.comparison}
          className={`w-full py-3 px-6 rounded-lg font-medium transition-all ${
            userAnswers.comparison
              ? user?.chosen_theme === 'superhelte'
                ? 'bg-blue-600 hover:bg-blue-700 text-white'
                : 'bg-pink-600 hover:bg-pink-700 text-white'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          Fortsæt til næste trin
        </button>
      </div>
    );
  };

  const renderStep3 = () => {
    if (!stepContent?.content) return null;

    const { superpower_cards, weakness_cards, quiz_questions } = stepContent.content;

    return (
      <div className="space-y-6">
        <div className={`p-6 rounded-lg ${user?.chosen_theme === 'superhelte' ? 'bg-blue-50 border-blue-200' : 'bg-pink-50 border-pink-200'} border-2`}>
          <h3 className="text-xl font-bold mb-4">
            {user?.chosen_theme === 'superhelte' ? '⚡ Superkræfter' : '✨ Magiske Evner'}
          </h3>
        </div>

        {superpower_cards && (
          <div className="space-y-4">
            <h4 className="font-semibold text-lg">
              {user?.chosen_theme === 'superhelte' ? '🦸‍♂️ ChatGPT\'s Superkræfter' : '🧚‍♀️ ChatGPT\'s Magiske Evner'}
            </h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {superpower_cards.map((card, index) => (
                <div key={index} className="p-4 bg-green-50 rounded-lg border-2 border-green-200">
                  <div className="text-2xl mb-2">{card.icon}</div>
                  <h5 className="font-bold text-green-800">{card.title}</h5>
                  <p className="text-sm text-green-700">{card.description}</p>
                  <div className="mt-2 text-xs bg-green-100 p-2 rounded">
                    <strong>Eksempel:</strong> {card.example}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {weakness_cards && (
          <div className="space-y-4">
            <h4 className="font-semibold text-lg">
              {user?.chosen_theme === 'superhelte' ? '🛡️ Begrænsninger' : '🔮 Grænser for Magien'}
            </h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {weakness_cards.map((card, index) => (
                <div key={index} className="p-4 bg-orange-50 rounded-lg border-2 border-orange-200">
                  <div className="text-2xl mb-2">{card.icon}</div>
                  <h5 className="font-bold text-orange-800">{card.title}</h5>
                  <p className="text-sm text-orange-700">{card.description}</p>
                  <div className="mt-2 text-xs bg-orange-100 p-2 rounded">
                    <strong>Eksempel:</strong> {card.example}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {quiz_questions && (
          <div className="space-y-4">
            <h4 className="font-semibold text-lg">🧠 Test din viden!</h4>
            
            {quiz_questions.map((question, qIndex) => (
              <div key={qIndex} className="p-4 bg-white rounded-lg border-2">
                <h5 className="font-medium mb-3">{question.question}</h5>
                
                <div className="space-y-2">
                  {question.options?.map((option, oIndex) => (
                    <button
                      key={oIndex}
                      onClick={() => {
                        const newAnswers = { ...userAnswers };
                        if (!newAnswers.quiz_answers) newAnswers.quiz_answers = [];
                        newAnswers.quiz_answers[qIndex] = option.charAt(0); // A, B, C, D
                        setUserAnswers(newAnswers);
                      }}
                      className={`w-full p-3 text-left rounded border transition-all ${
                        userAnswers.quiz_answers?.[qIndex] === option.charAt(0)
                          ? user?.chosen_theme === 'superhelte'
                            ? 'bg-blue-100 border-blue-300'
                            : 'bg-pink-100 border-pink-300'
                          : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>

                {userAnswers.quiz_answers?.[qIndex] && (
                  <div className="mt-3 p-3 bg-gray-50 rounded text-sm">
                    <strong>Forklaring:</strong> {question.explanation}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        <button
          onClick={() => submitStep(3, {
            card_sorting: userAnswers.card_sorting || {},
            quiz_answers: userAnswers.quiz_answers || []
          })}
          disabled={!userAnswers.quiz_answers || userAnswers.quiz_answers.length < (quiz_questions?.length || 0)}
          className={`w-full py-3 px-6 rounded-lg font-medium transition-all ${
            userAnswers.quiz_answers && userAnswers.quiz_answers.length >= (quiz_questions?.length || 0)
              ? user?.chosen_theme === 'superhelte'
                ? 'bg-blue-600 hover:bg-blue-700 text-white'
                : 'bg-pink-600 hover:bg-pink-700 text-white'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
        >
          Afslut Aktivitet 1
        </button>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-3xl font-bold">
            {activityData?.activity?.name || 'Hvad er ChatGPT?'}
          </h1>
          <div className="text-sm text-gray-600">
            Trin {currentStep} af 3
          </div>
        </div>
        
        {/* Progress bar */}
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className={`h-2 rounded-full transition-all duration-300 ${
              user?.chosen_theme === 'superhelte' ? 'bg-blue-600' : 'bg-pink-600'
            }`}
            style={{ width: `${(currentStep / 3) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Step content */}
      <div className="mb-8">
        {currentStep === 1 && renderStep1()}
        {currentStep === 2 && renderStep2()}
        {currentStep === 3 && renderStep3()}
      </div>

      {/* Hint section */}
      {attemptCount > 0 && (
        <div className="mb-6">
          <button
            onClick={getHint}
            className="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-all"
          >
            💡 Få et hint
          </button>
          
          {showHint && hint && (
            <div className="mt-3 p-4 bg-yellow-50 border-2 border-yellow-200 rounded-lg">
              <div className="font-medium text-yellow-800 mb-2">💡 Hint:</div>
              <p className="text-yellow-700">{hint}</p>
            </div>
          )}
        </div>
      )}

      {/* Navigation */}
      <div className="flex justify-between">
        <button
          onClick={() => currentStep > 1 && loadStep(currentStep - 1)}
          disabled={currentStep <= 1}
          className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ← Forrige
        </button>
        
        <div className="text-sm text-gray-600 flex items-center">
          {user?.chosen_theme === 'superhelte' ? '🤖 PROMPT-BOT' : '✨ PROMPT-FE'} hjælper dig!
        </div>
      </div>
    </div>
  );
};

export default Activity1;

