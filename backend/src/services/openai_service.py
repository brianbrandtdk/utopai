import os
import json
from typing import Dict, List, Optional
from openai import OpenAI

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    def get_system_prompt(self, theme: str, activity_type: str) -> str:
        """Get system prompt based on theme and activity type"""
        base_prompt = "Du er en venlig AI-assistent der hjælper børn på 9-12 år med at lære om AI og prompting."
        
        theme_prompts = {
            'superhelte': "Du bruger superhelte-tema i dine svar. Brug ord som 'superkræfter', 'mission', 'helt', og 'redde verden'. Vær inspirerende og modig i din tone.",
            'prinsesse': "Du bruger prinsesse-tema i dine svar. Brug ord som 'magi', 'eventyr', 'slot', og 'fe'. Vær elegant og magisk i din tone."
        }
        
        activity_prompts = {
            'intro': "Du forklarer koncepter på en simpel og engagerende måde.",
            'quiz': "Du stiller spørgsmål og giver konstruktiv feedback.",
            'chat': "Du har en naturlig samtale og svarer på spørgsmål.",
            'prompt_builder': "Du hjælper med at bygge og forbedre prompts."
        }
        
        return f"{base_prompt} {theme_prompts.get(theme, '')} {activity_prompts.get(activity_type, '')}"
    
    def generate_activity_1_intro(self, theme: str) -> Dict:
        """Generate personalized introduction for Activity 1"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav en kort, spændende introduktion til Aktivitet 1: "Hvad er ChatGPT?"
            
            Introduktionen skal:
            - Være på dansk og børnevenlig
            - Bruge {theme}-tema
            - Forklare hvad ChatGPT er på en simpel måde
            - Være motiverende og opmuntrende
            - Være max 100 ord
            
            Svar i JSON format:
            {{
                "welcome_message": "Velkomstbesked",
                "explanation": "Simpel forklaring af ChatGPT",
                "motivation": "Motiverende besked om at lære AI"
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
                "explanation": "ChatGPT er en smart computer der kan snakke med dig og hjælpe dig med at lære!",
                "motivation": "Du skal blive en rigtig AI-ekspert!"
            }
    
    def generate_ai_thinking_explanation(self, theme: str) -> Dict:
        """Generate explanation of how AI 'thinks'"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Forklar hvordan AI "tænker" til børn på 9-12 år.
            
            Forklaringen skal:
            - Bruge {theme}-tema
            - Være simpel og forståelig
            - Bruge analogier børn kan forstå
            - Inkludere et sjovt eksempel
            - Være max 150 ord
            
            Svar i JSON format:
            {{
                "explanation": "Hovedforklaring",
                "analogy": "Analogi børn kan forstå",
                "example": "Konkret eksempel",
                "fun_fact": "Sjov fakta"
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
            print(f"AI thinking error: {e}")
            return {
                "explanation": "AI tænker ved at kigge på mønstre i tekst, ligesom du lærer at genkende ord!",
                "analogy": "Det er som at have en kæmpe bog med alle svar - AI finder det rigtige svar hurtigt!",
                "example": "Når du spørger om katte, finder AI alle ting den ved om katte og giver dig det bedste svar.",
                "fun_fact": "AI kan læse tusindvis af bøger på få sekunder!"
            }
    
    def generate_word_chain_game(self, theme: str) -> Dict:
        """Generate word chain game for Activity 1"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav et ordkæde-spil til børn om AI og {theme}-tema.
            
            Spillet skal:
            - Have 5-7 ord der hænger sammen
            - Starte med "AI" eller "ChatGPT"
            - Bruge {theme}-tema
            - Være lærerigt og sjovt
            - Have en forklaring af sammenhængen
            
            Svar i JSON format:
            {{
                "word_chain": ["ord1", "ord2", "ord3", "ord4", "ord5"],
                "explanation": "Forklaring af hvordan ordene hænger sammen",
                "learning_point": "Hvad lærer børn af dette spil"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Word chain error: {e}")
            return {
                "word_chain": ["AI", "Computer", "Hjælper", "Læring", "Sjovt"],
                "explanation": "AI er en computer der hjælper os med læring, og det er sjovt!",
                "learning_point": "AI er en teknologi der kan hjælpe os på mange måder."
            }
    
    def generate_ai_powers_and_limits(self, theme: str) -> Dict:
        """Generate AI powers and limitations explanation"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav en forklaring af AI's "superkræfter" og begrænsninger til børn.
            
            Forklaringen skal:
            - Bruge {theme}-tema
            - Liste 3-4 ting AI er god til
            - Liste 3-4 ting AI ikke kan
            - Være balanceret og ærlig
            - Være børnevenlig
            
            Svar i JSON format:
            {{
                "powers": [
                    {{
                        "title": "Superkraft titel",
                        "description": "Hvad AI kan gøre",
                        "example": "Konkret eksempel"
                    }}
                ],
                "limitations": [
                    {{
                        "title": "Begrænsning titel", 
                        "description": "Hvad AI ikke kan",
                        "why": "Hvorfor ikke"
                    }}
                ],
                "conclusion": "Afsluttende besked om AI"
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
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Powers and limits error: {e}")
            return {
                "powers": [
                    {
                        "title": "Hurtig læring",
                        "description": "AI kan læse mange bøger meget hurtigt",
                        "example": "Kan svare på spørgsmål om historie på få sekunder"
                    }
                ],
                "limitations": [
                    {
                        "title": "Kan ikke føle",
                        "description": "AI har ikke følelser som mennesker",
                        "why": "AI er en computer, ikke et levende væsen"
                    }
                ],
                "conclusion": "AI er et fantastisk værktøj, men mennesker er stadig vigtige!"
            }
    
    def generate_quiz_question(self, theme: str, topic: str, difficulty: int = 1) -> Dict:
        """Generate quiz question for Activity 1"""
        try:
            system_prompt = self.get_system_prompt(theme, 'quiz')
            
            prompt = f"""Lav et quiz-spørgsmål om {topic} til børn på 9-12 år.
            
            Spørgsmålet skal:
            - Bruge {theme}-tema
            - Have sværhedsgrad {difficulty} (1=let, 2=medium, 3=svær)
            - Have 3-4 svarmuligheder
            - Have en forklaring af det rigtige svar
            - Være lærerigt og engagerende
            
            Svar i JSON format:
            {{
                "question": "Spørgsmål",
                "options": ["A) svar", "B) svar", "C) svar"],
                "correct_answer": "A",
                "explanation": "Forklaring af hvorfor svaret er rigtigt",
                "fun_fact": "Sjov ekstra fakta"
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
            print(f"Quiz question error: {e}")
            return {
                "question": "Hvad er ChatGPT?",
                "options": ["A) En robot", "B) En AI-assistent", "C) Et spil"],
                "correct_answer": "B",
                "explanation": "ChatGPT er en AI-assistent der kan hjælpe med at svare på spørgsmål!",
                "fun_fact": "ChatGPT kan snakke på mange forskellige sprog!"
            }
    
    def evaluate_activity_1_answer(self, user_answer: str, correct_answer: str, theme: str) -> Dict:
        """Evaluate user's answer in Activity 1"""
        try:
            is_correct = user_answer.upper() == correct_answer.upper()
            
            if is_correct:
                encouragement = {
                    'superhelte': "Fantastisk arbejde, superhelt! Du reddede dagen! 🦸‍♂️",
                    'prinsesse': "Perfekt, prinsesse! Din visdom skinner! ✨"
                }
                return {
                    'correct': True,
                    'message': encouragement.get(theme, "Rigtig godt klaret! 🎉"),
                    'points_earned': 25
                }
            else:
                hint = {
                    'superhelte': "Hver superhelt fejler nogle gange. Prøv igen, helt! 💪",
                    'prinsesse': "Selv de klogeste prinsesser lærer ved at prøve igen! 🌟"
                }
                return {
                    'correct': False,
                    'message': hint.get(theme, "Ikke helt rigtigt. Prøv igen! 🤔"),
                    'points_earned': 0
                }
                
        except Exception as e:
            print(f"Activity 1 evaluation error: {e}")
            return {
                'correct': False,
                'message': "Der skete en fejl. Prøv igen!",
                'points_earned': 0
            }
    
    def get_activity_1_hint(self, question_topic: str, theme: str, attempt_number: int) -> str:
        """Get progressive hints for Activity 1"""
        try:
            if attempt_number == 1:
                return "Tænk over hvad vi lige har lært om AI..."
            elif attempt_number == 2:
                return "Kig på spørgsmålet igen - hvad er nøgleordet?"
            else:
                return "Du er tæt på! Læs alle svarmulighederne en gang til."
                
        except Exception as e:
            print(f"Activity 1 hint error: {e}")
            theme_encouragement = {
                'superhelte': "Fortsæt kampen, superhelt! Du kan godt finde ud af det! 💪",
                'prinsesse': "Tro på din magi, prinsesse! Du klarer det! ✨"
            }
            return theme_encouragement.get(theme, "Du kan godt finde ud af det! Prøv igen! 🌟")


# Global instance
openai_service = OpenAIService()

