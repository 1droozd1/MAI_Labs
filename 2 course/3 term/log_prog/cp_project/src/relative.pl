:- ['my_tree.pl'].

mother(X,Y) :-
    child(Y,X),
    female(X).

father(X,Y):-
    child(Y,X),
    male(X).

son(X,Y):-
    child(X,Y),
    male(X).

daughter(X,Y):-
    child(X,Y),
    female(X).

brother(X,Y):-
    child(X,Z),
    child(Y,Z),
    X\=Y,
    male(X).

sister(X,Y):-
    child(X,Z),
    child(Y,Z),
    X \= Y,
    female(X).


parent(X,Y):-
    child(Y,X).

wife(X,Y):-
    child(Z,X),
    child(Z,Y),
    X \= Y,
    female(X).

husband(X,Y):-
    child(Z,X),
    child(Z,Y),
    X \= Y,
    male(X).


check(husband,X,Y):- 
    husband(X,Y).

check(wife,X,Y):-
    wife(X,Y).

check(brother,X,Y):-
    brother(X,Y).

check(son,X,Y):-
    son(X,Y).

check(sister,X,Y):-
    sister(X,Y).

check(father,X,Y):-
    father(X,Y).

check(mother,X,Y):-
    mother(X,Y).

check(parent,X,Y):-
    parent(X,Y).

check(daughter,X,Y):-
    daughter(X,Y).

check(child,X,Y):-
    child(X,Y).

add(E,[],[E]).
add(E,[H|T],[H|T1]):-add(E,T,T1).

accordance([_],T,T).
accordance([First,Second|Tail],T,R):-
    check(Relation,First,Second),
    add(Relation,T,X),
    accordance([Second|Tail],X,R),!.

prolong([X|T],[Y,X|T]):-
    check(_,X,Y), 
    not(member(Y,[X|T])).

search_in_width(X,Y,P):-
    width([[X]],Y,L),
    reverse(L,P).

width([[Finish|T]|_],Finish,[Finish|T]).
width([Next|B],Finish,Ans):-
    findall(X,prolong(Next,X),T),
    append(B,T,Bn),
    width(Bn,Finish,Ans),!.
width([_|T],Finish,Ans):-
    width(T,Finish,Ans).

relative(X, Y, Z):-
    search_in_width(Y, Z, R),!,
    accordance(R,[] ,X).