% Лабораторная работа 1: Создание базы знаний и выполнение запросов в Prolog
% Тема: Настольные игры

% ФАКТЫ С ОДНИМ АРГУМЕНТОМ 
% Настольные игры 
game(catan).
game(carcassonne).
game(pandemic).
game(ticket_to_ride).
game(dominion).
game(seven_wonders).
game(terraforming_mars).
game(gloomhaven).
game(chess).
game(go).
game(splendor).
game(coup).
game(dixit).
game(azul).
game(agricola).
game(battlestar_galactica).
game(root).
game(scythe).
game(wingspan).
game(love_letter).

% Жанры
genre(eurogame).
genre(ameritrash).
genre(abstract).
genre(cooperative).
genre(deck_builder).
genre(party).
genre(wargame).
genre(engine_builder).
genre(set_collection).
genre(social_deduction).

% Механики
mechanic(worker_placement).
mechanic(tile_placement).
mechanic(drafting).
mechanic(deck_building).
mechanic(dice_rolling).
mechanic(area_control).
mechanic(hidden_roles).
mechanic(hand_management).
mechanic(resource_management).
mechanic(tableau_building).
mechanic(set_collection).
mechanic(route_building).

% Известные авторы 
designer(klaus_teuber).
designer(antoine_bauza).
designer(matt_leacock).
designer(elizabeth_hargrave).
designer(uwe_rosenberg).
designer(vlaada_chvatil).
designer(corey_konieczka).
designer(jamey_stegmaier).

% ФАКТЫ С ДВУМЯ АРГУМЕНТАМИ
% Игра относится к жанру
has_genre(catan, eurogame).
has_genre(carcassonne, eurogame).
has_genre(pandemic, cooperative).
has_genre(dominion, deck_builder).
has_genre(seven_wonders, eurogame).
has_genre(agricola, eurogame).
has_genre(dixit, party).

% У игры есть механика
has_mechanic(agricola, worker_placement).
has_mechanic(carcassonne, tile_placement).
has_mechanic(dominion, deck_building).
has_mechanic(root, area_control).
has_mechanic(coup, hidden_roles).

% Автор игры
designer_of(catan, klaus_teuber).
designer_of(wingspan, elizabeth_hargrave).
designer_of(pandemic, matt_leacock).

% ПРАВИЛА
% 1) Евро + размещение рабочих
euro_worker_placement(Game) :-
    has_genre(Game, eurogame),
    has_mechanic(Game, worker_placement).

% 2) Декбилдинг: либо жанр deck_builder, либо механика deck_building
deck_builder_game(Game) :-
    has_genre(Game, deck_builder) ;
    has_mechanic(Game, deck_building).

% 3) Кооператив или скрытые роли (социальная дедукция)
cooperative_or_hidden_teamplay(Game) :-
    has_genre(Game, cooperative) ;
    has_mechanic(Game, hidden_roles).

% 4) Пороговый "входной" (gateway) — простые механики без area control
gateway_game(Game) :-
    (has_mechanic(Game, tile_placement) ; has_mechanic(Game, set_collection)),
    \+ has_mechanic(Game, area_control).

% 5) Глубокая стратегия без «случайности кубов»
deep_strategy(Game) :-
    (has_mechanic(Game, worker_placement) ; has_mechanic(Game, area_control)),
    \+ has_mechanic(Game, dice_rolling).

% 6) Классификация сложности с отсечками (!)
% Приоритеты: heavy > light > medium
complexity(Game, heavy) :- has_mechanic(Game, worker_placement), !.
complexity(Game, heavy) :- has_mechanic(Game, area_control), !.
complexity(Game, light) :- has_genre(Game, party), !.
complexity(_Game, medium).

% 7) «Современная классика» — от известных авторов
modern_classic(Game) :-
    designer_of(Game, klaus_teuber) ;
    designer_of(Game, matt_leacock).

