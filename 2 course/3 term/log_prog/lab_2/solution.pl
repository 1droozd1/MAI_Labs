prof('mechanic').
prof('chemist').
prof('builder').
prof('radioman').

best_chess(Win, Lose).
better_ski(Better, Worse).
younger(Young, Old).
more_theatre(More, Less).


solve([Borisov, Kirillov, Danin, Savin]):-
    
    prof(P1),
    Borisov = prof(P1),
    
    prof(P2),
    P2 @< P1,
    Kirillov = prof(P2),

    prof(P3),
    P3 @< P1, P3 @< P2,
    Danin = prof(P3),

    prof(P4),
    P4 @< P3, P4 @< P2, P4 @< P1,
    Savin = prof(P4),

    best_chess(Borisov, Danin),
    best_chess(Savin, Borisov),
    better_ski(Borisov, X),
    younger(X, Borisov),
    more_theatre(Borisov, Y),
    younger(Kirillov, Y),
    more_theatre(prof('chemist'), prof('mechanic')),
    more_theatre(prof('builder'), prof('chemist')),
    younger(prof('chemist'), _), younger(_, prof('chemist')),
    better_ski(prof('radioman'), prof('builder')),
    best_chess(prof('mechanic'), prof('builder')),
    best_chess(younger(_, (prof('chemist'); prof('mechanic'); prof('builder'); prof('radioman'))), _),
    more_theatre(younger(_, prof('chemist'); prof('mechanic'); prof('builder'); prof('radioman')), _),
    better_ski(younger(prof('chemist'); prof('mechanic'); prof('builder'); prof('radioman'), _), _).