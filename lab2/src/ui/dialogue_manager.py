from typing import List
from src.engine import RecommendationEngine
from src.parsers import InputParser
from src.validators import InputValidator


class DialogueManager:
    def __init__(self, recommendation_engine: RecommendationEngine):
        self.engine = recommendation_engine
        self.preferences = None
    
    def start_dialogue(self):
        print("Система рекомендаций настольных игр".center(60))
        print()
        
        initial_input = self._ask_initial_preferences()
        self.preferences = InputParser.parse_preferences(initial_input)
        
        self._refine_preferences()
        
        recommendations = self.engine.get_recommendations(self.preferences)
        
        if not recommendations:
            print("К сожалению, не найдено игр по вашим критериям.")
            self._suggest_alternatives()
            return
        
        self._display_recommendations(recommendations)
    
    def _ask_initial_preferences(self) -> str:
        print("Расскажите о своих предпочтениях:")
        print("Например: 'Мне нравятся кооперативные игры и евро'")
        print("или: 'Хочу простые партийные игры'")
        print()
        
        max_attempts = 3
        for attempt in range(max_attempts):
            user_input = input("Ваши предпочтения: ").strip()
            
            is_valid, error_msg = InputValidator.validate_user_input(user_input)
            
            if not is_valid:
                print(f"{error_msg}")
                if attempt < max_attempts - 1:
                    print("Попробуйте еще раз:\n")
                continue
            
            sanitized = InputValidator.sanitize_input(user_input)
            
            if not InputValidator.has_meaningful_content(sanitized):
                print("Пожалуйста, опишите свои предпочтения подробнее")
                if attempt < max_attempts - 1:
                    print("Попробуйте еще раз:\n")
                continue
            
            return sanitized
        
        print("Превышено количество попыток. Используем значения по умолчанию.")
        return "хочу популярные игры"
    
    def _refine_preferences(self):
        print("\nДавайте уточним ваши предпочтения...")
        print()
        
        if not self.preferences.complexity:
            print("Какую сложность игры вы предпочитаете?")
            print("1. Легкие игры")
            print("2. Средней сложности")
            print("3. Сложные игры")
            print("4. Не важно")
            
            is_valid, error_msg, choice_num = InputValidator.validate_choice(
                input("Выберите (1-4): "), 1, 4
            )
            
            if not is_valid:
                print(f"{error_msg}, пропускаем...")
            elif choice_num and choice_num <= 3:
                complexity_map = {1: 'light', 2: 'medium', 3: 'heavy'}
                self.preferences.complexity = complexity_map[choice_num]
        
        if self.preferences.cooperative is None:
            print("\nВы предпочитаете:")
            print("1. Кооперативные игры (играть вместе)")
            print("2. Конкурентные игры (играть друг против друга)")
            print("3. Не важно")
            
            is_valid, error_msg, choice_num = InputValidator.validate_choice(
                input("Выберите (1-3): "), 1, 3
            )
            
            if not is_valid:
                print(f"{error_msg}, пропускаем...")
            elif choice_num == 1:
                self.preferences.cooperative = True
            elif choice_num == 2:
                self.preferences.cooperative = False
        
        if not self.preferences.genres and not self.preferences.mechanics:
            print("\nВыберите жанр:")
            print("1. Евро (стратегия и ресурсы)")
            print("2. Партийные игры")
            print("3. Кооперативные")
            print("4. Декбилдеры")
            
            is_valid, error_msg, choice_num = InputValidator.validate_choice(
                input("Выберите (1-4): "), 1, 4
            )
            
            if not is_valid:
                print(f"{error_msg}, используем популярные игры...")
                self.preferences.genres.add('eurogame')
            elif choice_num:
                genre_map = {1: 'eurogame', 2: 'party', 3: 'cooperative', 4: 'deck_builder'}
                self.preferences.genres.add(genre_map[choice_num])
    
    def _display_recommendations(self, games: List[str]):
        ranked = self.engine.rank_recommendations(games, self.preferences)
        
        print("Рекомендованные игры".center(60))
        print()
        
        for i, (game, score, info) in enumerate(ranked[:5], 1):
            print(f"{i}. {game.upper()}")
            
            if info['genres']:
                genres_ru = ', '.join(info['genres'])
                print(f"   Жанры: {genres_ru}")
            
            if info['mechanics']:
                mechanics_ru = ', '.join(info['mechanics'])
                print(f"   Механики: {mechanics_ru}")
            
            if info['complexity']:
                print(f"   Сложность: {info['complexity']}")
            
            print(f"   Соответствие: {'★' * min(int(score), 5)}")
            print()
    
    def _suggest_alternatives(self):
        print("\nПопробуйте изменить критерии поиска или посмотрите популярные игры:")
        
        gateway = self.engine.kb.query_gateway_games()
        if gateway:
            print("\nПопулярные входные игры:")
            for game in gateway[:3]:
                print(f"  • {game}")

