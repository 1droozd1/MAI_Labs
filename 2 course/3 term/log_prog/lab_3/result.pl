exception('Коза', 'Волк').
exception('Волк', 'Коза').
exception('Коза', 'Капуста').
exception('Капуста', 'Коза').

add(E, [], [E]).
add(E, [H|T], [H|T1]) :- add(E, T, T1).

printRes([]).
printRes([A|T]) :- printRes(T), write(A), nl.

check([Item1, Item2]) :- exception(Item1, Item2).

move(s([Item1, Item2, Item3], 'L', []), s([Item1, Item2], 'R', [Item3])) :- not(check([Item1, Item2])).
move(s([Item1, Item2, Item3], 'L', []), s([Item1, Item3], 'R', [Item2])) :- not(check([Item1, Item3])).
move(s([Item1, Item2, Item3], 'L', []), s([Item2, Item3], 'R', [Item1])) :- not(check([Item2, Item3])).

move(s([Left|T], 'R', Right), s([Left|T], 'L', Right)) :- not(check(Right)).
move(s(Left, 'R', [Item1, Item2]), s(Out, 'L', [Item2])) :- check([Item1, Item2]), add(Item1, Left, Out).

move(s([L|LT], 'L', [R|RT]), s(LT, 'R', Out)) :- add(L, [R|RT], Out).
move(s([X, L|LT], 'L', [R|RT]), s([X|LT], 'R', Out)) :- add(L, [R|RT], Out).

prolong([In|InT], [Out, In|InT]) :- move(In, Out), not(member(Out, [In|InT])).

int(1).
int(X) :- int(Y), X is Y + 1.

dpth([X|T], X, [X|T]).
dpth(P, F, L) :- prolong(P, P1), dpth(P1, F, L).

deapth_search(A, B) :-
    write('deapth_search START'), nl,
    get_time(Time1),
    dpth([A], B, L),
    printRes(L),
    get_time(Time2),
    write('deapth_search END'), nl, nl,
    Time is Time1 - Time2,
    write('TIME IS '), write(T1), nl, nl.

bdth([[B|T]|_], B, [B|T]).
bdth([H|QT], X, R) :-
    findall(Z, prolong(H, Z), T),
    append(QT, T, OutQ), !,
    bdth(OutQ, X, R).
bdth([_|T], X, R) :- bdth(T, X, R).

bdth_search(X, Y) :-
    write('bdth_search START'), nl,
    get_time(Time1),
    bdth([[X]], Y, L),
    printRes(L),
    get_time(Time2),
    write('bdth_search END'), nl, nl,
    Time is Time1 - Time2,
    write('TIME IS '), write(T1), nl, nl.

depthId([Finish|T], Finish, [Finish|T], 0).
depthId(Path, Finish, R, N) :-
    N > 0,
    prolong(Path, NewPath),
    N1 is N - 1,
    depthId(NewPath, Finish, R, N1).

iter_search(Start, Finish) :-
    write('iter_search START'), nl,
    get_time(Time1),
    int(DepthLimit),
    depthId([Start], Finish, Res, DepthLimit),
    printRes(Res),
    get_time(Time2),
    write('iter_search END'), nl, nl,
    Time is Time1 - Time2,
    write('TIME IS '), write(T1), nl, nl.
iter_search(Start, Finish, Path) :- int(Level), iter_search(Start, Finish, Path, Level).