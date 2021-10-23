%  Tell prolog that known/3 will be added later by asserta
:- dynamic known/3.
:- discontiguous ask/2.
:- discontiguous numberask/2.
:- discontiguous menuask/3.

food(nasic_lemak) :-
    preference(asian),
    use_rice(yes),
    has_sambal(yes),
    contain_coconutmilk(yes).
food(fried_rice) :-
    preference(asian),
    use_rice(yes),
    fry(yes).
food(dandan_noodle) :-
    preference(asian),
    soup(no),
    origin(china).
food(pho) :-
    preference(asian),
    soup(yes),
    origin(vietnam).
food(kebab) :-
    preference(eastern),
    contain_meat(yes),
    use_rice(yes),
    heavy_portion(yes).
food(baguette) :-
    preference(western),
    use_bread(yes),
    origin(france).

my_dict(_{
    nasic_lemak: 644,
    fried_rice: 800,
    pho: 400,
    dandan_noodle: 378,
    kebab: 2000,
    fried_eggplant: 322,
    baguette: 130
}).

abs(X, Y) :- Y is sign(X) * X.
calories(X, Y, Z) :- abs(X-Y, Z).

recommend(X) :- bagof(Y, food(Y), Z), expected_calories(M), min_difference(Z, M, X).

diff(Base, L, Z):- my_dict(Dc), R=Dc.L, calories(R, Base, Z).

min_difference([L|Ls], Base, X) :- diff(Base, L, Z), min_difference(Ls, Z, L, Base, X).

min_difference([], Min, X, Base, X).
min_difference([L|Ls], Min, X0, Base, X) :- diff(Base, L, Z), Z >= Min, min_difference(Ls, Min, X0, Base, X).

min_difference([L|Ls], Min, X0, Base, X) :- diff(Base, L, Z), Z < Min, min_difference(Ls, Min, L, Base, X).

% Askables
expected_calories(X) :- numberask(expected_calories, X).
preference(P):- menuask(preference, P, [asian, western, eastern]).
origin(P):- menuask(origin, P, [vietnam, france, china]).
spicy(X) :- ask(spicy, X).
noodle(X) :- ask(noodle, X).
use_rice(X) :- ask(use_rice, X).
has_sambal(X) :- ask(has_sambal, X).
contain_coconutmilk(X) :- ask(contain_coconutmilk, X).
fry(X) :- ask(fry, X).
soup(X) :- ask(soup, X).
contain_meat(X) :- ask(contain_meat, X).
heavy_portion(X) :- ask(heavy_portion, X).
use_bread(X) :- ask(use_bread, X).

% Remember what I've been told is correct
ask(Attr, Val) :- known(yes, Attr, Val), !.
menuask(Attr, Val, _) :- known(yes, Attr, Val), !.
numberask(Attr, Val) :- known(yes, Attr, Val), !.

% Remember what I've been told is wrong
ask(Attr, Val) :- known(_, Attr, Val), !, fail.
menuask(Attr, Val, _) :- known(_, Attr, Val), !, fail.
numberask(Attr, Val) :- known(_, Attr, Val), !, fail.

% Remember when I've been told an attribute has a different value
ask(Attr, Val) :- known(yes, Attr, V), V \== Val, !, fail.
numberask(Attr, Val) :- known(yes, Attr, V), V \== Val, !, fail.
menuask(Attr, Val, _) :- known(yes, Attr, V), V \== Val, !, fail.

multivalued(ingredient).
multivalued(preference).
multivalued(origin).

ask(A, V):-
    known(yes, A, V), % succeed if true
    !.	% stop looking

ask(A, V):-
    known(_, A, V), % fail if false
    !, fail.

numberask(A, V):-
    known(yes, A, V), % succeed if true
    !.	% stop looking

numberask(A, V):-
    known(_, A, V), % fail if false
    !, fail.

% If not multivalued, and already known, don't ask again for a different value.
ask(A, V):-
    \+multivalued(A),
    known(yes, A, V2),
    V \== V2,
    !.

ask(A, V):-
    read_py_ask(A,V,Y), % get the answer
    asserta(known(Y, A, V)), % remember it
    write_py(known(Y, A, V)),
    Y == yes.	% succeed or fail

numberask(Attr, Val) :-
    read_py_numberask(Attr, Val),
    asserta(known(yes, Attr, Val)),
    write_py(known(yes, Attr, Val)).

menuask(Attr, Val, List) :-
    read_py_menuask(Attr, Ans, List),
    check_val(Ans, Attr, Val, List),
    asserta(known(yes, Attr, Ans)),
    write_py(known(yes, Attr, Ans)),
    Ans == Val.

check_val(Ans, _, _, List) :-
    member(Ans, List),
    !.
check_val(Ans, Attr, Val, List) :-
    read_py_menuask(Attr, Ans, List),
    menuask(Attr, Val, List).