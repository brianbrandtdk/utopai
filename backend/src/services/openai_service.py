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

    # ===== ACTIVITY 2 METHODS =====
    
    def generate_activity_2_intro(self, theme: str) -> Dict:
        """Generate personalized introduction for Activity 2: Dit første prompt"""
        try:
            system_prompt = self.get_system_prompt(theme, 'intro')
            
            prompt = f"""Lav en kort, spændende introduktion til Aktivitet 2: "Dit første prompt"
            
            Introduktionen skal:
            - Være på dansk og børnevenlig
            - Bruge {theme}-tema
            - Forklare hvad prompts er på en simpel måde
            - Være motiverende og opmuntrende
            - Være max 100 ord
            
            Svar i JSON format:
            {{
                "welcome_message": "Velkomstbesked",
                "explanation": "Simpel forklaring af prompts",
                "motivation": "Motiverende besked om at lære prompting"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Activity 2 intro error: {e}")
            return {
                "welcome_message": f"Velkommen til din første prompt-mission, {theme}!",
                "explanation": "En prompt er en besked du sender til AI for at få svar.",
                "motivation": "Lad os lære at skrive fantastiske prompts sammen!"
            }

    def generate_guided_prompt_builder(self, theme: str) -> Dict:
        """Generate guided prompt builder content for step 1"""
        try:
            system_prompt = self.get_system_prompt(theme, 'prompt_builder')
            
            prompt = f"""Lav indhold til guidet prompt-builder for børn med {theme}-tema.
            
            Indholdet skal inkludere:
            - 4 prompt-dele: rolle, opgave, kontekst, tone
            - Eksempler for hver del
            - Vejledning til at kombinere delene
            
            Svar i JSON format:
            {{
                "title": "Byg din første prompt",
                "instruction": "Vejledning",
                "prompt_parts": {{
                    "role": {{
                        "label": "Hvem skal AI være?",
                        "examples": ["eksempel1", "eksempel2"],
                        "placeholder": "Skriv en rolle..."
                    }},
                    "task": {{
                        "label": "Hvad skal AI gøre?",
                        "examples": ["eksempel1", "eksempel2"],
                        "placeholder": "Skriv en opgave..."
                    }},
                    "context": {{
                        "label": "Hvad skal AI vide?",
                        "examples": ["eksempel1", "eksempel2"],
                        "placeholder": "Giv kontekst..."
                    }},
                    "tone": {{
                        "label": "Hvordan skal AI svare?",
                        "examples": ["eksempel1", "eksempel2"],
                        "placeholder": "Vælg en tone..."
                    }}
                }}
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Guided prompt builder error: {e}")
            return {
                "title": "Byg din første prompt",
                "instruction": "Lad os bygge en prompt sammen!",
                "prompt_parts": {
                    "role": {
                        "label": "Hvem skal AI være?",
                        "examples": ["En venlig lærer", "En hjælpsom guide"],
                        "placeholder": "Skriv en rolle..."
                    },
                    "task": {
                        "label": "Hvad skal AI gøre?",
                        "examples": ["Forklar noget", "Hjælp med opgave"],
                        "placeholder": "Skriv en opgave..."
                    },
                    "context": {
                        "label": "Hvad skal AI vide?",
                        "examples": ["Jeg er 10 år", "Det er til skole"],
                        "placeholder": "Giv kontekst..."
                    },
                    "tone": {
                        "label": "Hvordan skal AI svare?",
                        "examples": ["Venligt", "Enkelt"],
                        "placeholder": "Vælg en tone..."
                    }
                }
            }

    def generate_politeness_training(self, theme: str) -> Dict:
        """Generate politeness training content for step 2"""
        try:
            system_prompt = self.get_system_prompt(theme, 'quiz')
            
            prompt = f"""Lav høflighedstræning for børn med {theme}-tema.
            
            Indholdet skal inkludere:
            - Gode vs dårlige prompt-eksempler
            - Quiz om høflighed
            - Tips til bedre prompts
            
            Svar i JSON format:
            {{
                "title": "Lær at være høflig mod AI",
                "good_examples": [
                    {{"prompt": "god prompt", "explanation": "hvorfor den er god"}},
                    {{"prompt": "god prompt", "explanation": "hvorfor den er god"}}
                ],
                "bad_examples": [
                    {{"prompt": "dårlig prompt", "explanation": "hvorfor den er dårlig"}},
                    {{"prompt": "dårlig prompt", "explanation": "hvorfor den er dårlig"}}
                ],
                "quiz": [
                    {{"question": "spørgsmål", "options": ["A", "B", "C"], "correct": 0, "explanation": "forklaring"}}
                ],
                "tips": ["tip1", "tip2", "tip3"]
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Politeness training error: {e}")
            return {
                "title": "Lær at være høflig mod AI",
                "good_examples": [
                    {"prompt": "Kan du venligst hjælpe mig?", "explanation": "Høflig og venlig tone"},
                    {"prompt": "Jeg vil gerne lære om...", "explanation": "Klar og respektfuld"}
                ],
                "bad_examples": [
                    {"prompt": "Gør det nu!", "explanation": "For kommanderende"},
                    {"prompt": "Du skal...", "explanation": "Ikke høflig nok"}
                ],
                "quiz": [
                    {"question": "Hvilken prompt er mest høflig?", "options": ["Gør det!", "Kan du hjælpe?", "Du skal svare"], "correct": 1, "explanation": "Høflige ord som 'kan du' er bedre"}
                ],
                "tips": ["Brug 'tak' og 'venligst'", "Vær klar og specifik", "Vær respektfuld"]
            }

    def generate_personalized_prompt_exercise(self, theme: str) -> Dict:
        """Generate personalized prompt exercise for step 3"""
        try:
            system_prompt = self.get_system_prompt(theme, 'prompt_builder')
            
            prompt = f"""Lav personaliseret prompt-øvelse for børn med {theme}-tema.
            
            Indholdet skal inkludere:
            - Prompt-forslag baseret på tema
            - Øvelser til at skrive egne prompts
            - Evaluering af prompt-kvalitet
            
            Svar i JSON format:
            {{
                "title": "Din personlige prompt-øvelse",
                "prompt_suggestions": [
                    {{"category": "kategori", "prompts": ["forslag1", "forslag2"]}},
                    {{"category": "kategori", "prompts": ["forslag1", "forslag2"]}}
                ],
                "exercises": [
                    {{"instruction": "øvelse beskrivelse", "example": "eksempel"}},
                    {{"instruction": "øvelse beskrivelse", "example": "eksempel"}}
                ],
                "evaluation_criteria": ["kriterium1", "kriterium2", "kriterium3"]
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Personalized exercise error: {e}")
            return {
                "title": "Din personlige prompt-øvelse",
                "prompt_suggestions": [
                    {"category": "Kreative historier", "prompts": ["Fortæl en historie om...", "Opfind en karakter der..."]},
                    {"category": "Læringshjælp", "prompts": ["Forklar hvordan...", "Hjælp mig med at forstå..."]}
                ],
                "exercises": [
                    {"instruction": "Skriv en prompt om dit yndlingsemne", "example": "Fortæl mig om dinosaurer på en sjov måde"},
                    {"instruction": "Lav en prompt der beder om hjælp", "example": "Kan du hjælpe mig med matematik?"}
                ],
                "evaluation_criteria": ["Er den høflig?", "Er den klar?", "Er den specifik?"]
            }

    def build_prompt_from_parts(self, prompt_parts: Dict, theme: str, step_id: int) -> str:
        """Build a complete prompt from individual parts"""
        try:
            role = prompt_parts.get('role', '')
            task = prompt_parts.get('task', '')
            context = prompt_parts.get('context', '')
            tone = prompt_parts.get('tone', '')
            
            # Build prompt with proper structure
            prompt_elements = []
            
            if role:
                prompt_elements.append(f"Du er {role}.")
            if task:
                prompt_elements.append(f"Jeg vil gerne have dig til at {task}.")
            if context:
                prompt_elements.append(f"Kontekst: {context}.")
            if tone:
                prompt_elements.append(f"Svar venligst på en {tone} måde.")
            
            return " ".join(prompt_elements)
            
        except Exception as e:
            print(f"Build prompt error: {e}")
            return "Hej! Kan du hjælpe mig?"

    def get_prompt_preview(self, prompt: str, theme: str) -> str:
        """Get a preview of what AI would respond to the prompt"""
        try:
            # Simulate AI response to show user what their prompt would generate
            system_prompt = self.get_system_prompt(theme, 'chat')
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Prompt preview error: {e}")
            return "Hej! Tak for din besked. Jeg vil gerne hjælpe dig!"

    def evaluate_prompt_quality(self, prompt: str) -> Dict:
        """Evaluate the quality of a prompt for beginners"""
        try:
            score = 0
            feedback = []
            
            # Basic quality checks
            if len(prompt) > 10:
                score += 2
                feedback.append("God længde på prompt")
            else:
                feedback.append("Prøv at skrive lidt mere")
            
            if any(word in prompt.lower() for word in ['tak', 'venligst', 'kan du']):
                score += 2
                feedback.append("Høflig tone")
            else:
                feedback.append("Prøv at være mere høflig")
            
            if '?' in prompt:
                score += 1
                feedback.append("Godt spørgsmål")
            
            # Convert to 1-10 scale
            quality_score = min(10, max(1, (score / 5) * 10))
            
            return {
                'score': quality_score,
                'feedback': feedback,
                'level': 'begynder' if quality_score < 7 else 'god'
            }
            
        except Exception as e:
            print(f"Prompt quality error: {e}")
            return {'score': 5, 'feedback': ['Prøv igen!'], 'level': 'begynder'}

    def get_prompt_improvement_suggestions(self, prompt: str, theme: str) -> List[str]:
        """Get suggestions for improving a prompt"""
        try:
            suggestions = []
            
            if len(prompt) < 10:
                suggestions.append("Skriv lidt mere detaljer")
            
            if not any(word in prompt.lower() for word in ['tak', 'venligst', 'kan du']):
                suggestions.append("Prøv at være mere høflig")
            
            if '?' not in prompt:
                suggestions.append("Stil et klart spørgsmål")
            
            if not suggestions:
                suggestions.append("Din prompt ser god ud!")
            
            return suggestions
            
        except Exception as e:
            print(f"Improvement suggestions error: {e}")
            return ["Fortsæt det gode arbejde!"]

    def moderate_content(self, content: str) -> bool:
        """Check if content is appropriate for children"""
        try:
            # Basic content moderation
            inappropriate_words = ['dårlig', 'dum', 'strid']  # Add more as needed
            
            content_lower = content.lower()
            for word in inappropriate_words:
                if word in content_lower:
                    return False
            
            return True
            
        except Exception as e:
            print(f"Content moderation error: {e}")
            return True  # Default to allowing content if error

    def get_themed_ai_response(self, prompt: str, theme: str) -> str:
        """Get AI response with theme applied"""
        try:
            system_prompt = self.get_system_prompt(theme, 'chat')
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Themed AI response error: {e}")
            return "Tak for din besked! Jeg vil gerne hjælpe dig."

    def evaluate_prompt_for_beginners(self, prompt: str, ai_response: str, theme: str) -> Dict:
        """Evaluate a prompt specifically for beginner level"""
        try:
            score = 0
            feedback = []
            
            # Beginner-friendly evaluation
            if len(prompt) >= 5:
                score += 3
                feedback.append("God længde")
            
            if any(word in prompt.lower() for word in ['hjælp', 'kan', 'vil']):
                score += 2
                feedback.append("Klar intention")
            
            if len(ai_response) > 20:
                score += 2
                feedback.append("AI gav et godt svar")
            
            # Theme encouragement
            theme_feedback = {
                'superhelte': "Fantastisk arbejde, superhelt! 💪",
                'prinsesse': "Magisk prompt, prinsesse! ✨"
            }
            
            feedback.append(theme_feedback.get(theme, "Godt arbejde!"))
            
            return {
                'score': min(10, score),
                'feedback': feedback,
                'encouragement': theme_feedback.get(theme, "Fortsæt det gode arbejde!"),
                'next_steps': ["Prøv at stille flere spørgsmål", "Vær endnu mere specifik"]
            }
            
        except Exception as e:
            print(f"Beginner evaluation error: {e}")
            return {
                'score': 5,
                'feedback': ["Godt forsøg!"],
                'encouragement': "Fortsæt med at øve dig!",
                'next_steps': ["Prøv igen"]
            }

    def evaluate_guided_prompt(self, prompt_parts: Dict, final_prompt: str, theme: str) -> Dict:
        """Evaluate guided prompt building exercise"""
        try:
            score = 0
            feedback = []
            
            # Check if all parts are filled
            parts_filled = sum(1 for part in prompt_parts.values() if part.strip())
            score += parts_filled * 2
            
            if parts_filled >= 3:
                feedback.append("Du udfyldte de fleste dele!")
            
            # Check final prompt quality
            quality = self.evaluate_prompt_quality(final_prompt)
            score += quality['score'] // 2
            
            feedback.extend(quality['feedback'])
            
            return {
                'score': min(10, score),
                'feedback': feedback,
                'parts_score': parts_filled,
                'quality_score': quality['score']
            }
            
        except Exception as e:
            print(f"Guided prompt evaluation error: {e}")
            return {'score': 5, 'feedback': ["Godt forsøg!"], 'parts_score': 0, 'quality_score': 5}

    def evaluate_politeness_training(self, examples: List, quiz: List, theme: str) -> Dict:
        """Evaluate politeness training exercise"""
        try:
            score = 0
            feedback = []
            
            # Check quiz answers
            correct_answers = sum(1 for answer in quiz if answer.get('correct', False))
            score += correct_answers * 3
            
            if correct_answers > len(quiz) // 2:
                feedback.append("Du forstår høflighed godt!")
            else:
                feedback.append("Øv dig mere i høflighed")
            
            # Check example understanding
            if len(examples) > 0:
                score += 2
                feedback.append("Du arbejdede med eksemplerne")
            
            return {
                'score': min(10, score),
                'feedback': feedback,
                'quiz_score': correct_answers,
                'total_questions': len(quiz)
            }
            
        except Exception as e:
            print(f"Politeness evaluation error: {e}")
            return {'score': 5, 'feedback': ["Godt forsøg!"], 'quiz_score': 0, 'total_questions': 0}

    def evaluate_personalized_exercise(self, personal_prompt: str, ai_response: str, theme: str) -> Dict:
        """Evaluate personalized prompt exercise"""
        try:
            score = 0
            feedback = []
            
            # Evaluate personal prompt
            quality = self.evaluate_prompt_quality(personal_prompt)
            score += quality['score']
            feedback.extend(quality['feedback'])
            
            # Check if they got a good AI response
            if len(ai_response) > 30:
                score += 3
                feedback.append("AI gav et detaljeret svar!")
            
            # Theme-specific encouragement
            theme_bonus = {
                'superhelte': "Du brugte dine prompt-superkræfter godt! 💪",
                'prinsesse': "Din prompt-magi virkede perfekt! ✨"
            }
            
            feedback.append(theme_bonus.get(theme, "Fantastisk arbejde!"))
            
            return {
                'score': min(10, score),
                'feedback': feedback,
                'prompt_quality': quality['score'],
                'response_quality': len(ai_response) // 10
            }
            
        except Exception as e:
            print(f"Personalized evaluation error: {e}")
            return {'score': 5, 'feedback': ["Godt forsøg!"], 'prompt_quality': 5, 'response_quality': 3}

    def get_activity_2_hint(self, step_id: int, question: str, current_prompt: str, attempt_number: int, theme: str) -> str:
        """Get progressive hints for Activity 2"""
        try:
            hints = {
                1: {  # Guided prompt building
                    1: "Prøv at udfylde alle fire dele af prompten",
                    2: "Husk at være høflig og specifik",
                    3: "Kombiner delene til en sammenhængende besked"
                },
                2: {  # Politeness training
                    1: "Tænk på hvordan du taler med dine venner",
                    2: "Ord som 'tak' og 'venligst' hjælper",
                    3: "Sammenlign de gode og dårlige eksempler"
                },
                3: {  # Personalized exercise
                    1: "Skriv om noget du interesserer dig for",
                    2: "Stil et klart spørgsmål til AI",
                    3: "Husk at være høflig og specifik"
                }
            }
            
            step_hints = hints.get(step_id, {})
            hint = step_hints.get(attempt_number, "Du klarer det! Prøv igen!")
            
            # Add theme-specific encouragement
            theme_encouragement = {
                'superhelte': f"{hint} Brug dine superkræfter! 💪",
                'prinsesse': f"{hint} Din magi vil hjælpe dig! ✨"
            }
            
            return theme_encouragement.get(theme, hint)
            
        except Exception as e:
            print(f"Activity 2 hint error: {e}")
            return "Fortsæt det gode arbejde!"

    def get_beginner_prompt_templates(self, theme: str) -> List[Dict]:
        """Get prompt templates for beginners"""
        try:
            templates = [
                {
                    'category': 'Spørgsmål',
                    'template': 'Kan du forklare {emne} på en simpel måde?',
                    'example': 'Kan du forklare hvordan regnbuer opstår på en simpel måde?'
                },
                {
                    'category': 'Hjælp',
                    'template': 'Jeg har brug for hjælp til {opgave}. Kan du guide mig?',
                    'example': 'Jeg har brug for hjælp til matematik. Kan du guide mig?'
                },
                {
                    'category': 'Kreativt',
                    'template': 'Fortæl mig en historie om {emne}',
                    'example': 'Fortæl mig en historie om en modig mus'
                }
            ]
            
            # Add theme-specific templates
            if theme == 'superhelte':
                templates.append({
                    'category': 'Superhelte',
                    'template': 'Fortæl om en superhelt der {handling}',
                    'example': 'Fortæl om en superhelt der redder dyr'
                })
            elif theme == 'prinsesse':
                templates.append({
                    'category': 'Prinsesse',
                    'template': 'Fortæl om en prinsesse der {handling}',
                    'example': 'Fortæl om en prinsesse der lærer magi'
                })
            
            return templates
            
        except Exception as e:
            print(f"Template error: {e}")
            return [
                {
                    'category': 'Basis',
                    'template': 'Kan du hjælpe mig med {emne}?',
                    'example': 'Kan du hjælpe mig med at lære?'
                }
            ]


# Global instance
openai_service = OpenAIService()

