from typing import Optional, List
import re


class ValidationError(Exception):
    pass


class InputValidator:
    MIN_LENGTH = 3
    MAX_LENGTH = 500
    
    ALLOWED_CHARS = re.compile(r'^[а-яА-ЯёЁa-zA-Z0-9\s,.:;!?\-]+$')
    
    @staticmethod
    def validate_user_input(text: str) -> tuple[bool, Optional[str]]:
        if not text or not text.strip():
            return False, "Введите непустую строку"
        
        text = text.strip()
        
        if len(text) < InputValidator.MIN_LENGTH:
            return False, f"Слишком короткий ввод (минимум {InputValidator.MIN_LENGTH} символа)"
        
        if len(text) > InputValidator.MAX_LENGTH:
            return False, f"Слишком длинный ввод (максимум {InputValidator.MAX_LENGTH} символов)"
        
        if not InputValidator.ALLOWED_CHARS.match(text):
            return False, "Ввод содержит недопустимые символы"
        
        return True, None
    
    @staticmethod
    def validate_choice(choice: str, min_val: int, max_val: int) -> tuple[bool, Optional[str], Optional[int]]:
        if not choice or not choice.strip():
            return False, "Выбор не может быть пустым", None
        
        choice = choice.strip()
        
        if not choice.isdigit():
            return False, "Введите число", None
        
        choice_num = int(choice)
        
        if choice_num < min_val or choice_num > max_val:
            return False, f"Выберите число от {min_val} до {max_val}", None
        
        return True, None, choice_num
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        if not text:
            return ""
        
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        text = text[:InputValidator.MAX_LENGTH]
        
        return text
    
    @staticmethod
    def has_meaningful_content(text: str) -> bool:
        words = text.split()
        return len(words) >= 2
    
    @staticmethod
    def get_validation_hints() -> List[str]:
        return [
            f"Длина текста: от {InputValidator.MIN_LENGTH} до {InputValidator.MAX_LENGTH} символов",
            "Используйте русские или латинские буквы",
            "Допустимы пробелы и знаки препинания",
            "Избегайте специальных символов"
        ]

