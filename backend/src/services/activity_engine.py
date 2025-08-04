"""
UTOPAI Activity Engine
Skalerbar system til håndtering af forskellige aktivitetstyper med AI integration
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from .openai_service import OpenAIService

class ActivityEngine:
    """
    Central engine til håndtering af alle aktivitetstyper i UTOPAI
    Designet til nem udvidelse med nye aktivitetstyper
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.activity_handlers = {
            'intro': self._handle_intro_activity,
            'prompt_builder': self._handle_prompt_builder_activity,
            'quiz': self._handle_quiz_activity,
            'chat': self._handle_chat_activity,
            'creative': self._handle_creative_activity,
            # Nem at tilføje nye typer her:
            # 'video': self._handle_video_activity,
            # 'image': self._handle_image_activity,
        }
    
    def get_activity_content(self, activity_id: int, user_theme: str) -> Dict[str, Any]:
        """
        Henter og genererer indhold til en aktivitet baseret på brugerens tema
        """
        from ..models.user import Activity
        
        activity = Activity.query.get(activity_id)
        if not activity:
            raise ValueError(f"Activity {activity_id} not found")
        
        # Parse existing content or create new
        base_content = json.loads(activity.content) if activity.content else {}
        
        # Get handler for this activity type
        handler = self.activity_handlers.get(activity.activity_type)
        if not handler:
            raise ValueError(f"No handler for activity type: {activity.activity_type}")
        
        # Generate theme-specific content
        themed_content = handler(activity, user_theme, base_content)
        
        return {
            'id': activity.id,
            'name': activity.name,
            'description': activity.description,
            'type': activity.activity_type,
            'difficulty': activity.difficulty_level,
            'points_reward': activity.points_reward,
            'content': themed_content
        }
    
    def evaluate_activity_response(self, activity_id: int, user_response: Dict[str, Any], user_theme: str) -> Dict[str, Any]:
        """
        Evaluerer brugerens svar på en aktivitet og returnerer feedback
        """
        from ..models.user import Activity
        
        activity = Activity.query.get(activity_id)
        if not activity:
            raise ValueError(f"Activity {activity_id} not found")
        
        handler = self.activity_handlers.get(activity.activity_type)
        if not handler:
            raise ValueError(f"No handler for activity type: {activity.activity_type}")
        
        # Evaluate response using appropriate handler
        evaluation = self._evaluate_response(activity, user_response, user_theme)
        
        return evaluation
    
    def _handle_intro_activity(self, activity: Any, user_theme: str, base_content: Dict) -> Dict[str, Any]:
        """Handler for intro/educational activities"""
        
        theme_content = self._get_theme_content(user_theme)
        
        return {
            'type': 'intro',
            'title': f"Velkommen til {theme_content['world_name']}!",
            'sections': [
                {
                    'title': 'Hvad er ChatGPT?',
                    'content': f"""
                    Hej {theme_content['greeting']}! 
                    
                    ChatGPT er en AI (Kunstig Intelligens) der kan hjælpe dig med mange ting:
                    
                    • Besvare spørgsmål om {theme_content['interests']}
                    • Hjælpe med lektier og læring
                    • Fortælle historier og være kreativ
                    • Forklare svære ting på en nem måde
                    
                    Men ChatGPT er ikke magisk - den har brug for gode instruktioner fra dig!
                    """,
                    'character': theme_content['mentor_character'],
                    'background': theme_content['background_image']
                },
                {
                    'title': 'Hvordan virker det?',
                    'content': f"""
                    Forestil dig ChatGPT som din {theme_content['helper_metaphor']}:
                    
                    • Du giver den en opgave (et "prompt")
                    • Den tænker over dit spørgsmål
                    • Den giver dig et svar tilbage
                    
                    Jo bedre du er til at forklare hvad du vil have, 
                    jo bedre svar får du tilbage!
                    """,
                    'interactive_element': {
                        'type': 'simple_demo',
                        'example_prompt': f"Fortæl mig om {theme_content['example_topic']}",
                        'example_response': f"Her er en spændende historie om {theme_content['example_topic']}..."
                    }
                }
            ],
            'completion_criteria': {
                'type': 'read_through',
                'sections_required': 2
            }
        }
    
    def _handle_prompt_builder_activity(self, activity: Any, user_theme: str, base_content: Dict) -> Dict[str, Any]:
        """Handler for prompt building activities"""
        
        theme_content = self._get_theme_content(user_theme)
        
        return {
            'type': 'prompt_builder',
            'title': 'Byg dit første prompt!',
            'instructions': f"""
            Nu skal du lære at lave gode prompts til ChatGPT!
            
            Din {theme_content['mentor_character']} vil hjælpe dig med at bygge 
            et perfekt prompt trin for trin.
            """,
            'steps': [
                {
                    'step': 1,
                    'title': 'Vælg et emne',
                    'description': f'Hvad vil du gerne vide mere om? Måske noget om {theme_content["interests"]}?',
                    'input_type': 'topic_selector',
                    'options': theme_content['topic_options'],
                    'custom_option': True
                },
                {
                    'step': 2,
                    'title': 'Vælg en stil',
                    'description': 'Hvordan skal ChatGPT svare dig?',
                    'input_type': 'style_selector',
                    'options': [
                        {'value': 'simple', 'label': 'Simpelt og nemt at forstå'},
                        {'value': 'story', 'label': 'Som en spændende historie'},
                        {'value': 'facts', 'label': 'Med mange interessante fakta'},
                        {'value': 'fun', 'label': 'Sjovt og underholdende'}
                    ]
                },
                {
                    'step': 3,
                    'title': 'Tilføj detaljer',
                    'description': 'Hvad vil du specifikt vide?',
                    'input_type': 'detail_builder',
                    'prompts': [
                        'Hvor langt skal svaret være?',
                        'Er der noget bestemt du vil fokusere på?',
                        'Skal det være til din alder?'
                    ]
                }
            ],
            'ai_assistance': {
                'enabled': True,
                'helper_prompts': [
                    f"Som {theme_content['mentor_character']}, hjælp barnet med at forbedre deres prompt",
                    "Giv konstruktiv feedback på promptets klarhed",
                    "Foreslå forbedringer på en venlig måde"
                ]
            },
            'completion_criteria': {
                'type': 'prompt_quality',
                'min_score': 7,
                'criteria': ['clarity', 'specificity', 'appropriateness']
            }
        }
    
    def _handle_quiz_activity(self, activity: Any, user_theme: str, base_content: Dict) -> Dict[str, Any]:
        """Handler for quiz activities"""
        
        theme_content = self._get_theme_content(user_theme)
        
        return {
            'type': 'quiz',
            'title': 'Klare vs. Uklare Prompts',
            'instructions': f"""
            Din {theme_content['mentor_character']} har brug for din hjælp!
            
            Kan du hjælpe med at finde ud af hvilke prompts der er gode, 
            og hvilke der kan forbedres?
            """,
            'questions': [
                {
                    'id': 1,
                    'type': 'comparison',
                    'question': 'Hvilket prompt er bedst?',
                    'context': f'Du vil gerne vide noget om {theme_content["example_topic"]}',
                    'options': [
                        {
                            'id': 'a',
                            'text': f'Fortæl om {theme_content["example_topic"]}',
                            'quality': 'poor',
                            'feedback': 'Dette prompt er for kort og uklart. ChatGPT ved ikke hvad du specifikt vil vide.'
                        },
                        {
                            'id': 'b', 
                            'text': f'Kan du forklare hvad {theme_content["example_topic"]} er, på en måde en 10-årig kan forstå, med 3 interessante fakta?',
                            'quality': 'good',
                            'feedback': 'Perfekt! Dette prompt er klart, specifikt og siger præcis hvad du vil have.'
                        }
                    ]
                },
                {
                    'id': 2,
                    'type': 'fix_prompt',
                    'question': 'Kan du forbedre dette prompt?',
                    'bad_prompt': 'Hjælp mig',
                    'context': 'Barnet vil have hjælp til matematik lektier',
                    'hints': [
                        'Hvad skal ChatGPT hjælpe med?',
                        'Hvilket niveau er det?',
                        'Hvad for en slags hjælp?'
                    ],
                    'good_examples': [
                        'Kan du hjælpe mig med at forstå gange-tabeller for 3. klasse?',
                        'Jeg har brug for hjælp til at løse plus-opgaver med tal op til 100'
                    ]
                }
            ],
            'ai_feedback': {
                'enabled': True,
                'feedback_style': theme_content['feedback_style']
            },
            'completion_criteria': {
                'type': 'score_based',
                'min_score': 80,
                'max_attempts': 3
            }
        }
    
    def _handle_chat_activity(self, activity: Any, user_theme: str, base_content: Dict) -> Dict[str, Any]:
        """Handler for chat activities"""
        
        theme_content = self._get_theme_content(user_theme)
        
        return {
            'type': 'chat',
            'title': f'Chat med din AI-{theme_content["mentor_title"]}',
            'instructions': f"""
            Nu får du chancen for at chatte med en rigtig AI!
            
            Din {theme_content['mentor_character']} er klar til at svare på dine spørgsmål.
            Prøv at bruge det du har lært om gode prompts!
            """,
            'ai_character': {
                'name': theme_content['mentor_name'],
                'personality': theme_content['mentor_personality'],
                'system_prompt': f"""
                Du er {theme_content['mentor_name']}, en venlig {theme_content['mentor_character']} 
                der hjælper børn på 9-12 år med at lære om AI og prompting.
                
                Personlighed: {theme_content['mentor_personality']}
                
                Regler:
                - Svar altid på dansk
                - Hold svarene korte og forståelige for børn
                - Vær opmuntrende og positiv
                - Hvis barnet stiller et dårligt prompt, hjælp dem med at forbedre det
                - Fokuser på {theme_content['theme_focus']}
                - Brug emojis og {theme_content['theme_emojis']}
                """,
                'avatar': theme_content['mentor_avatar'],
                'background': theme_content['chat_background']
            },
            'guided_prompts': [
                f"Spørg om {theme_content['suggested_topics'][0]}",
                f"Bed om hjælp til {theme_content['suggested_topics'][1]}",
                "Prøv at stille et meget specifikt spørgsmål",
                "Bed AI'en om at forklare noget svært på en nem måde"
            ],
            'success_criteria': [
                'Stil mindst 3 spørgsmål',
                'Få AI\'en til at give dig et godt svar',
                'Prøv at forbedre et prompt baseret på AI\'ens feedback',
                'Chat i mindst 5 minutter'
            ],
            'completion_criteria': {
                'type': 'interaction_based',
                'min_messages': 6,
                'min_duration_minutes': 3,
                'quality_check': True
            }
        }
    
    def _handle_creative_activity(self, activity: Any, user_theme: str, base_content: Dict) -> Dict[str, Any]:
        """Handler for creative activities"""
        
        theme_content = self._get_theme_content(user_theme)
        
        return {
            'type': 'creative',
            'title': 'Kreativ Prompt-Udfordring!',
            'instructions': f"""
            Nu er det tid til den ultimative udfordring!
            
            Din {theme_content['mentor_character']} har en særlig mission til dig:
            Lav det mest kreative og interessante prompt du kan!
            """,
            'challenges': [
                {
                    'id': 1,
                    'title': f'{theme_content["creative_challenge_1"]["title"]}',
                    'description': theme_content["creative_challenge_1"]["description"],
                    'example': theme_content["creative_challenge_1"]["example"],
                    'difficulty': 'medium'
                },
                {
                    'id': 2,
                    'title': f'{theme_content["creative_challenge_2"]["title"]}',
                    'description': theme_content["creative_challenge_2"]["description"],
                    'example': theme_content["creative_challenge_2"]["example"],
                    'difficulty': 'hard'
                }
            ],
            'creativity_boosters': [
                'Kombiner to forskellige emner',
                'Bed om svaret i en sjov stil',
                'Tilføj en overraskende detalje',
                'Bed om en historie med dig som hovedperson'
            ],
            'ai_evaluation': {
                'enabled': True,
                'criteria': [
                    'creativity',
                    'clarity', 
                    'originality',
                    'appropriateness'
                ],
                'feedback_style': 'encouraging'
            },
            'completion_criteria': {
                'type': 'creativity_score',
                'min_creativity_score': 7,
                'peer_review': False  # Kan aktiveres senere
            }
        }
    
    def _get_theme_content(self, user_theme: str) -> Dict[str, Any]:
        """Returnerer tema-specifikt indhold"""
        
        if user_theme == 'superhelte':
            return {
                'world_name': 'Superhelte Akademiet',
                'greeting': 'unge helt',
                'mentor_character': 'AI-superhelt',
                'mentor_name': 'Captain Prompt',
                'mentor_title': 'mentor',
                'mentor_personality': 'Modig, hjælpsom og altid klar til at redde dagen med god AI-viden',
                'mentor_avatar': '🦸‍♂️',
                'helper_metaphor': 'superhelt-partner',
                'background_image': 'superhero_city.jpg',
                'chat_background': 'superhero_hq.jpg',
                'interests': 'superhelte, redning af verden, teknologi og retfærdighed',
                'example_topic': 'superhelte kræfter',
                'theme_focus': 'at bruge AI-kræfter til at hjælpe andre og lære nye ting',
                'theme_emojis': '🦸‍♂️🦸‍♀️⚡🛡️🌟',
                'feedback_style': 'Som en opmuntrende superhelt-mentor',
                'topic_options': [
                    'Superhelte og deres kræfter',
                    'Teknologi og gadgets',
                    'Hvordan man hjælper andre',
                    'Videnskab og opfindelser'
                ],
                'suggested_topics': [
                    'superhelte teknologi',
                    'hvordan man redder verden'
                ],
                'creative_challenge_1': {
                    'title': 'Superhelt Historie Mission',
                    'description': 'Lav et prompt der får AI\'en til at skrive en historie hvor DU er superhelten!',
                    'example': 'Skriv en kort historie hvor jeg er en superhelt der bruger AI-kræfter til at hjælpe børn med lektier'
                },
                'creative_challenge_2': {
                    'title': 'Opfind en Superhelt Gadget',
                    'description': 'Få AI\'en til at hjælpe dig med at opfinde en ny superhelt-gadget!',
                    'example': 'Hjælp mig med at opfinde en superhelt-gadget der kan oversætte alle sprog og forklar hvordan den virker'
                }
            }
        else:  # prinsesse theme
            return {
                'world_name': 'Det Magiske AI-Kongerige',
                'greeting': 'lille prinsesse',
                'mentor_character': 'magisk fe',
                'mentor_name': 'Fe Promptina',
                'mentor_title': 'vejleder',
                'mentor_personality': 'Venlig, magisk og fuld af visdom om AI-magi',
                'mentor_avatar': '🧚‍♀️',
                'helper_metaphor': 'magisk assistent',
                'background_image': 'magical_castle.jpg',
                'chat_background': 'fairy_garden.jpg',
                'interests': 'magi, eventyr, smukke ting og hjælpe andre',
                'example_topic': 'magiske væsener',
                'theme_focus': 'at bruge AI-magi til at skabe smukke ting og hjælpe andre',
                'theme_emojis': '👸✨🦄🌸🏰',
                'feedback_style': 'Som en venlig og opmuntrende fe',
                'topic_options': [
                    'Magiske væsener og eventyr',
                    'Smukke slotte og haver',
                    'Hvordan man hjælper andre',
                    'Kunst og kreativitet'
                ],
                'suggested_topics': [
                    'magiske væsener',
                    'hvordan man skaber smukke ting'
                ],
                'creative_challenge_1': {
                    'title': 'Magisk Eventyr Mission',
                    'description': 'Lav et prompt der får AI\'en til at skrive et eventyr hvor DU er hovedpersonen!',
                    'example': 'Skriv et kort eventyr hvor jeg er en prinsesse der bruger AI-magi til at hjælpe dyr i skoven'
                },
                'creative_challenge_2': {
                    'title': 'Design et Magisk Slot',
                    'description': 'Få AI\'en til at hjælpe dig med at designe det perfekte magiske slot!',
                    'example': 'Hjælp mig med at designe et magisk slot der kan lære børn nye ting og beskriv alle de fantastiske rum'
                }
            }
    
    def _evaluate_response(self, activity: Any, user_response: Dict[str, Any], user_theme: str) -> Dict[str, Any]:
        """Evaluerer brugerens svar baseret på aktivitetstype"""
        
        activity_type = activity.activity_type
        
        if activity_type == 'intro':
            return self._evaluate_intro_response(user_response)
        elif activity_type == 'prompt_builder':
            return self._evaluate_prompt_builder_response(user_response, user_theme)
        elif activity_type == 'quiz':
            return self._evaluate_quiz_response(user_response)
        elif activity_type == 'chat':
            return self._evaluate_chat_response(user_response, user_theme)
        elif activity_type == 'creative':
            return self._evaluate_creative_response(user_response, user_theme)
        else:
            return {'success': False, 'error': 'Unknown activity type'}
    
    def _evaluate_intro_response(self, user_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluerer intro aktivitet - typisk bare completion tracking"""
        sections_completed = user_response.get('sections_completed', 0)
        required_sections = user_response.get('required_sections', 2)
        
        success = sections_completed >= required_sections
        
        return {
            'success': success,
            'score': 100 if success else (sections_completed / required_sections) * 100,
            'feedback': 'Godt klaret! Du har nu lært grundlæggende om ChatGPT.' if success else 'Læs alle sektioner for at fortsætte.',
            'points_earned': 50 if success else 0,
            'next_hint': 'Nu er du klar til at bygge dit første prompt!' if success else None
        }
    
    def _evaluate_prompt_builder_response(self, user_response: Dict[str, Any], user_theme: str) -> Dict[str, Any]:
        """Evaluerer prompt builder aktivitet med AI assistance"""
        
        user_prompt = user_response.get('final_prompt', '')
        
        if not user_prompt:
            return {
                'success': False,
                'score': 0,
                'feedback': 'Du skal bygge et prompt først!',
                'points_earned': 0
            }
        
        # Use AI to evaluate prompt quality
        evaluation_prompt = f"""
        Evaluer dette prompt skrevet af et barn på 9-12 år:
        "{user_prompt}"
        
        Bedøm på en skala fra 1-10 baseret på:
        - Klarhed (er det klart hvad barnet vil have?)
        - Specificitet (er det specifikt nok?)
        - Passende for alder
        
        Giv konstruktiv feedback på dansk der er opmuntrende og hjælpsom.
        
        Svar i JSON format:
        {{
            "score": [1-10],
            "feedback": "Din feedback her",
            "strengths": ["styrke1", "styrke2"],
            "improvements": ["forbedring1", "forbedring2"]
        }}
        """
        
        try:
            ai_evaluation = self.openai_service.get_completion(evaluation_prompt)
            evaluation = json.loads(ai_evaluation)
            
            score = evaluation.get('score', 5)
            success = score >= 7
            
            return {
                'success': success,
                'score': score * 10,  # Convert to percentage
                'feedback': evaluation.get('feedback', 'Godt forsøg!'),
                'strengths': evaluation.get('strengths', []),
                'improvements': evaluation.get('improvements', []),
                'points_earned': 100 if success else 50,
                'ai_suggestion': self._get_prompt_improvement_suggestion(user_prompt, user_theme) if not success else None
            }
            
        except Exception as e:
            # Fallback evaluation if AI fails
            return self._fallback_prompt_evaluation(user_prompt)
    
    def _evaluate_quiz_response(self, user_response: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluerer quiz svar"""
        answers = user_response.get('answers', {})
        total_questions = len(answers)
        correct_answers = 0
        
        # Check each answer (this would be more sophisticated in real implementation)
        for question_id, answer in answers.items():
            if self._is_correct_answer(question_id, answer):
                correct_answers += 1
        
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        success = score >= 80
        
        return {
            'success': success,
            'score': score,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'feedback': f'Du fik {correct_answers} ud af {total_questions} rigtige!',
            'points_earned': 75 if success else 25,
            'detailed_feedback': self._get_quiz_detailed_feedback(answers)
        }
    
    def _evaluate_chat_response(self, user_response: Dict[str, Any], user_theme: str) -> Dict[str, Any]:
        """Evaluerer chat aktivitet"""
        messages = user_response.get('messages', [])
        duration_minutes = user_response.get('duration_minutes', 0)
        
        user_messages = [msg for msg in messages if msg.get('sender') == 'user']
        message_count = len(user_messages)
        
        # Basic criteria checking
        meets_message_requirement = message_count >= 6
        meets_duration_requirement = duration_minutes >= 3
        
        # Quality check using AI
        quality_score = self._evaluate_chat_quality(user_messages, user_theme)
        
        success = meets_message_requirement and meets_duration_requirement and quality_score >= 7
        
        return {
            'success': success,
            'score': min(100, (message_count * 10) + (duration_minutes * 5) + (quality_score * 5)),
            'message_count': message_count,
            'duration_minutes': duration_minutes,
            'quality_score': quality_score,
            'feedback': self._get_chat_feedback(message_count, duration_minutes, quality_score),
            'points_earned': 150 if success else 75
        }
    
    def _evaluate_creative_response(self, user_response: Dict[str, Any], user_theme: str) -> Dict[str, Any]:
        """Evaluerer kreativ aktivitet med AI"""
        creative_prompt = user_response.get('creative_prompt', '')
        challenge_id = user_response.get('challenge_id', 1)
        
        if not creative_prompt:
            return {
                'success': False,
                'score': 0,
                'feedback': 'Du skal lave et kreativt prompt først!',
                'points_earned': 0
            }
        
        # AI evaluation of creativity
        creativity_evaluation = self._evaluate_creativity_with_ai(creative_prompt, user_theme)
        
        return creativity_evaluation
    
    # Helper methods for evaluation
    def _fallback_prompt_evaluation(self, prompt: str) -> Dict[str, Any]:
        """Fallback evaluation hvis AI fejler"""
        score = 5  # Default score
        
        # Simple heuristics
        if len(prompt) > 20:
            score += 1
        if '?' in prompt:
            score += 1
        if any(word in prompt.lower() for word in ['hjælp', 'forklar', 'fortæl']):
            score += 1
        if any(word in prompt.lower() for word in ['specifik', 'detaljer', 'eksempel']):
            score += 2
        
        score = min(10, score)
        success = score >= 7
        
        return {
            'success': success,
            'score': score * 10,
            'feedback': 'Godt forsøg! Prøv at være endnu mere specifik næste gang.' if not success else 'Godt prompt!',
            'points_earned': 100 if success else 50
        }
    
    def _get_prompt_improvement_suggestion(self, prompt: str, theme: str) -> str:
        """Genererer forbedringsforslag til prompt"""
        try:
            suggestion_prompt = f"""
            Et barn har lavet dette prompt: "{prompt}"
            
            Giv et kort, venligt forslag til hvordan de kan forbedre det.
            Fokuser på {theme} tema og hold det simpelt for børn.
            """
            return self.openai_service.get_completion(suggestion_prompt)
        except:
            return "Prøv at være mere specifik om hvad du vil have svar på!"
    
    def _is_correct_answer(self, question_id: str, answer: str) -> bool:
        """Checker om quiz svar er korrekt"""
        # This would contain the correct answers for each question
        correct_answers = {
            '1': 'b',  # The better prompt option
            '2': 'improved_prompt'  # Any improved version
        }
        return answer == correct_answers.get(question_id, '')
    
    def _get_quiz_detailed_feedback(self, answers: Dict) -> List[str]:
        """Returnerer detaljeret feedback for quiz svar"""
        feedback = []
        for question_id, answer in answers.items():
            if self._is_correct_answer(question_id, answer):
                feedback.append(f"Spørgsmål {question_id}: Rigtigt! 🎉")
            else:
                feedback.append(f"Spørgsmål {question_id}: Prøv igen - tænk på hvad der gør et prompt klart og specifikt")
        return feedback
    
    def _evaluate_chat_quality(self, user_messages: List[Dict], theme: str) -> int:
        """Evaluerer kvaliteten af chat beskeder"""
        if not user_messages:
            return 0
        
        # Simple quality metrics
        avg_length = sum(len(msg.get('content', '')) for msg in user_messages) / len(user_messages)
        has_questions = any('?' in msg.get('content', '') for msg in user_messages)
        variety = len(set(msg.get('content', '')[:10] for msg in user_messages))  # Check for variety
        
        score = 5  # Base score
        if avg_length > 10:
            score += 1
        if has_questions:
            score += 2
        if variety > 2:
            score += 2
        
        return min(10, score)
    
    def _get_chat_feedback(self, message_count: int, duration: int, quality: int) -> str:
        """Genererer feedback for chat aktivitet"""
        feedback_parts = []
        
        if message_count >= 6:
            feedback_parts.append("Du stillede mange gode spørgsmål! 💬")
        else:
            feedback_parts.append(f"Prøv at stille flere spørgsmål (du stillede {message_count}, men 6+ er bedre)")
        
        if duration >= 3:
            feedback_parts.append("Du tog dig god tid til at chatte! ⏰")
        else:
            feedback_parts.append("Prøv at chatte lidt længere næste gang")
        
        if quality >= 7:
            feedback_parts.append("Dine prompts var rigtig gode! 🌟")
        else:
            feedback_parts.append("Prøv at være endnu mere specifik i dine spørgsmål")
        
        return " ".join(feedback_parts)
    
    def _evaluate_creativity_with_ai(self, prompt: str, theme: str) -> Dict[str, Any]:
        """Evaluerer kreativitet med AI assistance"""
        try:
            evaluation_prompt = f"""
            Evaluer kreativiteten i dette prompt lavet af et barn:
            "{prompt}"
            
            Bedøm på skala 1-10 for:
            - Kreativitet og originalitet
            - Klarhed
            - Passende for {theme} tema
            
            Giv opmuntrende feedback på dansk.
            
            JSON format:
            {{
                "creativity_score": [1-10],
                "clarity_score": [1-10], 
                "theme_fit_score": [1-10],
                "overall_score": [1-10],
                "feedback": "Din feedback",
                "highlights": ["det bedste ved promptet"]
            }}
            """
            
            ai_response = self.openai_service.get_completion(evaluation_prompt)
            evaluation = json.loads(ai_response)
            
            overall_score = evaluation.get('overall_score', 5)
            success = overall_score >= 7
            
            return {
                'success': success,
                'score': overall_score * 10,
                'creativity_score': evaluation.get('creativity_score', 5),
                'clarity_score': evaluation.get('clarity_score', 5),
                'theme_fit_score': evaluation.get('theme_fit_score', 5),
                'feedback': evaluation.get('feedback', 'Godt kreativt forsøg!'),
                'highlights': evaluation.get('highlights', []),
                'points_earned': 200 if success else 100
            }
            
        except Exception as e:
            # Fallback evaluation
            return {
                'success': True,
                'score': 80,
                'feedback': 'Fantastisk kreativt prompt! Du tænker virkelig ud af boksen! 🎨',
                'points_earned': 150
            }

