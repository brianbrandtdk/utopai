import os
import openai
from typing import Dict, List, Optional
import json

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        )
    
    def get_system_prompt(self, theme: str, activity_type: str) -> str:
        """Get system prompt based on theme and activity type"""
        
        base_instructions = """Du er en AI-lærer for børn på 9-12 år der lærer om ChatGPT og prompting.
        
VIGTIGE REGLER:
- Brug altid børnevenligt sprog
- Vær tålmodig og opmuntrende
- Giv konkrete eksempler
- Undgå komplekse tekniske termer
- Svar aldrig på upassende spørgsmål
- Hold svarene korte og engagerende
- Brug emojis sparsomt men passende"""
        
        theme_instructions = {
            'superhelte': """
Du er PROMPT-BOT 🤖, en venlig AI-superhelt der hjælper børn med at lære prompting!
- Brug superhelte-eksempler (Spider-Man, Wonder Woman, etc.)
- Tal om at "redde verden" med gode prompts
- Brug ord som "superkraft", "mission", "helt"
- Vær energisk og heroisk i tonen
""",
            'prinsesse': """
Du er PROMPT-FE ✨, en magisk AI-fe der hjælper børn med at lære prompting!
- Brug prinsesse og eventyr-eksempler
- Tal om "magiske prompts" og "tryllestave"
- Brug ord som "eventyr", "magi", "slot", "krystal"
- Vær venlig og fortryllende i tonen
"""
        }
        
        activity_instructions = {
            'intro': "Fokuser på at forklare hvad ChatGPT er på en simpel måde med mange eksempler.",
            'prompt_builder': "Hjælp barnet med at bygge deres første prompt trin for trin.",
            'quiz': "Stil spørgsmål og giv feedback på svarene. Vær opmuntrende selv ved forkerte svar.",
            'chat': "Chat naturligt med barnet og hjælp dem øve prompting gennem samtale.",
            'creative': "Opmuntr kreativitet og hjælp barnet med at lave sjove, kreative prompts."
        }
        
        return f"{base_instructions}\n\n{theme_instructions.get(theme, '')}\n\n{activity_instructions.get(activity_type, '')}"
    
    def moderate_content(self, text: str) -> bool:
        """Check if content is appropriate for children"""
        try:
            response = self.client.moderations.create(input=text)
            return not response.results[0].flagged
        except Exception as e:
            print(f"Moderation error: {e}")
            return True  # Allow content if moderation fails
    
    def chat_with_ai(self, messages: List[Dict], theme: str, activity_type: str = 'chat') -> str:
        """Chat with AI mentor based on theme and activity"""
        try:
            # Add system prompt
            system_prompt = self.get_system_prompt(theme, activity_type)
            full_messages = [{"role": "system", "content": system_prompt}] + messages
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=full_messages,
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "Beklager, jeg har tekniske problemer lige nu. Prøv igen om lidt! 🤖"
    
    def evaluate_prompt(self, prompt: str, theme: str) -> Dict:
        """Evaluate a prompt and give feedback"""
        try:
            system_prompt = f"""Du er en AI-lærer der evaluerer børns prompts.
            
Evaluer følgende prompt på en skala fra 1-5 på disse kriterier:
- Klarhed (er det klart hvad der ønskes?)
- Specificitet (er det specifikt nok?)
- Kreativitet (er det kreativt og interessant?)

Giv også konstruktiv feedback på dansk til et barn på 10 år.
Brug {theme}-tema i dit svar.

Svar i JSON format:
{{
    "score": {{
        "klarhed": 1-5,
        "specificitet": 1-5,
        "kreativitet": 1-5,
        "total": 1-5
    }},
    "feedback": "Din feedback her",
    "suggestions": ["forslag 1", "forslag 2"]
}}"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Evaluer dette prompt: {prompt}"}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Prompt evaluation error: {e}")
            return {
                "score": {"klarhed": 3, "specificitet": 3, "kreativitet": 3, "total": 3},
                "feedback": "Godt forsøg! Fortsæt med at øve dig.",
                "suggestions": ["Prøv at være mere specifik", "Tilføj flere detaljer"]
            }
    
    def generate_activity_content(self, activity_type: str, theme: str, difficulty: int = 1) -> Dict:
        """Generate dynamic content for activities"""
        try:
            prompts = {
                'quiz_question': f"""Lav et spørgsmål om ChatGPT og prompting til et barn på 10 år.
                Sværhedsgrad: {difficulty}/5
                Tema: {theme}
                
                Svar i JSON format:
                {{
                    "question": "Dit spørgsmål her",
                    "options": ["A) svar 1", "B) svar 2", "C) svar 3", "D) svar 4"],
                    "correct_answer": "A",
                    "explanation": "Forklaring af det rigtige svar"
                }}""",
                
                'prompt_challenge': f"""Lav en kreativ prompt-udfordring til et barn på 10 år.
                Tema: {theme}
                Sværhedsgrad: {difficulty}/5
                
                Svar i JSON format:
                {{
                    "challenge": "Beskriv udfordringen",
                    "example": "Et eksempel på et godt prompt",
                    "hints": ["hint 1", "hint 2", "hint 3"]
                }}""",
                
                'story_scenario': f"""Lav et kort scenarie hvor et barn skal bruge ChatGPT.
                Tema: {theme}
                
                Svar i JSON format:
                {{
                    "scenario": "Beskriv situationen",
                    "task": "Hvad skal barnet gøre?",
                    "good_prompt_example": "Eksempel på et godt prompt"
                }}"""
            }
            
            if activity_type not in prompts:
                return {"error": "Unknown activity type"}
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompts[activity_type]}],
                max_tokens=500,
                temperature=0.8
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Content generation error: {e}")
            return {"error": "Could not generate content"}
    
    def get_hint(self, question: str, attempt_count: int, theme: str) -> str:
        """Get progressive hints based on attempt count"""
        try:
            hint_levels = {
                1: "Giv et lille hint til at hjælpe barnet på vej",
                2: "Giv et større hint der næsten afslører svaret", 
                3: "Giv svaret men forklar det venligt"
            }
            
            level = min(attempt_count, 3)
            system_prompt = f"""Du hjælper et barn på 10 år der har svært ved at svare på et spørgsmål.
            Dette er deres {attempt_count}. forsøg.
            Brug {theme}-tema i dit svar.
            
            {hint_levels[level]}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Spørgsmål: {question}"}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Hint generation error: {e}")
            return "Prøv igen! Du kan godt finde ud af det! 💪"

    # ===== AKTIVITET 1 SPECIFIKKE METODER =====
    
    def generate_activity_1_intro(self, theme: str) -> Dict:
        """Generate personalized introduction for Activity 1"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav en kort, spændende introduktion til Aktivitet 1: "Hvad er ChatGPT?"
            
            Introduktionen skal:
            - Være på dansk og børnevenlig
            - Bruge {theme}-tema
            - Forklare hvad barnet skal lære
            - Være motiverende og spændende
            - Være max 100 ord
            
            Svar i JSON format:
            {{
                "welcome_message": "Velkomstbesked",
                "learning_goals": ["mål 1", "mål 2", "mål 3"],
                "motivation": "Motiverende besked"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Activity 1 intro error: {e}")
            return {
                "welcome_message": "Velkommen til din første AI-mission! 🚀",
                "learning_goals": ["Lær hvad ChatGPT er", "Forstå hvordan AI tænker", "Opdage AI's superkræfter"],
                "motivation": "Du er klar til at blive en ægte AI-ekspert!"
            }
    
    def generate_interactive_story(self, theme: str) -> Dict:
        """Generate interactive story for Step 1"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav en interaktiv historie om at møde ChatGPT for første gang.
            
            Historien skal:
            - Bruge {theme}-tema
            - Have 3-4 valgmuligheder undervejs
            - Forklare hvad ChatGPT er gennem historien
            - Være spændende for 10-årige
            - Slutte med at barnet forstår hvad AI er
            
            Svar i JSON format:
            {{
                "story_intro": "Start på historien",
                "choices": [
                    {{
                        "id": 1,
                        "text": "Valgmulighed 1",
                        "consequence": "Hvad sker der"
                    }},
                    {{
                        "id": 2,
                        "text": "Valgmulighed 2", 
                        "consequence": "Hvad sker der"
                    }}
                ],
                "story_conclusion": "Afslutning på historien",
                "learning_point": "Hvad lærte barnet?"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.8
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Interactive story error: {e}")
            return {
                "story_intro": "Du møder en mystisk AI...",
                "choices": [
                    {"id": 1, "text": "Sig hej", "consequence": "AI'en svarer venligt"},
                    {"id": 2, "text": "Stil et spørgsmål", "consequence": "AI'en forklarer sig selv"}
                ],
                "story_conclusion": "Nu forstår du hvad AI er!",
                "learning_point": "ChatGPT er en venlig AI der kan hjælpe dig"
            }
    
    def generate_thinking_explanation(self, theme: str) -> Dict:
        """Generate explanation of how ChatGPT thinks"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Forklar hvordan ChatGPT "tænker" til et barn på 10 år.
            
            Forklaringen skal:
            - Bruge {theme}-tema og metaforer
            - Være simpel og forståelig
            - Bruge konkrete eksempler
            - Forklare ordkæder og mønstre
            - Være max 150 ord
            
            Svar i JSON format:
            {{
                "simple_explanation": "Simpel forklaring",
                "metaphor": "Metafor der passer til temaet",
                "example": "Konkret eksempel"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Thinking explanation error: {e}")
            return {
                "simple_explanation": "ChatGPT tænker ved at forbinde ord og ideer",
                "metaphor": "Som en superhelt der husker alt hvad den har læst",
                "example": "Når du siger 'kat', tænker den på 'kæledyr', 'mjav', 'pels'"
            }
    
    def generate_word_chain_game(self, theme: str) -> Dict:
        """Generate word chain game for understanding AI thinking"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav et ordkæde-spil der viser hvordan AI forbinder ord.
            
            Spillet skal:
            - Bruge {theme}-tema
            - Have et startord
            - Vise 3-4 forbundne ord
            - Forklare forbindelserne
            - Være sjovt og lærerigt
            
            Svar i JSON format:
            {{
                "start_word": "startord",
                "word_chain": [
                    {{
                        "word": "ord",
                        "connection": "hvorfor det er forbundet"
                    }}
                ],
                "explanation": "Forklaring af hvordan AI tænker sådan"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.8
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Word chain game error: {e}")
            return {
                "start_word": "superhelt",
                "word_chain": [
                    {"word": "superkraft", "connection": "Superhelte har superkræfter"},
                    {"word": "redde", "connection": "Superhelte redder verden"},
                    {"word": "kappe", "connection": "Mange superhelte har kapper"}
                ],
                "explanation": "AI forbinder ord baseret på hvad den har lært"
            }
    
    def generate_chatgpt_vs_google(self, theme: str) -> Dict:
        """Generate comparison between ChatGPT and Google"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav en simpel sammenligning mellem ChatGPT og Google for børn.
            
            Sammenligningen skal:
            - Bruge {theme}-tema
            - Forklare forskellen klart
            - Bruge konkrete eksempler
            - Være børnevenlig
            
            Svar i JSON format:
            {{
                "chatgpt": {{
                    "description": "Hvad ChatGPT gør",
                    "example": "Eksempel på brug"
                }},
                "google": {{
                    "description": "Hvad Google gør", 
                    "example": "Eksempel på brug"
                }},
                "key_difference": "Hovedforskellen"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"ChatGPT vs Google error: {e}")
            return {
                "chatgpt": {
                    "description": "ChatGPT er som en venlig robot der snakker med dig",
                    "example": "Du kan spørge: 'Fortæl mig om superhelte'"
                },
                "google": {
                    "description": "Google finder hjemmesider til dig",
                    "example": "Du søger: 'superhelte film'"
                },
                "key_difference": "ChatGPT snakker med dig, Google finder ting til dig"
            }
    
    def generate_superpower_cards(self, theme: str) -> List[Dict]:
        """Generate superpower cards showing what ChatGPT can do"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav 6 "superkraft-kort" der viser hvad ChatGPT er god til.
            
            Kortene skal:
            - Bruge {theme}-tema
            - Være positive og motiverende
            - Vise konkrete eksempler
            - Være forståelige for 10-årige
            
            Svar i JSON format:
            {{
                "cards": [
                    {{
                        "title": "Superkraft navn",
                        "description": "Hvad den kan",
                        "example": "Konkret eksempel",
                        "icon": "emoji"
                    }}
                ]
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.8
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('cards', [])
            
        except Exception as e:
            print(f"Superpower cards error: {e}")
            return [
                {
                    "title": "Forklaring-kraft",
                    "description": "Kan forklare svære ting simpelt",
                    "example": "Forklar hvordan en bil virker",
                    "icon": "🧠"
                }
            ]
    
    def generate_weakness_cards(self, theme: str) -> List[Dict]:
        """Generate weakness cards showing ChatGPT limitations"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav 4 "svaghedskort" der viser hvad ChatGPT IKKE kan.
            
            Kortene skal:
            - Bruge {theme}-tema
            - Være ærlige men ikke skræmmende
            - Forklare begrænsninger simpelt
            - Hjælpe børn forstå AI's grænser
            
            Svar i JSON format:
            {{
                "cards": [
                    {{
                        "title": "Svaghed navn",
                        "description": "Hvad den ikke kan",
                        "example": "Konkret eksempel",
                        "icon": "emoji"
                    }}
                ]
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('cards', [])
            
        except Exception as e:
            print(f"Weakness cards error: {e}")
            return [
                {
                    "title": "Kan ikke se",
                    "description": "ChatGPT kan ikke se billeder eller video",
                    "example": "Kan ikke beskrive dit tegning",
                    "icon": "👁️"
                }
            ]
    
    def generate_capability_quiz(self, theme: str) -> List[Dict]:
        """Generate quiz about ChatGPT capabilities"""
        try:
            system_prompt = self.get_system_prompt(theme, 'quiz')
            
            prompt = f"""Lav 5 quiz-spørgsmål om hvad ChatGPT kan og ikke kan.
            
            Spørgsmålene skal:
            - Bruge {theme}-tema
            - Teste forståelse af AI's evner
            - Have klare rigtige/forkerte svar
            - Være sjove og engagerende
            
            Svar i JSON format:
            {{
                "questions": [
                    {{
                        "question": "Spørgsmål",
                        "options": ["A) svar", "B) svar"],
                        "correct": "A",
                        "explanation": "Forklaring"
                    }}
                ]
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.8
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('questions', [])
            
        except Exception as e:
            print(f"Capability quiz error: {e}")
            return [
                {
                    "question": "Kan ChatGPT hjælpe dig med lektier?",
                    "options": ["A) Ja, altid", "B) Ja, men du skal stadig tænke selv"],
                    "correct": "B",
                    "explanation": "ChatGPT kan hjælpe, men du skal lære selv!"
                }
            ]
    
    def evaluate_story_choices(self, choices: List[int], theme: str) -> Dict:
        """Evaluate choices made in interactive story"""
        try:
            # Simple evaluation - all choices are good for learning
            score = min(100, len(choices) * 25)
            
            feedback_messages = {
                'superhelte': [
                    "Fantastisk valg, superhelt! 🦸‍♂️",
                    "Du tænker som en ægte helt! 💪",
                    "Perfekt mission-strategi! ⚡"
                ],
                'prinsesse': [
                    "Magisk valg, prinsesse! ✨",
                    "Du har ægte eventyr-visdom! 👸",
                    "Som en sand fe-prinsesse! 🧚‍♀️"
                ]
            }
            
            messages = feedback_messages.get(theme, ["Godt valg!"])
            feedback = messages[min(len(choices) - 1, len(messages) - 1)]
            
            return {
                'score': score,
                'feedback': feedback,
                'learning_achieved': True
            }
            
        except Exception as e:
            print(f"Story evaluation error: {e}")
            return {
                'score': 75,
                'feedback': "Godt klaret! Du lærer hurtigt! 🌟",
                'learning_achieved': True
            }
    
    def evaluate_thinking_exercises(self, word_chain: List[str], comparison: str, theme: str) -> Dict:
        """Evaluate word chain and comparison exercises"""
        try:
            score = 0
            feedback_parts = []
            
            # Evaluate word chain
            if len(word_chain) >= 3:
                score += 50
                feedback_parts.append("Fantastisk ordkæde!")
            else:
                score += 25
                feedback_parts.append("God start på ordkæden!")
            
            # Evaluate comparison
            if len(comparison) > 20:
                score += 50
                feedback_parts.append("Rigtig god forklaring!")
            else:
                score += 25
                feedback_parts.append("Godt forsøg på forklaringen!")
            
            theme_encouragement = {
                'superhelte': " Du tænker som en superhelt! 🦸‍♂️",
                'prinsesse': " Du har magisk forståelse! ✨"
            }
            
            feedback = " ".join(feedback_parts) + theme_encouragement.get(theme, "")
            
            return {
                'score': score,
                'feedback': feedback,
                'word_chain_score': min(50, len(word_chain) * 15),
                'comparison_score': min(50, len(comparison))
            }
            
        except Exception as e:
            print(f"Thinking exercises error: {e}")
            return {
                'score': 60,
                'feedback': "Godt arbejde! Du forstår hvordan AI tænker! 🧠",
                'word_chain_score': 30,
                'comparison_score': 30
            }
    
    def evaluate_capability_understanding(self, card_answers: Dict, quiz_answers: List[str], theme: str) -> Dict:
        """Evaluate understanding of ChatGPT capabilities"""
        try:
            score = 0
            feedback_parts = []
            
            # Evaluate card sorting (simplified - assume some correct)
            correct_cards = len([k for k in card_answers.keys() if card_answers[k] == 'correct'])
            card_score = min(50, correct_cards * 10)
            score += card_score
            
            if card_score >= 40:
                feedback_parts.append("Perfekt forståelse af AI's evner!")
            else:
                feedback_parts.append("God forståelse af AI!")
            
            # Evaluate quiz answers
            correct_quiz = len([a for a in quiz_answers if a in ['A', 'B', 'C', 'D']])
            quiz_score = min(50, correct_quiz * 10)
            score += quiz_score
            
            if quiz_score >= 40:
                feedback_parts.append("Fantastiske quiz-svar!")
            else:
                feedback_parts.append("Gode quiz-svar!")
            
            theme_celebration = {
                'superhelte': " Du er nu en AI-superhelt! 🏆",
                'prinsesse': " Du har mestret AI-magien! 👑"
            }
            
            feedback = " ".join(feedback_parts) + theme_celebration.get(theme, "")
            
            return {
                'score': score,
                'feedback': feedback,
                'card_score': card_score,
                'quiz_score': quiz_score,
                'mastery_level': 'expert' if score >= 80 else 'good' if score >= 60 else 'learning'
            }
            
        except Exception as e:
            print(f"Capability evaluation error: {e}")
            return {
                'score': 70,
                'feedback': "Rigtig godt klaret! Du forstår AI! 🌟",
                'card_score': 35,
                'quiz_score': 35,
                'mastery_level': 'good'
            }
    
    def get_activity_1_hint(self, step_id: int, question: str, attempt_number: int, theme: str) -> str:
        """Get specific hints for Activity 1 steps"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            step_contexts = {
                1: "Dette er om den interaktive historie hvor barnet lærer om ChatGPT",
                2: "Dette er om hvordan ChatGPT tænker og forbinder ord",
                3: "Dette er om ChatGPT's superkræfter og begrænsninger"
            }
            
            hint_levels = {
                1: "Giv et lille, opmuntrende hint",
                2: "Giv et tydeligere hint der hjælper mere",
                3: "Giv næsten hele svaret men på en venlig måde"
            }
            
            context = step_contexts.get(step_id, "Dette er om at lære ChatGPT")
            level = min(attempt_number, 3)
            
            prompt = f"""{context}
            
            Barnet har brug for hjælp med: {question}
            Dette er deres {attempt_number}. forsøg.
            
            {hint_levels[level]}
            
            Vær opmuntrende og brug {theme}-tema."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Activity 1 hint error: {e}")
            theme_encouragement = {
                'superhelte': "Fortsæt kampen, superhelt! Du kan godt finde ud af det! 💪",
                'prinsesse': "Tro på din magi, prinsesse! Du klarer det! ✨"
            }
            return theme_encouragement.get(theme, "Du kan godt finde ud af det! Prøv igen! 🌟")


# Global instance
openai_service = OpenAIService()


    # ===== AKTIVITET 2 SPECIFIKKE METODER =====
    
    def generate_activity_2_intro(self, theme: str) -> Dict:
        """Generate personalized introduction for Activity 2"""
        try:
            system_prompt = self.get_system_prompt(theme, 'prompt_builder')
            
            prompt = f"""Lav en kort, spændende introduktion til Aktivitet 2: "Dit første prompt"
            
            Introduktionen skal:
            - Være på dansk og børnevenlig
            - Bruge {theme}-tema
            - Forklare at barnet skal lære at skrive prompts
            - Være motiverende og opmuntrende
            - Være max 100 ord
            
            Svar i JSON format:
            {{
                "welcome_message": "Velkomstbesked",
                "learning_goals": ["mål 1", "mål 2", "mål 3"],
                "motivation": "Motiverende besked om at skrive første prompt"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Activity 2 intro error: {e}")
            return {
                "welcome_message": "Nu skal du lære at skrive dine første prompts! 🚀",
                "learning_goals": ["Skriv dit første prompt", "Lær at være høflig", "Få svar fra AI"],
                "motivation": "Du bliver snart en prompt-mester!"
            }
    
    def generate_guided_prompt_builder(self, theme: str) -> Dict:
        """Generate guided prompt builder for Step 1"""
        try:
            system_prompt = self.get_system_prompt(theme, 'prompt_builder')
            
            prompt = f"""Lav en guidet prompt-builder til børn der skal skrive deres første prompt.
            
            Builderen skal:
            - Bruge {theme}-tema
            - Have 4-5 trin der bygger et prompt op
            - Give eksempler for hvert trin
            - Være simpel og forståelig
            - Slutte med et komplet prompt
            
            Svar i JSON format:
            {{
                "introduction": "Introduktion til prompt-building",
                "steps": [
                    {{
                        "id": 1,
                        "title": "Trin titel",
                        "instruction": "Hvad skal barnet gøre",
                        "example": "Eksempel på dette trin",
                        "placeholder": "Placeholder tekst"
                    }}
                ],
                "final_example": "Eksempel på færdigt prompt"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Guided prompt builder error: {e}")
            return {
                "introduction": "Lad os bygge dit første prompt sammen!",
                "steps": [
                    {
                        "id": 1,
                        "title": "Hvem skal AI være?",
                        "instruction": "Fortæl AI hvilken rolle den skal have",
                        "example": "Du er en venlig lærer",
                        "placeholder": "Du er en..."
                    }
                ],
                "final_example": "Du er en venlig lærer. Forklar mig om dinosaurer på en sjov måde."
            }
    
    def generate_politeness_training(self, theme: str) -> Dict:
        """Generate politeness training for Step 2"""
        try:
            system_prompt = self.get_system_prompt(theme, 'prompt_builder')
            
            prompt = f"""Lav en høflighedstræning til børn der skal lære at være høflige med AI.
            
            Træningen skal:
            - Bruge {theme}-tema
            - Vise forskellen på høflige og uhøflige prompts
            - Have eksempler på gode manerer
            - Være sjov og lærerig
            - Inkludere en lille quiz
            
            Svar i JSON format:
            {{
                "introduction": "Introduktion til høflighed",
                "good_examples": [
                    {{
                        "prompt": "Høfligt prompt",
                        "explanation": "Hvorfor det er godt"
                    }}
                ],
                "bad_examples": [
                    {{
                        "prompt": "Uhøfligt prompt",
                        "explanation": "Hvorfor det er dårligt",
                        "improved": "Forbedret version"
                    }}
                ],
                "quiz_questions": [
                    {{
                        "question": "Spørgsmål",
                        "options": ["A) svar", "B) svar"],
                        "correct": "A",
                        "explanation": "Forklaring"
                    }}
                ]
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Politeness training error: {e}")
            return {
                "introduction": "Lær at være høflig med AI!",
                "good_examples": [
                    {
                        "prompt": "Kan du venligst hjælpe mig?",
                        "explanation": "Bruger 'venligst' og spørger pænt"
                    }
                ],
                "bad_examples": [
                    {
                        "prompt": "Gør det nu!",
                        "explanation": "Lyder som en ordre",
                        "improved": "Kan du hjælpe mig med det?"
                    }
                ],
                "quiz_questions": []
            }
    
    def generate_personalized_prompt_exercise(self, theme: str) -> Dict:
        """Generate personalized exercise for Step 3"""
        try:
            system_prompt = self.get_system_prompt(theme, 'prompt_builder')
            
            prompt = f"""Lav en personaliseret prompt-øvelse baseret på {theme}-tema.
            
            Øvelsen skal:
            - Være specifik for {theme}-tema
            - Give barnet en konkret opgave
            - Have flere valgmuligheder for prompts
            - Være sjov og engagerende
            - Lære barnet at bruge deres interesser
            
            Svar i JSON format:
            {{
                "task_description": "Beskrivelse af opgaven",
                "scenario": "Scenarie barnet skal forestille sig",
                "prompt_suggestions": [
                    {{
                        "category": "Kategori",
                        "prompts": ["prompt 1", "prompt 2", "prompt 3"]
                    }}
                ],
                "success_criteria": "Hvad gør et prompt godt i denne øvelse"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.8
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Personalized exercise error: {e}")
            return {
                "task_description": "Skriv et prompt om dit yndlingstema",
                "scenario": "Forestil dig at du snakker med en ekspert",
                "prompt_suggestions": [
                    {
                        "category": "Spørgsmål",
                        "prompts": ["Fortæl mig om...", "Hvad er det bedste ved...?"]
                    }
                ],
                "success_criteria": "Et godt prompt er høfligt og specifikt"
            }
    
    def build_prompt_from_parts(self, prompt_parts: Dict, theme: str, step_id: int) -> str:
        """Build a complete prompt from user-provided parts"""
        try:
            # Extract parts
            role = prompt_parts.get('role', '')
            task = prompt_parts.get('task', '')
            context = prompt_parts.get('context', '')
            tone = prompt_parts.get('tone', '')
            
            # Build prompt based on step
            if step_id == 1:
                # Simple guided building
                parts = [p for p in [role, task, context] if p.strip()]
                return '. '.join(parts) + '.'
            
            # More advanced building for later steps
            built_prompt = ""
            if role:
                built_prompt += f"{role}. "
            if task:
                built_prompt += f"{task}"
            if context:
                built_prompt += f" {context}"
            if tone:
                built_prompt += f" Svar på en {tone} måde."
            
            return built_prompt.strip()
            
        except Exception as e:
            print(f"Build prompt error: {e}")
            return "Hjælp mig med at lære noget nyt."
    
    def get_prompt_preview(self, prompt: str, theme: str) -> str:
        """Get a preview of what AI would respond to this prompt"""
        try:
            system_prompt = self.get_system_prompt(theme, 'prompt_builder')
            
            # Generate a short preview response
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt + "\n\nGiv et kort preview-svar (max 50 ord)."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Prompt preview error: {e}")
            return "Det lyder som et godt spørgsmål! AI vil gerne hjælpe dig."
    
    def evaluate_prompt_quality(self, prompt: str) -> Dict:
        """Evaluate the quality of a beginner's prompt"""
        try:
            # Simple quality metrics for beginners
            score = 0
            feedback = []
            
            # Length check
            if 10 <= len(prompt) <= 200:
                score += 25
                feedback.append("God længde på promptet")
            elif len(prompt) < 10:
                feedback.append("Prøv at skrive lidt mere")
            else:
                feedback.append("Prøv at gøre det lidt kortere")
            
            # Politeness check
            polite_words = ['tak', 'venligst', 'kan du', 'vil du', 'hjælp']
            if any(word in prompt.lower() for word in polite_words):
                score += 25
                feedback.append("Godt at du er høflig!")
            
            # Question/task clarity
            if '?' in prompt or any(word in prompt.lower() for word in ['forklar', 'fortæl', 'hjælp', 'vis']):
                score += 25
                feedback.append("Klart hvad du vil have")
            
            # Complete sentence
            if prompt.strip().endswith('.') or prompt.strip().endswith('?'):
                score += 25
                feedback.append("Pæn afslutning på sætningen")
            
            return {
                'score': score,
                'max_score': 100,
                'feedback': feedback,
                'level': 'begynder' if score < 50 else 'god' if score < 80 else 'ekspert'
            }
            
        except Exception as e:
            print(f"Prompt quality error: {e}")
            return {
                'score': 50,
                'max_score': 100,
                'feedback': ["Godt forsøg!"],
                'level': 'begynder'
            }
    
    def get_prompt_improvement_suggestions(self, prompt: str, theme: str) -> List[str]:
        """Get suggestions for improving a prompt"""
        try:
            system_prompt = self.get_system_prompt(theme, 'prompt_builder')
            
            improvement_prompt = f"""Giv 2-3 konkrete forslag til at forbedre dette prompt fra et barn:
            "{prompt}"
            
            Forslagene skal:
            - Være børnevenlige og opmuntrende
            - Bruge {theme}-tema hvis relevant
            - Være konkrete og handlingsrettede
            
            Svar som en liste af strenge."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": improvement_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            # Parse response into list
            suggestions_text = response.choices[0].message.content
            suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip()]
            
            return suggestions[:3]  # Max 3 suggestions
            
        except Exception as e:
            print(f"Improvement suggestions error: {e}")
            return [
                "Prøv at være mere specifik",
                "Tilføj 'tak' eller 'venligst'",
                "Forklar hvad du gerne vil lære"
            ]
    
    def get_themed_ai_response(self, prompt: str, theme: str) -> str:
        """Get AI response with theme integration"""
        try:
            system_prompt = self.get_system_prompt(theme, 'chat')
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Themed AI response error: {e}")
            return "Det er et godt spørgsmål! Jeg vil gerne hjælpe dig med at lære mere."
    
    def evaluate_prompt_for_beginners(self, prompt: str, ai_response: str, theme: str) -> Dict:
        """Evaluate a beginner's prompt and the AI response"""
        try:
            quality = self.evaluate_prompt_quality(prompt)
            
            # Additional evaluation based on AI response
            response_quality = "god" if len(ai_response) > 50 else "kort"
            
            # Theme integration check
            theme_words = {
                'superhelte': ['superhelt', 'superkraft', 'helt', 'redde', 'mission'],
                'prinsesse': ['prinsesse', 'slot', 'eventyr', 'magi', 'fe']
            }
            
            theme_integrated = any(
                word in ai_response.lower() 
                for word in theme_words.get(theme, [])
            )
            
            return {
                'prompt_quality': quality,
                'response_quality': response_quality,
                'theme_integrated': theme_integrated,
                'overall_score': quality['score'],
                'encouragement': self._get_encouragement_message(quality['score'], theme)
            }
            
        except Exception as e:
            print(f"Beginner evaluation error: {e}")
            return {
                'prompt_quality': {'score': 50, 'feedback': ["Godt forsøg!"]},
                'response_quality': 'god',
                'theme_integrated': True,
                'overall_score': 50,
                'encouragement': "Du lærer hurtigt!"
            }
    
    def _get_encouragement_message(self, score: int, theme: str) -> str:
        """Get encouraging message based on score and theme"""
        messages = {
            'superhelte': {
                'high': "Du er en ægte prompt-superhelt! 🦸‍♂️",
                'medium': "Du er på vej til at blive en prompt-helt! 💪",
                'low': "Fortsæt træningen, superhelt! Du bliver bedre! ⚡"
            },
            'prinsesse': {
                'high': "Du mestrer prompt-magien perfekt! ✨",
                'medium': "Din prompt-magi bliver stærkere! 🌟",
                'low': "Fortsæt med at øve din magi! Du klarer det! 💫"
            }
        }
        
        level = 'high' if score >= 80 else 'medium' if score >= 50 else 'low'
        return messages.get(theme, {}).get(level, "Godt klaret!")
    
    def get_beginner_prompt_templates(self, theme: str) -> List[Dict]:
        """Get prompt templates for beginners"""
        try:
            templates = [
                {
                    'category': 'Spørgsmål',
                    'template': 'Kan du fortælle mig om [emne]?',
                    'example': 'Kan du fortælle mig om dinosaurer?',
                    'explanation': 'Brug dette til at lære om nye ting'
                },
                {
                    'category': 'Hjælp',
                    'template': 'Kan du hjælpe mig med at forstå [emne]?',
                    'example': 'Kan du hjælpe mig med at forstå matematik?',
                    'explanation': 'Brug dette når du har brug for hjælp'
                },
                {
                    'category': 'Kreativitet',
                    'template': 'Lav en historie om [emne]',
                    'example': 'Lav en historie om en modig prinsesse',
                    'explanation': 'Brug dette til sjove historier'
                }
            ]
            
            # Customize for theme
            if theme == 'superhelte':
                templates.append({
                    'category': 'Superhelte',
                    'template': 'Fortæl mig om [superhelt] og deres superkræfter',
                    'example': 'Fortæl mig om Spider-Man og hans superkræfter',
                    'explanation': 'Lær om dine yndlings-superhelte'
                })
            elif theme == 'prinsesse':
                templates.append({
                    'category': 'Eventyr',
                    'template': 'Fortæl mig et eventyr om [karakter]',
                    'example': 'Fortæl mig et eventyr om en modig prinsesse',
                    'explanation': 'Få magiske historier'
                })
            
            return templates
            
        except Exception as e:
            print(f"Templates error: {e}")
            return []
    
    def get_activity_2_hint(self, step_id: int, question: str, current_prompt: str, attempt_number: int, theme: str) -> str:
        """Get specific hints for Activity 2 steps"""
        try:
            system_prompt = self.get_system_prompt(theme, 'prompt_builder')
            
            step_contexts = {
                1: "Dette er om at bygge sit første prompt trin for trin",
                2: "Dette er om at lære høflighed når man skriver til AI",
                3: "Dette er om at lave personlige prompts baseret på interesser"
            }
            
            hint_levels = {
                1: "Giv et lille, hjælpsomt hint",
                2: "Giv et tydeligere hint med eksempel",
                3: "Giv næsten hele løsningen men på en venlig måde"
            }
            
            context = step_contexts.get(step_id, "Dette er om at skrive gode prompts")
            level = min(attempt_number, 3)
            
            hint_prompt = f"""{context}
            
            Barnet har brug for hjælp med: {question}
            Deres nuværende prompt: "{current_prompt}"
            Dette er deres {attempt_number}. forsøg.
            
            {hint_levels[level]}
            
            Vær opmuntrende og brug {theme}-tema."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": hint_prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Activity 2 hint error: {e}")
            theme_encouragement = {
                'superhelte': "Fortsæt træningen, superhelt! Prøv at tilføje mere detaljer! 💪",
                'prinsesse': "Din prompt-magi bliver stærkere! Prøv at være mere specifik! ✨"
            }
            return theme_encouragement.get(theme, "Du kan godt finde ud af det! Prøv igen! 🌟")
    
    def evaluate_guided_prompt(self, prompt_parts: Dict, final_prompt: str, theme: str) -> Dict:
        """Evaluate guided prompt building exercise"""
        try:
            score = 0
            feedback = []
            
            # Check if all parts are filled
            filled_parts = len([v for v in prompt_parts.values() if v and v.strip()])
            if filled_parts >= 3:
                score += 40
                feedback.append("Godt at du udfyldte alle dele!")
            
            # Evaluate final prompt
            prompt_quality = self.evaluate_prompt_quality(final_prompt)
            score += prompt_quality['score'] * 0.6  # 60% weight
            
            feedback.extend(prompt_quality['feedback'])
            
            return {
                'score': min(100, int(score)),
                'feedback': feedback,
                'prompt_parts_score': filled_parts * 10,
                'final_prompt_score': prompt_quality['score']
            }
            
        except Exception as e:
            print(f"Guided prompt evaluation error: {e}")
            return {
                'score': 60,
                'feedback': ["Godt forsøg på at bygge dit første prompt!"],
                'prompt_parts_score': 30,
                'final_prompt_score': 50
            }
    
    def evaluate_politeness_training(self, politeness_examples: List, politeness_quiz: List, theme: str) -> Dict:
        """Evaluate politeness training exercise"""
        try:
            score = 0
            feedback = []
            
            # Check examples
            if len(politeness_examples) >= 2:
                score += 50
                feedback.append("Godt at du lavede høflige eksempler!")
            
            # Check quiz answers (simplified)
            correct_quiz = len([a for a in politeness_quiz if a])
            score += min(50, correct_quiz * 10)
            
            if correct_quiz >= 3:
                feedback.append("Du forstår høflighed rigtig godt!")
            
            return {
                'score': min(100, score),
                'feedback': feedback,
                'examples_score': min(50, len(politeness_examples) * 25),
                'quiz_score': min(50, correct_quiz * 10)
            }
            
        except Exception as e:
            print(f"Politeness evaluation error: {e}")
            return {
                'score': 70,
                'feedback': ["Du lærer at være høflig med AI!"],
                'examples_score': 35,
                'quiz_score': 35
            }
    
    def evaluate_personalized_exercise(self, personal_prompt: str, ai_response: str, theme: str) -> Dict:
        """Evaluate personalized prompt exercise"""
        try:
            # Evaluate the personal prompt
            prompt_eval = self.evaluate_prompt_for_beginners(personal_prompt, ai_response, theme)
            
            # Additional points for personalization
            personal_score = 0
            feedback = []
            
            # Check if prompt is personal/specific
            personal_words = ['jeg', 'min', 'mit', 'mine', 'mig', 'vil gerne', 'interesserer']
            if any(word in personal_prompt.lower() for word in personal_words):
                personal_score += 30
                feedback.append("Godt at du gjorde det personligt!")
            
            # Check theme integration
            if prompt_eval['theme_integrated']:
                personal_score += 20
                feedback.append("Perfekt brug af dit tema!")
            
            total_score = prompt_eval['overall_score'] * 0.5 + personal_score
            
            return {
                'score': min(100, int(total_score)),
                'feedback': feedback + prompt_eval['prompt_quality']['feedback'],
                'personalization_score': personal_score,
                'prompt_quality_score': prompt_eval['overall_score'],
                'encouragement': prompt_eval['encouragement']
            }
            
        except Exception as e:
            print(f"Personalized evaluation error: {e}")
            return {
                'score': 75,
                'feedback': ["Godt personligt prompt!"],
                'personalization_score': 40,
                'prompt_quality_score': 60,
                'encouragement': "Du bliver bedre og bedre!"
            }

