from abc import ABC, abstractmethod
from typing import List, Dict


class KnowledgeBase(ABC):
    @abstractmethod
    def query_games_by_genre(self, genre: str) -> List[str]:
        pass
    
    @abstractmethod
    def query_games_by_mechanic(self, mechanic: str) -> List[str]:
        pass
    
    @abstractmethod
    def query_games_by_complexity(self, complexity: str) -> List[str]:
        pass
    
    @abstractmethod
    def query_cooperative_games(self) -> List[str]:
        pass
    
    @abstractmethod
    def query_gateway_games(self) -> List[str]:
        pass
    
    @abstractmethod
    def query_deep_strategy_games(self) -> List[str]:
        pass
    
    @abstractmethod
    def get_game_info(self, game: str) -> Dict[str, any]:
        pass

