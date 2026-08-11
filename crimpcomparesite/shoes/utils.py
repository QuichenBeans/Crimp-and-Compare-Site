from django.conf import settings
from openai import OpenAI
import logging
import json

logger = logging.getLogger(__name__)

class DeepSeekClimbingShoeClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = OpenAI(
                api_key="sk-fea5789c50e04243894c26ec46a5115d", # Replace with env data
                base_url="https://api.deepseek.com"
            )
        return cls._instance
    
    def get_recommendation(self, quiz_data):
        """Generate shoe recommendations from quiz answers"""
        
        prompt = self._build_prompt(quiz_data)
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an expert climbing shoe consultant. Give specific, practical advice with real shoe models. Use markdown formatting with emojis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=1500
        )
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return {"error": True, "raw": response.choices[0].message.content}
    
    def _build_prompt(self, data):
        return f"""
            You are an expert climbing shoe consultant.
            
            A climber completed a quiz:
            - Level: {data.get('level')}
            - Primary Climbing: {data.get('climbing_type')}
            - Foot Shape: {data.get('foot_shape')}
            - Budget: {data.get('budget')}
            - Priority: {data.get('priority')}
            
            IMPORTANT: Return ONLY valid JSON. Do NOT include any other text.
            
            Use this EXACT structure:
            
            {{
                "top_pick": {{
                    "brand": "La Sportiva",
                    "model": "Solution"
                }},
                "alternatives": [
                    {{
                        "brand": "Scarpa",
                        "model": "Instinct VS"
                    }},
                    {{
                        "brand": "Tenaya",
                        "model": "Oasi"
                }}
                ],
                "pro_tips": [
                    "Break in new shoes gradually",
                    "Try before you buy if possible"
                ]
            }}
            
            Rules:
            - Return ONLY valid JSON, no markdown, no explanation
            - Use real brands and models that exist
            - Match brand names exactly to: La Sportiva, Scarpa, Tenaya, Butora, Evolv, Mad Rock, Ocun, Unparallel
            - For beginners, recommend beginner-friendly shoes (Tarantula, Finale, Drifter, Defy)
            - For advanced/experts, recommend aggressive shoes (Solution, Instinct, Oasi, Shaman)
            - Don't add prices or URLs - your code will handle that
        """
    