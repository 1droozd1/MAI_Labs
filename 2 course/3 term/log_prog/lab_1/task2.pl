:- set_prolog_flag(encoding, utf8).
:- ['three.pl'].
print_list([]). 
print_list([H|T]) :-
    write(H),
    write('\n'),
    print_list(T).

append1([], List2, List2). 
append1([Head|Tail], List2, [Head|TailResult]):-
   append1(Tail, List2, TailResult).

group_grades_list(Num, L) :- 
    findall(X, student(Num, _, [grade('LP',X),grade('MTH',_),grade('FP',_),grade('INF',_),grade('ENG',_),grade('PSY',_)]), LP),
    findall(X, student(Num, _, [grade('LP',_),grade('MTH',X),grade('FP',_),grade('INF',_),grade('ENG',_),grade('PSY',_)]), MTH),
    findall(X, student(Num, _, [grade('LP',_),grade('MTH',_),grade('FP',X),grade('INF',_),grade('ENG',_),grade('PSY',_)]), FP),
    findall(X, student(Num, _, [grade('LP',_),grade('MTH',_),grade('FP',_),grade('INF',X),grade('ENG',_),grade('PSY',_)]), INF),
    findall(X, student(Num, _, [grade('LP',_),grade('MTH',_),grade('FP',_),grade('INF',_),grade('ENG',X),grade('PSY',_)]), ENG),
    findall(X, student(Num, _, [grade('LP',_),grade('MTH',_),grade('FP',_),grade('INF',_),grade('ENG',_),grade('PSY',X)]), PSY),
    append1(LP, MTH, A),
    append1(FP, INF, B),
    append1(ENG, PSY, C),
    append1(A, B, D),
    append1(C, D, L).

sum_list([],0). 
sum_list([H|T], S) :-
	sum_list(T, S1), 
	S is H + S1.

group_grades_sum(Num, Sum) :- 
    group_grades_list(Num, L),
    sum_list(L, Sum).

group_grades_av(Num, Av) :- 
    group_grades_sum(Num, Sum),
    group_grades_list(Num, L),
    length(L, Le),
    Av is Sum / Le.

all_groups_grades_av() :- 
    write("Средние оценки 101 группы: "),
    group_grades_av(101, A),
    write(A),
    write('\n'),
    write("Средние оценки 102 группы: "),
    group_grades_av(102, B),
    write(B),
    write('\n'),
    write("Средние оценки 103 группы: "),
    group_grades_av(103, C),
    write(C),
    write('\n'),
    write("Средние оценки 104 группы: "),
    group_grades_av(104, D),
    write(D),
    write('\n').

group_list(Num, L) :- 
    findall(X, student(Num, X, _), L). 

group_table() :- 
    write("\nГруппа 101:\n"),
    group_list(101, A),
    print_list(A),
    write("\nГруппа 102:\n"),
    group_list(102, B),
    print_list(B),
    write("\nГруппа 103:\n"),
    group_list(103, C),
    print_list(C),
    write("\nГруппа 104:\n"),
    group_list(104, D),
    print_list(D),
    write('\n').

task1() :- 
    group_table(),
    all_groups_grades_av().

lp_grade2_list(L) :- 
    findall(X, student(_, X, [grade('LP',2),grade('MTH',_),grade('FP',_),grade('INF',_),grade('ENG',_),grade('PSY',_)]), L).

mth_grade2_list(L) :-
    findall(X, student(_, X, [grade('LP',_),grade('MTH',2),grade('FP',_),grade('INF',_),grade('ENG',_),grade('PSY',_)]), L).

fp_grade2_list(L) :-
    findall(X, student(_, X, [grade('LP',_),grade('MTH',_),grade('FP',2),grade('INF',_),grade('ENG',_),grade('PSY',_)]), L).

inf_grade2_list(L) :-
    findall(X, student(_, X, [grade('LP',_),grade('MTH',_),grade('FP',_),grade('INF',2),grade('ENG',_),grade('PSY',_)]), L).

eng_grade2_list(L) :-
    findall(X, student(_, X, [grade('LP',_),grade('MTH',_),grade('FP',_),grade('INF',_),grade('ENG',2),grade('PSY',_)]), L).

psy_grade2_list(L) :-
    findall(X, student(_, X, [grade('LP',_),grade('MTH',_),grade('FP',_),grade('INF',_),grade('ENG',_),grade('PSY',2)]), L).

task2() :- 
    write("\nСтуденты, которые не сдали -логическое программирование- :\n"),
    lp_grade2_list(A),
    print_list(A),
    write("\nСтуденты, которые не сдали -математический анализ- :\n"),
    mth_grade2_list(B),
    print_list(B),
    write("\nСтуденты, которые не сдали -функциональное программирование- :\n"),
    fp_grade2_list(C),
    print_list(C),
    write("\nСтуденты, которые не сдали -информатику- :\n"),
    inf_grade2_list(D),
    print_list(D),
    write("\nСтуденты, которые не сдали -английский язык- :\n"),
    eng_grade2_list(E),
    print_list(E),
    write("\nСтуденты, которые не сдали -психологию- :\n"),
    psy_grade2_list(F),
    print_list(F).

delete([], _Elem, []):-!. 
delete([Elem|Tail], Elem, ResultTail):-
   delete(Tail, Elem, ResultTail), !.
delete([Head|Tail], Elem, [Head|ResultTail]):-
   delete(Tail, Elem, ResultTail).

delete_list([], _, []). 
delete_list(L, [], L).
delete_list(L, [H2|T2], Res) :-
    delete(L, H2, Res2),
    delete_list(Res2, T2, Res).

group_amount(Num, Am) :- 
    group_list(Num, L),
    lp_grade2_list(LP),
    mth_grade2_list(MTH),
    fp_grade2_list(FP),
    inf_grade2_list(INF),
    eng_grade2_list(ENG),
    psy_grade2_list(PSY),
    append1(LP, MTH, A),
    append1(FP, INF, B),
    append1(ENG, PSY, C),
    append1(A, B, D),
    append1(C, D, N),
    delete_list(L, N, R),
    length(R, Am).

task3() :- 
    write("\nКоличество студентов в 101 группе, которые провалились на экзамене: "),
    group_amount(101, Am1),
    group_list(101, L1),
    length(L1, A1),
    X is A1 - Am1,
    write(X),
    write("\nКоличество студентов в 102 группе, которые провалились на экзамене: "),
    group_amount(102, Am2),
    group_list(102, L2),
    length(L2, A2),
    Y is A2 - Am2,
    write(Y),
    write("\nКоличество студентов в 103 группе, которые провалились на экзамене: "),
    group_amount(103, Am3),
    group_list(103, L3),
    length(L3, A3),
    Z is A3 - Am3,
    write(Z),
    write("\nКоличество студентов в 104 группе, которые провалились на экзамене: "),
    group_amount(104, Am4),
    group_list(104, L4),
    length(L4, A4),
    W is A4 - Am4,
    write(W),
    write('\n').
