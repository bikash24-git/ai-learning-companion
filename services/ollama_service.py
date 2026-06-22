"""
Service for interacting with local Ollama LLM.
"""
import requests
import json
from typing import Optional
import re


class OllamaService:
    """Handles communication with local Ollama instance."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2"):
        """
        Initialize Ollama service.
        
        Args:
            base_url: Base URL of Ollama instance
            model: Default model to use
        """
        self.base_url = base_url
        self.model = model
    
    def check_connection(self) -> bool:
        """
        Check if Ollama is running and accessible.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            return False
    
    def get_available_models(self) -> list:
        """
        Get list of available models.
        
        Returns:
            List of available model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'].split(':')[0] for model in data.get('models', [])]
                return list(set(models))
            return []
        except Exception as e:
            return []
    
    def generate_text(self, prompt: str, model: Optional[str] = None, temperature: float = 0.7) -> str:
        """
        Generate text using Ollama.
        
        Args:
            prompt: Prompt for the model
            model: Model to use (defaults to self.model)
            temperature: Temperature for generation
            
        Returns:
            Generated text
            
        Raises:
            Exception: If generation fails
        """
        if model is None:
            model = self.model
        
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                raise Exception(f"API returned status code {response.status_code}")
        
        except requests.Timeout:
            raise Exception("Request timeout - model generation took too long")
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")
    
    def generate_summary(self, text: str, summary_type: str = "short") -> str:
        """
        Generate a summary of the provided text.
        
        Args:
            text: Text to summarize
            summary_type: Type of summary ('short', 'detailed', 'bullet')
            
        Returns:
            Generated summary
        """
        if summary_type == "short":
            prompt = f"Provide a concise summary (2-3 sentences) of the following text:\n\n{text}"
        elif summary_type == "detailed":
            prompt = f"Provide a detailed summary (5-7 sentences) of the following text, maintaining all important details:\n\n{text}"
        elif summary_type == "bullet":
            prompt = f"Summarize the following text in bullet points (5-10 key points):\n\n{text}"
        else:
            prompt = f"Summarize the following text:\n\n{text}"
        
        return self.generate_text(prompt)
    
    def generate_flashcards(self, text: str, num_cards: int = 10) -> list:
        """
        Generate flashcards from the provided text.
        
        Args:
            text: Text to generate flashcards from
            num_cards: Number of flashcards to generate
            
        Returns:
            List of dictionaries with 'question' and 'answer' keys
        """
        prompt = f"""Generate {num_cards} flashcards from the following text.
        
Format each flashcard exactly like this:
Question: [question text]
Answer: [answer text]

Text:
{text}

Generate flashcards now:"""
        
        response = self.generate_text(prompt)
        
        flashcards = []
        cards = response.split('\n\n')
        
        for card in cards:
            lines = card.strip().split('\n')
            question = None
            answer = None
            
            for line in lines:
                if line.startswith('Question:'):
                    question = line.replace('Question:', '').strip()
                elif line.startswith('Answer:'):
                    answer = line.replace('Answer:', '').strip()
            
            if question and answer:
                flashcards.append({
                    'question': question,
                    'answer': answer
                })
        
        return flashcards[:num_cards]
    
    def generate_mcqs(self, text: str, num_questions: int = 10) -> list:
        """
        Generate multiple choice questions from the provided text.
        
        Args:
            text: Text to generate MCQs from
            num_questions: Number of MCQs to generate
            
        Returns:
            List of dictionaries with question details
        """
        prompt = f"""Generate {num_questions} multiple choice questions from the following text.

Format each question exactly like this:
Question: [question text]
A) [option A]
B) [option B]
C) [option C]
D) [option D]
Answer: [A/B/C/D]

Text:
{text}

Generate MCQs now:"""
        
        response = self.generate_text(prompt)
        
        mcqs = []
        questions_text = response.split('\n\n')
        
        for q_text in questions_text:
            lines = q_text.strip().split('\n')
            question = None
            options = {'A': '', 'B': '', 'C': '', 'D': ''}
            answer = None
            
            for line in lines:
                if line.startswith('Question:'):
                    question = line.replace('Question:', '').strip()
                elif line.startswith('A)'):
                    options['A'] = line.replace('A)', '').strip()
                elif line.startswith('B)'):
                    options['B'] = line.replace('B)', '').strip()
                elif line.startswith('C)'):
                    options['C'] = line.replace('C)', '').strip()
                elif line.startswith('D)'):
                    options['D'] = line.replace('D)', '').strip()
                elif line.startswith('Answer:'):
                    answer = line.replace('Answer:', '').strip().upper()
            
            if question and all(options.values()) and answer:
                mcqs.append({
                    'question': question,
                    'option_a': options['A'],
                    'option_b': options['B'],
                    'option_c': options['C'],
                    'option_d': options['D'],
                    'correct_answer': answer
                })
        
        return mcqs[:num_questions]
    
    def generate_important_questions(self, text: str) -> dict:
        """
        Generate important questions for exam preparation.
        
        Args:
            text: Text to generate questions from
            
        Returns:
            Dictionary with 'short_answer', 'long_answer', and 'exam_focused' lists
        """
        # Short Answer Questions
        short_prompt = f"""Generate 5 short answer questions (2-4 words answer expected) from the text:

{text}

Format:
Question: [question]
Answer: [answer]

Generate now:"""
        
        # Long Answer Questions
        long_prompt = f"""Generate 5 long answer questions (paragraph answer expected) from the text:

{text}

Format:
Question: [question]
Answer: [answer]

Generate now:"""
        
        # Exam-Focused Questions
        exam_prompt = f"""Generate 5 exam-focused important questions from the text:

{text}

Format:
Question: [question]
Answer: [answer]

Generate now:"""
        
        short_response = self.generate_text(short_prompt)
        long_response = self.generate_text(long_prompt)
        exam_response = self.generate_text(exam_prompt)
        
        def parse_questions(response):
            questions = []
            items = response.split('\n\n')
            for item in items:
                lines = item.strip().split('\n')
                question = None
                answer = None
                for line in lines:
                    if line.startswith('Question:'):
                        question = line.replace('Question:', '').strip()
                    elif line.startswith('Answer:'):
                        answer = line.replace('Answer:', '').strip()
                if question and answer:
                    questions.append({'question': question, 'answer': answer})
            return questions
        
        return {
            'short_answer': parse_questions(short_response),
            'long_answer': parse_questions(long_response),
            'exam_focused': parse_questions(exam_response)
        }
