from src.models import UserPreferences
from src.validators import InputValidator


class InputParser:
    GENRE_MAPPING = {
        'евро': 'eurogame',
        'еврогейм': 'eurogame',
        'кооператив': 'cooperative',
        'кооперативные': 'cooperative',
        'партийные': 'party',
        'вечеринка': 'party',
        'партийка': 'party',
        'декбилдер': 'deck_builder',
        'абстрактные': 'abstract',
        'варгейм': 'wargame',
        'дедукция': 'social_deduction',
    }
    
    MECHANIC_MAPPING = {
        'рабочие': 'worker_placement',
        'размещение рабочих': 'worker_placement',
        'тайлы': 'tile_placement',
        'драфт': 'drafting',
        'колодостроение': 'deck_building',
        'кубики': 'dice_rolling',
        'контроль территории': 'area_control',
        'скрытые роли': 'hidden_roles',
        'управление рукой': 'hand_management',
        'ресурсы': 'resource_management',
    }
    
    COMPLEXITY_MAPPING = {
        'простые': 'light',
        'легкие': 'light',
        'средние': 'medium',
        'сложные': 'heavy',
        'тяжелые': 'heavy',
    }
    
    @staticmethod
    def parse_preferences(user_input: str) -> UserPreferences:
        if not user_input:
            return UserPreferences(set(), set(), None, None)
        
        user_input = InputValidator.sanitize_input(user_input)
        user_input_lower = user_input.lower()
        
        genres = set()
        for key, value in InputParser.GENRE_MAPPING.items():
            if key in user_input_lower:
                genres.add(value)
        
        mechanics = set()
        for key, value in InputParser.MECHANIC_MAPPING.items():
            if key in user_input_lower:
                mechanics.add(value)
        
        complexity = None
        for key, value in InputParser.COMPLEXITY_MAPPING.items():
            if key in user_input_lower:
                complexity = value
                break
        
        cooperative = None
        if 'кооператив' in user_input_lower or 'вместе' in user_input_lower:
            cooperative = True
        elif 'конкурент' in user_input_lower or 'против' in user_input_lower:
            cooperative = False
        
        return UserPreferences(genres, mechanics, complexity, cooperative)

