ПРИМЕРЫ ЗАПРОСОВ PROLOG
1) Простые факты:
```
game(root).
```

2) С переменными:
```
has_genre(G, eurogame).
```

3) С логическими операторами И/ИЛИ/НЕ:
```
(has_genre(G, eurogame) ; has_genre(G, deck_builder)), has_mechanic(G, deck_building).

game(G), \+ has_mechanic(G, hidden_roles).
```

4) Запросы, требующие правил:
```
euro_worker_placement(G).

deck_builder_game(G).

cooperative_or_hidden_teamplay(G).

gateway_game(G).

deep_strategy(G).

complexity(dixit, C).

modern_classic(G).
```

-------

ПРИМЕРЫ ЗАПРОСОВ PROTEGE
	
1.	Простые факты:
```
Game and {root}
```

2.	С «переменными» (подбираем подходящие игры):
```
Game and (hasGenre value eurogame)
```

3.	С логическими операторами И/ИЛИ/НЕ:

```
Game and ( (hasGenre value eurogame) or (hasGenre value deck_builder) ) and (hasMechanic value deck_building)
```

4.	Запросы, требующие «правил» (эквивалентных классов):

```
EuroWorkerPlacement

DeckBuilderGame

CooperativeOrHiddenTeamplay

{dixit} and (hasGenre value party)
{dixit} and ( (hasMechanic value worker_placement) or (hasMechanic value area_control) )
```