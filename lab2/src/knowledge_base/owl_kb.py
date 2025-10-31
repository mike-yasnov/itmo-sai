from typing import List, Dict
import xml.etree.ElementTree as ET

from .base import KnowledgeBase


class OWLKnowledgeBase(KnowledgeBase):
    def __init__(self, owl_file: str):
        try:
            self.tree = ET.parse(owl_file)
            self.root = self.tree.getroot()
        except ET.ParseError as e:
            raise ValueError(f"Ошибка парсинга OWL файла: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"OWL файл не найден: {owl_file}")
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки онтологии: {e}")
        
        self.ns = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'owl': 'http://www.w3.org/2002/07/owl#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'bg': 'http://example.org/boardgames#'
        }
        
        self._games = set()
        self._genres = set()
        self._mechanics = set()
        self._game_genres = {}
        self._game_mechanics = {}
        self._game_designers = {}
        
        self._parse_ontology()
    
    def _extract_name(self, uri: str) -> str:
        return uri.split('#')[-1] if '#' in uri else uri.split('/')[-1]
    
    def _parse_ontology(self):
        for individual in self.root.findall('.//owl:NamedIndividual', self.ns):
            about = individual.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
            if not about:
                continue
            
            name = self._extract_name(about)
            
            types = individual.findall('.//rdf:type', self.ns)
            for t in types:
                resource = t.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
                if resource:
                    type_name = self._extract_name(resource)
                    if type_name == 'Game':
                        self._games.add(name)
                    elif type_name == 'Genre':
                        self._genres.add(name)
                    elif type_name == 'Mechanic':
                        self._mechanics.add(name)
            
            if name in self._games:
                self._game_genres[name] = []
                self._game_mechanics[name] = []
                self._game_designers[name] = []
                
                for genre_elem in individual.findall('.//bg:hasGenre', self.ns):
                    genre_uri = genre_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
                    if genre_uri:
                        self._game_genres[name].append(self._extract_name(genre_uri))
                
                for mechanic_elem in individual.findall('.//bg:hasMechanic', self.ns):
                    mechanic_uri = mechanic_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
                    if mechanic_uri:
                        self._game_mechanics[name].append(self._extract_name(mechanic_uri))
                
                for designer_elem in individual.findall('.//bg:designedBy', self.ns):
                    designer_uri = designer_elem.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource')
                    if designer_uri:
                        self._game_designers[name].append(self._extract_name(designer_uri))
    
    def query_games_by_genre(self, genre: str) -> List[str]:
        return [game for game, genres in self._game_genres.items() if genre in genres]
    
    def query_games_by_mechanic(self, mechanic: str) -> List[str]:
        return [game for game, mechanics in self._game_mechanics.items() if mechanic in mechanics]
    
    def query_games_by_complexity(self, complexity: str) -> List[str]:
        results = []
        for game in self._games:
            comp = self._calculate_complexity(game)
            if comp == complexity:
                results.append(game)
        return results
    
    def _calculate_complexity(self, game: str) -> str:
        mechanics = self._game_mechanics.get(game, [])
        genres = self._game_genres.get(game, [])
        
        if 'worker_placement' in mechanics or 'area_control' in mechanics:
            return 'heavy'
        if 'party' in genres:
            return 'light'
        return 'medium'
    
    def query_cooperative_games(self) -> List[str]:
        results = []
        for game in self._games:
            genres = self._game_genres.get(game, [])
            mechanics = self._game_mechanics.get(game, [])
            if 'cooperative' in genres or 'hidden_roles' in mechanics:
                results.append(game)
        return results
    
    def query_gateway_games(self) -> List[str]:
        results = []
        for game in self._games:
            mechanics = self._game_mechanics.get(game, [])
            if ('tile_placement' in mechanics or 'set_collection' in mechanics) and \
               'area_control' not in mechanics:
                results.append(game)
        return results
    
    def query_deep_strategy_games(self) -> List[str]:
        results = []
        for game in self._games:
            mechanics = self._game_mechanics.get(game, [])
            if ('worker_placement' in mechanics or 'area_control' in mechanics) and \
               'dice_rolling' not in mechanics:
                results.append(game)
        return results
    
    def get_game_info(self, game: str) -> Dict[str, any]:
        return {
            'name': game,
            'genres': self._game_genres.get(game, []),
            'mechanics': self._game_mechanics.get(game, []),
            'complexity': self._calculate_complexity(game)
        }

