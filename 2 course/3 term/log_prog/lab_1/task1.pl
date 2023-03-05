length_([], 0).
length_([_|A], N) :- length_(A, N1), N is N1 + 1.

member(A, [A|_]). 
member(A, [_|B]) :- member(A, B).

append([], List2, List2).
append([H|T], List2, [H|TR]) :- append(T, List2, TR).

remove([], _Elem, []).
remove([Elem|T], Elem, TR) :- remove(T, Elem, TR), !.
remove([H|T], Elem, [H|TR]) :- remove(T, Elem, TR).

permute([],[]).
permute(L,[X|T]) :- remove(L,X,R), permute(R,T).

sub_start([], _List).
sub_start([H|TSub], [H|TList]) :- sub_start(TSub, TList).
sublist(Sub, List) :- sub_start(Sub, List), !.
sublist(Sub, [_H|T]) :- sublist(Sub, T).

%Вариант 9: Получение N-го элемента списка
find(0,[Result|_],Result):-!.
find(Number,[_|Tail],Result):-N is Number-1,find(N,Tail,Result).

%С использованием стандартных предикатов:
/* ?- nth0(1,[1, 2, 3],Elem).
Elem = 2.
?- nth0(0,[1, 2, 3],Elem).
Elem = 1.*/

%task 1.2
/*?- geom([1,3,9,27]).
true.

?- geom([1,3,9,17]).
false.

?- geom([1,2,4,8,16,32]).
true.*/


pregeom([F],N):-number(F),!.
pregeom([F,S|Tail],N):-number(F),number(S),S =:= F*N,pregeom([S|Tail],N).
geom([F]):-number(F),!.
geom([F,S|Tail]):-number(F),number(S),N is S/F,pregeom([S|Tail],N).

%Пример совместного использования:
%вывод возможных перестановок, если список - геометрическая прогресиия
test(List,R):-
    geom(List),
    permutation(List,R). 
