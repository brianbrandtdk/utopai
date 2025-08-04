import React, { useState, useEffect } from 'react';
import { ChevronRight, ChevronLeft, Lightbulb, Eye, CheckCircle, Star, Sparkles, MessageCircle, Edit3, Target } from 'lucide-react';

const Activity2 = ({ userTheme = 'superhelte', onComplete, onBack }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [stepData, setStepData] = useState({});
  const [promptParts, setPromptParts] = useState({
    role: '',
    task: '',
    context: '',
    tone: ''
  });
  const [builtPrompt, setBuiltPrompt] = useState('');
  const [promptPreview, setPromptPreview] = useState('');
  const [promptQuality, setPromptQuality] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [hintText, setHintText] = useState('');
  const [attemptCount, setAttemptCount] = useState(0);
  const [completedSteps, setCompletedSteps] = useState(new Set());
  const [activityStarted, setActivityStarted] = useState(false);
  const [introContent, setIntroContent] = useState(null);

  // Theme-specific styling
  const themeStyles = {
    superhelte: {
      primary: 'from-blue-600 to-purple-600',
      secondary: 'from-blue-500 to-purple-500',
      accent: 'bg-blue-100 border-blue-300 text-blue-800',
      icon: '🦸‍♂️',
      bgPattern: 'bg-gradient-to-br from-blue-50 to-purple-50'
    },
    prinsesse: {
      primary: 'from-pink-500 to-purple-500',
      secondary: 'from-pink-400 to-purple-400',
      accent: 'bg-pink-100 border-pink-300 text-pink-800',
      icon: '👸',
      bgPattern: 'bg-gradient-to-br from-pink-50 to-purple-50'
    }
  };

  const theme = themeStyles[userTheme] || themeStyles.superhelte;

  // Start activity
  useEffect(() => {
    if (!activityStarted) {
      startActivity();
    }
  }, []);

  const startActivity = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/activity/2/start', {
        method: 'POST',
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        setIntroContent(data.intro_content);
        setActivityStarted(true);
      }
    } catch (error) {
      console.error('Error starting activity:', error);
    } finally {
      setLoading(false);
    }
  };

  // Load step content
  const loadStepContent = async (stepId) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/activity/2/step/${stepId}`, {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        setStepData(prev => ({
          ...prev,
          [stepId]: data.step
        }));
      }
    } catch (error) {
      console.error('Error loading step:', error);
    } finally {
      setLoading(false);
    }
  };

  // Load current step when it changes
  useEffect(() => {
    if (activityStarted && currentStep <= 3) {
      loadStepContent(currentStep);
    }
  }, [currentStep, activityStarted]);

  // Build prompt from parts
  const buildPromptFromParts = async () => {
    try {
      const response = await fetch('/api/activity/2/build-prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          prompt_parts: promptParts,
          step_id: currentStep
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setBuiltPrompt(data.built_prompt);
        setPromptPreview(data.preview_response);
        setPromptQuality(data.quality_score);
      }
    } catch (error) {
      console.error('Error building prompt:', error);
    }
  };

  // Test prompt with AI
  const testPrompt = async (prompt) => {
    try {
      setLoading(true);
      const response = await fetch('/api/activity/2/test-prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          prompt: prompt,
          step_id: currentStep
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        return data;
      }
    } catch (error) {
      console.error('Error testing prompt:', error);
    } finally {
      setLoading(false);
    }
  };

  // Get hint
  const getHint = async () => {
    try {
      const response = await fetch('/api/activity/2/hint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          step_id: currentStep,
          question: 'Jeg har brug for hjælp',
          current_prompt: builtPrompt,
          attempt_number: attemptCount + 1
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setHintText(data.hint);
        setShowHint(true);
        setAttemptCount(prev => prev + 1);
      }
    } catch (error) {
      console.error('Error getting hint:', error);
    }
  };

  // Submit step
  const submitStep = async () => {
    try {
      setLoading(true);
      let submitData = {};
      
      if (currentStep === 1) {
        submitData = {
          prompt_parts: promptParts,
          final_prompt: builtPrompt
        };
      } else if (currentStep === 2) {
        submitData = {
          politeness_examples: stepData[2]?.politeness_examples || [],
          politeness_quiz: stepData[2]?.quiz_answers || []
        };
      } else if (currentStep === 3) {
        submitData = {
          personal_prompt: builtPrompt,
          ai_response: promptPreview
        };
      }
      
      const response = await fetch(`/api/activity/2/step/${currentStep}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(submitData)
      });
      
      if (response.ok) {
        const data = await response.json();
        setCompletedSteps(prev => new Set([...prev, currentStep]));
        
        if (data.activity_completed) {
          onComplete?.(data);
        } else {
          setCurrentStep(prev => prev + 1);
        }
      }
    } catch (error) {
      console.error('Error submitting step:', error);
    } finally {
      setLoading(false);
    }
  };

  // Render introduction
  if (!activityStarted || !introContent) {
    return (
      <div className={`min-h-screen ${theme.bgPattern} flex items-center justify-center p-4`}>
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full text-center">
          <div className="text-6xl mb-4">{theme.icon}</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            Starter Aktivitet 2...
          </h2>
          {loading && (
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          )}
        </div>
      </div>
    );
  }

  // Render step content
  const renderStepContent = () => {
    const currentStepData = stepData[currentStep];
    
    if (!currentStepData) {
      return (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Indlæser step indhold...</p>
        </div>
      );
    }

    switch (currentStep) {
      case 1:
        return renderGuidedPromptBuilder(currentStepData);
      case 2:
        return renderPolitenessTraining(currentStepData);
      case 3:
        return renderPersonalizedExercise(currentStepData);
      default:
        return null;
    }
  };

  // Step 1: Guided Prompt Builder
  const renderGuidedPromptBuilder = (stepData) => (
    <div className="space-y-6">
      <div className={`p-4 rounded-lg ${theme.accent}`}>
        <h3 className="font-bold text-lg mb-2 flex items-center">
          <Edit3 className="mr-2" size={20} />
          {stepData.title}
        </h3>
        <p className="text-sm">{stepData.content?.introduction}</p>
      </div>

      {/* Prompt Builder Steps */}
      <div className="space-y-4">
        {stepData.content?.steps?.map((step, index) => (
          <div key={step.id} className="bg-white border-2 border-gray-200 rounded-lg p-4">
            <label className="block font-medium text-gray-700 mb-2">
              {step.title}
            </label>
            <p className="text-sm text-gray-600 mb-3">{step.instruction}</p>
            <input
              type="text"
              placeholder={step.placeholder}
              value={promptParts[Object.keys(promptParts)[index]] || ''}
              onChange={(e) => {
                const key = Object.keys(promptParts)[index];
                setPromptParts(prev => ({
                  ...prev,
                  [key]: e.target.value
                }));
              }}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            {step.example && (
              <p className="text-xs text-gray-500 mt-2">
                <strong>Eksempel:</strong> {step.example}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* Build Prompt Button */}
      <button
        onClick={buildPromptFromParts}
        disabled={!Object.values(promptParts).some(v => v.trim())}
        className={`w-full bg-gradient-to-r ${theme.primary} text-white font-bold py-3 px-6 rounded-lg hover:opacity-90 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center`}
      >
        <Target className="mr-2" size={20} />
        Byg Mit Prompt
      </button>

      {/* Built Prompt Display */}
      {builtPrompt && (
        <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
          <h4 className="font-bold text-gray-800 mb-2 flex items-center">
            <MessageCircle className="mr-2" size={16} />
            Dit Færdige Prompt:
          </h4>
          <p className="text-gray-700 bg-white p-3 rounded border italic">
            "{builtPrompt}"
          </p>
          
          {promptQuality && (
            <div className="mt-3 p-3 bg-blue-50 rounded border">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-blue-800">Kvalitet:</span>
                <span className="text-blue-600 font-bold">
                  {promptQuality.score}/100
                </span>
              </div>
              <div className="space-y-1">
                {promptQuality.feedback?.map((feedback, index) => (
                  <p key={index} className="text-sm text-blue-700">
                    ✓ {feedback}
                  </p>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Preview Response */}
      {promptPreview && (
        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
          <h4 className="font-bold text-green-800 mb-2 flex items-center">
            <Eye className="mr-2" size={16} />
            AI Preview Svar:
          </h4>
          <p className="text-green-700 bg-white p-3 rounded border">
            {promptPreview}
          </p>
        </div>
      )}
    </div>
  );

  // Step 2: Politeness Training
  const renderPolitenessTraining = (stepData) => (
    <div className="space-y-6">
      <div className={`p-4 rounded-lg ${theme.accent}`}>
        <h3 className="font-bold text-lg mb-2 flex items-center">
          <Star className="mr-2" size={20} />
          {stepData.title}
        </h3>
        <p className="text-sm">{stepData.content?.introduction}</p>
      </div>

      {/* Good Examples */}
      <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
        <h4 className="font-bold text-green-800 mb-3">✅ Gode Eksempler:</h4>
        <div className="space-y-3">
          {stepData.content?.good_examples?.map((example, index) => (
            <div key={index} className="bg-white p-3 rounded border">
              <p className="font-medium text-gray-800">"{example.prompt}"</p>
              <p className="text-sm text-green-600 mt-1">{example.explanation}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Bad Examples */}
      <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4">
        <h4 className="font-bold text-red-800 mb-3">❌ Dårlige Eksempler:</h4>
        <div className="space-y-3">
          {stepData.content?.bad_examples?.map((example, index) => (
            <div key={index} className="bg-white p-3 rounded border">
              <p className="font-medium text-gray-800">"{example.prompt}"</p>
              <p className="text-sm text-red-600 mt-1">{example.explanation}</p>
              <p className="text-sm text-green-600 mt-2">
                <strong>Bedre:</strong> "{example.improved}"
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Quiz */}
      {stepData.content?.quiz_questions?.length > 0 && (
        <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
          <h4 className="font-bold text-blue-800 mb-3">🧠 Quiz:</h4>
          <div className="space-y-4">
            {stepData.content.quiz_questions.map((question, index) => (
              <div key={index} className="bg-white p-4 rounded border">
                <p className="font-medium text-gray-800 mb-3">{question.question}</p>
                <div className="space-y-2">
                  {question.options?.map((option, optIndex) => (
                    <label key={optIndex} className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="radio"
                        name={`quiz_${index}`}
                        value={option}
                        className="text-blue-600"
                      />
                      <span className="text-gray-700">{option}</span>
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  // Step 3: Personalized Exercise
  const renderPersonalizedExercise = (stepData) => (
    <div className="space-y-6">
      <div className={`p-4 rounded-lg ${theme.accent}`}>
        <h3 className="font-bold text-lg mb-2 flex items-center">
          <Sparkles className="mr-2" size={20} />
          {stepData.title}
        </h3>
        <p className="text-sm">{stepData.content?.task_description}</p>
      </div>

      {/* Scenario */}
      <div className="bg-purple-50 border-2 border-purple-200 rounded-lg p-4">
        <h4 className="font-bold text-purple-800 mb-2">🎭 Scenarie:</h4>
        <p className="text-purple-700">{stepData.content?.scenario}</p>
      </div>

      {/* Prompt Suggestions */}
      <div className="bg-yellow-50 border-2 border-yellow-200 rounded-lg p-4">
        <h4 className="font-bold text-yellow-800 mb-3">💡 Prompt Forslag:</h4>
        <div className="space-y-3">
          {stepData.content?.prompt_suggestions?.map((category, index) => (
            <div key={index} className="bg-white p-3 rounded border">
              <h5 className="font-medium text-gray-800 mb-2">{category.category}:</h5>
              <div className="space-y-1">
                {category.prompts?.map((prompt, pIndex) => (
                  <button
                    key={pIndex}
                    onClick={() => setBuiltPrompt(prompt)}
                    className="block w-full text-left p-2 text-sm text-gray-600 hover:bg-gray-50 rounded border-dashed border hover:border-solid transition-all"
                  >
                    "{prompt}"
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Custom Prompt Input */}
      <div className="bg-white border-2 border-gray-200 rounded-lg p-4">
        <label className="block font-medium text-gray-700 mb-2">
          Skriv Dit Eget Personlige Prompt:
        </label>
        <textarea
          value={builtPrompt}
          onChange={(e) => setBuiltPrompt(e.target.value)}
          placeholder="Skriv dit prompt her..."
          rows={4}
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        
        <button
          onClick={() => testPrompt(builtPrompt)}
          disabled={!builtPrompt.trim() || loading}
          className={`mt-3 w-full bg-gradient-to-r ${theme.primary} text-white font-bold py-2 px-4 rounded-lg hover:opacity-90 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center`}
        >
          {loading ? (
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
          ) : (
            <Eye className="mr-2" size={16} />
          )}
          Test Mit Prompt
        </button>
      </div>

      {/* AI Response */}
      {promptPreview && (
        <div className="bg-green-50 border-2 border-green-200 rounded-lg p-4">
          <h4 className="font-bold text-green-800 mb-2 flex items-center">
            <MessageCircle className="mr-2" size={16} />
            AI Svar:
          </h4>
          <p className="text-green-700 bg-white p-3 rounded border">
            {promptPreview}
          </p>
        </div>
      )}
    </div>
  );

  return (
    <div className={`min-h-screen ${theme.bgPattern} p-4`}>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={onBack}
              className="flex items-center text-gray-600 hover:text-gray-800 transition-colors"
            >
              <ChevronLeft size={20} className="mr-1" />
              Tilbage
            </button>
            
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-800 flex items-center justify-center">
                <span className="text-3xl mr-2">{theme.icon}</span>
                Aktivitet 2: Dit Første Prompt
              </h1>
              <p className="text-gray-600 mt-1">
                Lær at skrive prompts der giver gode svar
              </p>
            </div>
            
            <div className="text-right">
              <div className="text-sm text-gray-500">Step</div>
              <div className="text-xl font-bold text-gray-800">{currentStep}/3</div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`bg-gradient-to-r ${theme.primary} h-2 rounded-full transition-all duration-500`}
              style={{ width: `${(currentStep / 3) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          {renderStepContent()}
        </div>

        {/* Action Buttons */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <div className="flex items-center justify-between">
            <button
              onClick={getHint}
              className="flex items-center px-4 py-2 text-yellow-600 border border-yellow-300 rounded-lg hover:bg-yellow-50 transition-colors"
            >
              <Lightbulb size={16} className="mr-2" />
              Få Hint
            </button>

            <div className="flex space-x-3">
              {currentStep > 1 && (
                <button
                  onClick={() => setCurrentStep(prev => prev - 1)}
                  className="flex items-center px-6 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <ChevronLeft size={16} className="mr-2" />
                  Forrige
                </button>
              )}
              
              <button
                onClick={submitStep}
                disabled={loading || !builtPrompt.trim()}
                className={`flex items-center px-6 py-2 bg-gradient-to-r ${theme.primary} text-white font-bold rounded-lg hover:opacity-90 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {loading ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                ) : completedSteps.has(currentStep) ? (
                  <CheckCircle size={16} className="mr-2" />
                ) : (
                  <ChevronRight size={16} className="mr-2" />
                )}
                {currentStep === 3 ? 'Afslut Aktivitet' : 'Næste Step'}
              </button>
            </div>
          </div>
        </div>

        {/* Hint Modal */}
        {showHint && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl shadow-2xl p-6 max-w-md w-full">
              <div className="flex items-center mb-4">
                <Lightbulb className="text-yellow-500 mr-2" size={24} />
                <h3 className="text-lg font-bold text-gray-800">Hint</h3>
              </div>
              <p className="text-gray-700 mb-4">{hintText}</p>
              <button
                onClick={() => setShowHint(false)}
                className={`w-full bg-gradient-to-r ${theme.primary} text-white font-bold py-2 px-4 rounded-lg hover:opacity-90 transition-all duration-300`}
              >
                Forstået!
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Activity2;

