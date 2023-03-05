my_remove(X,[X|T],T).
my_remove(X,[Y|T],[Y|T1]):- my_remove(X,T,T1).

agent_list(['Даша','Света','Саша','Коля','Катя','Маша']).
verb_list(['любит','хочет','кушает','лежат']).
obj_list(['деньги','шоколад','фильмы','книги','мандарины']).

an_verb('любит','любить').
an_verb('хочет','хотеть').
an_verb('кушает','кушать').
an_verb('лежат','лежать','лежит').

an_v([X],Y):- 
    verb_list(L),
    member(X,L),
    an_verb(X,Y).
    
    an_s1([X],object(X)):- 
    obj_list(L),
    member(X,L).
    
    an_s2([X],agent(X)):- 
    agent_list(L),
    member(X,L).    

an_q(L,(Y,X,Z)):-
member('Кто',L),
member('?',L),
my_remove('?',L,NewL),
my_remove('Кто',NewL,NewL2),
append(L1,L2,NewL2),
an_v(L1,Y),
an_s1(L2,Z),
X = agent('Y').

an_q(L,(Y,Z,X)):-
member('Что',L),
member('?',L),
my_remove('?',L,NewL),
my_remove('Что',NewL,NewL2),
append(L1,L2,NewL2),
an_v(L1,Y),
an_s2(L2,Z),
X = object('Y').

an_q(L,(Y,Z,X)):-
member('Где',L),
member('?',L),
my_remove('?',L,NewL),
my_remove('Где',NewL,NewL2),
append(L1,L2,NewL2),
an_v(L1,Y),
an_s1(L2,Z),
X = loc('Y').
