from typing import List
from src.knowledge_base import KnowledgeBase
from src.models import UserPreferences


class RecommendationEngine:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
    
    def get_recommendations(self, preferences: UserPreferences) -> List[str]:
        candidates = set()
        
        for genre in preferences.genres:
            games = self.kb.query_games_by_genre(genre)
            candidates.update(games)
        
        for mechanic in preferences.mechanics:
            games = self.kb.query_games_by_mechanic(mechanic)
            candidates.update(games)
        
        if preferences.cooperative:
            coop_games = self.kb.query_cooperative_games()
            if candidates:
                candidates.intersection_update(coop_games)
            else:
                candidates.update(coop_games)
        
        if preferences.complexity:
            complex_games = self.kb.query_games_by_complexity(preferences.complexity)
            if candidates:
                candidates.intersection_update(complex_games)
            else:
                candidates.update(complex_games)
        
        if not candidates:
            gateway = self.kb.query_gateway_games()
            candidates.update(gateway[:3])
        
        return list(candidates)
    
    def rank_recommendations(self, games: List[str], preferences: UserPreferences) -> List[tuple]:
        ranked = []
        
        for game in games:
            info = self.kb.get_game_info(game)
            score = 0
            
            genre_matches = len(set(info['genres']) & preferences.genres)
            mechanic_matches = len(set(info['mechanics']) & preferences.mechanics)
            
            score += genre_matches * 2
            score += mechanic_matches * 1.5
            
            if preferences.complexity and info['complexity'] == preferences.complexity:
                score += 1
            
            ranked.append((game, score, info))
        
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked

